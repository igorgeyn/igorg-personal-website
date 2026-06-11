# Blog Cover Image Prompts

Generated 2026-06-03. One prompt per post, designed to be pasted into ChatGPT (DALL-E / image generation) or any other text-to-image tool.

## Shared aesthetic

All five prompts share a deliberate house style so the blog has visual coherence:

- **Style anchor:** editorial illustration in the tradition of *The New Yorker* + mid-century Bauhaus poster work.
- **Restrained palette:** warm off-white background with light paper texture, graphite black for line work, **one accent color per post** (varied so each cover feels distinct).
- **Composition:** generous negative space; conceptual rather than literal.
- **No text, no labels, no signage.**
- **Aspect ratio:** 3:2 landscape (good for blog headers). For a portrait variant, replace with 4:5.

If a model interprets too literally, append: *"subtle, restrained, conceptual rather than literal, generous negative space."*

---

## 1. Understanding the Fire Risk in California's Power Grid: Generation

**Date:** 2026-04-06
**URL:** [`california-generation-fire-risk.html`](california-generation-fire-risk.html)
**Topic:** How California's 3,018 generators overlap with fire threat zones, historical fire perimeters, and fire weather patterns.

### Prompt

```
An editorial-style conceptual illustration for a blog post about California
electricity generation and wildfire risk. Composition: a stylized aerial view
of California rendered in fine ink-on-paper style. Across the state, several
dozen small geometric markers (circles and squares of varying sizes) represent
power generation facilities, scattered concentrating in the Central Valley,
the desert southeast, and along the coast. Behind them, soft washes of warm
ember orange and burnt sienna bleed across the topography to suggest the
state's fire-threat geography — the warmest shading concentrated in the
foothills and Sierra Nevada. The two layers overlap rather than compete:
some generators sit clearly within the warm-shaded zones, others outside.
Color palette: warm off-white background (slight paper texture), graphite
black for line work, accents of ember orange and burnt sienna (one warm
color family). Style: New Yorker editorial illustration crossed with
mid-century Bauhaus poster, restrained, no text or labels. Landscape
orientation, 3:2 aspect ratio.
```

---

## 2. How Much Fire Risk Is California Building? A Case Study of the Manning–Metcalf 500 kV Corridor

**Date:** 2026-03-04
**URL:** [`california-data-center-fire-risk.html`](california-data-center-fire-risk.html)
**Topic:** Case study of a specific high-voltage transmission corridor and the data center buildout it serves.

### Prompt

```
An editorial-style conceptual illustration for a blog post about a specific
California transmission corridor serving data center expansion. Composition:
the foreground shows a single tall, finely drawn transmission tower — clean
geometric ink line work, slightly silhouetted — receding into the middle
distance where it joins a chain of two or three more towers that march into
the background. The towers cross a stylized dry-grass hillside rendered in
warm muted gold and graphite. At the far horizon line, the faint silhouette
of a low, windowless rectangular building (a data center) sits where the
transmission line terminates — small enough to read as institutional rather
than industrial. The sky is a pale warm gradient suggesting late afternoon
under high-pressure conditions; a single thin haze line low in the sky
hints at wildfire smoke without being literal. Color palette: warm off-white
sky, graphite black line work, accents of muted gold and a single thin
band of dusty rose along the horizon. Editorial illustration style with
generous negative space, restrained, no text. Landscape orientation, 3:2.
```

---

## 3. Understanding California's Power Shutoffs

**Date:** 2026-02-09
**URL:** [`california-psps-analysis.html`](california-psps-analysis.html)
**Topic:** PSPS (Public Safety Power Shutoff) burden distribution, outage duration, and effectiveness of the fire prevention strategy.

### Prompt

```
An editorial-style conceptual illustration for a blog post about Public
Safety Power Shutoffs in California. Composition: a darkened residential
California streetscape at night, drawn in fine ink line work — a row of
three or four houses with steeply pitched roofs, a couple of utility
poles connecting them. The vast majority of the windows are dark. One
single window in one house is lit with a soft warm glow (perhaps a
flashlight or candle interior), and one streetlight just barely casts
light onto the pavement in front of it. The composition is asymmetric:
the lit window is offset to one side, leaving most of the image in
quiet darkness. Above the rooftops, a deep midnight-blue sky with no
moon. Color palette: midnight blue and graphite black for the dominant
darkness, one warm accent of soft amber for the lit window. Editorial
illustration style, conceptual (not photoreal), generous negative space,
no text. Landscape orientation, 3:2 aspect ratio.
```

---

## 4. Does Subsidized College Make People Vote? A Causal Analysis with 16 Million Records

**Date:** 2026-01-19
**URL:** [`tuition-subsidies-voting.html`](tuition-subsidies-voting.html)
**Topic:** Linking 16.4 million financial aid applications to voter records to estimate civic returns to tuition subsidies.

### Prompt

```
An editorial-style conceptual illustration for a blog post about the
relationship between college tuition subsidies and voter turnout.
Composition: a clean still-life arrangement on a wooden tabletop, drawn
in fine ink-and-wash style with a slight pencil texture. Three objects
in restrained composition: (1) a stack of forms or papers — clearly
institutional, official, with thin horizontal lines suggesting form
fields — but rendered abstractly enough that the content is not legible;
(2) a single ballot envelope, slightly open, with one corner of a ballot
slip just visible; (3) a graduation tassel resting across the corner of
the stack of papers, its short cord and decorative knot drawn with
delicate precision. The three objects sit close to each other, suggesting
relation. Lighting is soft and even, like early morning at a desk. Color
palette: warm off-white background, graphite and soft sepia for the
papers, one accent of deep emerald green for the ballot envelope and
graduation tassel. Style: editorial illustration crossed with botanical-
illustration restraint, generous negative space, no text or labels.
Landscape orientation, 3:2 aspect ratio.
```

---

## 5. How Effective Is PSPS at Preventing Wildfires?

**Date:** 2026-06-11
**URL:** [`california-psps-effectiveness.html`](california-psps-effectiveness.html)
**Topic:** Estimating the causal effect of PSPS on wildfire ignitions, and why the missing counterfactual requires utility-held operational data.

### Prompt

```
An editorial-style conceptual illustration for a blog post about estimating
the causal effect of Public Safety Power Shutoffs (PSPS) on wildfire
ignitions. Composition: a finely drawn utility circuit crosses a sparse
California foothill landscape, then splits near the center into two nearly
identical parallel branches like a causal comparison. One branch is solid
graphite and de-energized with an open switch; the other is faint and
ghosted as the missing counterfactual path. Around the branches, a few
small abstract data marks and blank record cards suggest observed data
versus utility-held records. Include one tiny restrained spark mark only as
a conceptual ignition point, not a literal fire. Color palette: warm
off-white background with paper texture, graphite black line work, exactly
one accent color: muted electric blue for the ghosted counterfactual and
data marks. Style: New Yorker editorial illustration crossed with
mid-century Bauhaus poster restraint, conceptual rather than literal,
generous negative space, no text, no labels, no numbers, no logos, no
people, no photorealism, no large flames. Landscape orientation, 3:2.
```

---

## File placement after generation

When the model returns an image, save the file into the post's image folder using the post's slug. Suggested locations:

| Post | Suggested file path |
|---|---|
| Generation fire risk | `blog/grid-fire-figures/cover.png` |
| Manning–Metcalf corridor | `blog/dc-fire-figures/cover.png` |
| PSPS analysis | `blog/psps-interactive/cover.png` or `blog/images/psps-cover.png` |
| PSPS effectiveness | `blog/images/california-psps-effectiveness-cover-v2.png` |
| Tuition subsidies × voting | `blog/images/tuition-voting-cover.png` |

Then add the appropriate `<img>` tag or Open Graph meta tag to the corresponding HTML file. (For Open Graph: `<meta property="og:image" content="...">` in the `<head>` of each post.)

## Notes

- Each post's accent color is intentionally different to give the blog index visual variety while keeping the underlying style consistent.
- All prompts deliberately avoid stock-photo clichés (no AI-generated faces, no literal flames, no literal lecterns or ballot boxes used as the only subject).
- If the model produces something with text artifacts (common with editorial illustration prompts), regenerate with the appended phrase: *"absolutely no text, no letters, no numbers, no labels, no signage."*
