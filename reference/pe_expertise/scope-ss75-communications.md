# Scope File: Ss_75_10 — Communications Systems (Structured Cabling, Fibre, Data Centres)

**Load when:** Query references structured cabling, copper (Cat 6A etc.), fibre (OM/OS), backbone, horizontal cabling, comms rooms / IDFs / MDF, data halls, racks and cabinets, patching, containment for data, WAPs, DAS, AV, telecoms incoming, cable testing/certification, or any Uniclass `Ss_75_10_` section (CAWS `W` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

**Standards (cite number; take edition from the spec — `reference/uk_regulations.yaml`):** BS EN 50173 (generic cabling design), BS EN 50174 parts 1–3 (installation), BS 6701 (UK telecoms installation), BS EN 50310 (bonding), BS EN 50346 (testing), BS EN 50600 (data centres), BS EN 50575 (CPR cable reaction to fire). Clause text is paywalled — never quote clause numbers or figures from memory.

---

## Uniclass Groups (NBS v1.43, July 2026)

- `Ss_75_10_21` Data distribution and telecommunications systems
- `Ss_75_10_46` Listening systems
- `Ss_75_10_68` Public communications systems (PA)
- `Ss_75_10_70` Radio and television distribution systems
- `Ss_75_10_72` Emergency communication systems (refuge / disabled toilet alarms — check which section the spec uses)
- Containment is `Ss_70_30_10` Cable management systems — usually in the electrical package.

---

## Cross-Reference Triggers

- Comms layouts — outlet locations and IDs, WAP positions, comms room locations.
- Comms room / data hall layouts (typically 1:20–1:50) — rack positions, clearances, cooling units, PDUs, earth bar, ladder rack.
- Rack elevations — patch panel and active equipment positions, cable management.
- Containment layouts — tray/basket routes, sizes, segregation from power.
- Backbone schematic — fibre and copper riser routes, core counts, cable IDs.
- Cable schedule / labelling standard — cable ID format, outlet numbering, patch panel ports.
- Electrical (Ss_70) — comms room supplies, UPS, PDUs, clean earth. (Matrix #26)
- Mechanical (Ss_65) — comms room / data hall cooling and redundancy. (Matrix #26)
- Fire strategy — CPR Euroclass required for cables on escape routes and in voids; fire-stopping of penetrations.
- Furniture / FF&E layout — desk outlets and floor boxes. (Matrix #18)
- **Submittal register** — cable system and warranty, fibre and copper components, racks, containment, test equipment calibration.
- **RFI log** — outlet counts, comms room sizing, containment routes, incoming services.

---

## Absence Detection Checklist

- [ ] Cabling category / class and fibre type (OM / OS) stated, and the system warranty required (manufacturer certified installer, warranty period).
- [ ] Cable CPR Euroclass stated for every cable type and consistent with the fire strategy (escape routes, voids).
- [ ] Labelling and cable ID scheme defined (outlet, panel, port, cable) — and matched in the cable schedule.
- [ ] Outlet quantities and positions match the furniture layout and room data sheets.
- [ ] Comms room sizes allow racks plus front/rear access clearances; door width allows rack delivery.
- [ ] Dedicated cooling to comms rooms, with redundancy if the client requires it. (Red Flag §4.4)
- [ ] Comms room power: dedicated supplies, UPS, PDUs, generator backing where required. (Matrix #26)
- [ ] Earthing and bonding of racks and containment (BS EN 50310 / project spec).
- [ ] Containment sized for fill with spare capacity; segregation from power cabling stated. (Matrix #25)
- [ ] Bend-radius and support requirements for fibre and Cat 6A on containment.
- [ ] Backbone routes between comms rooms per floor, and resilient routes if specified.
- [ ] Incoming telecoms ducts from site boundary to the main comms room / entry room (Openreach / other provider requirements; AD R for dwellings).
- [ ] Fire-stopping of every containment and cable penetration through compartment walls/floors — named tested system. (Matrix #10)
- [ ] WAP, DAS and AV first-fix positions shown, with power (PoE budget or local supply).
- [ ] Test regime: permanent link / channel testing, fibre OTDR/power-meter, test result format, tester calibration.
- [ ] Handover: test results, as-installed drawings, cable schedule, warranty certificate.
- [ ] Data centre jobs: BS EN 50600 availability class or client tier stated; hot/cold aisle containment; raised floor or overhead distribution decided.

---

## Sequencing Context

```
Comms rooms built and enclosed (dust-free before active kit)
  → Earth bar, ladder rack, cable tray, racks installed
  → POINT OF NO RETURN: Backbone and containment
    ├── Riser and backbone containment in place before risers close
    ├── Incoming telecoms ducts installed during groundworks / external works
    └── Fire-rated sleeves through compartment walls/floors for comms routes
  → Horizontal cabling pulled (after ceiling grid, before tiles)
  → Outlets and patch panels terminated
  → POINT OF NO RETURN: In-wall comms before board closure
    ├── Back boxes and drops for outlets, AV, access control readers
    ├── Display mount pattressing and AV conduit
    └── AV rough-in is FREQUENTLY missed in the wall closure sequence
  → Fire-stopping of penetrations (and inspection/photograph record)
  → Testing and certification (100% of links — check spec)
  → Active equipment install (client / IT) — needs clean, cooled, powered rooms
```

**Critical rule:** Comms is often a design-and-build or performance-spec package. The skeleton — rooms, risers, containment, power, cooling, earthing, incoming ducts — must still be in the base build design. Verify it is, even when the cabling itself is contractor's design.

---

## Coordination Overlaps

- **With Electrical:** comms room power, UPS, containment fill and segregation, earthing. (Matrix #25, #26)
- **With Mechanical:** comms room and data hall cooling, redundancy, condensate routes away from racks. (Matrix #26)
- **With Architecture / Ceilings:** room sizes, door widths, ceiling void depth for tray, ceiling grid vs WAPs. (Matrix #12)
- **With FF&E:** outlet locations aligned with workstation layout. (Matrix #18)
- **With Security:** access control readers and CCTV on the structured cabling (PoE) — agree who installs and tests. (Matrix #14)
- **With Fire-stopping:** every penetration fire-stopped with a tested system, recorded. (Matrix #10)
- **Scope boundary (pe_behavior.md §7.2):** who installs containment for the cabling installer, who fire-stops comms penetrations, who supplies racks and PDUs (client IT or contractor).
