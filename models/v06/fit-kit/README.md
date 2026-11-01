# Minimal v0.6 fit kit

Open **fit-kit-plate.3mf** in Bambu Studio as geometry, select your H2D and intended filament, and inspect the slice before printing. This is an **unsliced, generic 3MF** containing five separate objects, not a configured Bambu project or G-code. No machine, nozzle, material, support or speed settings are included.

## Print contents

| Part | Quantity | Size mm | Checks |
|---|---:|---|---|
| 01-mount-coupon.stl | 1 | 39.65 x 49.65 x 5 | Rounded slots, centered M2 countersink, rear pad socket, neighboring hook clearance, seam teeth |
| 02-seam-mate.stl | 1 | 39.65 x 19.65 x 5 | Receiving steps, 0.35 mm seam, whole slots and front separation |
| 03-single-carrier.stl | 1 | 20 x 31 x 18.4 | Actual v0.6 open-sided support, registration pads, captive nut spring, M5 seat and extrusion keys |
| 04-two-pixel-tile.stl | 2 | 9.6 x 19.6 x 9.1 | Monochrome version of the existing two-pixel axial spring tile; insertion, retention, removal and adjacent tile spacing |

The 3MF already contains two tile copies. Its occupied footprint is approximately 95 x 56 mm, without brims or supports. Combined solid geometry is about 13.5 cubic centimeters; actual filament use and time depend on slicing. Individual STLs retain CAD coordinates; drop to bed and orient if importing them separately. Do not print the complete assembly STEP as one fused object: it includes nominal metal reference hardware and overlapping assembly bounding boxes.

The native **fit-kit-v06.f3d** contains editable sketches, features and parameters. The companion STEP is an assembly reference. The preview shows the assembled seam and mounting station, with the tile alongside.

## Printing

- Use the intended production filament and nozzle so the fit result transfers. For a 0.4 mm nozzle, a starting fit-trial setup is 0.20 mm layers, four walls and four top/bottom layers. Keep extrusion and dimensional compensation settings consistent with the eventual panels. This is a proposed setup, not a sliced/validated profile.
- The panel samples are front-face down in the 3MF. This places their rear locating recess upward; inspect first-layer expansion around the entrances and countersink. The two tiles have their pixel faces down and springs upward.
- The carrier is turned rail-face down, with its two 0.8 mm anti-rotation keys touching the bed. Its broad rear face therefore sits 0.8 mm above the bed: **provide removable support under that face**, clear of the keys. Inspect the support preview; do not fill the captive-nut track, spring reliefs or screw passage with inaccessible support. Inspect internal bridges as well. Remove support before testing extrusion fit. Carrier support cleanup can affect fit, so record the chosen orientation/settings.
- Check that the narrow spring and support-spine walls survive slicing as continuous paths. Do not use a coarse layer height or enlarge the model to make them printable.
- Leave the holes and slot edges as printed for the first trial. Record any later deburring or filing rather than treating a modified part as an as-printed pass.

## Hardware and existing parts

- One M2 x 20, 0.4 mm pitch, 90-degree flat-head screw; nominal 3.8 mm head.
- One ordinary M2 hex nut, nominal 4 mm across flats and 1.6 mm thick.
- One M5 x 12 Phillips flat-head screw, nominal 9.2 mm head, plus one **physically compatible metal channel nut** for your extrusion. Generic M5 hex nuts are not substitutes. Head dimensions and channel nut fit remain to be verified.
- Use an accessible end of your actual 2020 extrusion; no need to cut a special piece. About 50 mm of clear rail length is enough to accommodate the 31 mm carrier and handling space. Have a real SKADIS hook/accessory sample available.

## Test order and record sheet

1. **Metal nut in bare extrusion:** slide the nut in, verify under-lip bearing and anti-rotation. Check the selected screw does not bottom against the channel floor. Stop if the nut jams or bears only on the sloping floor.
2. **Carrier alone:** slide the M2 nut into its printed track until the spring retains it. Confirm screw alignment and that the nut does not turn. Test removal/reloading gently; record whether the spring cracks or takes a permanent bend.
3. **Carrier on rail:** check both mouth keys fit without forcing. Seat the M5 head in its recess and confirm the carrier sits flat and does not rock. Install the carrier before the panel; this kit does not need the full positioning jig.
4. **Coupon on carrier:** align its two blind rear pad seats, insert the M2 screw and seat it gently flush. Confirm the panel rear is 10 mm ahead of the carrier's main block. Inspect the 1.35 mm front ligament and the open-sided carrier passage; do not tighten harder to cure a bad fit.
5. **Hooks:** compare slots away from the station with the slots immediately beside it. Test the complete insertion/removal motion, not just the resting position. The earlier 6 mm continuous hook envelope overlaps the shifted screw by 0.25 mm; universal hook compatibility is still unresolved. Stop rather than forcing a hook against the screw.
6. **Mosaic tiles:** try each tile in a free slot, then near the mounted screw; compare insertion effort, latch engagement, release and wiggle. Put the two tiles in successive slots in the same column to check pixel spacing. The spring fit is experimental; inspect for whitening or cracks after repeated cycles.
7. **Seam:** bring the mate against the upper teeth with the faces aligned. Check that it seats with a small visible gap and can lift straight forward without binding. This short sample checks local fit; it does not establish full-panel flatness or removal from a surrounding array. The mate has no carrier and is supported by hand during this test.

| Observation | Result / measurement |
|---|---|
| Filament, nozzle, layer height, compensation, support setup | |
| Actual screw heads and nut dimensions | |
| Metal channel nut and M5 engagement / bottoming | |
| Carrier keys and rear face seating | |
| M2 nut insertion, retention, anti-rotation, removal | |
| M2 head flushness and rear pad fit | |
| Free-slot hook insertion vs screw-adjacent slots | |
| Tile insertion / release / permanent deformation | |
| Seam seating / gap / straight-front release | |

This is a **fit test, not a load test**. It does not qualify the full panel, shared double carrier, long frame, joints or wall anchors. Avoid hanging weights from this single-station coupon. After fit is established, use the intended filament and a defined load target for a separate complete mounting/load specimen.

## Verification

Fusion reports 138 healthy timeline features and fully constrained sketches. No static collisions were found between coupon, carrier, reference hardware and seam mate. All four STL meshes have closed edges, and the carrier mesh matches the delivered v0.6 single-carrier export exactly. See `validation.json` and `mesh-validation.json`. The 3MF was packaged from those Fusion exports; it has not been sliced or physically printed.
