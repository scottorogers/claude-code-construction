# Scope File: Ss_40 — Catering, Laboratory and Process Equipment

**Load when:** Query references catering equipment, kitchen canopies, lab fume cupboards, process or specialist equipment, client-supplied equipment, or the relevant Uniclass `Ss_40_` FF&E groups (`Ss_40_20`, `Ss_40_25`, `Ss_40_30`, `Ss_40_50`).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Cross-Reference Triggers

- Equipment schedule — supplier, who installs, services required (power rating, water, drainage, gas, extract, data).
- Equipment layout vs M&E services layout.
- Catering canopy and suppression specification. (Matrix #22)
- Gas safety interlock requirements for commercial catering (take from the spec).

---

## Absence Detection Checklist

- [ ] Every item has a services data sheet and the M&E design used the same revision. (Matrix #17)
- [ ] Final connections assigned (supplier or M&E).
- [ ] Canopy extract, make-up air and fire suppression scoped. (Matrix #22)
- [ ] Gas interlock with ventilation where gas catering equipment is fitted.
- [ ] Floor gullies and plinths where equipment needs them.

---

## Sequencing Context

```
Equipment selection frozen → services designed → first fix to fixed locations
  → POINT OF NO RETURN: Equipment change after first fix = rework
```

---

## Coordination Overlaps

- **With All M&E:** services to exact positions. (Matrix #17)
- **With Fire suppression:** wet chemical system. (Matrix #22)
