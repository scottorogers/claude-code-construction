---
name: subcontract-writer
description: >
  Generate a UK subcontract (JCT 2024 DBSub/SBCSub or NEC4 ECS/ECSS) from a
  firm's template, awarded tender and project specs. Outputs Word. Triggers:
  'subcontract', 'sub order', 'draft subcontract', 'ECS', 'DBSub'. Requires
  awarded tender.
argument-hint: "<scope_of_work>"
disable-model-invocation: true
---

# Subcontract Writer

Generates a complete subcontract for **UK** projects from a firm's template, the awarded tender, and project specifications. It supports both **JCT 2024** sub-contracts (DBSub/A + DBSub/C, SBCSub/A + SBCSub/C, SBCSub/D/A + SBCSub/D/C) and **NEC4** (ECS / ECSS) — see `reference/uk_regulations.yaml` § contracts.

**Copyright rule:** JCT and NEC conditions are licensed publications. Never reproduce their printed clauses. The output is the firm's agreement / order and schedules — Sub-Contract Particulars (JCT) or Subcontract Data (NEC4), scope, pricing, programme, the firm's schedule of amendments or Z clauses — which **incorporate the standard conditions by reference**. If the firm's template contains the full printed conditions, preserve them only as the template provides them and flag that the firm must hold a licence. **You are the intelligence layer** — you read every document, extract all data, generate every article's text, make legal/commercial judgments, and write fully-populated JSON files. The Python formatter is a thin rendering utility that makes no content decisions.

**Output:** Word document (.docx) matching the firm's template structure.

**Dependency:** Requires `python-docx` in the construction Python environment.

**Key principle:** The bid document is the PRIMARY input. It establishes what was priced, at what rates, with what inclusions and exclusions. Specifications inform scope descriptions and technical requirements. The template provides article structure and standard boilerplate.

---

## Pipeline Position
This skill can be invoked directly when the user has an awarded bid and wants to generate a subcontract, or as the final step of the bid pipeline:
```
/bid-tabulator → /bid-evaluator → user confirms → THIS SKILL
```
Either way, the awarded bid document (Slot B) is the mandatory input.

## Mode Detection
Check for `.construction/` directory at the project root.
- **AgentCM mode**: Read specs from `.construction/spec_text/{section}.txt`. Use sheet index from `.construction/index/sheet_index.yaml` for drawing references. Read project metadata from `.construction/CLAUDE.md`.
- **Flat File mode**: Discover spec PDFs via project `CLAUDE.md` paths or directory search. Read drawing sheets directly from PDF.

---

## Architecture: Five Phases in Order

Execute in five sequential phases. Each phase has a defined output that must be completed before the next begins. **Do not skip phases or combine them.** The most common failure mode is attempting Phase 4 (writing) before Phase 3 (validation) is complete.

```
Subcontract Writer Progress:
Phase 1  →  Phase 2  →  Phase 3  →  USER CHECKPOINT  →  Phase 4  →  Phase 5
Triage     Extract     Validate      Confirm data         Write       Verify
```

---

## Phase 1 — Document Triage and Slot Assignment

Before reading any document substantively, assign each uploaded file to its slot. State the assignments to the user before proceeding.

| Slot | Role | Source | What It Provides |
|------|------|--------|-----------------|
| A | Template | Subcontract PDF/DOCX | Article structure, boilerplate language, required sections |
| B | Awarded bid | Subcontractor bid PDF | **Contract sum, quantities, unit rates, inclusions, exclusions, VE alternates** |
| C | Specifications | Spec section PDFs | Scope descriptions, submittal requirements, warranty clauses, installer qualifications |
| D | Drawings | Finish schedule, floor plans | Room codes, area takeoffs, scope boundaries |

**Slot B is mandatory.** If missing, stop and output:
```
I need the awarded subcontractor's bid document before I can generate this
subcontract. The bid is the source of truth for the contract sum, quantities,
and unit rates. Which file is the awarded bid?
```

Read Slot A first to understand the required article structure. Note every article heading. Flag any article that requires project-specific content (not just boilerplate) — these become required extraction targets in Phase 2.

If no template is provided, ask: "Do you have a standard subcontract template or order form?" If none is available, ask which form governs — **JCT** (which sub-contract) or **NEC4** (ECS or ECSS, which Main Option) — and use the matching fallback structure in Phase 4. Do not pick the form yourself; it must match the main contract.

### Contract Form Detection

Read the template, the tender enquiry and the main contract references. Record `contract_form`:
- `jct_dbsub` / `jct_sbcsub` / `jct_sbcsub_d` — JCT 2024 family (check edition year in the template)
- `nec4_ecs` / `nec4_ecss` — NEC4, plus `main_option` and `secondary_options` from the Subcontract Data
- `bespoke` — firm's own conditions

The vocabulary changes with the form — never mix them:

| Concept | JCT | NEC4 |
|---|---|---|
| Change | Variation (instruction) | Compensation event |
| Delay mechanism | Relevant Event → extension of time | Compensation event → change to Completion Date |
| Programme | Sub-Contract programme / progress | Accepted Programme |
| Price | Sub-Contract Sum / Sum | Prices / Price for Work Done to Date |
| Finish | Practical Completion | Completion |
| Defects | Rectification Period | defects date / defect correction period |
| Damages for delay | LADs (Sub-Contract Particulars) | delay damages (Option X7) |
| Risk notice | Notice of delay | Early warning |
| Spec / requirements | Sub-Contract Documents | Scope |

---

## Phase 2 — Structured Extraction, One Slot at a Time

Run a separate extraction pass for each slot. Write extracted data to `scope_data.json` incrementally. Do not combine slots in a single read.

### Slot B Extraction (Bid Document) — Run First

Read the bid PDF using vision. Extract every field below. Mark any field not found as `MISSING` — do not infer or estimate.

**Commercial data:**
- Subcontractor company name (exact legal name from letterhead)
- Address, phone, email
- Company registration number (Companies House) and VAT number
- CIS status (gross / net) if stated
- Estimator/contact name
- Proposal number and date
- Bid validity period (if stated)
- Total sum (exact amount in £, stating whether VAT exclusive — UK tenders normally are)

**Scope data:**
- Line items with: spec section, description, quantity, unit, unit rate, extended amount
- Inclusions list (verbatim from bid)
- Exclusions list (verbatim from bid — critical for scope gap prevention)
- Value engineering options / alternatives with ID, description, and saving
- Qualifications or clarifications

**Verify:** Line item amounts must sum to the total contract sum. If they don't, flag the discrepancy.

### Slot A Extraction (Template)

**If .docx template:** Use python-docx to read headings, paragraphs, and identify article structure.

**If PDF template:** Use vision to read the template. Rasterize pages if needed:
```bash
${CLAUDE_SKILL_DIR}/../../bin/construction-python ${CLAUDE_SKILL_DIR}/../../scripts/pdf/rasterize_page.py template.pdf {page} --dpi 200 --output template_page_{page}.png
```

Extract the list of required articles and any fill-field placeholders (`[DATE]`, `[CONTRACT SUM]`, `[SUBCONTRACTOR]`).

For each article, determine:
- `number` and `title` (exactly as shown in template)
- `content_type`: one of:
  - `"preserve"` — standard boilerplate (payment terms, insurance, dispute resolution, indemnity, safety, default/termination, general provisions). Transcribe the EXACT text verbatim.
  - `"generate"` — scope-specific content (scope of work, contract documents, schedule, submittals, warranty). You will write this from extracted data.
  - `"fill-in"` — project-specific values (contract sum, dates). You will populate from the Data Model.

**Critical:** Transcribe ALL preserved article text verbatim. Do not summarize or paraphrase template boilerplate.

### Slot C Extraction (Specifications)

For each specification section listed in the tender scope, read the PDF and extract the requirements below. NBS sections (Uniclass `Ss_` / CAWS) are organised by clause number, not US Parts 1–3 — find each topic by heading. One extraction block per section.

Extract per spec section:
- **Submissions / technical submittals:** drawings, product data, samples, certification, design calculations (contractor's design portions)
- **Quality and competence:** installer qualifications, manufacturer-certified installers, competent person schemes, third-party certification (fire-stopping, fire doors, fire alarm), mock-ups, testing
- **Warranty / guarantee provisions:** manufacturer guarantees, system warranties (e.g. structured cabling system warranty), periods
- **Testing and commissioning:** test regime, witness requirements, certificates (e.g. EIC under BS 7671, cable test results)
- **Execution:** installation methods, tolerances, protection, environmental conditions

Also check the Preliminaries (`PM_` sections / NBS Preliminaries) for project-wide requirements: CDM 2015 duties and RAMS, site rules, CSCS/ECS cards, BIM/information requirements, social value, BREEAM, handover and O&M deliverables.

### Slot D Extraction (Drawings/Finish Schedule) — If Provided

Extract room/area codes relevant to scope boundaries. Identify explicit exclusions (rooms marked "by others" or scoped to a different trade). This extraction is scope-dependent — only extract data relevant to the trade being contracted.

---

## Phase 3 — Data Validation

Before surfacing anything to the user, validate the extracted data. Every `MISSING` field in a required category is a blocking error.

### Required Fields (blocking — cannot proceed if absent)

| Field | Source | Why Required |
|-------|--------|--------------|
| `subcontractor.company_name` | Slot B letterhead | Legal party identification |
| `subcontractor.company_number` | Slot B letterhead/footer or Companies House | Legal party identification |
| `subcontractor.proposal_number` | Slot B header | Bid traceability |
| `contract_form` | Template / tender enquiry | Decides vocabulary and structure |
| `contract_sum.formatted` | Slot B | Must include £ and comma formatting; state ex-VAT |
| `contract_sum.written_words` | Computed | Required for legal enforceability |
| `pricing_schedule` (≥1 entry) | Slot B | Quantities from tender only (BoQ / activity schedule / lump sum breakdown) |
| `exclusions` (non-empty) | Slot B | Scope gap prevention |
| Per-spec submittal requirements | Slot C | Cannot leave the submittals schedule as placeholder |
| Per-spec warranty provisions | Slot C | Cannot leave the warranty schedule as placeholder |

Spec-specific requirements are conditional — only required if that spec section appears in the bid scope.

### Legal Completeness Checks

- Contract sum written words matches numeral mathematically
- Pricing schedule quantities match the tender (not master scope estimates)
- No quantity in the pricing schedule differs from the tender by more than 2%
- VE options list is complete (check all tender pages — options often appear on page 2+)
- Payment terms comply with the Construction Act (HGCRA 1996 Part II as amended): an adequate mechanism for interim payments, due dates and final dates, payment notice and pay less notice, no pay-when-paid (except upstream insolvency), right to adjudicate. Flag any template term that cuts across these for legal review — do not redraft statutory terms yourself.
- Exclusions cross-checked against drawings (if Slot D provided)

### Compute Derived Fields

After validation, compute fields the user will need to confirm:

| Derived Field | How to Compute |
|---------------|----------------|
| `subcontract_number` | Firm's order numbering from template, or `[MC TO ASSIGN]` |
| `start_and_completion` | From the main contract programme / tender enquiry — sectional dates if any |
| `delay_damages_rate` | JCT: LADs in Sub-Contract Particulars; NEC4: Option X7 rate — from template or main contract flow-down. Never guess — `[MC TO CONFIRM]` |
| `retention` | Percentage and release stages from template / main contract (NEC4: Option X16) — never assume a standard % |
| `security` | Performance bond, parent company guarantee, collateral warranties / third-party rights — from template / main contract |
| `insurance` | Employer's liability, public liability, contractors' all risks (who insures the works), professional indemnity where the sub designs — levels from template only |
| `cis_and_vat` | CIS status; whether the VAT domestic reverse charge applies to these services (flag for the firm's finance team to confirm) |
| `governing_law` | England and Wales / Scotland / Northern Ireland — from template; never infer from address alone |

---

## USER CHECKPOINT — Show Data Model, Wait for Confirmation

**This is the most important step in the skill. Do not skip it.**

After Phase 3 validation passes, surface the complete extracted data to the user in readable format before writing any contract prose. The user must explicitly confirm or correct the data.

Format the checkpoint output:

```
I've read all [N] documents. Here's what I extracted — please review before
I generate the subcontract.

━━━ SUBCONTRACTOR ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Company:       [company_name]
  Company no.:   [company_number]   VAT: [vat_number]   CIS: [cis_status]
  Form:          [contract_form]  ([main_option] for NEC4)
  Proposal:      [proposal_number]  (dated [bid_date])
  Estimator:     [estimator_name]  ·  [email]  ·  [phone]

━━━ CONTRACT SUM ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Amount:        [formatted]
  Written:       [written_words]

━━━ PRICING SCHEDULE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [spec]  [description]              [qty] [unit] @ [unit_cost] = [extended]
  [spec]  [description]              [qty] [unit] @ [unit_cost] = [extended]
  ...
  TOTAL:  [formatted]

━━━ INCLUSIONS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • [inclusion 1]
  • [inclusion 2]

━━━ EXCLUSIONS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • [exclusion 1]
  • [exclusion 2]

━━━ VALUE ENGINEERING OPTIONS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [id]  [description]    [amount]

━━━ SPEC REQUIREMENTS (submittals + warranty schedules) ━━━━━
  [spec section]:
    Installer cert required:  [yes/no — source]
    Mockup required:          [yes/no — details]
    Warranty:                 [duration and form]
    Key submittals:           [list]

━━━ GAPS / ITEMS NEEDING YOUR INPUT ━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚠  [any MISSING or derived fields needing confirmation]

Is any of this wrong or missing? Correct me now and I'll update the data
before writing. Once you confirm, I'll generate the subcontract.
```

**Do not proceed until the user responds with explicit confirmation.**

Accepted confirmation signals:
- "Looks good, go ahead"
- "That's correct"
- "Add [X] and proceed"
- Any correction followed by "proceed" or "continue"

If the user makes a correction, update the extracted data, echo the specific change back to confirm it was applied, and ask if they are ready to proceed. Do not re-show the entire data model unless another correction is made.

---

## Phase 4 — Article Generation in Three Groups

Generate the contract in three groups. After each group, show the drafted articles and wait for confirmation before continuing to the next group.

### Generation Rules

**Rule 1: Every number comes from the Data Model — never from training data.** If a number appears in the contract prose, it must be traceable to extracted data. If a field is missing and the number cannot be derived, use `[MC TO CONFIRM]` as the placeholder — not a guessed value.

**Rule 2: No article is left as a generic placeholder.** If an article has placeholder text, it means Phase 2 extraction for the relevant spec section was incomplete. Stop, re-run extraction, and update the data before writing that article.

**Rule 3: The template provides structure, the Data Model provides content.** Do not copy boilerplate from the template that contains the wrong party names, wrong amounts, or wrong scope. Boilerplate means language structure only — specific values always come from the Data Model.

**Rule 4: Scope quantities come from the bid, not the specs.** The specs describe what the product must be. The bid describes how much of it was priced. These are different numbers. Use bid quantities in the contract.

---

### Group 1: Identity and Scope (show → confirm → continue)

**Cover / Order Page** — `info_table` block: subcontract/order number, project name and address, client (Employer), main contractor, contract administrator / Project Manager, main contract reference and form, subcontractor name, registered address, company number, VAT number, tender reference and date, form of subcontract (e.g. "NEC4 ECS, Main Option [x]" or "JCT DBSub/C 2024"), date (blank for execution), sum in BOTH numerals (`£X,XXX,XXX.XX`) AND words, stated as exclusive of VAT.

**Subcontract Documents / Order of Precedence** — list the documents that form the subcontract: the agreement/order, the standard conditions **by reference** with edition, the firm's schedule of amendments (JCT) or Z clauses (NEC4), Sub-Contract Particulars or Subcontract Data, scope/Sub-Contract Documents, specification sections, drawings (container ID + revision + status), tender and post-tender clarifications. State precedence only as the template or main contract sets it. Preliminaries apply to ALL subcontractors — always include them.

**Scope of Works** — five components:
1. Scope description: "The Subcontractor shall design (where stated), supply, install, test and commission…" — use "supply and install" unless the tender is supply-only or labour-only
2. `table` block: pricing lines from the tender — Section, Description, Qty, Unit, Rate, Amount (£)
3. `bullet_list` block: inclusions (tender inclusions + spec requirements)
4. `bullet_list` block: exclusions (tender exclusions — MUST include specific areas/rooms where applicable)
5. `table` block: VE options with ID, description, saving (instructed only by Variation / compensation event)

Name any contractor's design portion explicitly — design responsibility drives professional indemnity insurance and the design submission programme.

After showing Group 1, ask: *"Does the scope and identification look right? Any corrections before I continue to programme and commercial terms?"*

---

### Group 2: Commercial Terms (show → confirm → continue)

**Programme / Time** — start date or access date, completion (and sectional completion) dates, programme submission requirements (NEC4: first programme for acceptance and revisions; JCT: progress and notice of delay). Delay damages flow-down with the specific rate (JCT LADs / NEC4 X7). If the rate is unknown, use `[MC TO CONFIRM]`. Include environmental constraints from the specs (cure times, temperature, humidity).

**Price** — sum in both forms (`£X,XXX,XXX.XX` + words), VAT exclusive. `table` block: pricing schedule grouped by spec section. For NEC4 state the Main Option basis (Activity Schedule, Bill of Quantities, target, cost reimbursable) as the Subcontract Data states it.

**Payment** — assessment / valuation dates, due date, final date for payment, payment notice and pay less notice periods — taken from the template and checked against the Construction Act (HGCRA 1996 Part II as amended). Retention and release (Practical Completion / Completion and end of Rectification Period / defects date). Final account and documents needed. **No pay-when-paid** — flag any such term for legal review. CIS deductions and the VAT reverse charge noted for finance to confirm.

**Changes** — JCT: Variations by written instruction, valuation rules from the template, daywork rates. NEC4: compensation events, notification periods, quotation and assessment, Defined Cost and fee from the Subcontract Data. Notice periods exactly as the template states — never invented.

After showing Group 2, ask: *"Do the commercial terms look right — programme, money, payments?"*

---

### Group 3: Legal and Closeout (show → confirm → write .docx)

**Insurance and Security** — insurance table with every cover and level from the template: employer's liability, public liability, contractors' all risks (state who insures the works), professional indemnity where the subcontractor designs. Security as required: performance bond (amount and form from template), parent company guarantee, collateral warranties or third-party rights schedule.

**Submittals / Technical Submissions** — submission programme deadline. For each spec section in scope, list all required submittals extracted from the spec, plus design submissions for contractor's design portions, RAMS, and certifications (competent person schemes, third-party certification). BIM / information deliverables from the Preliminaries. **Do not leave this as a placeholder under any circumstances.**

**Health, Safety and Site Rules** — CDM 2015: the subcontractor's duties as a contractor (and as a designer where it designs), RAMS before start, induction, site cards (CSCS / ECS for electrical operatives — as the Preliminaries require), permits to work. Reference the construction phase plan; do not restate it.

**Liability and Indemnity** — preserve the template text. Do not add US-style "sole negligence" carve-outs; UK law has no general anti-indemnity statute. Check for a liability cap, net contribution clause and exclusion of consequential loss, and flag anything unusual for legal review rather than redrafting it.

**Warranty and Defects** — defects obligations per the form (Rectification Period / defects date). Manufacturer guarantees and system warranties: one row per spec section with the requirement from the Data Model. **Do not leave this as a placeholder under any circumstances.**

**Remaining clauses** — template boilerplate with project values injected (termination, disputes — adjudication is a statutory right, governing law). Include scope-specific handover deliverables from the specs and Preliminaries: O&M content, as-builts, test certificates (e.g. EIC under BS 7671, cable test results), H&S file information, fire safety information.

**Schedules / Appendices** — minimum:
- Pricing schedule / rates
- Programme
- Scope / specification and drawing list (with revisions and status)
- Schedule of amendments (JCT) or Z clauses (NEC4) — from the firm's template only
- Insurance and security requirements
- Tender and post-tender clarifications (mark "for information — does not govern scope" unless the firm's template incorporates them)

### Preserved Article Legal Review

For each preserved clause, check — and flag, do not redraft — these points:

**Payment (Construction Act):** due dates, final dates, payment notice and pay less notice mechanism present; no pay-when-paid; no term that removes the right to adjudicate.

**Contract form consistency:** NEC4 vocabulary not mixed into a JCT order (or the reverse); the standard form edition stated matches the main contract.

**Insurance and security:** levels and forms match the main contract flow-down; professional indemnity present where the subcontractor designs.

**Delay damages:** flow-down present with a rate (JCT LADs / NEC4 X7) or `[MC TO CONFIRM]`.

**Copyright:** no printed JCT/NEC clauses reproduced unless they came from the firm's own licensed template.

If you find an issue, change `content_type` from `"preserve"` to `"review"` and add a `legal_flags` entry:
```json
{"severity": "critical", "issue": "Template contains a pay-when-paid clause", "recommendation": "Refer to the firm's legal adviser — likely ineffective under HGCRA 1996 s.113", "fixed": false}
```

After showing Group 3, ask: *"Any final changes? Once confirmed I'll write the Word document."*

---

## Phase 4 Output — Write JSON Files

After all three groups are confirmed, write two files to the output directory:

### scope_data.json

Raw structured data for downstream use and eval scoring:
```json
{
  "project_name": "...",
  "project_address": "...",
  "client": "...",
  "contract_form": "nec4_ecs",
  "main_option": "A",
  "contractor_name": "...",
  "subcontractor": {"company_name": "...", "company_number": "...", "vat_number": "...", ...},
  "currency": "GBP",
  "contract_value": 1392618,
  "spec_sections": [{"number": "Ss_75_10_21", "title": "Data distribution and telecommunications systems"}, ...],
  "line_items": [{"spec": "...", "quantity": 850, "unit": "nr", "rate": 0.0, "amount": 0.0}, ...],
  "exclusions": ["..."],
  "value_engineering_alternates": [{"id": "VE-1", "description": "...", "amount": 0.0}, ...],
  "submittal_requirements": ["..."],
  "warranty": "...",
  "special_conditions": ["..."]
}
```

Keep numeric values as raw numbers in scope_data.json (eval scorer uses these).

### template_data.json

Fully-populated document structure:
```json
{
  "cover_page": {
    "text": "SUBCONTRACT AGREEMENT\n\nThis Agreement is entered into...",
    "blocks": [
      {"type": "info_table", "rows": [
        {"label": "Project", "value": "..."},
        {"label": "Subcontract Sum (exclusive of VAT)", "value": "£X,XXX,XXX.XX (Written Words...)"}
      ]}
    ]
  },
  "articles": [
    {
      "number": 2,
      "title": "Scope of Work",
      "content_type": "generate",
      "text": "2.1 The Subcontractor shall supply, install, test and commission...",
      "blocks": [
        {"type": "table", "label": "Scope Description Table",
         "headers": ["Section", "Description", "Qty", "Unit", "Rate (£)", "Amount (£)"],
         "rows": [["Ss_75_10_21", "...", "850", "nr", "£0.00", "£0.00"]]},
        {"type": "bullet_list", "label": "The Work includes:", "items": ["..."]},
        {"type": "bullet_list", "label": "Exclusions:", "items": ["..."]},
        {"type": "table", "label": "VE Alternates",
         "headers": ["VE #", "Description", "Saving (£)"], "rows": [["VE-1", "...", "£0.00"]]}
      ],
      "legal_flags": []
    }
  ],
  "exhibits": [
    {"letter": "A", "title": "Pricing Schedule and Rates"},
    {"letter": "B", "title": "Programme"},
    {"letter": "C", "title": "Schedule of Amendments / Z Clauses"},
    {"letter": "D", "title": "Tender Clarifications (for information; does not govern scope)"}
  ]
}
```

Block types: `table` (headers + rows), `bullet_list` (label + items), `numbered_list` (label + items), `info_table` (rows with label + value).

All display values in blocks must be pre-formatted strings (e.g., `"£1,392,618.00"` not `1392618`). Use `format_currency()` / `amount_to_words()` in `subcontract_formatters.py` (GBP default, pence carried) to check figures and words.

### Produce Word Document

Call the thin formatter:
```bash
${CLAUDE_SKILL_DIR}/../../bin/construction-python ${CLAUDE_SKILL_DIR}/scripts/generate_subcontract_docx.py \
  --template template_data.json \
  --scope scope_data.json \
  --output Subcontract_[SubName]_[SCNumber].docx
```

The formatter renders your pre-populated content into .docx format. It makes no content decisions.

---

## Phase 5 — Post-Generation Verification

After writing the `.docx`, run the following checks against the generated file. If any check fails, fix the specific issue in the JSON, regenerate the .docx, and re-verify. Do not present a document with known failures.

### Verification Checks

**Identity:**
- Sum line contains `£` and `,` formatting and says exclusive of VAT
- Written words for the sum present and match the numeral (pounds AND pence)
- Subcontract/order number present in document
- Subcontractor company number present
- Contract form and edition stated; vocabulary consistent with that form

**No placeholders:**
- No `[Generated content` strings
- No `review and customize` strings
- No `[placeholder]` or `[INSERT]` strings
- Any `[MC TO CONFIRM]` fields have been approved by user

**Scope completeness:**
- All tender quantities appear in the scope
- Exclusions list present with specific references
- All spec sections from bid are referenced in scope

**Legal elements:**
- Payment notice / pay less notice mechanism present; no pay-when-paid
- Delay damages flow-down present (JCT LADs / NEC4 X7) with rate or `[MC TO CONFIRM]`
- No reproduced JCT/NEC printed text unless from the firm's licensed template

**Completeness:**
- Submittals schedule contains spec-specific requirements (not placeholder)
- Warranty schedule contains spec-specific provisions (not placeholder)
- Test certificates and handover deliverables listed

If all checks pass, present the file and state which checks passed. If any check fails, fix the specific issue, regenerate, and note the fix.

### Present for Review

Present a summary:
- Articles generated vs. preserved vs. reviewed
- Any legal flags raised (with severity and what was fixed)
- Verification check results
- Scope highlights: spec section count, line item count, total contract sum
- **Remind the user:** "Contract documents require professional review before execution."

Write graph entry:
```bash
${CLAUDE_SKILL_DIR}/../../bin/construction-python ${CLAUDE_SKILL_DIR}/../../scripts/graph/write_finding.py \
  --type "subcontract_generated" \
  --title "Subcontract: {scope} — {subcontractor}" \
  --output-file "{output_path}" \
  --data '{"scope": "...", "subcontractor": "...", "contract_sum": ..., "spec_sections": ..., "line_items": ..., "legal_flags": ...}'
```

---

## Targeted Correction Workflow

When the user requests a change to the generated document after Phase 5:

1. **Identify the affected Data Model field(s)** — every contract element traces back to extracted data
2. **Update the JSON files** — make the change at the data layer
3. **Identify the affected article(s)** — typically one or two articles maximum
4. **Regenerate only those articles** — do not rewrite the entire document
5. **Show the changed paragraphs specifically** — not the full article
6. **Confirm the change** before writing the updated `.docx`

**Do not regenerate the full document for single-article changes.**

---

## Common Failure Modes

| Failure | Cause | Prevention |
|---------|-------|------------|
| Wrong sum | Reading specs instead of tender | Slot B extraction runs first; validate numeral against bid PDF directly |
| Placeholder articles | Skipping spec extraction | Phase 3 validation blocks generation if spec fields are MISSING |
| Missing quantities | Using master scope estimates | Quantities come from bid SOV, not spec sections |
| Wrong subcontractor info | Using template example info | Always extract company name, address, company number from Slot B, not Slot A |
| Inconsistent amounts | Generating prose without Data Model | All numbers inject from extracted data — never hardcoded |
| Missing exclusions | Only reading inclusions | Explicitly extract exclusions section from bid; cross-check against drawings |
| VE options missing | Tender spans multiple pages | Read all pages; options typically on page 2+ |
| Mixed JCT/NEC vocabulary | Generic drafting | Detect the form first; use the vocabulary table |
| Pay-when-paid in template | Old template | Flag for legal review — Construction Act |

---

## File Safety

Never overwrite an existing subcontract. The formatter uses `safe_output_path()` which appends `_v2`, `_v3`, etc. automatically.

---

## Allowed Scripts

- `${CLAUDE_SKILL_DIR}/../../bin/construction-python`
- `${CLAUDE_SKILL_DIR}/../../scripts/pdf/rasterize_page.py`
- `${CLAUDE_SKILL_DIR}/scripts/generate_subcontract_docx.py`
- `${CLAUDE_SKILL_DIR}/../../scripts/graph/write_finding.py`

## Tips

- "Supply and install" is the standard scope phrase unless the sub is supply-only or labour-only
- Preliminaries apply to ALL subcontractors — always include in the subcontract documents list
- Watch for scope gaps between trades (e.g. pattressing, fire-stopping, BWIC, containment for comms, temporary protection) — flag for user
- Detect template placeholder patterns (`<<SCOPE>>`, `[INSERT]`, `{FIELD}`) and replace them
- Firms use JCT 2024 sub-contracts, NEC4 ECS/ECSS, or their own order forms with standard conditions incorporated by reference — adapt to whatever is provided
- Never state a JCT or NEC clause number unless it appears in the user's documents
- For large contracts (many spec sections), generate JSON incrementally — don't try to hold all article text in a single response
