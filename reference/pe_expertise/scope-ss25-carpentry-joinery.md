# Scope File: Ss_25 / Ss_40 — Carpentry, Joinery and Timber Frame

**Load when:** Query references carpentry, pattressing, grounds, joinery, fitted furniture, timber frame, CLT, skirtings, architraves, or timber sections of Uniclass `Ss_25_10` Framed wall systems / `Ss_40` FF&E (CAWS `G`, `K`, `P`, `Z` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Cross-Reference Triggers

- Partition and pattress details; wall-mounted item schedules (sanitaryware, AV, grab rails, signage).
- Joinery drawings and shop drawings — dimensions, materials, ironmongery, services cut-outs.
- Fire-retardant treatment and reaction-to-fire classification where required by the fire strategy.
- Timber frame / CLT — fire strategy, cavity barriers, moisture protection during construction.

---

## Absence Detection Checklist

- [ ] Pattressing shown for every wall-mounted item before board closure. (Matrix #11)
- [ ] Joinery shop drawings show cut-outs and service routes for power/data.
- [ ] Reaction-to-fire class of timber linings on escape routes (fire strategy).
- [ ] Cavity barriers in timber frame / CLT at compartment lines.
- [ ] Moisture content limits for joinery before installation.

---

## Sequencing Context

```
First-side boarding → services → pattressing
  → POINT OF NO RETURN: Second-side boarding
Joinery after wet trades and when the building is weathertight and heated
```

---

## Coordination Overlaps

- **With FF&E / AV:** pattress locations and loads. (Matrix #11)
- **With Electrical / Comms:** joinery cut-outs and desk/joinery power and data. (Matrix #18)
