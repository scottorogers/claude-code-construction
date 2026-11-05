# Scope File: Ss_55_30 — Fire-Extinguishing Systems (Sprinklers, Risers, Gas Suppression)

**Load when:** Query references sprinklers, sprinkler tanks and pumps, wet or dry risers, hose reels, gaseous suppression (data halls, comms rooms), water mist, kitchen wet chemical, or Uniclass `Ss_55_30` Fire-extinguishing systems (CAWS `S` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

**Standards (cite number; take edition from spec):** BS EN 12845 (sprinklers), BS 9251 (residential sprinklers), the fire strategy, and insurer requirements (e.g. LPC rules) where the spec names them.

---

## Cross-Reference Triggers

- Fire strategy — where sprinklers are required, which design standard, hazard class.
- Sprinkler layouts and hydraulic calculations (often contractor's design).
- Tank and pump room layouts; water supply test / water undertaker information.
- Dry/wet riser locations and fire service access.
- Data hall / comms room suppression — agent type, room integrity test, hold-off/abort.
- Fire alarm interface — flow switches, valve monitoring, gas release. (Matrix #15)

---

## Absence Detection Checklist

- [ ] Design standard and hazard class stated and matching the fire strategy.
- [ ] Hydraulic calculations and water supply evidence.
- [ ] Sprinkler head layout coordinated with ceiling grid and obstructions. (Matrix #12)
- [ ] Flow switches and valve monitoring wired to fire alarm. (Matrix #15)
- [ ] Gas suppression: room integrity test, pressure relief venting, warning signs, interface with HVAC shutdown.
- [ ] Pump supply fire-protected where required.
- [ ] Commissioning certificates and third-party certification.

---

## Sequencing Context

```
Mains and range pipes before ceilings
  → Pressure test
  → POINT OF NO RETURN: Ceiling closed over untested pipework
Gas suppression: room sealed and integrity tested before commissioning
```

---

## Coordination Overlaps

- **With Ceilings:** head positions. (Matrix #12)
- **With Fire alarm:** monitoring and release. (Matrix #15)
- **With Catering:** wet chemical. (Matrix #22)
- **With Comms / Data centres:** gaseous suppression in data halls.
