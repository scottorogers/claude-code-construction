# Tag Types — Uniclass Group & Drawing Discipline Reference

## Common Count-Based Tag Types

Sheet ranges below are US-style examples; on UK sets read the ISO 19650 container ID (Role letter E, M, A…) and the drawing register.

| Tag Type              | Uniclass     | Discipline | Typical Sheets   | Schedule Source          |
|-----------------------|-------------|------------|------------------|--------------------------|
| Room tags             | Various     | Arch       | A1.xx-A2.xx      | Room finish schedule     |
| Door tags             | Ss_25_30    | Arch       | A1.xx-A2.xx      | Door schedule            |
| Window tags           | Ss_25_30    | Arch       | A1.xx, A4.xx     | Window schedule          |
| Luminaires            | Ss_70_80    | Elec       | E1.xx-E2.xx      | Luminaire schedule       |
| Electrical accessories| Ss_70_30_80 | Elec       | E1.xx            | DB schedules             |
| Data outlets / WAPs   | Ss_75_10_21 | Comms      | T1.xx / E1.xx    | Outlet / cable schedule  |
| Containment routes    | Ss_70_30_10 | Elec       | E1.xx            | Containment schedule     |
| Fire alarm devices    | Ss_75_50_28 | Elec/FA    | FA1.xx           | Fire alarm device schedule|
| Access control doors  | Ss_75_40_02 | Security   | SE1.xx           | Door / access schedule   |
| Sanitaryware          | Ss_50_30    | PH         | P1.xx            | Sanitaryware schedule    |
| Sprinkler devices     | Ss_55_30    | FP         | FP1.xx           | FP device schedule       |
| Mechanical plant      | Ss_60/Ss_65 | Mech       | M1.xx            | Equipment schedule       |
| Grilles/diffusers     | Ss_65_40    | Mech       | M1.xx            | Diffuser schedule        |
| Equipment tags        | Various     | Multiple   | Varies           | Equipment schedule       |
| Finish tags           | Ss_30_42 etc| Arch       | A1.xx            | Room finish schedule     |
| Furniture tags        | Ss_40       | Arch/Int   | A1.xx, ID1.xx    | Furniture schedule       |
| Joinery tags          | Ss_40       | Arch       | A1.xx, A6.xx     | Joinery schedule         |
| Callout: single ref   | Various     | All        | Plan/section/detail| Cross-reference log     |
| Callout: multi ref    | Various     | All        | Plan sheets primarily| Cross-reference log    |

**Canonical callout types:** Use `simple_callout` for single-reference
callouts (detail bubbles, section marks). Use `multi_detail_callout` for
multi-reference callouts (elevation markers with N/E/S/W spokes).
These are base types in the platform — do NOT create custom alternatives.

## View Type Classification Guide

When vision identifies a tag, classifying the view it sits in
determines whether it becomes an Element Instance or Type Definition.

**Element Instance views (direct count):**
- Floor plans (A1.xx, P1.xx, E1.xx, M1.xx, etc.)
- Roof plans
- Site plans
- Reflected ceiling plans (for light fixtures, devices)

**Type Definition views (multiply across locations):**
- Enlarged plans (e.g., "TYPICAL TOILET", "TYPICAL CLASSROOM")
- Details (e.g., "DOOR HEAD DETAIL", "LAVATORY MOUNTING DETAIL")
- Sections (e.g., "TYPICAL WALL SECTION")
- Elevations (interior elevations showing mounted equipment)

**Classification signals:**
- View title contains "TYPICAL" → almost always a type definition
- View title contains "ENLARGED" → usually a type definition
- View title contains a room name → type definition (check if it
  maps to multiple rooms on floor plans)
- Detail/section bubbles with reference numbers → type definition
- Full floor level shown with grid lines → element instance

## Schedule Cross-Reference

When available, the schedule for a tag type is the ground truth
for completeness checking. Schedules tell you:
- How many items should exist (row count)
- What each item is called (tag designation)
- Where each item is located (room or area column)
- What properties it has (type, size, finish, hardware)

If a schedule exists, the QTO should reconcile against it. If a
schedule says 47 doors and the tag audit found 43, the 4 missing
tags are the primary output — they drive the completeness metric
that makes this skill valuable.
