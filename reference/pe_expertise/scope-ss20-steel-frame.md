# Scope File: Ss_20 / Ss_35 — Steel Frame, Metalwork and Stairs

**Load when:** Query references structural steel, connections, metal decking, fire protection to steel, secondary steel, plant supports, balustrades, stairs, ladders, or Uniclass `Ss_20_10` / `Ss_20_20` / `Ss_20_30` / `Ss_20_70` / `Ss_35` / `Ss_25_15` (CAWS `G`, `L` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Cross-Reference Triggers

- Structural GA, connection design responsibility note, member schedules (UK section designations, e.g. `533x210x82 UB`).
- Steel fire protection specification — intumescent / board, required period, DFT schedule.
- Metal deck layout and shear stud details.
- Secondary steel for plant, containment, façade support — who designs it.
- Balustrade and handrail loads, heights (AD K).
- Execution class and fabrication standard named in the spec (take from spec).

---

## Absence Detection Checklist

- [ ] Connection design responsibility assigned (structural engineer or steelwork contractor). (Red Flag §4.1)
- [ ] Fire protection product, period and DFT/thickness for every member that needs it.
- [ ] M&E fixings to steel coordinated before fire protection. (Matrix #7)
- [ ] Holes in beams for services — designed and shown (cellular beams or reinforced openings).
- [ ] Secondary steel for plant, containment and façade designed and scoped to a package.
- [ ] Bonding of the steel frame (main protective bonding / lightning protection down conductors) agreed with electrical.
- [ ] Balustrade loading and guarding heights to AD K.

---

## Sequencing Context

```
Holding-down bolts cast in → erection → decking and studs → slab pour
  → POINT OF NO RETURN: Fire protection to steel (M&E fixings first)
```

---

## Coordination Overlaps

- **With Concrete:** holding-down bolts and embeds. (Matrix #3)
- **With M&E:** fixings, beam penetrations, plant supports. (Matrix #7)
- **With Electrical:** bonding and lightning protection.
