# Scope File: Finishes — Drylining, Ceilings, Flooring, Raised Floors, Decoration

**Load when:** Query references drylining, partitions, plasterboard, shaftwall, plastering, suspended ceilings, raised access floors, screeds, flooring (carpet, LVT, vinyl, resin, tiles), decoration, wall finishes, or Uniclass `Ss_25_10` Framed wall / `Ss_25_25` Wall lining / `Ss_25_45` Wall covering / `Ss_30_20` Flooring / `Ss_30_25` Ceiling / `Ss_30_42` Floor covering / `Ss_30_47` Ceiling covering / `Ss_32_46` Lath and plaster / `Ss_40_90` General finishing (CAWS `K`, `M` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Cross-Reference Triggers

- Partition types schedule — fire rating (minutes), acoustic rating (dB), board type, stud size and centres, head detail.
- Manufacturer's tested system data — the partition type must match a tested configuration.
- Reflected ceiling plans — grid, tile, access, integration of M&E. (Matrix #12)
- Finishes schedule / room data sheets.
- Raised access floor — grade, finished floor height, void for services, pedestal fixing.
- Screed and flooring — moisture testing method, flatness tolerance. (Matrix #20)
- AD M — visual contrast; AD E — sound insulation; AD B — reaction to fire of linings.

---

## Absence Detection Checklist

- [ ] Fire-rated partitions go full height to soffit. (Red Flag §4.3)
- [ ] Partition type matches a tested system; head detail suits deflection.
- [ ] Every service penetration through a fire-rated partition has a fire-stopping detail. (Matrix #10)
- [ ] Pattressing shown before closure. (Matrix #11)
- [ ] Access panels at dampers, valves, FCUs, junction boxes — fire-rated in fire-rated ceilings/walls.
- [ ] Ceiling void depth suits containment, ductwork, sprinklers; ceiling grid coordinated with all M&E. (Matrix #12)
- [ ] Raised floor void height suits floor boxes and under-floor containment.
- [ ] Moisture testing and flatness before flooring. (Matrix #20)
- [ ] Moisture-resistant / impact-resistant board where expected.

---

## Sequencing Context

```
Studs → first-side boarding → M&E first fix → insulation → pattressing
  → POINT OF NO RETURN: Second-side boarding (fire-stopping and inspection first)
Ceiling grid
  → POINT OF NO RETURN: Above-ceiling services installed, tested and inspected before tiles
Screed cures → moisture test → flooring
```

---

## Coordination Overlaps

- **With All M&E:** penetrations, access panels, ceiling coordination. (Matrix #10, #12)
- **With Comms / Electrical:** raised floor and ceiling void for containment.
- **With Concrete:** rebates and flatness. (Matrix #1, #20)
