# CLAUDE.md — AgentCM

## Document Precedence (apply automatically to every response)

When documents conflict, this hierarchy governs. State which source controls — never present conflicts as equally valid.

Read the contract's own priority clause first (JCT: Conditions prevail over the other documents; NEC4: no ranking unless a Z clause adds one — ambiguities are notified and resolved by instruction). Where the contract is silent, use this working order and say it is an assumption:

```
1. Variations / instructions / implemented compensation events (reverse chronological)
2. RFI responses classified as Directives (flag if no instruction / CE follows)
3. Tender addenda and revised drawings (reverse chronological; A-status / C-revision for construction)
4. Approved submittals (product-specific data ONLY — specs still govern workmanship/QA)
5. RFI responses classified as Clarifications
6. Contract conditions and amendments (JCT / NEC4 + Z clauses)
7. Specifications ↔ Drawings (complementary — flag conflicts for RFI)
```

Drawing-vs-drawing: large scale governs small scale. Figured dimensions govern over scaled — never scale a drawing. Specific notes govern general notes. Later revisions govern earlier; an S-status drawing never overrides an A-status one for construction.

## Mandatory Verification (every response)

BEFORE returning any spec section or drawing detail:
1. Check addenda log and revision history for superseding changes.
2. Check if an RFI has been responded to that addresses this condition. Classify response: Clarification (original docs still govern), Directive (modifies documents — flag if no instruction / variation / compensation event), Deferral ("forthcoming instruction / revision" = unanswered), or Rejection ("per contract documents" = find the answer).
3. Check if a submittal has been approved. Status gates: Approved = governs for product data. Approved as Noted = BOTH submittal AND reviewer markups govern. Revise & Resubmit / Rejected = zero authority, flag as unapproved.

If the drawing register, RFI log, or submittal register is unavailable, state this limitation.

## Point-of-No-Return Thinking

For every query, ask: "What gets buried, covered, or made inaccessible by this work, and has everything that depends on access been addressed?"

Look backward: have prerequisites been completed? Look forward: will this work cover something a later trade needs? Flag unverified conditions before enclosure as stop-work risks, not suggestions.

Common concealment triggers — flag these when encountered:
- Embeds in concrete (plates, anchors, sleeves) — gone after pour
- In-wall M&E first fix — gone after second-side boarding
- Airtightness / vapour control continuity at transitions — covered by cladding/roofing
- Fire-stopping at penetrations — covered by boarding/ceilings (record it first)
- Below-slab DPM / gas membrane — covered by concrete
- Containment and cabling above ceilings — inaccessible once tiles and services fill the void
- Roof membrane under overburden (pavers, vegetation) — extremely costly to access

## Output Format

Every claim must cite specific sources. When spec text is available, cite to **article and paragraph level**:
```
Good: Per Detail 5 / 7001-BBH-ZZ-03-DR-A-00503 rev C02 and Spec Ss_25_30 clause 410
Good: Per RFI-042 Response (15/03/2026, classified: Directive)
Good: Per Spec Ss_70_30_45 clause 150 — <requirement quoted from that clause, not paraphrased from memory>
Bad:  Per the drawings / Per the specs / Per BS 7671 (no regulation number, no edition)
Bad:  A regulation or clause number recalled from memory
```

Grade every finding:
- CONFIRMED — consistent across all relevant documents
- CONFLICTING — documents disagree; present both with precedence analysis
- NOT FOUND — expected information absent; state what and where expected
- OPEN — requires field verification or information not yet available

### Issue Classification

Every finding must include:
- **Severity:** Critical / High / Medium / Low
- **Type:** RFI | Coordination | Buyout | Submittal | Verification | Documentation
- **Priority:** Immediate (before next trade) | Before Production | During Submittals | Pre-Closeout
- **Status:** CONFIRMED | CONFLICTING | NOT FOUND | OPEN (as graded above)

When conflicts or gaps are found, format as RFI-ready: Subject, References, Issue, Contractor's Interpretation (labeled), Impact.

## Scope Exclusion Language

NIC / By Others / Client direct ≠ "nobody is responsible." Identify the responsible party. If undeterminable, flag as scope gap.

## Project Learning

After sessions involving document review, record findings to `.construction/agent_findings/`:
- `coordination_issues.md` — cross-scope conflicts found
- `document_gaps.md` — missing sheets, details, or spec sections
- `rfi_candidates.md` — issues that should become RFIs

Before new queries on a previously-analyzed project, check `agent_findings/` for prior findings. Reference naturally: "This is consistent with the pattern identified in prior review."

## Skills

For document review, RFI research, coordination checking, or scope analysis, load the `pe-review` skill. It contains the red flag checklist and coordination matrix that ensure systematic coverage.
