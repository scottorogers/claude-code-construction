# Scope File: Ss_25_30 / Ss_25_38 — Doors, Windows, Ironmongery and Curtain Walling

**Load when:** Query references doors, doorsets, fire doors, ironmongery, door schedules, windows, curtain walling, glazing, rooflights, automatic doors, or Uniclass `Ss_25_30` Door and window systems / `Ss_25_38` Wall and barrier opening hardware systems / `Ss_25_20` Wall cladding systems (CAWS `H`, `L` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Cross-Reference Triggers

- Door schedule — fire rating (FD30, FD30S, FD60, FD60S…), acoustic rating, ironmongery set, access control, vision panels, leaf sizes.
- Ironmongery schedule — sets, closers, escape hardware, electric locks.
- AD M Vol 2 Table 2 — door effective clear widths (`reference/ad_m_vol2_access.yaml`).
- AD M Vol 2 para 2.13(a) — opening force.
- Fire strategy — which doors are fire doors, which need hold-open devices, escape hardware type.
- Access control layouts — controlled doors, lock type. (Matrix #14)
- Curtain wall / window contractor's design — interfaces, fixings, cavity barriers, slab-edge fire-stopping. (Matrix #9)

---

## Absence Detection Checklist

- [ ] Every fire door: rating, certification (third-party certified doorset), self-closer, intumescent and smoke seals where S-rated. (Matrix #24)
- [ ] Effective clear widths checked against AD M Vol 2 Table 2.
- [ ] Opening force within AD M para 2.13(a), or powered operation provided.
- [ ] Escape hardware type stated for every escape door (fire strategy).
- [ ] Electric locks: fail-safe / fail-secure and fire alarm release agreed; cabling to frame before closure. (Matrix #14)
- [ ] Door hold-open devices linked to the fire alarm.
- [ ] Window / curtain wall: airtightness, membranes and sill details. (Matrix #8)
- [ ] Guarding to low-level glazing and opening lights (AD K).
- [ ] Long-lead check: curtain wall, specialist glazing, certified fire doorsets.

---

## Sequencing Context

```
Frames set → first-fix cabling to frames (access control, auto operators)
  → POINT OF NO RETURN: Board closure around frames
Doors hung after wet trades → ironmongery → access control commissioning with fire alarm
```

---

## Coordination Overlaps

- **With Security / Fire alarm:** access control and door release. (Matrix #14, #15)
- **With Electrical:** auto operators, electric locks.
- **With Fire strategy:** fire doors in fire-rated walls. (Matrix #24)
- **With Envelope:** membranes and cavity barriers at frames. (Matrix #8, #9)
