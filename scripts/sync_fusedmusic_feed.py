#!/usr/bin/env python3
"""
Fetches the RSS feed from fusedmusic.org (a Wix site) and converts it into
a small JSON file (data/sessions-feed.json) that the blog's "Sessions" tab
reads client-side. Designed to be run by the GitHub Action in
.github/workflows/sync-feed.yml — runs server-to-server, so there's no
CORS issue like there would be fetching this directly from a browser.

Uses only the Python standard library (urllib + xml.etree) so nothing
needs to be installed on the GitHub Actions runner.
"""

import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET

FEED_URL = "https://www.fusedmusic.org/blog-feed.xml"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sessions-feed.json")
MAX_ITEMS = 30
DESCRIPTION_MAX_LEN = 220

YOUTUBE_PATTERNS = [
    re.compile(r"(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{6,})"),
]


def youtube_thumbnail(url):
    for pattern in YOUTUBE_PATTERNS:
        m = pattern.search(url)
        if m:
            return f"https://i.ytimg.com/vi/{m.group(1)}/hqdefault.jpg"
    return None


def clean_description(raw):
    if not raw:
        return ""
    text = re.sub(r"<[^>]+>", "", raw).strip()
    if len(text) > DESCRIPTION_MAX_LEN:
        text = text[:DESCRIPTION_MAX_LEN].rsplit(" ", 1)[0] + "…"
    return text


def fetch_feed(url):
    req = urllib.request.Request(url, headers={"User-Agent": "FusedMusicBlogSync/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def parse_feed(xml_bytes):
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.findall(".//item")[:MAX_ITEMS]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        description = clean_description(item.findtext("description") or "")

        enclosure = item.find("enclosure")
        media_url = enclosure.get("url") if enclosure is not None else None
        media_type_attr = (enclosure.get("type") if enclosure is not None else "") or ""

        image = None
        media_type = "none"
        if media_url:
            if media_type_attr.startswith("image"):
                image = media_url
                media_type = "image"
            else:
                media_type = "video"
                image = youtube_thumbnail(media_url)  # None if not a YouTube link

        items.append({
            "title": title,
            "link": link,
            "pubDate": pub_date,
            "description": description,
            "image": image,
            "mediaType": media_type,
            "mediaUrl": media_url,
        })
    return items


def main():
    xml_bytes = fetch_feed(FEED_URL)
    items = parse_feed(xml_bytes)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump({"items": items, "source": FEED_URL}, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(items)} items to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
