# v0.2 parametric frame-mounted pegboard

Engineering prototype, not a load-rated installation. Physical hook, print-fit, creep and wall attachment tests remain pending. The mosaic tiles are a subsequent design stage.

## Native model and configuration

`models/v02/frame-assembly-v02.f3d` contains a 2 x 2 demonstration with four 120 mm nominal modules, three vertical rails, four horizontal ties, nine visible shared mounting caps, removable rear keys, metal rear rail splice plates and wall standoff interfaces. It is a local Fusion archive with editable sketches and timeline features, not an imported mesh.

To regenerate the complete assembly from source, run `fusion/BuildCompleteSystemV02.py` inside Fusion. It creates a new document, builds the assembly, checks it and exports it. It can take several minutes. Run `ExportPanelLibraryV02.py` afterward for the six additional interior/edge/standalone panel files. These scripts use the Fusion API and do not run in standalone Python.

In Fusion, change `columns` and `rows` under Modify > Change Parameters to resize all panels and their frame together. Each count is a 20 mm cell; use even integers. Nominal module size and physical panel size differ by `seamGap` (initially 0.2 mm). Do not scale exported meshes. The 2 x 2 assembly is a detail prototype, not a CAD model or structural design for an entire 20 ft wall.

For a different edge configuration, edit `EDGES=(left,right,bottom,top)` in `fusion/BuildPanelLibraryV02.py`, where 0 is internal and 1 is finished, and run that script inside Fusion. This regenerates topology, rear key sockets and corner selections together. The generated native model remains dimensionally parametric. Do not change the assembly's boundary flags independently: that would leave its adjacent panels and mounting arrangement inconsistent. A 90-degree rotation is not a substitute for a different edge configuration because slots must remain vertical.

Configurations with both top and bottom finished need at least six rows (120 mm nominal height) with this pattern-strip construction. Other configurations start at four rows. Edge flags are generator configuration inputs; changing their numeric values alone in Fusion does not regenerate socket topology or corner-edge selections.

## Geometry and appearance

- Two staggered slot families retain the 20 mm repeat and 10 mm relative offset. Nominal slot throat remains 5 x 15 mm, through a 5 mm panel.
- Front entrances have a 0.4 mm radius. This rounds the entry without enlarging the specified minimum throat throughout the board thickness.
- Finished sides remove complete outer slot rows/columns. The border follows the original lattice datum; it does not shift holes relative to neighboring panels. Complete additional slots are reserved near mounting nodes.
- Only actual exterior corners receive the large 6 mm radius. Face-edge rounding also gives a small intentional seam reveal.
- Horizontal internal seams retain the split-slot strategy, with a 0.2 mm assembly gap. Test a hook across that seam; CAD continuity does not establish a successful physical fit.
- One decorative metal cap retains up to four panel corners. Exterior nodes sit 12 mm inward so the hardware stays within the outside silhouette. A four-panel prototype uses nine visible mounting screws rather than the v0.1 pattern of 24 holes per panel.

## Registration and mounting stack

Two straight and two staggered removable rear keys register the four demonstration seams. Pegs are 3 mm diameter x 0.8 mm deep in 3.4 mm x 1 mm blind sockets. Keys sit in the unperforated corridors and lift away axially; there is no four-sided captive dovetail. Panels are retained by the metal cap/frame stack, not by friction in the keys. Individual panel removal requires removal/loosening of its shared caps; support adjacent panels and catch loose keys while servicing.

Each node comprises a visible 18 mm metal cap, M5 screw envelope, an 8 mm diameter metal compression shoulder through an 8.4 mm panel opening, a printed rear bearing seat, a 12 mm base on the metal spacer, and a nominal slot-6 T-nut. At the default dimensions, the compression spacer is 15 mm long: 7 mm of 8 mm shoulder and 8 mm of 12 mm base. These stepped spacers and decorative caps are custom metal parts, not assumed off-the-shelf purchases and not load-bearing plastic print instructions. Tune shoulder length/shimming to the actual printed thickness so the cap retains the panel without crushing it or leaving it loose.

The 10 mm clear cavity is measured from panel rear to the extrusion front. The seats and keys intentionally occupy small local areas in that cavity. The rails can sit behind slots in front elevation, but seated hooks and their insertion/removal sweep still need checking. No actual IKEA hook was used to certify the cavity.

Default depth: panel 5 + hook cavity 10 + extrusion 20 = 35 mm from board face to frame rear. The wall interface adds 10 mm; visible caps and screw heads project forward separately. Rear splice plates and bracket screw heads fit within that additional wall gap.

## Metal frame and wall interface

Rail CAD uses a simplified 20 mm envelope with a 6 mm slot mouth and a 10 mm internal nut cavity on the front/rear. It deliberately omits irrelevant longitudinal relief and internal extrusion details. It is an interface model, not a manufacturer-exact extrusion cross-section or mass model. Confirm slot lip thickness, cavity, fasteners, end cuts and nut insertion route against the purchased extrusion before fabrication.

Rear metal splice plates connect horizontal ties to vertical rails. Nominal screw and T-nut bodies omit threads and socket detail; use them to inspect placement, not as manufacturing geometry. Front screw length follows the modeled stack and is not automatically a standard stock length. Select length and any washer adjustment from actual thread engagement and bottoming clearance.

Four metal standoff brackets provide wall attachment interfaces, with their feet turned inward behind the panels. They represent machined or welded parts; sharp internal corners are not sheet-metal bend allowances. Their 6.5 mm anchor hole is a placeholder interface, not an anchor specification. Assemble the rear rail attachment hardware before placing the frame against the wall; wall feet remain accessible through the open frame with panels removed.

For a large installation, determine anchoring, rail spacing, segmentation, thermal movement and primary member sizes from actual wall construction and loads. The prototype's count of four wall interfaces is not an installation anchor schedule.

## Print and assembly checks

Print one small panel pair and keys first. Use the same face-down orientation and build plate finish for all panels, with rear sockets upward. Rotate keys onto their broad rear faces with pegs upward. Slicer auto-placement/recentering is necessary because assembly-derived exports retain their component coordinates.

Import panels as separate printable objects and arrange them with bed separation; do not print the assembled 0.2 mm seams as one plate layout, where first-layer expansion could fuse adjacent panels. No slicer project or tested material profile is supplied yet.

Check slot throat and entry radius, seam gap/step, key fit, mounting preload, front removal, and hook insertion at a rail-backed slot. Start with the 10 mm cavity agreed for testing. Increase `hookClearance` if the actual hook sweep requires it. Metal spacers and screw lengths must follow any cavity change.

Keep wall brackets, caps, compression spacers and joining plates as metal parts. STL availability does not imply that a metal part should be printed for structural service.

## Default prototype parts

| Part | Quantity / nominal size |
|---|---|
| Printed corner panels | 4, each 119.8 x 119.8 x 5 mm |
| Printed registration keys | 2 horizontal + 2 staggered vertical |
| Printed rear seats | 9 |
| Metal decorative caps and stepped spacers | 9 of each |
| Vertical 2020 members | 3 x 236 mm |
| Horizontal 2020 ties | 4 x 88 mm |
| Metal rear joining plates | 4 end plates + 2 middle plates |
| Metal wall standoffs | 2 left + 2 right |
| Front M5 fasteners | 9; modeled shank length 22 mm, select actual length/stack after hardware fit check |
| Rear M5 fasteners | 22 nominal M5x8 references |
| T-nuts | 31 nominal slot-6 M5 references |
| Wall anchor interfaces | 4 holes; anchor choice/count for a real installation remains site-specific |

This is a geometry inventory, not a purchase-ready hardware list. In particular, modeled thread engagement is only about 3 mm with the nominal nut envelopes: verify the actual nut's required engagement and screw bottoming clearance before choosing lengths.

## Verification performed

- Final assembly: 114 components, each one solid; 1,062 timeline items checked inside 114 named groups; no unhealthy features or unconstrained sketches.
- Assembly resized to 80 mm modules and back to 120 mm, with correct panel bounds and healthy features.
- Interior panel checked at 80 x 80, 160 x 240, 280 x 280 and 120 x 120 mm nominal sizes. All six additional panel configurations built with fully constrained sketches and healthy features. The other configurations have not each been swept through every possible size.
- Temporary BRep solid-difference checks, with positive and negative controls: 160 candidate assembly part pairs, no overlaps above 0.01 mm3 and no unresolved operations. This tests static modeled geometry, not actual hook insertion, panel service motion, manufacturing tolerances or strength.
- All 13 printable STL exports passed closed-edge incidence and scale checks. No slicing or printing was performed.

Machine-readable evidence: `cad-validation-v02.json`, `panel-library-validation-v02.json`, `final-cad-health-v02.json`, `interference-v02.json`, and `mesh-validation-v02.json` in this directory.
