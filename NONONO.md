# Fused Music Studio — fusedmusic.studio

Professional website for Rebecca's assistive music technology practice.

## Site Structure
```
fusedmusic/
├── index.html        ← Home page
├── services.html     ← Services page
├── about.html        ← About Rebecca
├── blog.html         ← Blog & Videos
├── contact.html      ← Contact & Booking
├── css/
│   └── style.css     ← Shared styles
└── js/
    └── main.js       ← Shared JavaScript
```

## Hosting on GitHub Pages

1. Create a GitHub account at github.com (free)
2. Create a new repository named `fusedmusic-studio`
3. Upload all files (drag and drop in the browser)
4. Go to Settings → Pages → Source: Deploy from branch → main → / (root)
5. Your site will be live at `yourusername.github.io/fusedmusic-studio`

## Connecting fusedmusic.studio domain

In Namecheap DNS settings, add these records:
- Type: A | Host: @ | Value: 185.199.108.153
- Type: A | Host: @ | Value: 185.199.109.153
- Type: A | Host: @ | Value: 185.199.110.153
- Type: A | Host: @ | Value: 185.199.111.153
- Type: CNAME | Host: www | Value: yourusername.github.io

In GitHub Pages settings:
- Custom domain: fusedmusic.studio
- Tick "Enforce HTTPS"

Allow up to 24 hours for DNS to propagate.

## Adding Calendly (contact page)

1. Create a free Calendly account at calendly.com
2. Set up a "Discovery Call" event (20 mins)
3. Go to Share → Embed → Inline Widget
4. Copy the embed code
5. In contact.html, replace the `.calendly-placeholder` div with your embed code

## To add a blog post

Copy this structure into blog.html's posts-grid:
```html
<a href="your-post.html" class="post-card" aria-label="Read: Your Post Title">
  <div class="post-thumb t1" aria-hidden="true">🎵<span class="post-type-badge">Article</span></div>
  <div class="post-body">
    <div class="post-meta">Category</div>
    <h4>Your Post Title</h4>
    <p>Brief description of the post.</p>
    <span class="post-read">Read article</span>
  </div>
</a>
```
