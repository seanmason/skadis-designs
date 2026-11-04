# v0.6.1 hook and snug-fit revision

Supersedes the v0.6 fit kit for the next physical trial. Open fit-kit-v061.f3d in Fusion for editable native features, or fit-kit-plate.3mf as unsliced geometry. See mk4s-print-record.md for the latest slicing and launch status. The full 480 mm v0.6 assembly remains the historical baseline pending this fit trial.

## Changes

- Replaced the axial snap springs with a rigid downward drop hook, 3.2 mm wide with a 2 mm rear toe and 0.2 mm clearance behind the 5 mm board.
- Insert from the front while raised 3.5 mm, push the backing against the face, then lower. Lift 3.5 mm before pulling forward to remove. Install each column bottom upward; remove top downward. To replace an interior tile, remove the tiles above it first. Leave at least 3.5 mm headroom above the top artwork tile.
- Backing increased from 0.8 to 1.2 mm. Pixel spacing remains 10 mm, with 0.4 mm visible gaps.
- registerClearance reduced from 0.20 to 0.05 mm per side. Socket width/length now 2.9 x 8.1 mm around the unchanged 2.8 x 8 mm carrier pad envelope. The M2 screw still retains the board.
- seamGap reduced from 0.35 to 0.15 mm. This is the nominal edge separation, not a per-side allowance.

## Fit targets

The desired result is snug seating with light friction and hand removal. Positive nominal clearance does not guarantee friction; actual extrusion width, first-layer expansion and support cleanup determine the printed fit. Test this kit before changing the full panel array. If the carrier socket remains loose, try registerClearance = 0 mm in the fit kit; if tight, try 0.10 mm. Avoid imposing interference along the entire panel seam, which can accumulate and bind across a large wall.

The hook removes the inaccessible latch. It does not positively lock against upward lifting and should be tested for rattle, accidental lift-off, and finger grip with neighboring tiles installed. Gravity may settle it slightly below its nominal CAD position within the rounded slot. This is an artwork-tile prototype, not a load-bearing hook.

## Printing and checks

Five objects: mounting coupon, seam mate, unchanged carrier, two new hook tiles. The generic 3MF is unsliced. The previous v0.6 G-code prints the old snap tiles and must not be reused for this revision. Inspect support beneath the carrier and beneath the hook toe; remove it carefully before evaluating fit. The current plate side-orients the tiles, allowing bed-only support under the hooks; inspect and remove those supports before testing.

Fusion reports 133 healthy timeline features and fully constrained sketches. All four exported STL meshes have closed edges. The CAD check sampled 164 board/neighbor collision tests along straight insertion and lowering, with no collisions, and confirmed that a straight pull is blocked while seated. Carrier/board and seam have no nominal solid overlap. This is a sampled geometric check, not a physical fit or strength test.

First test the two board pieces and carrier fit, then one hook tile, then a second tile in the same column. Record insertion force, wobble, lifting grip, support cleanup, and whether the top-down removal order is acceptable.

