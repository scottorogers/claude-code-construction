# Scope File: Ss_30_40 / Ss_32 — Roofing, Waterproofing, Insulation and Fire-Stopping

**Load when:** Query references roofs, membranes, warm/cold roof, falls, rainwater outlets, tanking, basement waterproofing, DPCs, insulation, vapour control, breather membranes, airtightness, cavity barriers, fire-stopping, or Uniclass `Ss_30_10` / `Ss_30_40` / `Ss_30_75` / `Ss_32_10` / `Ss_32_20` / `Ss_32_30` / `Ss_32_80` (CAWS `J`, `K`, `P` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Cross-Reference Triggers

- Roof plan — falls, outlets, overflows, plant upstands, walkways, edge protection.
- Roof build-up — deck, VCL, insulation (thickness for AD L U-value), membrane.
- Condensation risk analysis for each build-up.
- Basement waterproofing design — BS 8102 grade, protection types.
- Airtightness strategy and test target (AD L).
- Fire strategy — reaction-to-fire class of external wall and roof materials, cavity barrier locations.
- Fire-stopping specification — tested systems, installer certification, inspection regime.

---

## Absence Detection Checklist

- [ ] Roof falls and outlet locations designed; overflows provided. (Red Flag §4.2)
- [ ] Every roof penetration and plant upstand detailed. (Matrix #19)
- [ ] VCL on the warm side; condensation risk analysis provided. (Red Flag §4.2)
- [ ] Basement waterproofing grade and continuity at joints. (Matrix #4)
- [ ] Airtightness line drawn on sections and continuous at transitions. (Matrix #8)
- [ ] Cavity barriers shown at compartment lines, floors and openings.
- [ ] Fire-stopping: tested system for each penetration type, third-party certified installer where specified, photographic record. (Matrix #10)
- [ ] Combustibility restrictions on external walls checked against building height/use (AD B / Building Regulations reg. 7(2) — confirm which applies).

---

## Sequencing Context

```
Deck → VCL → insulation → membrane → upstands and penetrations → protection
  → POINT OF NO RETURN: Plant installed on finished roof without protection
Fire-stopping after all services through each wall/floor are installed — and before the wall is boxed in
```

**Critical rule:** fire-stopping is installed last and checked least. Every penetration needs a named, tested system and a record. Missing records block handover on many jobs.

---

## Coordination Overlaps

- **With M&E:** roof penetrations, plant upstands, service penetrations needing fire-stopping. (Matrix #10, #19)
- **With Windows / Cladding:** membranes and cavity barriers. (Matrix #8, #9)
- **With Concrete:** basement waterproofing. (Matrix #4)
