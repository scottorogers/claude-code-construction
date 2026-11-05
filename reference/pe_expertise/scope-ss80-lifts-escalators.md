# Scope File: Ss_80_50 / Ss_80_20 — Lifts, Escalators and Hoists

**Load when:** Query references lifts, firefighting lifts, evacuation lifts, platform lifts, escalators, goods hoists, lift pits and shafts, or Uniclass `Ss_80_50` Lift systems / `Ss_80_20` Conveying systems / `Ss_80_30` Crane and hoist systems (CAWS `X` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Cross-Reference Triggers

- Lift contractor's builder's work drawings — shaft size, pit depth, headroom, motor room or MRL.
- Fire strategy — firefighting lift, evacuation lift requirements (AD B 16 Sept 2026 update added evacuation lift guidance for taller residential buildings — read it if relevant).
- Electrical — dedicated supply, secondary supply for firefighting lift, shaft lighting, pit socket.
- Fire alarm cause-and-effect — lift homing / fire control. (Matrix #23)
- Comms — lift emergency telephone / remote monitoring line.
- AD M Vol 2 — lift and lifting platform provisions (VERIFY paragraphs before citing).

---

## Absence Detection Checklist

- [ ] Shaft and pit dimensions match the lift contractor's requirements.
- [ ] Pit drainage / sump where required. (Matrix #23)
- [ ] Dedicated supplies and isolators; secondary supply for firefighting lifts.
- [ ] Fire alarm interface designed and responsibility assigned at both ends.
- [ ] Lift alarm / communication line provided (comms package or lift contractor?).
- [ ] Ventilation of lift motor room or shaft as required.
- [ ] Use of permanent lifts during construction — insurance and handover condition.

---

## Sequencing Context

```
Shaft built and plumbed → brackets → rails and car → electrical supply → commissioning
  → POINT OF NO RETURN: Shaft size and pit depth fixed in the frame
Lift commissioning and LOLER thorough examination before handover
```

---

## Coordination Overlaps

- **With Fire alarm:** lift fire control. (Matrix #23)
- **With Electrical / Comms:** supplies and alarm line.
- **With Structure:** shaft tolerances, lifting beams.
