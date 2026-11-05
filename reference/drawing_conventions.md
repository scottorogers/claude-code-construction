# Construction Drawing Conventions

## UK Drawing and Document Numbering (BS EN ISO 19650-2 UK National Annex)

UK projects normally name every information container (drawing, model, spec,
schedule) to the BS EN ISO 19650-2 UK National Annex convention. Read the
project's **BIM Execution Plan (BEP)** or **Information Standard** first — it
fixes the field codes for the job and overrides anything here.

Worked example from UK BIM Framework Guidance Part 2 (Figure 4):
`7001-BBH-ZZ-ZZ-DR-A-00301`

| Field | Example | Meaning |
|---|---|---|
| Project | 7001 | Project code |
| Originator | BBH | Organisation that produced it |
| Volume / System | ZZ | Zone, block or system (ZZ = all / multiple) |
| Level / Location | ZZ | Floor or location (ZZ = multiple) |
| Type | DR | Container type (DR = drawing, M3 = 3D model) |
| Role | A | Discipline role of the originator |
| Number | 00301 | Sequence number |

Role and Type code lists: **VERIFY against the project BEP** — they were not
extracted from the National Annex for this file. Do not decode a role letter
from memory; if the BEP is not in the project documents, report the code as
read and say it could not be decoded.

### Status (suitability) codes — Table NA.1

Source: UK BIM Framework, ISO 19650 Guidance Part 2 (3rd edition).

| Code | Meaning | Can it be built from? |
|---|---|---|
| S0 | Initial status (work in progress) | No |
| S1 | Suitable for coordination | No |
| S2 | Suitable for information | No |
| S3 | Suitable for review and comment | No |
| S4 | Suitable for stage approval | No |
| S6 | Suitable for PIM authorization | No |
| S7 | Suitable for AIM authorization | No |
| A1, A2… | Authorized and accepted | Yes — check the contract for what "for construction" means on this job |
| B1, B2… | Partial sign-off (with comments) | Only the signed-off parts; comments must be resolved |
| CR | As constructed record document | Record only |

S5 has been withdrawn and should not appear on current drawings. **Red flag:**
installing from an S-status drawing. That is working at risk — raise it.

### Revision codes

- `P01`, `P02`… — Preliminary (non-contractual)
- `C01`, `C02`… — Contractual
- `P01.01`, `P01.02`… — WIP versions within a revision

A drawing moving from P to C is the point it becomes contractual. Compare
the revisions before accepting a C revision as the
basis of an install.

### Scales

UK drawings are metric. Always read the scale against the printed sheet size
(A0/A1/A3) and a scale bar or known dimension — see `scale_factors.yaml`.

---

## US Sheet Numbering (US National CAD Standard — legacy / US projects only)

Standard format: `{Discipline Prefix}-{Level/Category}.{Sequence}`

### Discipline Prefixes

| Prefix | Discipline |
|---|---|
| G | General (cover, notes, symbols, abbreviations) |
| H | Hazardous Materials |
| V | Survey / Geotechnical |
| C | Civil / Site |
| L | Landscape |
| S | Structural |
| A | Architectural |
| I | Interiors |
| Q | Equipment |
| F | Fire Protection |
| P | Plumbing |
| D | Process / Piping |
| M | Mechanical / HVAC |
| E | Electrical |
| W | Distributed Energy |
| T | Telecommunications |
| R | Resource (BIM reference) |
| X | Other Disciplines |
| Z | Contractor / Shop Drawings |

### Level/Category Digit

| Digit | Category |
|---|---|
| 0 | General (schedules, notes, diagrams, legends) |
| 1 | Plans — Lowest level (basement, site) |
| 2 | Plans — Ground/first floor |
| 3 | Plans — Upper floors |
| 4 | Elevations (A) / Plans continued (others) |
| 5 | Sections (A) / Plans continued (others) |
| 6-7 | Details and enlarged plans |
| 8 | Sections and details (A) |
| 9 | 3D views, schedules, or details |

Example: `A-2.01` = Architectural, Level 2 (first floor), sheet 01

## Common Symbols

### Section Cut
A line with arrows showing the direction of view. End markers are triangles or circles containing the section number over the sheet number where the section is drawn.

### Detail Callout
A circle (sometimes with a tail/leader) containing the detail number over the sheet number. Example: `5` over `A-5.01` means detail 5 is found on sheet A-5.01.

### Elevation Marker
A triangle or circle with a number pointing in the direction of view. The number references the elevation drawing, and the sheet number appears below.

### Door/Window Tags
Circles or hexagons containing an alphanumeric mark that cross-references a schedule.

### Revision Cloud
An irregular bumpy closed shape enclosing changed content. Accompanied by a delta triangle with the revision number.

### North Arrow
Indicates drawing orientation. Project north may differ from true north.

### Grid Lines / Column Lines
Lettered (A, B, C) in one direction and numbered (1, 2, 3) in the other. These are the primary location reference system.

### Level / Elevation Marks
Triangles or circles at section cuts showing elevation above a datum (usually finish floor).

## Line Types

| Line | Meaning |
|---|---|
| Solid thick | Visible outlines, walls in section |
| Solid thin | Dimensions, leaders, hatching |
| Dashed | Hidden or below-grade elements |
| Dash-dot | Center lines, grid lines |
| Dash-dot-dot | Property lines |
| Dotted | Elements above (shown on plan) |

## Hatching / Fill Patterns

| Pattern | Material |
|---|---|
| Diagonal lines (45°) | Earth/fill (in section) |
| Small dots | Concrete (in section) |
| Brick pattern | Masonry (in section) |
| Diagonal cross-hatch | Steel/metal (in section) |
| Wavy lines | Insulation |
| Wood grain | Wood (in section) |
| No fill (white) | Open space / air |

## Title Block Standard Fields

Every drawing sheet has a title block containing:
- Project name and number
- Sheet number and title
- Scale(s)
- Date
- Drawn by / Checked by initials
- Architect/Engineer firm name (US drawings also carry a professional seal; UK drawings do not)
- Revision history (number, date, description)
- Client name
- Project location (address, postcode)
- UK: ISO 19650 container ID, status code (S0–S7 / A / B / CR) and revision (P01 / C01)
