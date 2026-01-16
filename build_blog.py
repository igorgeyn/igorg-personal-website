#!/usr/bin/env python3
"""
Blog Build Script
Converts Markdown files in blog/posts/ to HTML pages.

Usage: python build_blog.py

Each .md file should have YAML frontmatter:
---
title: "Post Title"
date: "2026-01-15"
description: "Brief description for the index page"
---

Post content in Markdown...
"""

import os
import re
import glob
from datetime import datetime
from pathlib import Path

# Try to import markdown library, fall back to basic conversion if not available
try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False
    print("Warning: 'markdown' library not installed. Using basic conversion.")
    print("Install with: pip install markdown")

BLOG_DIR = Path(__file__).parent / "blog"
POSTS_DIR = BLOG_DIR / "posts"
OUTPUT_DIR = BLOG_DIR

# HTML template for individual blog posts
POST_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Igor Geyn</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <nav class="nav">
        <div class="nav-inner">
            <a href="../index.html" class="nav-logo">Igor Geyn</a>
            <button class="nav-toggle" aria-label="Toggle menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <ul class="nav-links">
                <li><a href="../index.html">Home</a></li>
                <li><a href="../resume.html">Resume/CV</a></li>
                <li><a href="../research.html">Research</a></li>
                <li><a href="../freelance.html">Freelance</a></li>
                <li><a href="../teaching.html">Teaching</a></li>
                <li><a href="index.html" class="active">Blog</a></li>
            </ul>
        </div>
    </nav>

    <main class="main">
        <article class="blog-post">
            <header class="post-header">
                <h1>{title}</h1>
                <time class="post-date" datetime="{date}">{date_formatted}</time>
            </header>
            <div class="post-content">
{content}
            </div>
            <footer class="post-footer">
                <a href="index.html">← Back to Blog</a>
            </footer>
        </article>
    </main>

    <footer class="footer">
        <p>Independent analysis. Does not reflect views of UCLA or any other organization.</p>
    </footer>

    <script src="../main.js"></script>
</body>
</html>
"""

# HTML template for blog index
INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog — Igor Geyn</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <nav class="nav">
        <div class="nav-inner">
            <a href="../index.html" class="nav-logo">Igor Geyn</a>
            <button class="nav-toggle" aria-label="Toggle menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <ul class="nav-links">
                <li><a href="../index.html">Home</a></li>
                <li><a href="../resume.html">Resume/CV</a></li>
                <li><a href="../research.html">Research</a></li>
                <li><a href="../freelance.html">Freelance</a></li>
                <li><a href="../teaching.html">Teaching</a></li>
                <li><a href="index.html" class="active">Blog</a></li>
            </ul>
        </div>
    </nav>

    <main class="main">
        <header class="page-header-compact">
            <h1>Blog</h1>
            <p class="header-subtitle">Thoughts on data science, causal inference, and research.</p>
        </header>

        <section class="blog-list">
{posts}
        </section>
    </main>

    <footer class="footer">
        <p>Independent analysis. Does not reflect views of UCLA or any other organization.</p>
    </footer>

    <script src="../main.js"></script>
</body>
</html>
"""

POST_ENTRY_TEMPLATE = """            <article class="blog-entry">
                <a href="{slug}.html" class="blog-entry-link">
                    <h2 class="blog-entry-title">{title}</h2>
                    <time class="blog-entry-date" datetime="{date}">{date_formatted}</time>
                    <p class="blog-entry-description">{description}</p>
                </a>
            </article>
"""


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content."""
    frontmatter = {}
    body = content

    # Check for frontmatter delimiters
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_content = parts[1].strip()
            body = parts[2].strip()

            # Simple YAML parsing (key: value pairs)
            for line in fm_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    frontmatter[key] = value

    return frontmatter, body


def markdown_to_html(md_content):
    """Convert markdown to HTML."""
    if HAS_MARKDOWN:
        return markdown.markdown(md_content, extensions=['fenced_code', 'tables', 'nl2br'])
    else:
        # Basic fallback conversion
        html = md_content
        # Paragraphs
        html = re.sub(r'\n\n+', '</p><p>', html)
        html = f'<p>{html}</p>'
        # Bold
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        # Italic
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        # Links
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
        # Headers
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        return html


def format_date(date_str):
    """Format date string for display."""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str


def build_post(md_file):
    """Build HTML from a markdown file."""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)

    # Get metadata with defaults
    title = frontmatter.get('title', 'Untitled')
    date = frontmatter.get('date', datetime.now().strftime('%Y-%m-%d'))
    description = frontmatter.get('description', '')

    # Convert markdown body to HTML
    html_content = markdown_to_html(body)

    # Generate slug from filename
    slug = Path(md_file).stem

    # Build the HTML page
    html = POST_TEMPLATE.format(
        title=title,
        date=date,
        date_formatted=format_date(date),
        content=html_content
    )

    # Write output file
    output_file = OUTPUT_DIR / f"{slug}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Built: {output_file}")

    return {
        'title': title,
        'date': date,
        'date_formatted': format_date(date),
        'description': description,
        'slug': slug
    }


def build_index(posts):
    """Build the blog index page."""
    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x['date'], reverse=True)

    # Generate post entries
    if posts:
        posts_html = '\n'.join([
            POST_ENTRY_TEMPLATE.format(**post)
            for post in posts
        ])
    else:
        posts_html = '            <p class="no-posts">No posts yet. Check back soon!</p>'

    # Build index HTML
    html = INDEX_TEMPLATE.format(posts=posts_html)

    # Write index file
    output_file = OUTPUT_DIR / "index.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Built: {output_file}")


def main():
    """Build all blog posts and index."""
    print("Building blog...")

    # Ensure directories exist
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    # Find all markdown files
    md_files = list(POSTS_DIR.glob('*.md'))

    if not md_files:
        print("No markdown files found in blog/posts/")
        print("Creating sample post...")
        # Create a sample post
        sample_post = POSTS_DIR / "sample-post.md"
        with open(sample_post, 'w') as f:
            f.write("""---
title: "Welcome to My Blog"
date: "2026-01-16"
description: "First post on my new blog - thoughts on data science and research."
---

This is a sample blog post. You can write your posts in Markdown format.

## How to Write Posts

1. Create a new `.md` file in `blog/posts/`
2. Add YAML frontmatter at the top (title, date, description)
3. Write your content in Markdown
4. Run `python build_blog.py` to generate HTML

## Markdown Features

You can use **bold**, *italic*, and [links](https://example.com).

### Code blocks

```python
def hello():
    print("Hello, world!")
```

Happy writing!
""")
        md_files = [sample_post]

    # Build each post
    posts = []
    for md_file in md_files:
        post_info = build_post(md_file)
        posts.append(post_info)

    # Build index
    build_index(posts)

    print(f"\nDone! Built {len(posts)} post(s).")


if __name__ == '__main__':
    main()
