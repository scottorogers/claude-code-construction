# Scope File: PM_ — Preliminaries, CDM, Programme and Handover

**Load when:** Query references preliminaries, general requirements, site set-up, welfare, CDM 2015, construction phase plan, programme, submittals procedure, quality, testing and commissioning, handover, O&M manuals, health and safety file, soft landings, or Uniclass `PM_` sections (NBS Preliminaries; CAWS `A` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Uniclass Groups (NBS v1.30, July 2026)

`PM_10` Project information · `PM_30` Site, ground and environmental information · `PM_35` Project performance requirements · `PM_40` Design and approvals information · `PM_50` Financial and commercial information · `PM_55` Contract information · `PM_60` Construction management information · `PM_70` Testing, commissioning and completion information · `PM_80` Asset management information.

---

## Cross-Reference Triggers

- Contract and subcontract — JCT or NEC4 form, amendments, Contract/Subcontract Data. (`reference/uk_regulations.yaml`)
- Employer's Requirements / Scope — what the client actually requires, including information requirements (EIR / BEP).
- Pre-construction information (CDM reg. 4 client duty; principal designer under reg. 11).
- Construction phase plan (CDM reg. 12) — site rules, permits, hot works, working at height.
- F10 notification (CDM reg. 6 and Schedule 1) for notifiable projects.
- Programme — the contract programme (JCT) or Accepted Programme (NEC4), lookaheads, key dates.
- Submittals / technical submissions procedure — review periods, status codes.
- Testing and commissioning plan, witness requirements, soft landings.
- Handover requirements — O&M manuals, as-builts, health and safety file (CDM reg. 12), Building Regulations completion, fire safety information (Building Regulations reg. 38).

---

## Absence Detection Checklist

- [ ] Contract form and amendments identified (JCT 2024 / NEC4 — which one, which options).
- [ ] CDM duty holders named: client, principal designer, principal contractor.
- [ ] Pre-construction information issued; construction phase plan in place before work starts.
- [ ] Notification made where the project is notifiable (check the F10 is displayed).
- [ ] Higher-risk building check (Building Safety Act 2022) — if HRB, gateway approvals govern change control.
- [ ] Submittal review period and status codes stated (and who reviews).
- [ ] Programme with key dates, sectional completion, and access dates for each trade.
- [ ] Testing and commissioning responsibilities and witness requirements.
- [ ] O&M manual and as-built deliverables, format (e.g. COBie / BEP), and the deadline relative to completion.
- [ ] Health and safety file content and who compiles it.
- [ ] Fire safety information for handover (reg. 38) — who compiles.
- [ ] Defects / rectification period and retention release terms.

---

## Sequencing Context

```
Pre-construction
  → Contract and subcontracts signed (do not start on a letter of intent without scope, value cap and end date)
  → CDM: pre-construction information → construction phase plan → F10
  → Programme accepted
Construction
  → Submittals approved before procurement / install (Matrix: RFI & submittal red flags)
  → POINT OF NO RETURN: Inspection before cover-up — every trade
Completion
  → Testing and commissioning complete, certificates issued
  → O&M, as-builts, H&S file, fire safety information
  → Practical Completion (JCT) / Completion (NEC4) — check what the contract makes a precondition
```

**Critical rule:** handover paperwork is a completion requirement on most contracts. If it is not current through the job, completion slips.

---

## Coordination Overlaps

- **With every package:** submittals, RAMS, permits, testing, O&M.
- **Scope boundary (pe_behavior.md §7.1):** BWIC, access equipment, protection, cleaning, waste.
