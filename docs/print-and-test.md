# Historical v0.1 H2D first-print protocol

**Archived instructions: do not use the M2×8 screws, printed pilots or bridge parts below for v0.4.** See the [v0.4 assembly and hardware notes](assembly-review-v04.md) and the [critical review's prototype/release sequence](design-review-2026-10-29.md#prototype-and-release-sequence) for the current work. The text below records the original experiment.

These are starting settings, not a sliced or printed profile. No print time or filament mass is claimed.

## First plate

Print two copies of panel-fit-coupon-80x80.stl, two bridge-horizontal.stl and two bridge-vertical.stl. Reuse the panels to test horizontal and vertical joining. A second pair lets you test a complete 2 x 2 intersection.

Use the H2D 0.4 mm nozzle and 0.20 mm layers as an initial setup. PLA is the initial panel material for a flat, cosmetic indoor face. PETG is a candidate for bridges; test it separately. Start with four walls, five top/bottom layers and 20% gyroid for panels, six walls / effectively solid small bridges. These choices are proposed for this geometry, not borrowed print-profile guarantees.

Panel orientation: face Z=0 on the plate, rear locating pockets upward. Keep support generation off unless the slicer identifies an actual overhang needing it; the panel has none by intent. Use the same plate finish/orientation for all visible faces.

Bridge orientation: rotate so the broad flat rear surface is on the bed and the locating pegs point upward. The exported coordinates have the peg tips below Z=0, so do not simply drop them on the plate in their exported orientation. There should be no supports after reorientation.

Use the stock printer/material temperature profiles as a starting point. Inspect the first layer and use elephant-foot compensation based on calibration, especially on the exposed face and split slots. Brim is optional after coupon adhesion testing. Check the full slicer envelope including brim and any prime tower; 280 mm is a design envelope, not a guarantee for every job layout.

## Hardware / assembly

Initial hardware: M2 x 8 mm screws with nominal head diameter no larger than 3.8 mm. Check the actual part drawing; a button head, pan head and socket head may have different dimensions. The screws are intentionally visible.

1. Deburr holes without enlarging them arbitrarily.
2. Test each pilot with a spare screw before assembly. A 1.6 mm pilot is a tuning starting point, not a verified thread standard for every filament.
3. Seat the bridge pegs into the rear pockets of two touching panels.
4. Insert screws from the face. Tighten gently and evenly; stop if the plastic whitens, splits or strips.
5. H bridge: straight two-peg bridge at a horizontal seam.
6. V bridge: offset bridge at a vertical seam, keeping the panels in the same upright orientation.
7. Check the seam under raking light and with a straightedge.

Do not force a tight peg by tightening the screw: adjust registerDiameter/pegDiameter after measurement. Do not scale the entire mesh to fix a screw fit.

## Record results

| Check | Acceptance target / record |
|---|---|
| Printed slot width and height | Measure at face/midsection/back; record actual values |
| IKEA single hook and multi-hook accessory | Insert, drop, seat, remove without damage; record accessory identity |
| Dense adjacent custom hooks | No interference during insertion or after seating |
| Locating pegs | Seat by hand; no cracking; no visible lateral rattle |
| Screw pilots | Tighten without splitting or stripping; inspect after 10 cycles |
| Seam | Target <=0.2 mm face step and <=0.3 mm gap; record measured result |
| Split slot at seam | Actual hook can enter and seat across seam without catching |
| Full 2 x 2 intersection | No forced bending or progressive grid drift |
| Coupon warp | Record corner lift and whether seams can be assembled without stressing them |
| Modest trial load | Begin over a bench; record load, time, deflection and creep rather than inferring a wall load rating |

After fit succeeds, print a 240 mm panel and check flatness before producing a full field. Final wall anchors, trim, edge backing and a validated mosaic hook are subsequent work.

