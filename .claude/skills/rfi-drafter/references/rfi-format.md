# RFI Format — Template & Field Guidance

## Template

```
REQUEST FOR INFORMATION / TECHNICAL QUERY

Project:      [Project Name]
Project No:   [Number]
RFI No:       [Next sequential number from RFI log, or "TBD"]
Date:         [DD/MM/YYYY]
From:         [Contractor — Name, Role]
To:           [Designer — Name, Firm] (via the contract administrator / Project Manager if the contract requires)
Contract:     [JCT / NEC4 form — and whether this is also notified as an early warning (NEC4)]

Subject:      [Clear, specific, < 15 words]

Spec Section: [Uniclass / NBS section and clause, or "N/A — Drawing-only issue"]
Drawing Ref:  [Drawing container ID(s) + revision + status, grid location(s), detail references]

DESCRIPTION:
[Clear description of the issue. What the drawings/specs show,
what the conflict or ambiguity is, and why clarification is needed.
Reference specific sheets, details, grid locations, room numbers.]

SUGGESTED RESOLUTION:
[Propose a solution. Frame as suggestion, not directive. Include
the reasoning. Faster response when the A/E can simply confirm.]

IMPACT IF NOT RESOLVED:
[What construction activity is affected. The date by which a
response is needed to avoid programme impact.]

CONTRACT POSITION:
[NEC4: state whether an early warning has also been recommended.
JCT: state whether a delay notice may be needed. Recommendation
only — never state that a notice has been served.]

ATTACHMENTS:
[List marked-up drawings, photos, reference documents. AgentCM
can generate annotated sheet crops showing the conflict area.]
```

## Field-by-Field Guidance

### Subject Line
Specific enough that anyone can understand the issue from the
subject alone. Include the location and nature of the issue.
- GOOD: "Corridor Width at Grid B Below AD M Vol 2 Para 3.14(b) Minimum"
- GOOD: "Conflicting Finish Schedules — Room 203 Flooring"
- BAD: "Question about the floor plan"
- BAD: "Dimension issue"

### To (Addressee)
Route to the design professional who OWNS the document containing
the issue. Common routing:
- Architectural drawings/specs → Architect
- Structural drawings/specs → Structural Engineer
- M&E drawings/specs → M&E consultant (specific discipline)
- Civil/drainage drawings → Civil Engineer
- Fire strategy questions → Fire Engineer
- Contractor's design portion → the subcontractor/designer holding design responsibility
- Conflict BETWEEN disciplines → Lead designer, CC the other discipline
Route through the contract administrator (JCT) or Project Manager (NEC4)
where the contract says communications go that way.

### Drawing References
Always use the full reference format. Never say "the floor plan"
or "the detail."
- Drawing references: "7001-BBH-01-02-DR-A-00201 rev C02 (status A1), Grid B-4"
- Detail references: "Detail 3 / 7001-BBH-ZZ-ZZ-DR-A-00702"
- Section references: "Section 2 / 7001-XYZ-ZZ-ZZ-DR-S-00401"
- Spec references: "Spec Ss_25_30, clause 410"
- Room references: "Room 2.03 (Meeting Room)"

If multiple sheets are involved, list each with its specific
grid location or area of concern.

### Description
Structure the description in three parts:
1. **What the documents show** — objective statement of current state
2. **What the conflict/ambiguity is** — why this is a problem
3. **Why clarification is needed** — what decision is blocked

Avoid opinion or blame. State facts. Let the evidence speak.

### Suggested Resolution
Common resolution patterns by issue type:
- **Dimension conflict**: "Dimension appears to be [X] based on
  adjacent dimensions. Please confirm."
- **Cross-discipline conflict**: "Recommend aligning with [discipline]
  drawing [sheet] which shows [condition]."
- **Missing detail**: "Request a [detail type] addressing [condition]."
- **Product conflict**: "Suggest using [product] per manufacturer's
  recommendation for this application."
- **Regulation conflict**: "[Approved Document / standard, edition,
  paragraph — from a verified source] states [requirement]. Please
  clarify how the design addresses this."

Always frame as a question or suggestion, never a directive.

### Impact Statement
Include three elements:
1. What work is affected
2. When that work is scheduled
3. When a response is needed to avoid delay

Example: "Partitions at Grid B are programmed to start 15/10.
A response is requested by 01/10 to allow for procurement and
setting out."

## Example RFI

Fictitious project and people. The AD M figure and paragraph are taken from
`reference/ad_m_vol2_access.yaml` (AD M Vol 2, 2015 edition with 2024
amendments) — every regulation reference in a real RFI must trace to a source
the same way.

```
REQUEST FOR INFORMATION / TECHNICAL QUERY

Project:      Example Office Refurbishment (fictitious)
Project No:   0000
RFI No:       RFI-026
Date:         18/09/2026
From:         Example Contractor Ltd — Site Project Manager
To:           Example Architects — Project Architect (via the Project Manager)
Contract:     NEC4 ECC (early warning also recommended)

Subject:      Corridor Width at Grid B Reduced Below AD M Vol 2
              Para 3.14(b) by Door Swing

Spec Section: N/A — Drawing / Building Regulations issue
Drawing Ref:  0000-EXA-01-01-DR-A-00201 rev C02 (status A1),
              Grid B between Rooms 1.04 and 1.05; door tag 1.05A

DESCRIPTION:
The corridor between Rooms 1.04 and 1.05 is dimensioned at 1200mm
clear on drawing 00201 rev C02. AD M Vol 2 para 3.14(b) gives an
unobstructed width, excluding projections, of at least 1200mm. Door
1.05A opens into the corridor and, when open, projects into that width.
It is not clear whether the design intends the door to be read as a
projection, or how the corridor meets para 3.14(b) with the door open.

SUGGESTED RESOLUTION:
Either (a) widen the corridor locally to keep 1200mm clear with the
door open, or (b) re-hang or recess door 1.05A so it does not open into
the corridor. Contractor's interpretation only — please confirm.

IMPACT IF NOT RESOLVED:
Partitions at Grid B are programmed to start 15/10/2026. A response
is requested by 01/10/2026 to avoid delay to partitions and drylining.

CONTRACT POSITION:
Recommend this is also notified as an early warning (possible change
to the Scope / programme).

ATTACHMENTS:
1. Annotated crop of drawing 00201 at Grid B showing the conflict area
2. Door schedule excerpt for door 1.05A
```
