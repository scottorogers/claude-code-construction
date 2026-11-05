# Scope File: Incoming Services and Below-Ground Drainage

**Load when:** Query references DNO / electricity supply, substations, water undertaker connection, gas connection, telecoms incoming (Openreach / other providers), below-ground foul and surface water drainage, SuDS, attenuation, or Uniclass `Ss_50_35` / `Ss_50_70` / `Ss_55_70` / `Ss_70_20` groups (CAWS `R` sections on legacy specs).

**Red flags and coordination matrix are in pe_behavior.md (always loaded).**

---

## Cross-Reference Triggers

- Utility connection offers and design drawings (DNO, water, gas, telecoms) — capacity, point of connection, programme.
- Substation requirements — room or kiosk, access, DNO specification.
- Drainage design — sewer connection consent (Section 106 / adoption agreement where applicable), SuDS approval, attenuation.
- Incoming duct routes from boundary to plant rooms and comms entry room.

---

## Absence Detection Checklist

- [ ] Utility applications made with lead times in the programme (DNO and substation work is long lead).
- [ ] Point of connection and capacity confirmed in writing for each utility.
- [ ] Incoming duct sizes and routes match the provider's requirements and the building M&E. (Matrix #16)
- [ ] Diverse incoming telecoms routes where the client requires resilience (common on data centres).
- [ ] Drainage connection consent and adoption agreements identified.
- [ ] Meter positions and access.

---

## Sequencing Context

```
Applications and offers → wayleaves → ducts during groundworks → utility installs → energisation / connection
  → POINT OF NO RETURN: Programme assumes a supply date the utility has not confirmed
```

**Critical rule:** utility dates are outside the contractor's control and are the most common cause of late energisation. Flag every unconfirmed date as a programme risk.

---

## Coordination Overlaps

- **With Groundworks / External works:** duct installation. (Matrix #16)
- **With Electrical:** intake room, metering, switchboard.
- **With Comms:** telecoms entry and diverse routes.
