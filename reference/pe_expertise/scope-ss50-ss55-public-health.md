# Scope File: Ss_50 / Ss_55_70 — Public Health (Above-Ground Drainage and Water Services)

**Load when:** Query references above-ground drainage, soil and waste, rainwater pipes, sanitaryware, cold and hot water services, boosters, water heaters, Legionella control, or Uniclass `Ss_50_30` Above-ground drainage collection / `Ss_55_70` Water distribution and supply / `Ss_55_15` Water storage (CAWS `R`, `S` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Cross-Reference Triggers

- Public health layouts and schematics — stacks, branches, AAVs, water distribution.
- Sanitaryware schedule vs architectural layouts. (Matrix #21)
- AD G (sanitation, hot water safety), AD H (drainage).
- Water Supply (Water Fittings) Regulations notification where required (check the spec).
- Legionella risk assessment / water hygiene commissioning (chlorination, sampling).
- Electrical — water heaters, boosters, pumps. (Matrix #13)

---

## Absence Detection Checklist

- [ ] Sanitaryware counts match architectural plans. (Red Flag §4.4)
- [ ] Stack venting / AAV provision.
- [ ] Gullies in plant rooms, lift pits, tank rooms. (Red Flag §4.4)
- [ ] Hot water temperature control and TMVs where required.
- [ ] Water hygiene: flushing, chlorination, sampling before occupation.
- [ ] Condensate routes from mechanical plant to drainage — who provides the connection.
- [ ] No water pipework routed over comms rooms, switchrooms or data halls.

---

## Sequencing Context

```
Below-slab drainage → stacks → branches → testing (air/water)
  → POINT OF NO RETURN: Boxing-in and ceilings over untested pipework
Water services → pressure test → flush → chlorinate → sample → handover
```

---

## Coordination Overlaps

- **With Architecture:** fixture locations. (Matrix #21)
- **With Electrical:** water heaters, pumps. (Matrix #13)
- **With Comms / Electrical rooms:** no water over critical rooms.
