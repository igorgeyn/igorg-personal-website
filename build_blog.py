#!/usr/bin/env python3
"""Build the curated blog index and Markdown-backed blog posts.

The blog has three production paths:

* Markdown posts in ``blog/posts`` built by this script.
* Hand-authored posts marked ``skip_build: true``.
* Externally rendered posts (currently the Quarto PSPS effectiveness article).

``POST_CATALOG`` is the shared presentation metadata for all three paths. This
keeps the index, social cards, cover art, attachments, and related-post links
stable when the Markdown-backed pages are rebuilt.
"""

import html as html_lib
import re
from datetime import datetime
from pathlib import Path

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
SITE_URL = "https://www.igorgeyn.com"


POST_CATALOG = {
    "california-psps-effectiveness": {
        "title": "How Effective Is PSPS at Preventing Wildfires?",
        "date": "2026-06-12",
        "description": (
            "Does shutting off the power actually prevent wildfires? A step-by-step "
            "causal analysis — why the headline numbers mislead, how far publicly "
            "available data can take us, and exactly what it would take to measure "
            "the real effect."
        ),
        "kicker": "Latest · Grid & Wildfire Risk",
        "cover": "images/california-psps-effectiveness-cover-v2.png",
        "cover_alt": (
            "Editorial illustration of utility poles and causal-analysis diagrams "
            "across a wildfire-prone landscape."
        ),
        "featured": True,
        "skip_build": True,
        "attachments": [
            ("▶", "Interactive slides", "psps-effectiveness-slides/index.html"),
            ("⇩", "PDF slides", "psps-effectiveness-slides/california-psps-effectiveness.pdf"),
        ],
    },
    "california-generation-fire-risk": {
        "kicker": "Grid & Wildfire Risk · Series Part 1",
        "cover": "images/california-generation-fire-risk-cover.png",
        "cover_alt": (
            "Editorial illustration of California power generation markers over "
            "wildfire-risk shading."
        ),
        "subtitle": "Part 1 of a series on California's energy grid and wildfire risk",
        "attachments": [
            ("▶", "Interactive slides", "grid-fire-slides/index.html"),
            ("⇩", "PDF slides", "grid-fire-slides/california-generation-fire-risk.pdf"),
        ],
        "related": [
            ("Case study", "california-data-center-fire-risk.html", "How Much Fire Risk Is California Building? A Case Study of the Manning–Metcalf 500 kV Corridor"),
            ("PSPS", "california-psps-analysis.html", "Understanding California's Power Shutoffs"),
            ("PSPS", "california-psps-effectiveness.html", "How Effective Is PSPS at Preventing Wildfires?"),
        ],
    },
    "california-data-center-fire-risk": {
        "kicker": "Grid & Wildfire Risk",
        "cover": "images/california-data-center-fire-risk-cover.png",
        "cover_alt": (
            "Editorial illustration of a California transmission corridor exposed "
            "to wildfire risk."
        ),
        "skip_build": True,
        "attachments": [
            ("▶", "Interactive slides", "dc-fire-slides/index.html"),
            ("⇩", "PDF slides", "dc-fire-slides/california-data-center-fire-risk.pdf"),
        ],
    },
    "california-psps-analysis": {
        "kicker": "Grid & Wildfire Risk",
        "cover": "images/california-psps-analysis-cover.png",
        "cover_alt": (
            "Editorial illustration of a darkened residential street with one "
            "warmly lit window."
        ),
        "strip_leading_byline": True,
        "attachments": [
            ("▶", "Interactive slides", "psps-slides/index.html"),
            ("⇩", "PDF slides", "psps-slides/california-psps-analysis.pdf"),
        ],
        "related": [
            ("Follow-up", "california-psps-effectiveness.html", "How Effective Is PSPS at Preventing Wildfires?"),
            ("Series Part 1", "california-generation-fire-risk.html", "Understanding the Fire Risk in California's Power Grid: Generation"),
            ("Case study", "california-data-center-fire-risk.html", "How Much Fire Risk Is California Building? A Case Study of the Manning–Metcalf 500 kV Corridor"),
        ],
    },
    "tuition-subsidies-voting": {
        "kicker": "Elections & Participation",
        "cover": "images/tuition-subsidies-voting-cover.png",
        "cover_alt": (
            "Editorial illustration of institutional papers, a ballot envelope, "
            "and a graduation tassel."
        ),
    },
}


THEME_INIT = """    <script>(function(){var t=localStorage.getItem('theme');if(!t)t=window.matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';document.documentElement.setAttribute('data-theme',t)})()</script>"""

THEME_TOGGLE = """            <button class="theme-toggle" aria-label="Switch to dark mode" title="Switch to dark mode">
                <svg class="icon-moon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
                <svg class="icon-sun" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="4.22" x2="19.78" y2="5.64"/></svg>
            </button>"""


def navigation(prefix=""):
    return f"""    <nav class="nav" aria-label="Primary navigation">
        <div class="nav-inner">
            <a href="{prefix}index.html" class="nav-logo"><img src="{prefix}images/logo.svg" alt="Igor Geyn" height="28"></a>
            <button class="nav-toggle" aria-label="Open navigation menu" aria-expanded="false" aria-controls="primary-navigation">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <ul class="nav-links" id="primary-navigation">
                <li><a href="{prefix}index.html">Home</a></li>
                <li><a href="{prefix}research.html">Research</a></li>
                <li><a href="{prefix}freelance.html">Freelance</a></li>
                <li><a href="{prefix}blog/index.html" class="active">Blog</a></li>
            </ul>
{THEME_TOGGLE}
        </div>
    </nav>"""


FOOTER = """    <footer class="footer">
        <p class="footer-links"><a href="mailto:igorgeyn@gmail.com">Email</a> &middot; <a href="https://www.linkedin.com/in/igorgeyn/" target="_blank" rel="noopener">LinkedIn</a> &middot; <a href="https://scholar.google.com/citations?user=LAA1on0AAAAJ" target="_blank" rel="noopener">Google Scholar</a></p>
        <p>Independent analysis. Does not reflect views of UCLA or any other organization.</p>
    </footer>"""


POST_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Igor Geyn</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical}">
{social_image_meta}
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">
{theme_init}
</head>
<body class="blog-post-page">
{navigation}

    <main class="main">
        <article class="blog-post">
            <nav class="post-breadcrumb" aria-label="Breadcrumb">
                <a href="index.html">← Blog</a>
            </nav>
            <header class="post-header">
                <h1>{title}</h1>
{subtitle_markup}                <time class="post-date" datetime="{date}">{date_formatted}</time>
            </header>
{cover_markup}{attachments_markup}            <div class="post-content">
{content}
            </div>
{related_markup}            <footer class="post-footer">
                <a href="index.html">← Back to Blog</a>
            </footer>
        </article>
    </main>

{footer}

    <script src="../main.js"></script>
</body>
</html>
"""


INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog — Igor Geyn</title>
    <meta name="description" content="Data-driven writing on climate and energy policy, causal inference, elections, and public-sector data.">
    <link rel="canonical" href="https://www.igorgeyn.com/blog/">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Blog — Igor Geyn">
    <meta property="og:description" content="Data-driven writing on climate and energy policy, causal inference, elections, and public-sector data.">
    <meta property="og:url" content="https://www.igorgeyn.com/blog/">
    <meta property="og:image" content="https://www.igorgeyn.com/blog/images/california-psps-effectiveness-cover-v2.png">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">
{theme_init}
</head>
<body class="blog-index">
{navigation}

    <main class="main">
        <header class="page-header-compact">
            <h1>Blog</h1>
            <p class="header-subtitle">Thoughts on data science, causal inference, and energy policy research.</p>
        </header>

        <section class="blog-list">
{posts}
        </section>
    </main>

{footer}

    <script src="../main.js"></script>
</body>
</html>
"""


def parse_frontmatter(content):
    """Parse simple key/value YAML frontmatter."""
    frontmatter = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_content = parts[1].strip()
            body = parts[2].strip()
            for line in fm_content.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return frontmatter, body


def as_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def markdown_to_html(md_content):
    if HAS_MARKDOWN:
        return markdown.markdown(md_content, extensions=["fenced_code", "tables"])

    converted = re.sub(r"\n\n+", "</p><p>", md_content)
    converted = f"<p>{converted}</p>"
    converted = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", converted)
    converted = re.sub(r"\*(.+?)\*", r"<em>\1</em>", converted)
    converted = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', converted)
    converted = re.sub(r"^### (.+)$", r"<h3>\1</h3>", converted, flags=re.MULTILINE)
    converted = re.sub(r"^## (.+)$", r"<h2>\1</h2>", converted, flags=re.MULTILINE)
    converted = re.sub(r"^# (.+)$", r"<h1>\1</h1>", converted, flags=re.MULTILINE)
    return converted


def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")
    except ValueError:
        return date_str


def strip_source_preamble(body, title, catalog):
    title_pattern = re.escape(title)
    body = re.sub(rf"^#\s+{title_pattern}\s*\n+", "", body, count=1)

    subtitle = catalog.get("subtitle")
    if subtitle:
        subtitle_pattern = re.escape(subtitle)
        body = re.sub(rf"^\*{subtitle_pattern}\*\s*\n+", "", body, count=1)

    if catalog.get("strip_leading_byline"):
        body = re.sub(r"^\*[^\n]+\*\s*\n+", "", body, count=1)

    return re.sub(r"^\s*---\s*\n+", "", body, count=1)


def add_caption_classes(content):
    return re.sub(
        r"<p>(<strong>(?:Figure|Table)\s+\d+\.</strong>.*?)</p>",
        r'<p class="caption">\1</p>',
        content,
        flags=re.DOTALL,
    )


def social_image_meta(cover):
    if not cover:
        return ""
    image_url = f"{SITE_URL}/blog/{cover}"
    return (
        f'    <meta property="og:image" content="{image_url}">\n'
        f'    <meta name="twitter:image" content="{image_url}">'
    )


def cover_markup(info):
    cover = info.get("cover")
    if not cover:
        return ""
    alt = html_lib.escape(info.get("cover_alt", ""), quote=True)
    return f'            <img class="post-cover" src="{cover}" alt="{alt}">\n'


def attachments_markup(info):
    attachments = info.get("attachments", [])
    if not attachments:
        return ""
    links = []
    for icon, label, href in attachments:
        action = "Download" if "PDF" in label else "Open"
        aria = f"{action} {label.lower()} for {info['title']}"
        links.append(
            f'                <a href="{href}" class="post-attachment" aria-label="{html_lib.escape(aria, quote=True)}">'
            f'<span aria-hidden="true">{icon}</span> {html_lib.escape(label)}</a>'
        )
    return "            <div class=\"post-attachments\">\n" + "\n".join(links) + "\n            </div>\n"


def related_markup(info):
    related = info.get("related", [])
    if not related:
        return ""
    items = []
    for label, href, title in related:
        items.append(
            f'                    <li><span class="post-related-label">{html_lib.escape(label)}:</span> '
            f'<a href="{href}">{html_lib.escape(title)}</a></li>'
        )
    return (
        '            <nav class="post-related" aria-label="Related posts">\n'
        '                <span class="post-related-title">More on California\'s grid &amp; wildfire risk</span>\n'
        '                <ul>\n'
        + "\n".join(items)
        + '\n                </ul>\n            </nav>\n'
    )


def build_post(md_file):
    content = Path(md_file).read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)
    slug = Path(md_file).stem
    catalog = dict(POST_CATALOG.get(slug, {}))

    info = {
        **catalog,
        "title": frontmatter.get("title", catalog.get("title", "Untitled")),
        "date": frontmatter.get("date", catalog.get("date", datetime.now().strftime("%Y-%m-%d"))),
        "description": frontmatter.get("description", catalog.get("description", "")),
        "slug": slug,
    }
    info["date_formatted"] = format_date(info["date"])

    should_skip = as_bool(frontmatter.get("skip_build", info.get("skip_build", False)))
    if should_skip:
        print(f"Preserved hand-authored output: {OUTPUT_DIR / f'{slug}.html'}")
        return info

    body = strip_source_preamble(body, info["title"], catalog)
    html_content = add_caption_classes(markdown_to_html(body))
    canonical = f"{SITE_URL}/blog/{slug}.html"
    title = html_lib.escape(info["title"], quote=True)
    description = html_lib.escape(info["description"], quote=True)
    subtitle = info.get("subtitle")
    subtitle_html = (
        f'                <p class="post-subtitle">{html_lib.escape(subtitle)}</p>\n'
        if subtitle
        else ""
    )

    page = POST_TEMPLATE.format(
        title=title,
        description=description,
        canonical=canonical,
        social_image_meta=social_image_meta(info.get("cover")),
        theme_init=THEME_INIT,
        navigation=navigation("../"),
        subtitle_markup=subtitle_html,
        date=info["date"],
        date_formatted=info["date_formatted"],
        cover_markup=cover_markup(info),
        attachments_markup=attachments_markup(info),
        content=html_content,
        related_markup=related_markup(info),
        footer=FOOTER,
    )

    output_file = OUTPUT_DIR / f"{slug}.html"
    output_file.write_text(page, encoding="utf-8")
    print(f"Built: {output_file}")
    return info


def render_index_attachments(info):
    attachments = info.get("attachments", [])
    if not attachments:
        return ""
    links = []
    for icon, label, href in attachments:
        action = "Download" if "PDF" in label else "Open"
        aria = f"{action} {label.lower()} for {info['title']}"
        links.append(
            f'                            <a href="{href}" class="blog-attachment" aria-label="{html_lib.escape(aria, quote=True)}">'
            f'<span class="preview-card-icon" aria-hidden="true">{icon}</span> {html_lib.escape(label)}</a>'
        )
    return '                        <div class="blog-attachments">\n' + "\n".join(links) + "\n                        </div>\n"


def render_index_entry(info):
    title = html_lib.escape(info["title"])
    description = html_lib.escape(info.get("description", ""))
    kicker = html_lib.escape(info.get("kicker", ""))
    href = f"{info['slug']}.html"
    attachments = render_index_attachments(info)
    cover = info.get("cover")

    body = f"""                    <div class="{'blog-hero-body' if info.get('featured') else 'blog-row-body'}">
                        <a href="{href}" class="blog-entry-link">
                            <span class="blog-kicker">{kicker}</span>
                            <h2 class="blog-entry-title">{title}</h2>
                            <time class="blog-entry-date" datetime="{info['date']}">{info['date_formatted']}</time>
                            <p class="blog-entry-description">{description}</p>
                        </a>
{attachments}                    </div>"""

    if info.get("featured"):
        cover_link = ""
        if cover:
            cover_link = f"""
                    <a href="{href}" class="blog-hero-cover-link" aria-hidden="true" tabindex="-1">
                        <img class="blog-hero-cover" src="{cover}" alt="" loading="lazy">
                    </a>"""
        return f"""            <article class="blog-hero">
                <div class="blog-hero-link">
{body}{cover_link}
                </div>
            </article>"""

    thumb = ""
    row_class = "blog-row"
    if cover:
        thumb = f"""                <a href="{href}" class="blog-row-thumb" aria-hidden="true" tabindex="-1">
                    <img class="blog-row-cover" src="{cover}" alt="" loading="lazy">
                </a>
"""
    else:
        row_class += " blog-row--text"
    return f"""            <article class="{row_class}">
{thumb}{body}
            </article>"""


def build_index(posts):
    by_slug = {post["slug"]: post for post in posts}
    for slug, catalog in POST_CATALOG.items():
        if slug not in by_slug:
            info = {**catalog, "slug": slug}
            info["date_formatted"] = format_date(info["date"])
            by_slug[slug] = info

    ordered = sorted(by_slug.values(), key=lambda item: item["date"], reverse=True)
    posts_html = "\n\n".join(render_index_entry(post) for post in ordered)
    page = INDEX_TEMPLATE.format(
        theme_init=THEME_INIT,
        navigation=navigation("../"),
        posts=posts_html,
        footer=FOOTER,
    )
    output_file = OUTPUT_DIR / "index.html"
    output_file.write_text(page, encoding="utf-8")
    print(f"Built: {output_file}")


def main():
    print("Building blog...")
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    md_files = sorted(POSTS_DIR.glob("*.md"))
    if not md_files:
        raise SystemExit("No Markdown files found in blog/posts/; refusing to create sample production content.")

    posts = [build_post(md_file) for md_file in md_files]
    build_index(posts)
    print(f"\nDone! Processed {len(posts)} Markdown source(s).")


if __name__ == "__main__":
    main()
