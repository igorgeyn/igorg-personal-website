# Diagnostic Figures: Summary and Report Integration Guide

**Date:** February 13, 2026
**Source scripts:**
- `scripts/visualizations/fig_a_ca_overview.py` (Figure A)
- `scripts/visualizations/polish_diagnostic_figures.py` (Figures B-F)
**Style:** All figures use `style_config.py` palette and formatting (200 DPI, fire-themed colors, consistent fonts).

---

## Figure Inventory

| Figure | Filename | Size | Purpose |
|--------|----------|------|---------|
| A | `fig_ca_overview.png` | 934 KB | Statewide transmission map with HFTD and corridor highlighted |
| B | `fig_psps_chronic_circuits.png` | 250 KB | Top 25 corridor PSPS circuits by frequency, color-coded by GIS match quality |
| C | `fig_psps_match_summary.png` | 147 KB | PSPS-to-GIS matching methodology results (donut + stacked bar) |
| D | `fig_owner_fire_exposure.png` | 224 KB | Transmission feature count and fire exposure by owner |
| E | `fig_voltage_hftd_2025.png` | 152 KB | HFTD exposure by voltage class with Manning-Metcalf reference |
| F | `fig_hifld_comparison.png` | 112 KB | Old vs. 2025 HIFLD extract comparison by voltage class |

---

## Recommended Placement

### Main Report Candidates

**1. Figure A: California Statewide Overview Map**
- **Where:** Section 2 ("Where California builds"), before or alongside Figure 3 (the existing gen/trans fire exposure comparison)
- **Why:** Provides geographic context that the existing figures lack. Readers unfamiliar with California geography need a visual anchor to understand where the corridor sits relative to the state's fire territory and transmission backbone.
- **Caption suggestion:** "California's transmission network and CPUC High Fire Threat Districts. The Manning-Metcalf corridor (boxed) cuts across the Coast Range foothills between Hollister and San Jose. Data: HIFLD (2025 vintage), CPUC HFTD v3."

**2. Figure E: Transmission Fire Exposure by Voltage Class**
- **Where:** Appendix A (voltage class analysis), replacing or supplementing Figure A1
- **Why:** This is the cleanest visualization of the 2025 validation results. The Manning-Metcalf corridor diamond at 50-60% against the 500 kV average of 22% is a powerful visual argument. The stacked bar panel provides the data density that Appendix A needs.
- **Caption suggestion:** "Transmission fire exposure by voltage class (2025 HIFLD, CPUC HFTD v3). Left: total line-km decomposed by fire tier. Right: HFTD exposure rate by voltage class. The Manning-Metcalf corridor (red diamond) at 50-60% is more than double the PG&E 500 kV average."

**3. Figure B: Chronic PSPS Circuits in the Data Center Corridor**
- **Where:** PSPS section, supplementing the existing Figure 7 (PSPS timeline)
- **Why:** Figure 7 shows temporal distribution; Figure B shows which circuits are most chronic and whether they can be mapped geographically. The color coding by GIS match quality adds a methodological dimension. Could be referenced in the PSPS section text: "The most chronic circuits — Los Gatos-1107, Milpitas-1109, Morgan Hill-2111 — are distribution feeders that cannot be directly mapped to transmission geometries, but their upstream transmission feeds pass through the same fire territory."
- **Caption suggestion:** "Top 25 corridor PSPS circuits ranked by event count (2013-2025). Color indicates GIS match quality: green = exact match to HIFLD transmission geometry, blue = partial match, orange = inferred from upstream transmission, gray = no match. [T] marks transmission-level circuits."

### Appendix / Documentation

**4. Figure C: PSPS Circuit Matching Results**
- **Where:** Appendix or methodology supplement
- **Why:** Documents the PSPS-GIS matching approach for reproducibility. Shows the 73% match rate and the distribution/transmission breakdown. Not essential for the narrative but useful for reviewers who want to understand the matching methodology.

**5. Figure D: Transmission Ownership and Fire Exposure**
- **Where:** Appendix A or omit from report (keep as supporting material)
- **Why:** Shows PG&E at 30% and SDG&E at 65% in context of all California transmission owners. The right panel's fire gradient coloring makes the exposure variation immediately visible. However, this largely duplicates information already in Figure 3 (the utility comparison panel). Include only if the report expands the utility comparison discussion.

**6. Figure F: HIFLD Extract Comparison**
- **Where:** Methodology/data section footnote, or omit from report
- **Why:** QA documentation showing the 2025 HIFLD pull vs. old extract. The +2,943 sub-100 kV annotation is the key takeaway. Important for audit trail but not for the narrative. The validation summary markdown (`output/hifld_2025_validation_summary.md`) already documents this comparison in detail.

---

## Data Sources

| Dataset | Vintage | File |
|---------|---------|------|
| HIFLD Transmission Lines | Aug 2025 (accessed Feb 2026) | `raw/hifld/transmission_lines_california_2025.geojson` |
| CPUC HFTD | v3, Aug 2021 | `raw/hftd/CPUC_FireThreatMapTiers2_3_v3r_08_19_2021.gdb` |
| PSPS Events | 2013-2025 | `psps_analysis/output/psps_cleaned.csv` |
| Transmission HFTD Overlay | Processed | `processed/transmission_hftd_overlay.csv` |
| Transmission by Voltage | Processed | `processed/transmission_hftd_by_voltage.csv` |

## Notes

- **Figure D** uses the overlay CSV generated from the old (2021 vintage) HIFLD extract. The 2025 validation confirmed the numbers are materially identical (statewide 22.7% vs 23.2%, PG&E 30.7% vs 30.3%).
- **Figure C** shows 60 corridor circuits with 73% match rate. The PSPS-GIS exploration document reports 77% for a slightly different circuit subset (60 circuits with corridor substation names). The difference reflects expanded corridor substation definitions in the automated matching.
- All figures use the `style_config.py` fire-themed color palette for consistency with existing report figures.
