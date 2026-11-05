# Scope File: Ss_15_30 — Demolition, Strip-Out, Asbestos and Enabling Works

**Load when:** Query references demolition, soft strip, strip-out, existing services isolation, asbestos, refurbishment surveys, temporary works for demolition, existing structure, or Uniclass `Ss_15_30` Remediation, repair and renovation systems (CAWS `C` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Cross-Reference Triggers

- Asbestos refurbishment and demolition survey — required before intrusive work on pre-2000 buildings; check it covers the actual work areas.
- Pre-construction information (CDM) — existing services, structural surveys, hazardous materials.
- Strip-out / demolition drawings — what is removed, what is retained, what is protected.
- Existing services drawings — live services to isolate, divert or keep live (comms and power often stay live for occupants).
- Temporary works design — propping, façade retention.
- Structural engineer's sequence for removal of structural elements.

---

## Absence Detection Checklist

- [ ] Refurbishment and demolition asbestos survey covers every area of intrusive work.
- [ ] Licensed asbestos removal scope and clearance certificates before follow-on trades enter.
- [ ] Live services identified and labelled; isolation and permit-to-work procedure stated.
- [ ] Retained services (e.g. live comms to an occupied floor) protected and shown.
- [ ] Temporary works designed and checked (temporary works coordinator named).
- [ ] Waste management / segregation and site waste responsibilities stated.
- [ ] Party wall / neighbour and noise/vibration limits where relevant.
- [ ] Existing fire compartmentation and alarm coverage maintained in occupied areas during works.

---

## Sequencing Context

```
Surveys (asbestos R&D, structural, services)
  → Isolations and diversions (permit to work)
  → Asbestos removal → clearance → handover to follow-on trades
  → Soft strip → structural removals (temporary works in place)
  → POINT OF NO RETURN: Removal of structure or retained services cut
```

**Critical rule:** in refurbishment, the existing building is the biggest unknown. Anything not surveyed is a risk — flag it as an early warning (NEC4) or a potential Relevant Event (JCT) the moment it is found.

---

## Coordination Overlaps

- **With Electrical / Comms:** live services, temporary supplies, retained circuits.
- **With Fire detection:** maintaining cover in occupied areas.
- **With Structure:** temporary works and propping.
