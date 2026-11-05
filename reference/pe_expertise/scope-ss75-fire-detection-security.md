# Scope File: Ss_75_40 / Ss_75_50 — Fire Detection & Alarm, Security Systems

**Load when:** Query references fire alarm, detection, sounders/beacons, cause and effect, voice alarm, refuge / emergency voice communication, disabled toilet alarm, access control, CCTV, intruder alarm, door entry, gas or leak detection, or any Uniclass `Ss_75_40_` / `Ss_75_50_` section.

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

**Standards (cite number; take edition from the spec):** BS 5839-1 (non-domestic fire detection and alarm), BS 5839-6 (domestic), the project **fire strategy**, AD B. Security standards are usually named in the spec — read them from there.

---

## Uniclass Groups (NBS v1.43, July 2026)

- `Ss_75_50_28` Fire and smoke detection and alarm systems
- `Ss_75_50_11` Emergency call systems
- `Ss_75_50_33` Gas detection and alarm systems
- `Ss_75_50_50` Liquid detection and alarm systems
- `Ss_75_40_02` Access control systems
- `Ss_75_40_53` Monitoring systems (CCTV)
- `Ss_75_40_75` Security detection alarm systems (intruder)
- `Ss_75_40_73` Security screening systems

---

## Cross-Reference Triggers

- Fire strategy report — evacuation strategy (simultaneous / phased / stay put), system category (L1–L5 / M / P under BS 5839-1 — take from the strategy), interfaces required.
- Fire alarm layouts — detectors, call points, sounders/beacons, interface units, panel and repeater locations.
- Cause-and-effect matrix — every input and every output. If none exists, flag it.
- Access control and door schedules — controlled doors, lock type, fail-safe / fail-secure, fire alarm release. (Matrix #14)
- CCTV layouts — camera positions, fields of view, recording and retention.
- Electrical — dedicated supplies to panels, fire-resistant cable for life-safety circuits.
- Mechanical — AHU shutdown, smoke damper control, smoke extract. (Matrix #15)
- Lifts — lift fire control / firefighting lift interface. (Matrix #23)
- Sprinklers — flow switches and valve monitoring. (Matrix #15)
- **Submittal register** — fire panel and devices (with third-party certification), cable type, access control hardware, CCTV.
- **RFI log** — system category, cause and effect, interface responsibilities.

---

## Absence Detection Checklist

- [ ] BS 5839-1 system category stated and matching the fire strategy.
- [ ] Cause-and-effect matrix issued and covering mechanical, lifts, sprinklers, access control, smoke control, gas shut-off, door holders.
- [ ] Fire-resistant cable type stated for fire alarm circuits (standard or enhanced grade per the spec).
- [ ] Fire panel location and fire information / repeater at the fire service access point where required.
- [ ] Voice alarm or sounder/beacon coverage stated; visual alarms where hearing-impaired occupants are expected.
- [ ] Refuge EVC and disabled toilet alarm where the fire strategy / AD M requires them.
- [ ] Access control doors on escape routes: fail-safe release on fire alarm and a break-glass / green emergency door release — agreed with the fire strategy.
- [ ] Interfaces with lift, AHU, smoke dampers and AOVs shown with responsibility for each end.
- [ ] Third-party certification required for designer and installer (e.g. BAFE / LPCB schemes) — read the spec.
- [ ] Commissioning deliverables: BS 5839-1 design, installation and commissioning certificates; cause-and-effect test record; zone plan at the panel.
- [ ] CCTV: data protection signage and retention policy noted as client-side items.

---

## Sequencing Context

```
First fix
  → Fire-resistant cabling and back boxes installed with M&E first fix
  → POINT OF NO RETURN: In-wall cabling and back boxes before board closure
    ├── Access control cabling to every controlled door frame
    ├── Door contacts, request-to-exit, break-glass units
    └── Interface units at AHUs, dampers, lifts
Second fix
  → Devices fitted after ceilings and decoration (detector covers on until clean)
Commission
  → Interface and cause-and-effect test with mechanical, lifts, sprinklers, access control witnessed together
  → Certificates issued — fire alarm is a precondition for building control completion and occupation
```

**Critical rule:** Fire alarm is the integrator. Every interface has two ends and two installers. If the cause-and-effect matrix does not say who does each end, the interface will be missed at commissioning.

---

## Coordination Overlaps

- **With Mechanical:** AHU shutdown, smoke dampers, smoke extract. (Matrix #15)
- **With Lifts:** lift homing, firefighting/evacuation lift control. (Matrix #23)
- **With Sprinklers:** flow switches, valve monitoring. (Matrix #15)
- **With Doors / Ironmongery:** maglocks, door holders, emergency release. (Matrix #14)
- **With Electrical:** dedicated supplies, fire-resistant cable routes, containment. (Matrix #25)
- **With Comms:** IP CCTV and access control on structured cabling — who tests what.
