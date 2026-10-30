# Frame grid recommendation — 2026-10-29

Design recommendation for the next revision, not an implemented or load-rated frame.

## Preferred starting layout

| Element | Nominal dimension |
| --- | --- |
| Printed panel pitch | 240 × 240 mm |
| Current panel body with 0.2 mm seam allowance | 239.8 × 239.8 mm |
| Interior vertical extrusion center spacing | 240 mm |
| Horizontal crossmember center spacing | 480 mm, every second panel row |
| Planning/assembly block | 960 × 960 mm, four panels each way |
| Nominal near-20 × 8 ft example | 6000 × 2400 mm, 25 × 10 panels |

This is a proposed structural layout for physical testing. Crossmember spacing is not an allowable unsupported span or a wall-anchor schedule. Wall attachment positions must suit the real substrate, loads and chosen joints.

## Printer and panel-size tradeoff

Bambu's H2D specification gives 325 × 320 mm single-nozzle XY capacity and 300 × 320 mm dual-nozzle XY capacity. The advertised 350 mm total width is the combined reach of the two nozzles, not a universal single-nozzle part envelope. Source: [Bambu H2D specification sheet](https://csm.bblcdn.com/hub/default/afc8b81112794109ab591822bb6f7152.pdf).

The 240 mm pitch preserves the 20 mm lattice, gives generous room for a brim and bed placement, and makes replacement prints smaller than a near-bed-sized panel. At identical thickness and support layout, a larger panel is generally more demanding for flatness and stiffness; no quantitative stiffness result is claimed here. A 280 mm panel is a useful optional size and already passed native CAD regeneration, but has not been physically validated. A 320 mm square leaves almost no depth margin and exceeds dual-nozzle width. A 300 mm size would also require extending the current even-cell parameter convention and validating it; it is not the recommended default.

Keep color changes between separately printed panels where practical. Fitting a part within the printer's nominal XY envelope does not also guarantee space for a purge tower or all slicer exclusion regions. Check the actual H2D plate/profile before release.

For the 6000 × 2400 mm example, 240 mm modules give 250 panels instead of 1000 at 120 mm. Four panel screws each would mean 1000 visible small screw heads across that whole installation; the two sizes cover the same area, so larger panels primarily reduce seams, assembly labor and per-panel hardware, not plastic area.

## Frame construction

Use continuous vertical rails where practical and horizontal crossmembers between them, all in the existing 20 mm-deep extrusion plane. Preserve the 10 mm hook cavity and 42 mm face-to-wall stack. Interior crossmember clear span is nominally 220 mm between rails on 240 mm centers; this is a geometric starting dimension, not a released saw-cut list. Edge rails are currently inset 10 mm from the panel perimeter, so end bays differ. Joint clearance and supplier tolerances also need a cut allowance.

The 960 mm block is a planning and erection module, not four separate perimeter frames automatically repeated. Adjacent blocks should share boundary rails. Splice details must preserve slot access and allow assembly without reaching behind the wall-mounted frame. If independent boxed cassettes are preferred later, account explicitly for doubled rails and the different carriers at their boundaries.

Horizontal members brace the frame but do not directly brace the printed panel face without a corresponding support. Start with the four existing panel screws and evaluate a narrow, non-fastened midpoint support on each vertical panel edge. Such supports must occupy the continuous solid corridors between hook columns and retain straight-forward panel removal. They would reduce inward edge movement without adding front screw heads; they do not prevent outward bowing or directly support the panel center.

Add crossmembers only at selected panel seams, initially every second row. Keep wall attachment positions independent of that pitch so anchors can engage suitable wall structure. Consider side-mounted wall tabs on horizontal rails for adjustable horizontal anchor positioning. Recheck bracket access, channel-nut loading, carrier clearance and splices in CAD before adopting this revision.

## First physical trial

Build a 480 × 480 mm, 2×2 array using 240 mm panels. Evaluate flatness after cooling, face movement during hook insertion, seam alignment, screw seating and individual panel removal. Test with representative hooks and mosaic loading. Use slicer mass estimates for panels and tiles, plus measured frame/hardware mass, before planning the full wall's anchors. Select intermediate crossmember/anchor spacing and any stronger perimeter rails from those results and the actual wall conditions.

No CAD changes were made by this recommendation. The v0.4 assembly remains the verified 120 mm demonstrator.
