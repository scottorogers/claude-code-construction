---
name: code-researcher
description: >
  UK regulation and standards gap analysis — extracts what project docs cite,
  researches what Building Regs, Approved Documents, BS 7671 and BS/BS EN
  standards should apply, surfaces the delta. Triggers: 'regs check', 'what
  regs apply', 'Part B', 'Part M', 'BS 7671', 'means of escape'.
argument-hint: "<scope_or_question> e.g. 'Ss_70_30_45 LV systems' or 'means of escape from the plant deck'"
---

# Code Researcher — Scope-Specific Gap Analysis

## What This Skill Does

An engineer managing one or more scopes asks: *"Are there any regulatory or
standards requirements for this scope that I'm missing?"*

**UK framework.** "Code" in this skill means the UK statutory and standards
framework: the Building Regulations 2010 and Approved Documents (England), the
devolved equivalents in Wales, Scotland and Northern Ireland, the Building
Safety Act 2022 regime for higher-risk buildings, CDM 2015, the Regulatory
Reform (Fire Safety) Order 2005, BS 7671, and the BS / BS EN standards the
spec and regulations call up. Start from `reference/uk_regulations.yaml`.

This skill answers that question in three passes:

**Pass 1 — What the scope already addresses**
Read the actual project documents — spec sections, drawings, schedules — and
extract every code citation, standard reference, and requirement already
incorporated by the design team.

**Pass 2 — What should apply**
Research all codes and standards that apply to this type of work in this
jurisdiction, regardless of what the project documents say.

**Pass 3 — The gap**
Diff Pass 1 against Pass 2. Present only what's in Pass 2 but absent from
Pass 1, with confidence levels and specific source citations from both the
code and the project documents.

**This is a gap finder, not a code summary.** If the spec already addresses a
requirement correctly, it does not appear in the output. The engineer's time is
spent only on things that may actually be missing.

---

## Framing Rule (Non-Negotiable)

Every finding is framed as:
> *"[Regulation / Approved Document para / standard clause X] requires [Y].
> The project documents [address this at / do not appear to address this].
> Confidence: [level]. Recommended action: [action]."*

Never frame findings as COMPLIANT / NON-COMPLIANT. The designer and building
control (local authority, registered building control approver, or the
Building Safety Regulator for higher-risk buildings) make compliance
determinations. This skill provides research.

**No citation without a source.** A paragraph, table or regulation number goes
in a finding only if it came from (a) `reference/` with its source line, (b) a
public document fetched in this session (GOV.UK, legislation.gov.uk), or (c) the
project documents. BS and BS EN clause text is paywalled — cite the standard
number and the edition from the spec, and mark clause-level content
`[VERIFY: user to confirm against licensed copy]`. Never fill a number from
memory.

---

## Research Philosophy

This skill uses a document-grounded research approach:
- **Construction documents are ground truth.** Every claim about what the project does or does not address must trace to a specific document read in Pass 1. Never infer project status from memory or assumption.
- **Claude's domain knowledge drives topic discovery.** Use your training knowledge of construction codes, standards, and regulatory frameworks to identify what requirements SHOULD apply to this scope. The documents tell you what IS addressed; your knowledge tells you what to check for.
- **Web research confirms current editions.** Approved Documents are amended regularly (AD B was updated 16/09/2026) and transitional provisions decide which version applies to a project. Use GOV.UK and legislation.gov.uk to confirm the current edition and read exact wording. Do not rely on training knowledge for paragraph numbers or thresholds.
- **Reference files hold verified figures.** `${CLAUDE_SKILL_DIR}/../../reference/` contains `ad_b_vol2_means_of_escape.yaml` and `ad_m_vol2_access.yaml` (figures with table/paragraph refs) and `uk_regulations.yaml` (legislation, ADs, BS 7671 edition, standards, contract forms). Items marked VERIFY there are not checked — treat them as unverified.
- **Which nation?** Approved Documents are England. Wales has its own ADs; Scotland uses the Building (Scotland) Regulations 2004 Technical Handbooks; Northern Ireland uses Technical Booklets. Confirm before researching — never apply English figures elsewhere.

---

## Workflow Overview

```
Phase 1 — Context and Scope Definition
  1a  Gather project context (jurisdiction, occupancy, construction type)
  1b  Define the research scope (which spec sections, which question)
  1c  USER CHECKPOINT — confirm scope before any research begins

Phase 2 — Project Document Extraction (Pass 1)
  2a  Read all project documents in scope
  2b  Extract every code citation, standard reference, requirement
  2c  Build the "already addressed" inventory

Phase 3 — Code Research (Pass 2)
  3a  Research jurisdiction and adopted code editions
  3b  Research applicable requirements for this scope and work type
  3c  USER CHECKPOINT — interim findings, confirm continuation

Phase 4 — Gap Analysis (Pass 3)
  4a  Diff research findings against project document inventory
  4b  Classify each gap by severity and confidence
  4c  USER CHECKPOINT — review gaps before report is written

Phase 5 — Report
  5a  Generate structured gap report
  5b  Write graph entry
```

**Human checkpoints at 1c, 3c, and 4c.** Do not skip them.

---

## Phase 1 — Context and Scope Definition

### 1a — Gather Project Context

Collect minimum required project parameters. Check in this order:

**AgentCM project files (if `.construction/` exists):**
- `.construction/project.yaml` — location, occupancy, construction type
- `.construction/index/sheet_index.yaml` — drawing set composition
- Database (read `query_command` from `.construction/database.yaml`):
  - `{query_command} -c "SELECT * FROM v_room_profile WHERE room_number = '...'"` — rooms with schedule data
  - `{query_command} -c "SELECT * FROM v_sheet_contents WHERE sheet_number = '...'"` — elements on sheets
  - Orientation: `{query_command} -c "SELECT COUNT(*) FROM sheets WHERE project_id = '...'; SELECT COUNT(*) FROM rooms WHERE project_id = '...'"`

**Project documents (read directly):**
- Architectural title block — project name, address, postcode (sets the nation)
- Preliminaries (`PM_10` Project information / NBS Preliminaries "Description
  of the project") — building use, purpose group, height, new build or
  refurbishment
- Fire strategy report — purpose group(s), evacuation strategy, height, sprinklers;
  this is the single most important input for any fire or escape question
- `PM_40` Design and approvals information — building control route (local
  authority / registered building control approver / Building Safety
  Regulator), planning conditions, standards the design team names
- Employer's Requirements / Scope — client standards that exceed regulation

Minimum required context — write to `.construction/code_research/project_context.yaml` using the schema at:
→ `${CLAUDE_SKILL_DIR}/references/schemas.yaml` § project_context

If any required field cannot be found in the documents, ask the user before
proceeding. Do not assume the nation, the purpose group, the building height,
or whether it is a higher-risk building — these determine which provisions
apply and an incorrect assumption cascades through the entire analysis.

### 1b — Define the Research Scope

Parse the user's question to identify:

1. **Target scope** — which spec sections, drawing sheets, systems, or elements
   the engineer wants checked. Examples:
   - A spec section: "Ss_70_30_45 Low-voltage systems"
   - A system: "means of escape from the level 5 plant deck"
   - A trade package: "mechanical package, Ss_60 and Ss_65 sections"
   - A regulation topic: "AD M access to the WC cores"

2. **Research question** — what specifically the engineer is worried about.
   Examples:
   - "Am I missing any code requirements?"
   - "Does the spec cover the slip resistance requirements?"
   - "Are there fire separation requirements I haven't addressed?"

3. **Scopes in scope** — if the engineer is managing multiple scopes (e.g.,
   scopes A through C), confirm which ones this research covers.

Write to `.construction/code_research/scope_definition.yaml` using the schema at:
→ `${CLAUDE_SKILL_DIR}/references/schemas.yaml` § scope_definition

Research topics are generated from the combination of:
- The work type (resinous flooring → surface profile requirements, slip
  resistance, chemical resistance, substrate preparation)
- The building use / purpose group (catering → environmental health and food hygiene overlay; data centre → client availability standard, BS EN 50600)
- The project type (refurbishment → material alteration, existing fire strategy, asbestos; higher-risk building → BSR gateways and change control)
- The question framing (gap analysis → broader research than targeted check)

**Use your full domain knowledge** to identify research topics. You know what
code requirements typically apply to each type of construction work, which
regulatory authorities have jurisdiction, and what gaps commonly appear in
specifications. The project documents tell you what the engineer has already
addressed — your job is to identify everything they should have considered.

### 1c — USER CHECKPOINT: Confirm Scope

Present to the user:

```
I have enough context to start. Before I begin research, here's what I'm planning:

PROJECT
  Name:          [project_name]
  Location:      [town, postcode — nation: England / Wales / Scotland / NI]
  Occupancy:     [group]
  Use / height:  [purpose group(s) from fire strategy, storeys/height, HRB yes/no]
  Sprinklered:   [yes/no/unknown]
  Code year:     [inferred from drawing date]

SCOPE I'LL RESEARCH
  Spec sections: [list]
  Sheets:        [list, or "none specified — I'll search for relevant sheets"]
  Your question: [restated in plain language]

RESEARCH TOPICS I'VE IDENTIFIED
  1. [topic] — because [reason derived from scope]
  2. [topic] — because [reason derived from scope]
  3. [topic] — because [reason derived from scope]
  [...]

TOPICS I'M NOT INCLUDING (and why)
  • [topic] — not applicable to this occupancy/type
  • [topic] — already covered by the fire strategy / Preliminaries

Before I spend time researching, please confirm:
  • Is the project context correct?
  • Should I add or remove any research topics?
  • Are there specific code concerns you already have that I should prioritize?
```

**Do not begin Phase 2 until the user responds.**

---

## Phase 2 — Project Document Extraction (Pass 1)

This phase reads what the project documents already say. It runs before web
research so the gap analysis has a firm baseline.

### 2a — Read All In-Scope Documents

For each spec section in scope:
- Read the full section (all parts — General, Products, Execution)
- Use pdfplumber for text-layer PDFs; use vision for scanned or image-heavy pages

For drawing sheets:
- Read title block, notes, schedules, and details relevant to the scope
- Use vision for plan sheets; extract text from schedules if text-layer

For referenced standards within spec sections:
- Note every standard cited (BS, BS EN, BS EN ISO, BS 7671, CIBSE/BSRIA guides,
  manufacturer certification schemes) with its edition year as cited in the spec.
  A standard cited with no year is itself a finding.

### 2b — Extract All Code and Standard Citations

For each document read, extract every code reference, standard citation, and
requirement into a structured inventory. Write to `.construction/code_research/pass1_project_inventory.yaml` using the schema at:
→ `${CLAUDE_SKILL_DIR}/references/schemas.yaml` § pass1_project_inventory

**Critical extraction discipline:**
- Record what IS there (citations found, requirements stated)
- Also record what is ABSENT that you would expect to find
- Do not interpret absence as compliance — absence is a potential gap
- Note edition years as specified — a correct requirement cited against the
  wrong edition is a potential gap

### 2c — Build the "Already Addressed" Inventory

Summarize Pass 1 into a flat inventory used for gap diffing in Phase 4. Write to `.construction/code_research/pass1_summary.yaml` using the schema at:
→ `${CLAUDE_SKILL_DIR}/references/schemas.yaml` § pass1_summary

---

## Phase 3 — Code Research (Pass 2)

### 3a — Research Jurisdiction and Adopted Codes

Before researching requirements, establish which regime and which edition of
each document applies. This is non-negotiable — Approved Documents carry
transitional provisions, so the version that applies depends on when the
building notice / full plans application / initial notice was given and when
work started.

Check, in this order:
```
1. Nation (England / Wales / Scotland / NI) from the address.
2. Higher-risk building? (Building Safety Act 2022 regime — BSR is the
   building control authority and gateway approvals apply.)
3. Building control route and application date (from PM_40 or the client).
4. Current Approved Document editions — GOV.UK collection page, and the
   transitional provisions on each AD's publication page.
5. BS 7671 edition the contract names (current: BS 7671:2018+A4:2026).
6. Standards editions as cited in the spec — flag undated citations.
```
Search GOV.UK / legislation.gov.uk first, e.g.
`"Approved Document B" transitional provisions site:gov.uk`.

Write to `.construction/code_research/jurisdiction.yaml` using the schema at:
→ `${CLAUDE_SKILL_DIR}/references/schemas.yaml` § jurisdiction

If the applicable edition cannot be confirmed, mark it `uncertain` and note
this prominently in the report. Do not assume the latest published edition is
the one that applies to this project.

### 3b — Research Requirements for Each Topic

For each topic in the confirmed research outline, research what the applicable
codes require. Organize research by logical topic clusters, not fixed batch sizes.

**For each topic, establish these three things:**

1. **What the regulation requires** — the Building Regulations requirement
   (e.g. B1, M1) and the Approved Document paragraph/table that gives the
   guidance, with edition. Fetch the AD and read it; do not rely on training
   memory for exact wording or numbers. Remember ADs are guidance — the
   requirement is the regulation; a fire-engineered or BS 9999 route can be
   equally valid.
2. **What standards apply** — the BS / BS EN standards the AD, the spec or the
   fire strategy calls up (BS 7671, BS 5839-1, BS 5266-1, BS EN 50173/50174,
   BS 8300…). Clause text is paywalled — cite number and edition, mark
   clause content `[VERIFY]`.
3. **What other authorities apply** — fire and rescue service consultation,
   environmental health, the water undertaker (Water Fittings Regulations),
   the DNO, planning conditions, insurer requirements, and the Regulatory
   Reform (Fire Safety) Order 2005 for the occupied building.

Use `${CLAUDE_SKILL_DIR}/../../reference/ad_b_vol2_means_of_escape.yaml` and
`ad_m_vol2_access.yaml` for verified figures (each carries its table/paragraph
ref). Read the table notes in the source PDF before relying on a figure.

Write to `.construction/code_research/topics/{slug}.yaml` using the schema at:
→ `${CLAUDE_SKILL_DIR}/references/schemas.yaml` § topic_findings

**Adaptive scope expansion:** If research reveals that a code requirement likely
applies but may be addressed in a spec section or drawing not yet read in Pass 1,
read that document before classifying the topic as a gap. Update the Pass 1
inventory with any new citations found. Note the additional documents read when
reporting to the user at checkpoint 3c.

### 3c — USER CHECKPOINT: Interim Findings

After completing a cluster of related topics, report to the user:

```
Completed research on [topic 1], [topic 2], and [topic 3].

(Format illustration only — every reference below must come from a source
read in this session or from reference/.)

PRELIMINARY GAPS IDENTIFIED SO FAR
  ⚠  HIGH   Fire-resistant cabling — spec Ss_70_30_45 does not state cable
             type for emergency lighting circuits; fire strategy section [x]
             requires [y]. Standard: BS 5266-1 [VERIFY clause].
  ⚠  HIGH   BS 7671 edition — spec cites "current edition" with no date;
             contract date falls after A4:2026 publication. Confirm A4.
  ○  MEDIUM  Cable CPR Euroclass — not stated for containment in escape
             corridors; fire strategy may set it (will check)

NO GAP (already addressed in spec)
  ✓  Emergency lighting duration — stated in Ss_70_80 clause [n]
  ✓  Test certificates — EIC and schedules listed in PM_70 clause [n]

UNCERTAIN (couldn't confirm)
  ?  Transitional provisions — could not confirm which AD B version applies;
     need the building control application date

Continuing with [next batch]: [topic 4], [topic 5].
Do you want me to dig deeper on any of these before continuing, or shall I proceed?
```

---

## Phase 4 — Gap Analysis (Pass 3)

### 4a — Diff Research Against Project Inventory

Compare every research finding from Phase 3 against the Pass 1 project
inventory. Write to `.construction/code_research/gap_analysis.yaml` using the schema at:
→ `${CLAUDE_SKILL_DIR}/references/schemas.yaml` § gap_analysis

Classify each finding into one of: `gaps` (with severity + confidence), `already_addressed`, or `uncertain`.

### 4b — Classify Each Gap

Each gap gets a severity and confidence rating:

**Severity:**
- `HIGH` — a code requirement clearly applies, is not addressed in the project
  documents, and creates regulatory or safety risk if unresolved
- `MEDIUM` — a code requirement likely applies but may be addressed elsewhere
  (e.g., in a Preliminaries section not yet reviewed) or its applicability
  depends on a condition that hasn't been confirmed
- `LOW` — a code reference that could be added for completeness but whose
  absence is unlikely to cause a compliance issue

**Confidence:**
- `confirmed` — the code requirement is definitively established (correct
  jurisdiction, correct edition, correct applicability) and the project
  document status is definitively established (read the full section)
- `needs_review` — the requirement likely applies but requires information
  not available in the current documents (building control confirmation, additional spec
  sections not provided, etc.)
- `uncertain` — conflicting sources, could not confirm jurisdiction's
  adopted code edition, or the code's applicability to this specific scope
  is genuinely ambiguous

### 4c — USER CHECKPOINT: Review Gaps Before Report

Before generating the report, present the gap summary:

```
GAP ANALYSIS COMPLETE

(Format illustration only — references must come from sources read this session.)

HIGH-CONFIDENCE GAPS (take action)
  GAP-001 ⚠ HIGH    Fire-stopping — no tested system named for containment
                     penetrations through compartment walls (Ss_70_30_10);
                     fire strategy section [x] requires compartmentation at [y]
                     Recommended action: TQ to designer for system and installer
                     certification requirement

  GAP-002 ⚠ HIGH    BS 7671 edition — spec cites no edition
                     Current is BS 7671:2018+A4:2026 (reference/uk_regulations.yaml)
                     Recommended action: confirm design edition in writing

MEDIUM-CONFIDENCE GAPS (confirm and close)
  GAP-003 ○ MEDIUM   Cable CPR Euroclass — not stated in Ss_70_30_45; may be
                      covered in the fire strategy — confirm and cross-reference

UNCERTAIN (need more information)
  ?  AD B transitional provisions — application date needed to confirm version

ALREADY ADDRESSED (no action needed)
  ✓  Emergency lighting design to BS 5266-1 — Ss_70_80 clause [n]
  ✓  Test certification — EIC and schedules — PM_70 clause [n]
  ✓  Installer qualification — competent person scheme membership required

Before I write the report:
  • Are any of these gaps ones you were already aware of and have addressed
    outside the documents I reviewed?
  • Should I research any topic further before finalizing?
  • Any gaps you want to remove from the report?
```

---

## Phase 5 — Report

### 5a — Generate Gap Report

Write to `.construction/code_research/report_{scope}_{date}.md` using the template at:
→ `${CLAUDE_SKILL_DIR}/references/gap_report_template.md`

Populate all placeholder fields from the gap_analysis.yaml and jurisdiction.yaml data. The report must include: applicable codes table, all gaps (action required + confirm and close), uncertain items, already addressed items, documents reviewed, and the disclaimer.

### 5b — Write Graph Entry

```bash
${CLAUDE_SKILL_DIR}/../../bin/construction-python \
  ${CLAUDE_SKILL_DIR}/../../scripts/graph/write_finding.py \
  --type "code_gap_analysis" \
  --title "Code gap analysis: {scope} — {n_gaps} gaps identified" \
  --data '{
    "scope": "[spec sections or topic]",
    "topics_researched": 0,
    "already_addressed": 0,
    "gaps_high": 0,
    "gaps_medium": 0,
    "gaps_low": 0,
    "uncertain": 0,
    "jurisdiction_confirmed": true
  }'
```

---

## Resumption

Check for `.construction/code_research/` before starting:

| Files Present | State | Action |
|---------------|-------|--------|
| Nothing | Fresh start | Begin Phase 1 |
| `scope_definition.yaml` only | Scope confirmed, research not started | Begin Phase 2 |
| `pass1_summary.yaml` | Project extraction done | Begin Phase 3 |
| `topics/` partial | Research in progress | Resume from next unresearched topic |
| All topics complete, no `gap_analysis.yaml` | Research done | Begin Phase 4 |
| `gap_analysis.yaml` exists | Gaps identified | Present to user, go to Phase 5 |
| `report_*.md` exists | Complete | Offer to update or re-run |

---

## Discipline Notes

PE discipline guidance for jurisdiction research, scope boundaries, regulatory overlays, and confidence levels:
→ `${CLAUDE_SKILL_DIR}/references/discipline_notes.md`

## File Safety
Never overwrite an existing gap report. Version output files (`_v2`, `_v3`) if a prior version exists at the target path.

---

## Allowed Scripts

- `${CLAUDE_SKILL_DIR}/../../bin/construction-python`
- `${CLAUDE_SKILL_DIR}/../../scripts/graph/write_finding.py`
