# Scope File: Ss_60 / Ss_65 — Mechanical (Heating, Cooling, Ventilation, BMS)

**Load when:** Query references heating, cooling, chillers, heat pumps, VRF, FCUs, AHUs, ductwork, fire and smoke dampers, smoke extract, BMS / controls, commissioning, or Uniclass `Ss_60_40` / `Ss_60_60` / `Ss_65_40` / `Ss_65_60` / `Ss_65_80` / `Ss_75_70` Control and management systems (CAWS `T`, `U` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Cross-Reference Triggers

- Mechanical layouts and schematics; plant schedules (duty, electrical rating).
- Fire and smoke damper schedule — locations at every fire-rated penetration, access, release type.
- Smoke control / AOV strategy from the fire strategy.
- Controls philosophy and BMS points list.
- AD F (ventilation), AD L (energy), AD O (overheating, dwellings).
- Commissioning specification — CIBSE / BSRIA guides as named in the spec.
- Refrigerant systems — F-gas certified installer, leak detection where required.

---

## Absence Detection Checklist

- [ ] Every plant item on the electrical design with matching rating and an isolator. (Matrix #13)
- [ ] Fire/smoke dampers at every duct penetration of a fire-rated element, with access panels. (Red Flag §4.4)
- [ ] Damper and AHU actions in the fire alarm cause-and-effect. (Matrix #15)
- [ ] Comms room / data hall cooling and redundancy. (Matrix #26)
- [ ] Condensate drainage from FCUs, VRF and AHUs. (Red Flag §4.4)
- [ ] BMS points list and integration (who wires what — Matrix scope gap).
- [ ] Commissioning and witnessing plan; seasonal commissioning if specified.

---

## Sequencing Context

```
Ductwork and pipework first fix → pressure/leakage tests
  → POINT OF NO RETURN: Ceilings closed over untested services or missing dampers
Plant set → electrical connections → controls → commissioning → witnessed tests
```

---

## Coordination Overlaps

- **With Electrical:** supplies and isolators. (Matrix #13)
- **With Fire alarm:** dampers, AHU shutdown, smoke control. (Matrix #15)
- **With Comms:** cooling to comms rooms. (Matrix #26)
- **With Ceilings / Partitions:** dampers, access panels, grilles. (Matrix #10, #12)
- **With Roofing:** plant upstands and penetrations. (Matrix #19)
