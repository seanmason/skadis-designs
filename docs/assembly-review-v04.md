# v0.4 flush-screw prototype

This revision replaces the v0.3 shared front caps. It is a functional CAD prototype for fit trials, not a load-rated wall system. The native Fusion source is `fusion/FrameSystemV04.py`. Earlier revisions remain available.

## Connection and appearance

Each panel has four independent M2×20 cross-recessed countersunk screws. A nominal 3.8 mm head sits 0.1 mm below the face in a 4 mm, 90° pocket. Screws sit on the solid columns between hook slots. There are no front caps and no omitted mounting-node slots. Rounded slot entrances remain 0.4 mm; exterior corners are R6. The nominal seam gap is 0.2 mm; the two rounded face edges produce an approximately 1 mm wide visible shadow line.

An integrated 3.2 × 12 mm support blade carries compression between the panel and a rear carrier. Two shallow rectangular registration pads enter a blind rear panel socket. Splitting the tongue around the screw passage avoids an unprintable 0.2 mm wall. The carrier's M2 metal nuts take screw tension; the plastic is not tapped. Each carrier stays bolted to the frame when a panel is removed. Shared vertical-seam carriers have two independent blades/nuts, one for each panel. The framework and carriers register the assembly; panels do not form a self-supporting interlock without the frame.

The provisional hook test envelope is a continuous 6 mm wide column behind each 5 mm slot column. Supports have 0.4 mm nominal lateral clearance to that envelope. This accounts conservatively for vertical hook movement but is not a substitute for testing actual hooks and the future mosaic tile.

Front-to-wall stack: 5 mm panel + 10 mm hook cavity + 7 mm carrier + 20 mm extrusion = **42 mm**. The extrusion rear and wall feet share the wall plane. The extra carrier thickness is in front of the extrusion, not an air gap behind it. Large hardware starts at the rear of the hook cavity.

## Assembly order

1. Cut and deburr the rails. Loosely pair each carrier with its M5 screw and front-channel nut, and slide these assemblies into the open rails. Load side-channel nuts for frame joints and wall tabs **before closing the rail ends**. Pairing the front nuts with carriers prevents loose nuts sliding down a vertical rail. The modeled nuts are end-loaded metal envelopes; drop-in compatibility has not been established.
2. Assemble and square the frame, with its carriers loosely attached, on a flat surface; protect the projecting blades. Install the in-bay metal angle brackets and side-mounted wall tabs. Side screw access is through the empty bays.
3. Mount and level the uncovered frame to the wall using anchors selected for the actual wall. Anchor drivers approach through the open bays. Only use leveling shims where the real wall requires them.
4. Insert M2 nuts into each carrier's top-loading tracks. Use the small handling plugs; their printed fit needs testing. The nuts are restrained against rotation and axial pull by the carrier, but the loose plug is not a structural retainer. Keep the carriers upright; temporary removable tape may be needed during handling until plug fit is tuned.
5. Position the loosely attached carriers and secure their M5×12 countersunk screws. The fixing is 11 mm below the support axis so its entire head can pass the support blade during insertion. Shallow rear keys align each carrier in the extrusion mouth. Set carrier spacing by trial-fitting a panel with enough initial M5 tension to hold each setting. Remove the trial panel, then tighten the M5 fixings before covering them.
6. Present each panel straight onto its registration tongues. Loosely engage all four M2 screws, check seams and then tighten gently and evenly. Do not use screw torque to force a distorted panel into alignment. Countersinks in printed plastic need a conservative tightening trial.
7. To remove a panel, remove mosaic tiles obscuring its four screw heads, remove only its four M2 screws, and pull straight forward. No neighboring panel fastener is released. A suction cup may help because the face has no projecting handles.

## Hardware and fabrication assumptions

- Per panel: four M2×20 screws and four AF4 × 1.6 mm M2 nuts. Nominal DIN965 M2 head diameter is 3.8 mm; check the purchased part, especially the under-head geometry and actual thread length. [Würth dimensional reference](https://eshop.wuerth.com.mt/countersunk-head-screw-with-recessed-head-h-38).
- Per carrier: one nominal DIN965 M5×12 screw, 9.2 mm head, and one provisional thin metal channel nut (8.8 × 12 × 2.7 mm). The screw tip is 5.1 mm beyond the rail front: 0.9 mm past the nominal nut back, 1.1 mm short of the measured slot floor. Tolerances must be checked physically. [DIN965 dimensional reference](https://www.alacermas.com/index.php/en/pdf/tornillo-cabeza-avellanada-din-965-h-iso-7046).
- The measured extrusion mouth is 6.28 mm, cavity width 11 mm, depth 6.2 mm; floor width 5.7 mm is less certain. The 1.5 mm lip and sloped shape remain approximations. The other chat's successful printed nut-carrier fit does not establish structural capacity for this assembly.
- Panel prints start face-down on a smooth plate, with rear sockets upward. Carrier prints can start on the broad rear face, with blades growing upward; the 2 mm high nut channels require a bridging/support trial. Anti-rotation keys on that face may require local supports or a different orientation. Exported meshes retain assembly coordinates; orient and place on the bed in the slicer.
- The blade's 2.4 mm screw bore leaves only 0.4 mm side walls. The blade is primarily a compression spacer, but print continuity and tongue strength are explicit prototype tests. The countersink also leaves a narrow surface web. Do not scale directly to a heavily loaded installation before testing.

## Parameterization and limits

`columns` and `rows` control the nominal module dimensions in 20 mm cells. Slot centers remain fixed to the compatible lattice. The 2×2 demonstrator uses four finished-corner variants; edge flags control the B-slot omissions at finished top/bottom boundaries. Exterior R6 selection is chosen when building a variant, so rebuild to change its edge topology. Native resizing preserves the chosen edge topology.

Finished horizontal boundaries omit boundary-centered B slots, leaving full holes. Internal horizontal seams combine complementary half-slots. No 90° panel rotation or mirroring is assumed. Keep the lattice pitch and slot geometry unchanged until compatibility is tested.

This small frame demonstrates assembly. A 20-foot wall needs rail splices, intermediate supports, wall attachment spacing and load verification designed separately. The present model provides no full-wall load rating.

## Rebuilding and checking

Run the phases listed in the `FrameSystemV04.py` docstring through Fusion's Python API. Separate calls keep each construction step within the tool response limit. Carrier stations use native rectangular occurrence patterns; upper frame joints and opposite wall tabs use 180° circular occurrence patterns about the parametric frame center. Do not retry a timed-out mutation until inspecting the document: the Fusion operation can finish after the tool response expires.

`ValidateV04.py` evaluates actual occurrence transforms, assembly bounds, 16 screw station positions, solid interference, provisional hook columns, 52 tool envelopes, and sampled axial removal paths. `ResizeV04.py` checks native regeneration and panel dimensions. Hardware references have no modeled threads. Print and fit the small parts before committing to a wall-sized installation.

Final checks passed at 80 mm and 120 mm square module sizes: no solid, hook-column, tool or sampled withdrawal interference; no front protrusions or parts beyond the assembly/wall envelope. Native regeneration also passed at 160 × 120 mm and 280 × 280 mm. The exported assembly is restored to 120 mm modules, with 159 occurrences and 946 healthy timeline features. All sketches are fully constrained. These are geometric checks, not load tests.

The export folder contains the assembly F3D/STEP, four corner-panel STEP/STLs, single/double carrier STEP/STLs and a keeper STEP/STL. `models/v04/panels/` adds individual F3D/STEP/STLs for interior, four straight-edge variants and standalone panels. All 13 printable meshes passed closed-edge incidence and millimetre-scale checks. In a front view, extrusion and carrier surfaces can be visible through slots; they sit behind the tested 10 mm hook cavity.

For the 2×2 demonstrator: four panels, eight single and four double carriers, sixteen M2 screws/nuts/keepers, twelve carrier M5 screws/channel nuts, seven extrusion rails, eight in-bay metal angles with sixteen M5 screw/nut sets, and four wall tabs with eight M5 screw/nut sets. Four wall-anchor heads are placeholders pending wall-specific anchor selection.
