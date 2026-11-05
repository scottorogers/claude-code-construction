# Scope File: Ss_70 — Electrical Systems

**Load when:** Query references LV distribution, switchgear, distribution boards, sub-mains, final circuits, small power, lighting, emergency lighting, containment (tray, basket, trunking, conduit), earthing and bonding, generators, UPS, EV charging, BS 7671, or any Uniclass `Ss_70_` section (CAWS `V`/`Y` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

**Standard:** BS 7671:2018+A4:2026 is current (`reference/uk_regulations.yaml`). Use the edition the contract names. Never quote a BS 7671 regulation number unless it appears in the project documents or a copy the user supplies — write `[VERIFY: BS 7671 reg — not checked]` instead.

---

## Uniclass Groups (NBS v1.43, July 2026)

- `Ss_70_10` Electrical power generation systems (generators, PV)
- `Ss_70_20` Electrical power transmission and distribution systems
- `Ss_70_30` Electricity distribution systems, including:
  - `Ss_70_30_10` Cable management systems (containment)
  - `Ss_70_30_25` Electrical protection systems
  - `Ss_70_30_35` High-voltage systems
  - `Ss_70_30_45` Low-voltage systems
  - `Ss_70_30_50` Medium-voltage systems
  - `Ss_70_30_80` Small power systems
  - `Ss_70_30_94` Vehicle charging systems
- `Ss_70_80` Lighting systems

---

## Cross-Reference Triggers

### Drawings
- Schematic / single-line diagram — DNO intake, main LV switchboard, sub-mains, DBs, generator and UPS changeover.
- Small power layouts at each level — socket outlets, fused spurs, floor boxes, plant connections.
- Lighting layouts — luminaire types, switching/control zones, emergency luminaires.
- Containment layouts — tray/basket/trunking routes, sizes, segregation, fixing method.
- Earthing and bonding schematic — main earthing terminal, protective conductors, supplementary bonding, clean earths for comms.
- DB schedules — way allocation, protective devices, RCD/RCBO arrangement, spare ways.
- Luminaire schedule — types, lumen output, control gear, emergency conversions.

### Specifications
- `Ss_70_30_45` Low-voltage systems — cable types, CPR Euroclass, installation methods, BS 7671 edition.
- `Ss_70_30_10` Cable management systems — containment type, finish, fill, support centres.
- `Ss_70_30_25` Electrical protection systems — protective devices, discrimination/selectivity study.
- `Ss_70_30_80` Small power systems.
- `Ss_70_80` Lighting systems — and the emergency lighting section (BS 5266-1).
- `Ss_70_10` Generation — generator, fuel, PV, battery storage where present.
- PM_70 Testing, commissioning and completion — EIC, test results, O&M content.

### Cross-Discipline (electrical serves every other trade)
- Mechanical (Ss_60 / Ss_65) — EVERY AHU, FCU, pump, fan, chiller, VRF unit needs a supply and local isolator. (Matrix #13)
- Public health (Ss_55_70) — water heaters, booster sets, sump and sewage pumps.
- Lifts (Ss_80_50) — dedicated supply, lift shaft lighting, pit socket.
- Fire suppression (Ss_55_30) — sprinkler pump supply (fire-protected route where required).
- Fire detection & security (Ss_75_40 / Ss_75_50) — dedicated supplies to fire panel, access control, CCTV.
- Comms (Ss_75_10) — comms room supplies, UPS, PDUs, rack power, clean earth. (Matrix #26)
- FF&E / furniture — floor box and desk power locations. (Matrix #18)

### RFI/Submittal Checks
- **Submittal register** — switchgear, DBs, generator, UPS, cable and containment, luminaires, emergency lighting.
- **RFI log** — DNO capacity, fault levels, discrimination, plant connections, lighting levels.

---

## Absence Detection Checklist

- [ ] BS 7671 edition stated in the spec. If not stated, raise it — current is BS 7671:2018+A4:2026.
- [ ] Schematic complete from DNO intake to every DB and plant item.
- [ ] Maximum demand and DNO supply capacity confirmed (DNO offer / connection agreement).
- [ ] Prospective fault current and earthing arrangement (TN-S / TN-C-S / TT) stated at the origin.
- [ ] Discrimination / selectivity study for protective devices.
- [ ] Cable sizing calculations (design software output) for sub-mains, not just a cable schedule.
- [ ] Cable CPR Euroclass stated for every cable type, and matched to the fire strategy.
- [ ] Fire-resistant cable specified for life-safety and firefighting circuits (fire alarm, emergency lighting, smoke control, sprinkler pumps, firefighting lifts) — check the fire strategy.
- [ ] RCD/RCBO protection arrangement shown on DB schedules where the design requires it.
- [ ] Containment fill limits and spare capacity stated; segregation from comms/security cabling shown. (Matrix #25)
- [ ] Support of wiring systems against premature collapse in a fire — fixings method stated (no plastic-only fixings on escape routes).
- [ ] Emergency lighting design to BS 5266-1 — escape routes, open areas, high-risk task areas, signage. (Red Flag §4.5)
- [ ] Local isolators at all mechanical plant. (Red Flag §4.4)
- [ ] Lightning protection risk assessment (BS EN 62305) — or a statement that none is needed.
- [ ] Spare ways in DBs (take the % from the spec — do not assume).
- [ ] Lighting controls to the AD L / spec requirements (presence/absence, daylight).
- [ ] EV charging provision to AD S where applicable.
- [ ] Test and certification deliverables: EIC, schedules of inspection and test results, emergency lighting completion certificate, as-installed drawings.
- [ ] Approved switchgear and generator submittals (check register — switchgear is long lead).

---

## Sequencing Context

```
DNO / incoming supply
  → DNO application and connection offer (long lead — months, not weeks)
  → Substation / intake room built to DNO requirements
  → Main LV switchboard manufactured (long lead — check submittal date)
  → POINT OF NO RETURN: Intake location, supply capacity, switchboard form and ratings
    └── Changing these after manufacture = major cost and delay

First fix
  → Containment installed (tray/basket/trunking) — coordinated with mechanical and comms
  → POINT OF NO RETURN: In-wall first fix before board closure
    ├── ALL back boxes, conduit drops and cable in partitions complete
    ├── Access control cabling to door frames (Ss_75_40) — BEFORE closure
    ├── Power to automatic door operators — BEFORE closure
    └── Motorised blind supplies at window heads — BEFORE closure
  → Fire-stopping of containment penetrations through fire-rated walls/floors (Matrix #10)
  → Sub-mains pulled, DBs installed

Second fix
  → Accessories installed (sockets, switches, fused spurs)
  → Luminaires installed (coordinate with ceiling grid — Matrix #12)
  → Plant connections completed

Inspection, test and commission
  → Dead tests (continuity, insulation resistance, polarity) before energising
  → Live tests (earth fault loop impedance, RCD operation, prospective fault current)
  → Generator and changeover tests, UPS tests
  → Emergency lighting full-duration test
  → EIC issued with schedules — required for handover
```

**Critical rule:** Electrical connects last but must know first. Every other trade's plant needs a supply. When mechanical or equipment schedules change (substitution, added inverter drive, kW change), the electrical design must be re-checked: supply rating, cable size, protective device, isolator. (Matrix #13)

---

## Coordination Overlaps

- **With Mechanical:** every plant item — supply rating, phase, isolator, controls interface. (Matrix #13)
- **With Comms:** containment sizing and segregation, comms room supplies, UPS, earthing. (Matrix #25, #26)
- **With Fire Detection & Alarm:** fire panel supply, fire-resistant cabling, interfaces. (Matrix #15)
- **With Lifts:** dedicated supply, firefighting lift secondary supply where required. (Matrix #23)
- **With FF&E:** floor box and desk power must match furniture layout. (Matrix #18)
- **With Doors / Ironmongery:** auto operators, electric locks, maglocks. (Matrix #14)
- **With Fire Suppression:** sprinkler pump supply.
- **Scope boundary (pe_behavior.md §7.2):** Controls wiring — BMS specialist or electrician? Final plant connection — who makes it? Comms containment — who installs, to what fill?
