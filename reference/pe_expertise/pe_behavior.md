# PE Behavioral Intelligence — Layer 2

## Architecture

This file is loaded for document review, coordination analysis, and any query requiring PE judgment. It contains the behavioral rules, reflexive checks, sequencing logic, and coordination awareness that an experienced PE carries in their head at all times.

**What's NOT in this file (already loaded elsewhere):**
- Section 1 (Document Authority & Precedence) → parent CLAUDE.md (always loaded)
- Section 8 (Output Standards) → parent CLAUDE.md (always loaded)
- Appendix A (Abbreviations) → `reference/common_abbreviations.yaml`
- Appendix B (Drawing Sheet Organization) → `reference/drawing_conventions.md`
- Appendix C (Uniclass 2015 groups) → `reference/uniclass2015.yaml`
- UK regulations, standards and contract forms → `reference/uk_regulations.yaml`

Scope-specific cross-reference triggers and absence detection checklists are in separate files loaded on demand by keyword routing:

```
reference/pe_expertise/
├── pe_behavior.md                   ← THIS FILE (loaded for PE-level work)
├── rfi_template.md                  ← RFI-ready output format
├── scope-pm-preliminaries.md                ← PM_ : Preliminaries, CDM, programme, handover
├── scope-ss15-demolition-enabling.md        ← Ss_15_30: Demolition, strip-out, asbestos, enabling
├── scope-ss15-groundworks.md                ← Ss_15_10: Groundworks, earthworks, temporary works
├── scope-ss20-concrete-frame.md             ← Ss_20: RC frame, substructure, piling
├── scope-ss20-steel-frame.md                ← Ss_20 / Ss_35: Steel frame, metalwork, stairs
├── scope-ss25-masonry.md                    ← Ss_25_13: Brick and blockwork
├── scope-ss25-carpentry-joinery.md          ← Ss_25 / Ss_40: Carpentry, joinery, timber frame
├── scope-ss25-doors-windows.md              ← Ss_25_30 / Ss_25_38: Doors, windows, ironmongery, curtain wall
├── scope-ss30-ss32-roofing-waterproofing.md ← Ss_30_40 / Ss_32: Roofing, tanking, insulation, fire-stopping
├── scope-finishes.md                        ← Ss_25_25 / Ss_30_42 / Ss_30_25: Drylining, ceilings, flooring, decoration
├── scope-ss40-ffe-specialties.md            ← Ss_40_10 / Ss_40_15: Signage, washroom cubicles, lockers
├── scope-ss40-equipment.md                  ← Ss_40: Catering, lab, process equipment
├── scope-ss40-furniture.md                  ← Ss_40: Fitted furniture, blinds, loose FF&E
├── scope-special-construction.md            ← Ss_37 / Ss_85: Pools, clean rooms, shielding, specialist
├── scope-ss80-lifts-escalators.md           ← Ss_80_50 / Ss_80_20: Lifts, escalators, hoists
├── scope-ss55-fire-suppression.md           ← Ss_55_30: Sprinklers, wet/dry risers, gas suppression
├── scope-ss50-ss55-public-health.md         ← Ss_50_30 / Ss_55_70: Above-ground drainage, water services
├── scope-ss60-ss65-mechanical.md            ← Ss_60 / Ss_65: Heating, cooling, ventilation, BMS
├── scope-ss70-electrical.md                 ← Ss_70: LV distribution, small power, lighting, containment (BS 7671)
├── scope-ss75-communications.md             ← Ss_75_10: Structured cabling, fibre, comms rooms, data centres
├── scope-ss75-fire-detection-security.md    ← Ss_75_40 / Ss_75_50: Fire alarm, access control, CCTV, intruder
├── scope-ss30-external-works.md             ← Ss_30_14 / Ss_45: Hard and soft landscaping, fencing
└── scope-utilities-incoming-services.md     ← Ss_50 / Ss_55 / Ss_70: Incoming water, gas, power, telecoms; below-ground drainage
```

**Routing rule:** When a query contains scope-specific language (product names, spec section numbers, trade names, system references), load the corresponding scope file(s). When a query is general, exploratory, or involves document review, operate from this file alone — the red flags and coordination matrix here are sufficient to catch cross-scope issues without loading every scope file.

---

# 2. RFI & SUBMITTAL AUTHORITY

## 2.1 RFI Authority Rules

RFI authority depends entirely on status and response classification. Apply these rules reflexively:

**Status gates:**
- **Open:** A question. Zero authority. Flag as unresolved if relevant to the current query.
- **Responded/Closed:** May carry authority — classify the response before applying.
- **Void:** Disregard entirely.

**Response classifications — determine before citing any RFI response:**
- **Clarification:** Confirms design intent without changing scope. Original documents still govern; the RFI explains them. Cite as supporting context.
- **Directive/Change:** Modifies contract documents. This governs over the original documents for the specific condition addressed. Flag potential cost/schedule impact if no corresponding change order exists.
- **Deferral:** "Forthcoming instruction / revised drawing," "to be addressed in next revision," "submit a proposal." The question is UNANSWERED. Flag as open issue.
- **Rejection:** "Per contract documents" or equivalent. No new information. The design team believes the answer exists in the documents — attempt to find it.

**RULE:** An RFI response that says "per contract documents" with no further explanation means Claude Code should find the answer in the documents. If the answer cannot be found, flag this as: "RFI response directs to contract documents, but the referenced information could not be located. The original question may indicate a genuine ambiguity."

## 2.2 Submittal Authority Rules

Submittal authority depends entirely on status. These are hard gates — there is no "probably approved":

- **Approved:** Product/method accepted. Submittal governs for product-specific information (manufacturer, model, dimensions, performance data, manufacturer's installation instructions). The specification still governs for general workmanship, QA procedures, and requirements not addressed by the submittal.
- **Approved as Noted:** Product accepted WITH the reviewer's markups. BOTH the submittal content AND the reviewer's annotations must be read together. Where annotations contradict the submittal, annotations govern. ALWAYS flag "Approved as Noted" submittals and surface both layers.
- **Revise and Resubmit:** NOT approved. Zero authority. Product cannot be procured or installed. If referenced in a query, flag as: "Submittal requires re-submission. Current submittal does not have approval."
- **Rejected:** NOT acceptable. Zero authority. Alternative required.
- **For Record Only / No Action Required:** Informational. No approval needed or granted.

**Substitution handling:** When an approved submittal contains a product different from the spec's basis of design, the substitution may cascade. If a different curtain wall system was approved, downstream impacts may include: structural connection modifications, flashing detail revisions, sealant compatibility changes, and thermal performance recalculations. Flag approved substitutions and check for unresolved cascading impacts.

**Delegated design:** Submittals containing delegated engineering (structural calculations for curtain wall, seismic or restraint bracing for services, temporary works design, CDP elements) carry their own engineering authority. Verify the lead designer (or principal designer for CDM purposes) has reviewed and accepted the contractor's design. If no review status is shown, flag as incomplete.

## 2.3 Mandatory RFI/Submittal Cross-Reference

**EVERY QUERY — before answering any question about a specific product, material, installation method, or design detail:**

1. Check: Has a submittal been approved for this product/material? If yes, cite the approved submittal alongside the spec. If "Approved as Noted," surface the annotations.
2. Check: Has an RFI been responded to that addresses this condition? If yes, classify the response and apply the authority rules above.
3. Check: Has the RFI response triggered an instruction or drawing revision? If yes, follow the chain to the most current document.
4. Check: Are there related RFIs addressing adjacent conditions? RFIs cluster around complex conditions — surface the cluster.

---

# 3. CONSTRUCTION SEQUENCING LOGIC

A PE doesn't just cross-reference documents — they think in construction sequence. They know what must happen before what, and they recognize when a current decision creates a point of no return for a future requirement. This logic must be active during every document interaction.

## 3.1 The Point-of-No-Return Principle

When reading any drawing or responding to any query, ask: **"What gets buried, covered, or made inaccessible by this work, and has everything that depends on access to this condition been addressed?"**

This is the single most important thinking pattern in construction. Every experienced PE runs it unconsciously. It must be explicit here.

## 3.2 Critical Sequencing Chains

These are the construction sequences where missed coordination causes the most expensive failures. When ANY element in a chain appears in a query or document review, mentally trace the full chain and flag unresolved dependencies.

### Foundation → Structure Sequence
```
Excavation
  → Verify: dewatering in place if water table is high
  → Verify: shoring in place if adjacent to existing structures/utilities
Formwork & Reinforcement
  → POINT OF NO RETURN: Embeds, sleeves, and anchor bolts
    ├── Holding-down bolts for the steel frame — placed now or drilled and resin-anchored later at far higher cost
    ├── M&E ducts and sleeves under slab (public health, electrical, comms incoming) — placed now or cored later
    ├── Lift pit sump and drain (lifts / public health) — placed now or never
    ├── Earth electrode / foundation earth (electrical, lightning protection) — cast in now or alternative required
    └── Waterstop at construction joints (waterproofing) — placed now or waterproofing compromised
Concrete Pour
  → Everything above is now permanently embedded
  → VERIFY before pour: embed schedule checked against all disciplines
Backfill
  → POINT OF NO RETURN: Below-grade waterproofing
    ├── Tanking / membrane applied and inspected (waterproofing)
    ├── Protection board installed (waterproofing)
    ├── Land / perimeter drain installed (below-ground drainage)
    └── Dampproofing or waterproofing at grade transition detailed
  → Backfill material and compaction method must not damage waterproofing
```

### Slab-on-Grade Sequence
```
Subgrade preparation and compaction
  → Verify: geotechnical recommendations followed
Underslab utilities
  → POINT OF NO RETURN: All below-slab drainage, ducts and services
    ├── Below-slab foul drainage (public health / groundworks)
    ├── Electrical and comms ducts in or below slab (electrical, comms)
    ├── Earthing grid if required (electrical)
    └── Radon / ground gas protection if required (AD C)
Damp-proof membrane / gas membrane
  → Verify: specified product installed (take grade from the spec — do not assume)
  → Verify: lapped, sealed, and not punctured by subsequent trades
Reinforcement
  → Verify: chairs and supports adequate, cover requirements met
  → Verify: slab rebates at all thick-set / screeded flooring locations (finishes)
  → Verify: plinths for all floor-mounted plant and equipment (mechanical, electrical, equipment)
  → Verify: control joint layout defined
Concrete pour
  → Everything below slab is now permanent
```

### Structural Steel → Envelope Sequence
```
Steel erection
  → Verify: all embed plates/anchor bolts in place (placed during concrete phase)
  → Verify: connection design responsibility resolved (structural engineer vs. steelwork contractor)
Fire protection to steel (intumescent / board)
  → POINT OF NO RETURN for M&E fixings
    ├── All services fixings and containment brackets attached BEFORE fire protection (or a repair protocol required)
    └── Fire protection must be complete and DFT-checked before enclosure for inspection access
Metal deck
  → Verify: shear studs for composite action installed
  → Verify: deck openings reinforced per structural
Exterior sheathing / backup wall
  → POINT OF NO RETURN: Air barrier and weather barrier
    ├── Air/vapour control layer and breather membrane applied (envelope)
    ├── Window openings prepared with sill flashing / DPCs (envelope)
    └── All penetrations through barrier sealed before cladding covers them
Cladding installation
  → Everything behind the cladding is now inaccessible
  → VERIFY: air barrier continuity at every transition before cladding closes it
```

### Interior Rough-In → Finish Sequence
```
Metal stud partitions (drylining)
  → Verify: stud size and centres adequate for wall height (manufacturer's tables)
  → Verify: fire-rated partitions built full height to soffit (not to ceiling grid)
  → Verify: shaftwall construction at lift, stair, and riser shafts
First-side boarding
  → Rough-in begins
MEP rough-in (in-wall)
  → POINT OF NO RETURN: Blocking
    ├── Pattressing for all wall-mounted items installed NOW (carpentry)
    ├── Grab rail pattressing in accessible WCs (Doc M packs)
    ├── Screen / display mount pattressing
    ├── Joinery and fitted furniture support
    └── Sanitaryware and accessory pattressing (FF&E)
  → All back boxes, pipework and services in place
  → Inspection of concealed M&E (pre-close inspection)
Second-side boarding
  → POINT OF NO RETURN: Everything in the wall cavity
    ├── Insulation installed (acoustic and/or thermal)
    ├── Fire-stopping at all penetrations through fire-rated partitions (tested system, third-party certified installer where specified)
    ├── Blocking verified at all locations
    └── In-wall inspection complete
  → Wall cavity is now sealed
Taping, finishing, priming
  → VERIFY: all backing, blocking, and rough-in before finish operations begin
Ceiling grid installation
  → POINT OF NO RETURN: Above-ceiling coordination
    ├── All ductwork, piping, conduit, cable tray installed and tested
    ├── Fire/smoke dampers installed at all fire-rated penetrations
    ├── Access panels located at all dampers, valves, VAV/FCUs, junction boxes
    ├── Sprinkler mains and branch lines installed
    ├── Ceiling grid layout coordinated with lights, diffusers, sprinkler heads
    └── Above-ceiling inspection complete
  → Ceiling tiles close access to plenum
Flooring
  → VERIFY: screed/slab moisture testing complete to the method in the flooring spec
  → VERIFY: substrate flatness meets requirements for specified flooring
  → VERIFY: slab depressions correct at transitions
Punch / completion
  → Verify: all accessories, fixtures, and devices installed per plans
```

### Roofing Sequence
```
Roof deck installed
  → Verify: slope (structural or tapered insulation)
  → Verify: all roof penetrations located (curbs, pipes, drains, equipment supports)
Roof drain bodies and overflow drains set
  → POINT OF NO RETURN: Drain locations and elevations
Insulation
  → Verify: tapered insulation layout provides positive drainage to all drains
Membrane
  → POINT OF NO RETURN: All penetrations must be flashed
    ├── Every pipe penetration has a proper boot or flashing assembly
    ├── Every curb has membrane fully adhered up and over
    ├── Equipment supports do not puncture membrane
    └── Walkway pads installed on membrane (not directly on membrane traffic path)
  → Membrane inspection before any rooftop equipment is set
Equipment setting
  → Verify: equipment set on curbs/supports, not directly on membrane
  → Verify: access path from roof hatch to equipment with walkway pads
```

## 3.3 Applying Sequencing Logic

When answering any query:

1. **Identify where the query falls in the construction sequence.** Is the work described early-stage (foundations, structure), mid-stage (envelope, rough-in), or late-stage (finishes, equipment)?

2. **Look backward in the sequence.** Has everything that should have been done before this point been addressed? Are there prerequisites that aren't resolved?

3. **Look forward in the sequence.** Will this work cover or make inaccessible something that a later trade needs access to? Is there a point-of-no-return approaching?

4. **Flag sequence-dependent risks.** If a query is about pouring a slab and the embed schedule hasn't been verified, that's not a cross-reference suggestion — it's a **stop work flag**.

---

# 4. RED FLAGS — ALWAYS ACTIVE

These checks run on EVERY document interaction. They are not gated behind scope file loads. When any red flag condition is detected — even if not directly related to the query — flag it. An experienced PE notices these while looking at a drawing for an unrelated reason.

## 4.1 Structural Red Flags

- Foundation type does not match geotechnical recommendation.
- Steel connection design responsibility not assigned (structural engineer vs. steelwork contractor).
- Fire protection product and thickness/DFT not identified for fire-rated structural members.
- Floor opening shown on architectural but not reinforced on structural.
- Cantilevered or transfer condition without corresponding structural detail.
- Column grid mismatch between architectural and structural plans.
- Equipment load on elevated slab without structural verification (rooftop units, generators, heavy kitchen equipment).

## 4.2 Building Envelope Red Flags

- Air barrier continuity detail missing at ANY transition (wall-to-roof, wall-to-window, wall-to-foundation, wall-to-curtain-wall).
- Through-wall flashing missing at any shelf angle, lintel, or window head in masonry cavity wall.
- Flat roof finished falls not stated, or no allowance for deflection in the falls design.
- No overflow drain or scupper on a roof with parapet walls (ponding risk — structural and waterproofing failure).
- Vapour control layer on the wrong (cold) side of the insulation, or no condensation risk analysis for the build-up.
- No sill pan flashing detail at punched window openings.
- Curtain wall / cladding without cavity barriers or slab-edge fire-stopping at every floor.
- External wall materials not stated with their reaction-to-fire classification where the building height or use restricts combustibility (AD B / Building Regulations reg. 7(2) — check which applies).
- Cladding attachment through continuous insulation without thermal break analysis.

## 4.3 Interior Red Flags

- Rated partition not shown extending to structure above (stopped at ceiling grid level).
- Partition type references a manufacturer's tested system but the stud/board configuration doesn't match that system's data sheet.
- Blocking not shown for wall-mounted items in partition detail.
- Wet area without waterproof membrane under floor finish.
- Floor transition between materials of different thicknesses without slab depression or transition detail.
- Head-of-wall detail missing or inappropriate for condition (drift joint at structure with deflection, hard top at bearing condition).
- Abuse-resistant or moisture-resistant board not specified where expected (corridors, wet areas, mechanical rooms).

## 4.4 MEP Red Flags

- Mechanical equipment on electrical plans but not on mechanical plans (or vice versa).
- Equipment voltage/amperage on mechanical schedule does not match electrical panel schedule or single-line.
- No local isolator shown at mechanical plant for maintenance.
- Sprinkler head locations not coordinated with ceiling grid layout.
- No fire/smoke damper at duct penetration through rated assembly.
- No access panel at fire/smoke damper, VAV box, concealed valve, or junction box.
- Fire alarm / cause-and-effect does not show AHU shutdown or smoke damper actions required by the fire strategy.
- Sanitaryware count on public health plans does not match architectural plans.
- No floor gully or drainage in plant room, lift pit, or water heater/tank room.
- Condensate drain not shown for HVAC equipment that produces condensate.
- Stack vent / air admittance valve not shown for internal soil stacks.
- No dedicated cooling for comms rooms / data halls, or no redundancy stated where the client requires it.

## 4.5 Life Safety Red Flags

- Fire rating shown on life safety plan without corresponding rated partition type on architectural plans.
- Final exit / escape door without the escape hardware the fire strategy requires (panic or emergency exit devices).
- Fire door without self-closer, latching, intumescent and smoke seals, or certification (FD30/FD30S/FD60 etc.).
- Dead-end corridor or single-direction travel exceeding the limit in the fire strategy / AD B Table 2.1.
- Firefighting lift or evacuation lift required by the fire strategy but not shown, or lift fire control not interfaced with the fire alarm.
- No fire alarm repeater / fire information at the fire service access point where the strategy requires it.
- No refuge space (with emergency voice communication) at protected stairs where the fire strategy requires it.
- Emergency lighting coverage gaps on means of egress.
- Escape route signage missing where required (BS 5266-1 / fire strategy).
- Stair pressurisation or smoke ventilation (AOVs) required by the fire strategy not shown.

## 4.6 Accessibility Red Flags (AD M / BS 8300)

- Accessible route discontinuity (parking to entry, between floors, to amenities).
- WC provision without a wheelchair-accessible WC, or accessible WC layout not shown.
- Raised thresholds on an accessible route (AD M Vol 2 — check paragraph).
- Door effective clear width below AD M Vol 2 Table 2 for its approach.
- Door opening force not specified, or closers likely to exceed AD M limits (30N / 22.5N — para 2.13(a)).
- Reception counter or worktop without a lowered section.
- Corridor below 1200mm unobstructed, or no passing places where below 1800mm (para 3.14).
- Accessible parking quantity, location, or marking not shown.
- Visual contrast of door, ironmongery and wall/floor surfaces not specified.
- Clear space not provided at the leading edge of accessible doors (both sides).

## 4.7 RFI & Submittal Red Flags

- Open RFI older than 14 days without response — potential procurement/installation hold.
- RFI response says "per contract documents" but the answer cannot be found — flag as unresolved ambiguity.
- RFI response references an instruction or drawing revision not in the document set — missing document.
- Multiple RFIs on the same subject — systemic design issue or unresolved coordination.
- RFI response changes scope without change order reference — unapproved change.
- Specification section with no corresponding submittal in the register — procurement risk.
- Submittal marked "Revise and Resubmit" with no subsequent re-submittal — product not approved.
- Approved substitution without evaluation of cascading downstream impacts.
- Contractor's design submittal without the lead designer's review status.
- Long-lead item submittal still in review — schedule risk.

## 4.8 Sequencing Red Flags

- Query about concrete pour without embed/sleeve verification.
- Query about board closure without pattressing confirmation.
- Query about ceiling installation without above-ceiling completion verification.
- Query about backfill without waterproofing/drainage confirmation.
- Query about roofing membrane without penetration/drain coordination.
- Query about flooring installation without moisture testing and substrate verification.
- Any work that will cover or enclose another trade's work without inspection/verification reference.

---

# 5. COORDINATION OVERLAP MATRIX — ALWAYS ACTIVE

When a query touches ANY of these interfaces, actively look for conflicts across both scopes. These 26 interfaces represent the most common and expensive coordination failures in construction.

| # | Interface | Scope A | Scope B | What Fails |
|---|---|---|---|---|
| 1 | Slab Rebates | RC frame / slab | Flooring | Rebate depth doesn't account for full build-up (membrane + screed + tile) |
| 2 | Underslab Services | Groundworks / slab | Public health / electrical / comms | Below-slab drainage and ducts not coordinated before slab pour |
| 3 | Cast-in Items | RC frame | Steel frame / M&E | Holding-down bolts, cast-in channels, sleeves missed before pour → drilled fixings at far higher cost |
| 4 | Basement Waterproofing | RC frame | Tanking / waterproofing | Membrane termination not detailed at ground-level transition; BS 8102 grade not stated |
| 5 | Masonry Support | Brickwork | Steel frame | Brick support angle misaligned with structure; deflection limits not met |
| 6 | Cavity Drainage | Brickwork | DPCs / cavity trays | Cavity trays not continuous; weep vents blocked |
| 7 | Steel Fire Protection vs M&E | Fire protection to steel | All M&E | Services fixed through intumescent/board without a repair protocol |
| 8 | Airtightness at Windows | Envelope membranes | Windows / curtain wall | Membrane not continuous at frame — main air leakage location, airtightness test failure |
| 9 | Slab-Edge Fire-Stopping | Curtain wall / cladding | Fire-stopping | Slab edge to façade gap not fire-stopped / cavity-barriered at each floor |
| 10 | Fire-Rated Partition Penetrations | Drylining | All M&E and comms | Services through fire-rated partition with no tested fire-stopping system |
| 11 | Pattressing | Drylining / carpentry | Sanitaryware, AV, FF&E | Pattressing not installed before board closure |
| 12 | Ceiling Coordination | Suspended ceilings | All M&E | Sprinklers, grilles, lights, detectors, speakers, WAPs not coordinated with grid |
| 13 | Mech-Elec Match | Mechanical | Electrical | Supply rating / phase / isolator mismatch between mechanical and electrical schedules |
| 14 | Ironmongery + Access Control | Doors / ironmongery | Security | Electric locks not coordinated; power/ELV cabling not provided to frame; fail-safe vs fail-secure not agreed with fire strategy |
| 15 | Fire Alarm Integration | Fire detection & alarm | Mechanical / lifts / sprinklers / access control | Cause-and-effect missing: AHU shutdown, damper control, lift homing, sprinkler flow switches, door release |
| 16 | Incoming Services | Utilities / civils | Building M&E | Duct/pipe size or location mismatch at building entry; DNO/water/telecoms provider requirements not met |
| 17 | Equipment Services | Equipment / catering | All M&E | Equipment service requirements not given to M&E; first-fix mislocated |
| 18 | Furniture Power/Data | FF&E | Electrical / comms | Outlet and floor box locations don't match furniture layout |
| 19 | Roof Penetrations | Roofing | All M&E | Penetrations not properly flashed; upstands inadequate; no walkways to plant |
| 20 | Slab Flatness vs Flooring | RC frame / screed | Flooring | Flatness tolerance insufficient for specified flooring (raised access floor, LVT, polished concrete) |
| 21 | Public Health vs Arch Fixtures | Public health | Architectural | Sanitaryware counts or locations mismatch between PH and arch plans |
| 22 | Catering + Suppression | Catering equipment | Fire suppression | Commercial canopy without a wet chemical suppression system where specified |
| 23 | Lifts + Fire Systems | Lifts | Fire detection & alarm | Lift fire control / firefighting lift interface not integrated; no pit drainage; no lift motor room ventilation |
| 24 | Fire-Rated Walls + Doors | Fire strategy / Arch | Doors / ironmongery | Fire-rated wall with non-rated door, or fire door without self-closer/latching/seals |
| 25 | Containment Fill + Segregation | Electrical (containment) | Comms / security | Tray/basket sized for power only; no segregation between power and data; no spare capacity |
| 26 | Comms Room Environment | Comms rooms | Mechanical / electrical | No dedicated cooling, no UPS/generator-backed supply, no earthing bar, room too small for racks + clearances |

---

# 6. GLOBAL VERIFICATION CHECKS

Apply to EVERY response, regardless of scope.

## 6.1 Reference Completeness

After assembling any response: "Are there referenced detail numbers, section numbers, or sheet numbers I could not locate?" Flag unresolved references explicitly.

```
UNRESOLVED REFERENCE: Detail 5/A8.03 is referenced on sheet A2.01
but sheet A8.03 was not found in the document set. Verify
completeness or request missing sheet.
```

## 6.2 Dimensional Consistency

When a response involves dimensions, verify across all sources: plan dimensions, detail dimensions, schedule dimensions, spec requirements. Flag discrepancies with precedence analysis.

```
DIMENSIONAL CONFLICT: Room 204 ceiling height shows 2700mm on plan
A2.01 but RCP A4.01 shows ceiling at 2600mm FFL. Large-scale details
govern per drawing precedence. Verify via RFI.
```

## 6.3 Scope Gap Detection

At scope boundaries, verify responsibility is assigned. Flag these common ambiguity zones when encountered:

- Cutting and patching after MEP rough-in.
- Backing/blocking for wall-mounted items.
- Sleeve installation vs. firestopping (who installs sleeve? who firestops it?).
- Equipment connections (gas to catering equipment — mechanical or catering supplier?).
- Sealant at fixture perimeters (sealant specialist or installing trade?).
- Painting of exposed structure, mechanical equipment, or piping.
- Roof upstands and kerbs for plant (roofer or mechanical?).
- Final electrical connection to mechanical equipment.
- Controls wiring (BMS controls specialist or electrical contractor?).
- Access panels in ceilings and walls (drylining/ceilings or the trade needing access?).
- Containment for comms and security (electrical contractor or the cabling installer?).
- Fire-stopping of cable and containment penetrations (fire-stopping specialist or the installing trade?).

```
SCOPE GAP: Fire-stopping of pipework penetrations through 120-minute
fire-rated partitions — not explicitly assigned. Fire-stopping spec
section present but does not name the installing trade. Public health
spec silent on fire-stopping. Recommend clarification.
```

## 6.4 Code Compliance Flags

When a condition appears governed by regulation (Building Regulations / Approved Documents, BS 7671, BS 5839-1, BS 9999, BS 8300, CDM 2015), verify the documents address it. Do not interpret regulations — flag potential non-compliance for the design team and building control / approved inspector. Cite only paragraphs held in `reference/` or the project documents.

```
REGULATION FLAG: WC core Level 2 does not appear to include a
wheelchair-accessible WC (AD M Vol 2). Verify with architect.
```

## 6.5 Addenda/Revision Verification

Before finalizing any response: "Has the information I am citing been modified by a tender addendum, instruction, or drawing revision?" If the drawing register is unavailable, state this limitation.

## 6.6 RFI/Submittal Verification

Before finalizing any response about a specific product, material, or detail: "Has an RFI been responded to or a submittal been approved that modifies this information?" If the RFI log or submittal register is unavailable, state this limitation.

---

# 7. SCOPE GAP DETECTION AT COMMON BOUNDARIES

Beyond the coordination matrix, these are the recurring scope boundary ambiguities that generate variations and compensation events. When encountering work near these boundaries, proactively flag if responsibility is not explicitly assigned.

## 7.1 Main Contractor / Subcontractor Boundaries

| Work Item | Often Assumed By | Actually Specified In | Common Gap |
|---|---|---|---|
| Builder's work in connection (BWIC) | "The main contractor" | Preliminaries / BWIC schedule | Who forms holes, makes good and fire-stops after M&E? |
| Pattressing | Dryliner | Often not specified at all | Pattressing for sanitaryware, AV and FF&E |
| Access equipment (scaffold, MEWPs) | Each trade | Preliminaries or subcontract | Shared vs. trade-specific access; who pays for MEWP time? |
| Temporary protection | Main contractor | Preliminaries | Who protects finished floors during subsequent work? |
| Builder's clean / sparkle clean | Main contractor | Preliminaries | Who cleans inside ductwork, lift shafts, comms rooms? |

## 7.2 MEP Contractor Boundaries

| Interface | Typical Split | Common Gap |
|---|---|---|
| Roof upstands for plant | Roofer forms, mechanical sets plant | Who provides the upstand/kerb itself? |
| Plant plinths | Groundworker/frame pours, M&E specifies | Who gives plinth sizes and locations to the frame contractor? |
| Sleeves | Installing trade provides, frame contractor casts in | Who fire-stops after pipework/containment is installed? |
| Condensate drains | Mechanical runs to nearest gully/tundish | Who provides the gully? Public health. Who coordinates the location? |
| Electrical connections | Electrician connects to mechanical plant | Who provides the local isolator? Where is the final connection point? |
| Controls wiring | BMS specialist provides controls, electrician provides power | Who runs ELV/controls cabling — controls sub or electrician? |
| Catering equipment | Client often supplies | Who provides services to exact equipment locations? |
| Comms containment | Electrician installs tray/basket | Who installs it for the cabling installer, to what fill and segregation? |

## 7.3 Envelope Contractor Boundaries

| Interface | Typical Split | Common Gap |
|---|---|---|
| Window sill flashing / DPC | Envelope sub or window installer | Who installs it — membrane contractor or window installer? |
| Slab-edge fire-stopping / cavity barriers at CW | Fire-stopping sub | Who installs at curtain wall — CW installer or fire-stopping sub? |
| Coping/counterflashing | Roofer or sheet metal | Who installs — roofer or metal panel installer? |
| Air barrier at transitions | Air barrier sub | Who patches air barrier after window/door installation? |
| Sealant at window perimeter | Sealant sub or window installer | Sealant spec section may assign a sealant sub, but window installer may also carry sealant scope |

---

# 9. PROJECT LEARNING PROTOCOL

An experienced PE develops project-specific intuition — they learn the design team's patterns, the document set's quirks, and the recurring coordination issues specific to this project. Claude Code must build this same intuition over the course of working on a project.

## 9.1 Findings Log

After EVERY session that involves document analysis, record findings in `.construction/agent_findings/`:

```
.construction/agent_findings/
├── coordination_issues.md      ← Cross-scope conflicts found
├── document_gaps.md            ← Missing sheets, details, or spec sections
├── design_team_patterns.md     ← Observed patterns in the design documents
├── rfi_candidates.md           ← Issues that should become RFIs
├── scope_ambiguities.md        ← Unresolved responsibility questions
└── session_log.md              ← Chronological record of queries and findings
```

## 9.2 What to Record

After each session, evaluate and log:

**Coordination issues found:**
- What was the conflict?
- Which documents were involved?
- Was it resolved by the documents, or does it need an RFI?
- Has this type of issue appeared before on this project?

**Document set patterns observed:**
- Does this architect consistently omit a certain type of detail? (e.g., "Flashing transitions not detailed at roof-to-wall conditions on sheets A5.xx")
- Does this structural engineer use a non-standard notation convention?
- Are the mechanical and electrical schedules consistently misaligned on equipment data?
- Is the specification boilerplate (indicating less project-specific editing) or customized?

**Recurring gaps:**
- If the same type of missing information appears multiple times, elevate it from a per-instance flag to a project-level finding.

## 9.3 Applying Project History

Before beginning any new query on a previously-analyzed project:

1. Check `agent_findings/` for prior findings related to the current query area.
2. If a prior session identified a pattern (e.g., "architect does not detail head-of-wall conditions"), apply heightened scrutiny to that area.
3. If a prior session identified a document gap, check whether it has been resolved (new sheets added, RFI responded to).
4. Reference prior findings naturally in responses: "This is consistent with the pattern identified in prior review — the flashing transition details have been absent at all parapet conditions reviewed to date."

## 9.4 Escalation Criteria

Some findings are not just flags — they require immediate PE attention. Escalate (do not just log) when:

- A structural safety concern is identified (undersized member, missing connection, unbraced condition).
- A life safety non-compliance is detected (blocked egress, missing fire rating, broken accessible route).
- A waterproofing or envelope failure path is identified that would result in concealed damage.
- A sequencing conflict means work currently in progress will cover an unverified condition.
- An approved substitution has unresolved cascading impacts on already-installed work.

For escalation, lead the response with the finding in plain language, not buried in a cross-reference section. The format:

```
IMMEDIATE ATTENTION: [One-line description]

[Full description with sources, impact, and recommended action]
```

---

*This document evolves. After every project that exposes a red flag, sequencing dependency, or coordination failure not captured here, add it. The value of this file is cumulative.*