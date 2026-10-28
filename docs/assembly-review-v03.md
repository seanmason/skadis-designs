# Flush-wall revision: assembly decisions before CAD

2026-10-27. User requested removal of the extra rear stand-off, with practical assembly considered first.

## Known extrusion

The user's **Design Quiet DIY Air Purifier** chat records a 20 x 20 mm extrusion and an end photograph. Its latest user measurements supersede the older identification document: mouth approximately 6.28 mm, widest cavity 11 mm, face-to-floor depth 6.2 mm, and floor width approximately 5.7 mm (least certain measurement). The first rectangular carriers DID NOT FIT. Do not repeat the rectangular-cavity assumption or assume full-height 4 mm M5 hex nuts fit.

The [Wellste W-6-2020 catalog drawing](https://www.wellste.com/wp-content/uploads/2021/05/2020-aluminum-extrusion_Catalog.pdf) is a plausible family comparison, not confirmed identification of the user's stock. The CAD uses the user's dimensions, with tentative 1.5 mm lips, 45-degree inner slopes and a 5 mm center bore. These latter details and corner radii remain unmeasured. Brand and load ratings are not established. The 5.7 mm floor estimate is an explicit parameter, not a verified tolerance.

Use suitably rated, profile-compatible METAL channel nuts for the wall frame. CAD nut envelopes are thin (2.7 mm), 8.8 mm wide and 12 mm long to avoid the deep narrowing and resist rotation. They are geometric placeholders, not a claim that an available nut of this size is rated or verified. The other project's chamfered carriers with thin M5 nuts are fit experiments, not approved structural hardware for this wall. Verify insertion, underside-lip bearing, anti-rotation, full thread engagement and screw bottoming using the real hardware before buying a quantity.

Latest cross-chat status checked on 2026-10-27: the user reports manually starting the revised chamfered-carrier print. No fit result has been reported. A successful print alone would not establish extrusion compatibility or structural capacity.

## Selected arrangement

1. Remove all rear splice plates, rear-facing frame screws and Z-shaped wall standoffs from the v0.3 assembly. Preserve v0.2 separately.
2. Join each horizontal tie to the vertical rails with metal L brackets inside the open frame bays. Brackets and lateral screw heads remain between the extrusion front and rear planes.
3. Attach wall tabs to inward-facing side slots. Their anchor feet and the extrusion backs share the wall plane. Anchor heads and driver access face forward into open bays. This avoids machining large counterbores through an unidentified profile.
4. Keep the 10 mm panel-back-to-frame-front gap. Board-face-to-wall distance is 35 mm before necessary leveling shims, with no designed air gap behind the extrusion.
5. Replace rear inter-panel bridge keys with four locating pins on each shared mounting seat. Corresponding blind pockets in the panel backs register the panels to those seats. The seats stay with the frame/spacer stack during removal. Attaching a rear bridge to one panel was rejected: pulling that panel forward would drive the bridge into its neighbor. No additional front screws or M2 key-retention screws are required.
6. Use 5 mm-thick decorative metal caps so the default stack can use nominal M5x25 front screws with the thin nuts. Other cavity/cap settings require recalculating screw length. Side brackets use nominal M5x8 references. These lengths have geometric clearance in the modeled assumptions, not verified real hardware engagement.

At the default dimensions, both screw paths project 5 mm past the extrusion face. The assumed lip plus nut thickness is 4.2 mm, leaving 0.8 mm beyond the nut and 1.2 mm before the slot floor. Actual thread runout, nut chamfers, screw tolerances and required thread strength are not represented by the smooth reference bodies.

## Assembly order and access

1. Confirm a sample metal nut fits the actual channel, and check the chosen screw length for engagement and bottoming. Cut and deburr rails; clear chips. Use compatible metal brackets; their reference CAD is not a manufacturer drawing or rated bracket specification.
2. Before tightening anything, end-load the required front and side nuts in position order. Use suitable spring-retained metal nuts or temporary placement aids for vertical channels. Do not assume arbitrary roll-in nuts fit the measured opening. Fit bracket nuts and wall-tab nuts before other fixed nuts block their sliding routes. Leave end caps until this is done.
3. Assemble the bare frame flat on a bench, with its front accessible. Attach all corner brackets, check diagonals and coplanarity, and tighten the lateral bolts with a short hex key. Wall-tab bolts are also tightened from the bays; none require a tool behind the frame.
4. Present the bare frame to the wall. Locate the actual structural backing, mark and prepare anchors, remove drilling debris, then refit it. Wall anchor positions are illustrative and must follow the wall construction, not the pegboard lattice. Keep anchor heads, washers and driver paths clear of corner brackets and other fasteners. A large installation needs a site-specific anchor and bay/splice plan.
5. Fit thin solid shims behind both rail contact points and wall-tab feet wherever needed to keep the frame planar. Do not pull a distorted wall flat with the frame or bridge an unsupported tab foot with screw preload. Tighten wall anchors through the open bays before any panels obscure access.
6. Bench-fit the registration seats to the panel-back sockets. Check the 2 mm pins in 2.4 mm sockets and align their square pattern with the board axes. The seats must release axially from every panel without being fastened to a neighboring panel.
7. Use temporary headless studs in the front channel nuts to locate the metal compression spacers and printed registration seats. Keep stud engagement within the nut/slot depth and leave enough front projection for a temporary nut. Fit a panel, its visible caps and temporary nuts, supporting it until retained. Add panels from lower left upward/rightward, aligning each seat's pins with the rear sockets. Replace temporary studs/nuts one node at a time with the final visible screws while supporting the local spacer. The studs are an assembly aid, not extra permanent hardware.
8. Leave panels unladen until retention and key fit are checked. Remove any installation aids. Fit the mosaic/accessories only after the 10 mm hook insertion clearance has been physically tested.

## Maintenance

Remove artwork around the affected fasteners first and support the target panel. Removing a shared cap also releases one corner of each adjoining panel; their other mounts must remain secure, with temporary support if necessary. Replace the target panel's four screws/caps with temporary headless studs before withdrawal so that the spacer/seat stacks remain captured. Pull the panel straight forward far enough to clear the locating pins and spacer shoulders. The seats stay on the frame/studs; no bridge travels into a neighboring panel. Removing the relevant panels exposes wall anchors and lateral frame screws. Never require rear access after wall mounting.

The temporary studs prevent loose stacks from dropping, but do not lock each seat axially. Hold an exposed outside-corner seat against its spacer as the panel releases; it may otherwise follow the panel on its pins. Shared seats are stopped by the adjoining panels. This is a supported removal operation, not a hands-free captive mounting system. Remove the temporary studs only after loose parts are supported.

## Demonstrator quantities and nut loading

The 2 x 2 demonstrator uses four 120 mm panels, three 236 mm vertical rails, four 88 mm horizontal ties, eight in-bay metal angles, four flush wall tabs, nine decorative caps, nine compression spacers and nine printed registration seats. It has nine front M5x25 screw references and 24 lateral M5x8 references, using 33 thin metal channel-nut references in total. Four wall-anchor heads are placeholders; anchor selection and quantity for a real wall are unresolved. Have nine temporary front studs available for initial assembly (four are needed to retain the nodes around one panel during service).

At each outer vertical rail, preload three front nuts plus six nuts in its inward side channel: two for the corner angles and four for the wall tabs. Keep wall-tab nut pairs together and in their intended height order; slide nuts from both rail ends if a clamped bracket blocks travel. The center rail needs three front nuts and two angle nuts in each side channel. Each horizontal tie needs one inward-facing nut near each end. Do not trap any required nuts behind tightened brackets.

## CAD validation

The completed 120 mm-module assembly has 120 solid components and 1,321 healthy timeline features, with fully constrained sketches. The [recorded check](validation-v03.json) found no positive-volume intersections among 211 bounding-box candidate pairs (0.01 mm³ reporting threshold), no parts behind the 35 mm wall datum, and no frame hardware entering the hook cavity. Boolean positive and negative controls passed.

All 52 modeled tool envelopes cleared the installed frame hardware at the intended assembly stage: 24 short-hex-key working legs, 24 return legs, and four forward wall-anchor drivers. This establishes clearance for those simplified envelopes; check the actual key, bit holder and anchor hardware before assembly. It does not simulate the full wrench swing or the user's hands.

Each panel was checked at forward travel distances of 0.2, 0.5, 1, 2, 5 and 10 mm, with its four front screws and caps removed, neighboring panels installed and the rear seats supported. No intersections were found. This is sampled motion checking, not a mathematical continuous-sweep proof.

The assembly regenerated healthily at 80 mm and returned to 120 mm modules. The complete interference, tool-envelope and sampled-removal suite also passed at [80 mm](validation-v03-80.json). These checks do not establish a 20-foot-wide frame design: long rail splices, bay spacing, support locations, anchorage and permissible loads still require a separate installation-specific design.

The [final native health record](final-health-v03.json) confirms 120 component timeline groups and 1,321 healthy expanded items. All six additional native panel variants passed their [configuration checks](panel-library-validation-v03.json). All 11 printable STLs passed [closed-edge incidence and scale checks](mesh-validation-v03.json), with 0.01 mm allowance for tessellation bounds. Panels are 119.8 × 119.8 × 5 mm; the seat is nominally 18 mm diameter and 2.8 mm overall including its pins.

Review checklist:

- No permanent frame bracket or head projects beyond the rear wall datum.
- Corner and wall-tab hardware remain out of the 10 mm hook cavity.
- Static solid interference, with thread/root envelopes explicitly distinguished from manufactured threads.
- Open-bay access for wall-anchor drivers and short hex-key working legs, with panels absent at the installation stage.
- Nut loading routes and quantities documented; no assumption that nuts can pass through already clamped nuts.
- Straight forward panel removal checked against installed neighbors, node seats and spacer shoulders after its shared front caps are removed.
- Native sizing check at a second supported module size; print mesh checks for changed panels and keys.

These checks address modeled assembly geometry. They do not establish anchor capacity, bracket strength, the actual profile fit, or a large-wall load rating.

## Native files and editing

Open [frame-assembly-v03.f3d](../models/v03/frame-assembly-v03.f3d) in Fusion for the complete four-panel demonstrator. Its timeline is grouped by component. The [v0.3 folder](../models/v03/) also contains native interior, left/right/top/bottom edge and standalone panel masters; the four corner variants are in the assembly. STEP and STL are derived exports.

Choose the appropriate edge master, then edit `columns` and `rows` in **Modify > Change Parameters**, using even integers 4–14. Keep `pitch=20 mm`. The interior master regenerated at 80 × 80, 160 × 240 and 280 × 280 mm, with 0.2 mm total seam-envelope reduction in each direction. Do not scale meshes to change module size. Edge flags are generator inputs for topology: changing to another edge combination requires selecting another master or regenerating it, rather than merely flipping an existing native flag and expecting new corner features.

Run the generators inside Fusion. For the connector's bounded execution window, use `build_base`, individual `node` batches, `add_joint_pair`, and individual `wall_tab` batches; a single long connector call may time out and roll back. `ExportPanelLibraryV03.export_variant` produces one library configuration per call. Existing v0.2 artifacts are preserved.
