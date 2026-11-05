# Scope File: Ss_25_13 — Brick and Blockwork

**Load when:** Query references brickwork, blockwork, cavity walls, wall ties, brick support angles, lintels, DPCs, cavity trays, movement joints, or Uniclass `Ss_25_13` Unit wall structure systems (CAWS `F` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Cross-Reference Triggers

- Elevations and wall sections — brick type, bond, coursing, movement joint layout.
- Brick support system design (often contractor's design) and support angle setting-out.
- Lintel schedule and DPC / cavity tray details at openings.
- Cavity barrier and fire-stopping requirements (AD B / fire strategy).
- Blockwork partitions — fire rating, acoustic rating, fixings for services.

---

## Absence Detection Checklist

- [ ] Brick support design responsibility and deflection tolerances. (Matrix #5)
- [ ] Cavity trays and stop ends over every opening and support angle. (Matrix #6)
- [ ] Movement joints shown on elevations.
- [ ] Cavity barriers at compartment lines and openings where required.
- [ ] Wall ties type and spacing from the spec.
- [ ] Chases in blockwork for M&E — depth limits and who forms them (BWIC).

---

## Sequencing Context

```
Frame and support angles → DPC / trays → brickwork lifts → cavity barriers and insulation as you go
  → POINT OF NO RETURN: Cavity closed
```

---

## Coordination Overlaps

- **With Steel frame:** support angles. (Matrix #5)
- **With Windows:** DPCs and trays at openings. (Matrix #8)
- **With Electrical:** chasing for first fix in blockwork walls.
