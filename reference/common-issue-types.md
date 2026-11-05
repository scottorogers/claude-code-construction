# Common Issue Types — What Skills Should Watch For

## Cross-Document Conflicts

### Drawing vs. Drawing
- Dimension conflicts between plan and detail
- Element location differs between disciplines (arch vs struct,
  arch vs MEP)
- Plan shows one condition, section/elevation shows another
- Large-scale drawing contradicts small-scale drawing
- Door/window locations differ between floor plan and elevation

### Drawing vs. Specification
- Spec calls for product type A, drawing schedules show type B
- Spec section references a detail that doesn't exist
- Drawing shows a condition not addressed by any spec section
- Material/finish specified in spec differs from schedule

### Drawing vs. Schedule
- Door schedule count differs from tagged doors on plans
- Fixture schedule lists item not shown on any drawing
- Schedule references room that doesn't appear on plans
- Hardware set or finish code in schedule not defined elsewhere

### Specification Internal
- Two spec sections claim responsibility for the same scope
- Spec references a standard edition that's been superseded
- Submittal requirement references a product not specified in
  Part 2 of the same section
- Conflicting performance requirements within one section

## Missing Information

### Missing Details
- Section mark on plan with no corresponding section drawing
- Detail bubble referencing a sheet/detail that doesn't exist
- Wall type tag with no wall type definition
- Head/jamb/sill detail missing for a non-standard condition

### Missing Specifications
- Product shown on drawings with no corresponding spec section
- Spec section referenced in drawings but absent from project manual
- Preliminaries (PM_ sections) reference other sections that aren't included

### Missing Dimensions
- Critical dimension missing (room width, corridor clearance,
  equipment clearance zone)
- Elevation dimension missing where floor-to-floor varies
- Clearance dimension missing at accessible routes

## Code and Standards Compliance

### Egress
- Corridor width below minimum for occupant load
- Door swing reducing effective egress width
- Dead-end corridor exceeding maximum length
- Exit signs or emergency lighting not shown where required

### Electrical (BS 7671)
- BS 7671 edition not stated in spec (current: BS 7671:2018+A4:2026)
- Containment fill, segregation of power and data, or support centres not specified
- No RCD/RCBO protection stated where the spec or design requires it
- Test and certification deliverables (EIC, schedules of test results) not listed

### Accessibility
- Accessible route clearances not maintained
- Turning radius not available at accessible fixtures
- Mounting heights not specified for accessible elements
- Door ironmongery not compliant with Approved Document M / BS 8300 as specified

### Fire Protection
- Rated wall penetration without firestop detail
- Fire damper not shown at rated wall/floor penetration
- Rated assembly label missing from partition schedule
- Sprinkler coverage gap in concealed space
- Cable or containment penetration through a compartment wall/floor with no fire-stopping detail or tested system named
- Cable Euroclass (CPR) not stated, or lower than the fire strategy requires

## Construction Feasibility

### Spatial Conflicts
- Insufficient clearance for equipment maintenance access
- Ductwork routing conflicts with structural members
- Plumbing rough-in location conflicts with structural elements
- Ceiling plenum depth insufficient for specified equipment

### Constructability
- Specified product discontinued or long lead time
- Assembly sequence physically impossible as detailed
- Tolerance stack-up exceeds allowable at interfaces
- Access for installation not available as currently detailed

## How to Use This Reference

This file is for SKILLS to reference when deciding what constitutes
a reportable issue. It is NOT a checklist to run mechanically.
Skills should recognize these patterns during their normal work and
log them to the issue registry when encountered organically.

The patterns here represent the issues most likely to generate
variations / compensation events if not caught during document review. They are
prioritized by cost impact: a missed fire rating generates larger
variations than a missing dimension typically.
