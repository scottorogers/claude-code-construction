# Scope File: Ss_20 — Concrete Frame, Substructure and Piling

**Load when:** Query references reinforced concrete, piling, pile caps, ground beams, slabs, post-tensioning, precast, screeds, cast-in items, basements, or Uniclass `Ss_20_05` Substructure / `Ss_20_10` Structural frame / `Ss_20_60` Retaining wall systems (CAWS `D`, `E` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Cross-Reference Triggers

- Structural GA and reinforcement drawings / bar bending schedules.
- Piling layout, pile schedule, integrity testing requirements.
- Cast-in items schedule — holding-down bolts, cast-in channels, sleeves, ducts, earthing.
- Basement waterproofing design — BS 8102 grade and protection type.
- M&E builder's work drawings — holes, sleeves, plinths.
- Floor flatness requirement for finishes (raised access floor, LVT, warehousing).
- Concrete specification — strength class, exposure class, cover (take from spec).

---

## Absence Detection Checklist

- [ ] Cast-in items checked against ALL disciplines before every pour. (Matrix #3)
- [ ] Sleeves and holes for M&E shown on structural drawings (not only on M&E drawings).
- [ ] Post-tensioned slab tendon zones shown — no post-drilling without scanning.
- [ ] Slab rebates for screeds and thick finishes. (Matrix #1)
- [ ] Plinths for plant shown with sizes from M&E.
- [ ] Floor flatness tolerance stated for the specified finish. (Matrix #20)
- [ ] Basement waterproofing grade and continuity at joints. (Matrix #4)
- [ ] Foundation earth / earth electrode requirement from electrical / lightning protection.
- [ ] Cube testing and pile testing regimes.

---

## Sequencing Context

```
Piling → pile caps / ground beams → below-slab drainage and ducts → slab
Frame floor by floor
  → POINT OF NO RETURN: Cast-in items, sleeves, holes before each pour
  → Back-propping and striking times
```

**Critical rule:** on post-tensioned slabs, any later fixing or core for containment and services needs tendon scanning. Get the M&E holes cast in.

---

## Coordination Overlaps

- **With Steel frame:** holding-down bolts and embeds. (Matrix #3)
- **With M&E:** sleeves, cast-in channels for containment, plinths. (Matrix #2)
- **With Flooring:** rebates and flatness. (Matrix #1, #20)
