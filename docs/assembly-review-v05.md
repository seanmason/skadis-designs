# v0.5 — accepted review proposals developed as CAD prototypes

2026-10-31. This revision implements the next prototype direction accepted after the critical review. Physical fit, fatigue, creep and wall anchorage remain untested. Do not treat the large-wall concept as a released installation design.

## Main assembly

The native Fusion document uses four panels on a nominal 480 × 480 mm array. `columns=12`, `rows=12`, and `pitch=20 mm` give 240 mm panel spacing. Three vertical 2020 rails support panel edges; horizontal ties occur at the top and bottom of the two-row demonstrator. Exterior rail centers are inset 10 mm, so the outer bays differ from a repeating interior bay. In a larger array, repeat interior rails at 240 mm and ties at 480 mm; share boundary rails rather than duplicating boxed frames.

Horizontal seams follow a 10 mm step between the two slot columns. A slots are centered at Y=10+20j; B slots belong wholly to the panel below, at Y=20+20j. A 240 mm interior panel therefore has 288 whole slots and an approximately 240 × 250 mm print envelope. Finished top edges omit the final B row. Finished bottoms remain straight and contain no partial slots. All four exterior corner combinations are represented in the main assembly. Interior/standalone comparison parts are separate native models.

`seamGap=0.35 mm` is a starting clearance on both horizontal and vertical step walls. Slot entrance and front outline rounding remains 0.4 mm; finished exterior corners use 6 mm. Tooth tips and their receiving corners use 0.6 mm plan rounding, patterned with the seed features so changing column count preserves the rounding. Tooth roots remain square in plan, with the rounded front edge; inspect them for chipping during the coupon trial. Stepped seams register neighbors in-plane but have no Z undercut: the screws retain panels against forward withdrawal. Printed clearance and thermal movement are still test questions.

The main assembly retains four flush M2×20 screws per panel, the 10 mm provisional hook cavity, 5 mm panel thickness, and a 42 mm face-to-wall stack. The extrusion rear remains at the wall plane. Generic angle, wall-tab and channel-nut geometry remains reference hardware pending supplier matching.

The separate sliding M2 nut keeper is replaced by an integral roof spring. A top-loaded nut passes under a ramp, deflecting the spring into a rear relief; the ramp returns behind the nut. The nut's axial location is unchanged. The nominal spring is 10 mm long, 3.3 mm wide and 0.8 mm thick, with a 1.2 mm retaining projection. This is a flexure coupon candidate, not a proven fatigue-resistant detail. Check print orientation, nut insertion/release, cracking and repeatability before making a batch.

## Practical assembly order

1. Fit channel nuts and side-joint hardware into open rail ends. Assemble the rail frame without closing off required nut insertion paths. Position wall tabs and mount/level the frame through open bays using substrate-appropriate anchors.
2. Fit the printed carriers loosely to their M5 fasteners. Insert M2 nuts from the open end of each carrier track and confirm the spring stop captures them. Do this before panels cover access.
3. Seat the reusable alignment jig on the carrier registration pads. Four temporary M2×20 screws can hold the jig. Its upper access holes and open lower edge expose the M5 screws for tightening. Work from a measured datum; do not accumulate panel-gap errors along a large wall.
4. Remove the jig and mount the panels with four M2 screws each. Check that neighboring stepped edges have clearance before tightening. Do not use screw force to flatten a warped print or force an interference fit.
5. Add artwork after verifying access and panel service. A screw lies between multiple pixel faces; artwork removal is still required to expose it.

For panel removal, clear the required artwork first. Insert the two handling keys vertically through two A slots on the same panel, rotate the thumb knobs 90 degrees, hold them in the locked orientation, and take the panel's weight before releasing the final screws. Pull forward. The tool is an untested concept with no anti-rotation detent or load rating; demonstrate it on a supported sample before lifting a populated panel. Its M2×6 knob screws require a tapping/retention trial in the printed 1.6 mm pilots. Assemble each key through the bridge from behind, then attach its square-drive knob from the front.

## Separate prototype models

- **240 mm alignment jig:** a 232 × 212 mm open frame with the panel's screw and rear-pad coordinates. It preserves M5 driver access while carriers are located.
- **Axial mosaic tile:** two independently colorable pixel regions on a common backing, with two flexible push/pull retention arms. The nominal 9.6 × 19.6 mm face provides 0.4 mm pixel gaps. Color regions are intended to be fused during a registered multipart print; the separate exports are not friction-fit caps. The tile is shown beside a two-slot fit coupon, not already installed. `snapInterference` is a tunable starting dimension. Check insertion force, vertical bearing, pull-off force, neighboring-tile access and repeated cycles. A dense-artwork pickup tool still needs physical evaluation; the panel handle is not a tile extractor.
- **Straight-edge mosaic terminals:** a third pixel extends the first/last B-column tile into the otherwise uncovered 10 mm perimeter band. These special three-pixel pieces share the standard retention geometry. They are a deliberate exception to the interior two-pixel format. Artwork clipping around the board's rounded exterior corners remains to be developed after the retention trial.
- **Metal clamp study:** a custom flanged countersunk sleeve and a separate 12 × 5.5 × 1 mm rear washer bridge the extrusion mouth. A 0.2 mm uncompressed axial gap illustrates controlled plastic compression before the sleeve meets the washer. It adds 1 mm to the rear stack, and therefore is NOT silently substituted in the 42 mm assembly. The sleeve needs a supplier or fabrication drawing, and tolerances, screw length, washer stiffness and torque must be established before adoption.
- **Whole-slot panel comparisons:** native 240 and 280 mm interior variants, plus finished-edge variants. Print/slice both before choosing the production module.
- **Surrounded seam coupons:** a 3×3 array of 80 mm modules at each candidate gap. Print nine copies of the individual coupon, not the assembled array as one fused part. Test the center panel's insertion/removal and tooth durability.

## Verification and release boundary

Initial slicing orientations: panels and jig front-face down; mosaic pixel faces down with all color regions registered as one multipart print. For the carrier spring trial, investigate printing with the open nut-track end toward the bed so the spring grows from its root; the protruding support blade will require accessible external support. Keep support material out of the spring relief and nut track, and inspect first-layer narrowing of the track entrance. This orientation is a proposed slicing setup, not a verified support-free print. Print the handling keys with their transverse tabs on the bed and use a brim as needed; check the long narrow shafts for layer defects before any handling test.

Native feature health, constrained sketches, geometry clearance, resize behavior and export topology are recorded separately with the generated files. Those checks do not measure printed fit or structural strength. The next release gate is physical: seam coupons and actual accessories, carrier/nut tests, 240/280 flatness comparison, then a populated 480 mm service demonstration. Final wall anchorage, splices, load cases and terminal mosaic coverage remain application-specific design work.

The original v0.4 files remain available as a comparison and fallback. The animation was not changed.

## Rebuilding and resizing

The main native document has editable `columns`, `rows`, `seamGap`, board and interface dimensions. Keep the 20 mm pitch and 5×15 mm slot throat for this compatibility trial. Interior-panel resizing was checked at 4, 14 and 12 cells per side (80, 280 and 240 mm), including whole-slot loop counts and bounding dimensions. Frame dimensions follow the module parameters; a 280 mm panel comparison does not qualify a 560 mm crossmember spacing. Finished-edge topology is selected by the generator or supplied variants; do not toggle the exposed edge flags and assume the complete outline will change topology.

To regenerate a fresh main document through the Fusion API, load `fusion/FrameSystemV05.py` and run these phases in separate calls: `start('')`; `panel(i)` for i=0..3; `phase('frame','')`; `phase('carrier_seed',0,0)`; `phase('carrier_seed',1,0)`; `repeat_carriers('')`; `phase('joints',0,0)`; `repeat_joints('')`; `phase('wall_seed','')`; `phase('repeat_wall_tabs','')`; `export('')`. The reusable seed stations and native patterns reduce repeated construction. `replace_panel` is an implementation repair utility, not a required normal build phase.

Run `ValidateV05.run('static')`, then `run('motion')`, then `run('tools')` to produce the combined assembly report in separate stages. The motion stage exceeded the connector's five-minute response window in this session but completed and wrote its report. A connector timeout does not necessarily cancel Fusion execution; check the report and wait for Fusion to become idle before retrying. Run `CheckArchiveV05` after exporting to verify the delivered F3D independently. `PrototypeToolsV05` generates the separate test library; each generated document is archived before it is closed.

## Delivered verification results

- Main assembly: 143 component instances, 850 healthy native features, 19 timeline groups and fully constrained sketches; 1,128 whole slots across its four finished-edge panels.
- [Assembly geometry](validation-v05.json): no static interference, provisional hook-column intrusion, sampled panel/screw removal interference, front protrusion or behind-wall geometry. All 52 frame-tool envelopes are clear. Motion is sampled at seven axial offsets, not continuously solved.
- [Native resizing](resize-validation-v05.json): interior panel passes 80, 280 and 240 mm regeneration with correct whole-slot counts and physical envelopes.
- [Mesh audit](mesh-validation-v05.json): all 41 exported STL bodies have closed edge incidence and nonzero volume; main-panel dimensions match millimeter-scale expectations.
- [Archive round trip](archive-validation-v05.json): delivered F3D reopened and recomputed with matching feature health, parameters and visible instances.

The 16 separate prototype archives also pass native health and sketch-constraint checks, recorded beside each file. Their retention forces, handling strength and printed fit have not been verified by these checks.
