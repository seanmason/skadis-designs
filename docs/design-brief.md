# Pegboard v0.1 design brief

## Agreed direction

Use Fusion 360, keep findings and models in seanmason/skadis-designs, print on a Bambu Lab H2D, support differently sized interlocking panels, maintain a clean face, preserve an IKEA-compatible subset, and double the linear hole density. Screws are acceptable and should be a visible design element. Mosaic tiles will be a later phase.

## Geometry

Coordinates are in millimeters. The panel face is Z=0; the back is Z=5.

With P=20, the dense slot centers are:

- A: (P/4 + iP, P/2 + jP)
- B: (3P/4 + iP, jP)

The panel width is columns*P and height is rows*P. Columns and rows are even integers, initially checked from 4 to 14. Full nominal slot width/height are retained. The A family alone contains both (5+40i,10+40j) and (25+40i,30+40j), an original-spaced pair of staggered lattices after translation. This establishes center-position compatibility mathematically; it does not prove every physical hook fits.

Standard density is 2/1600 holes/mm2. Proposed density is 2/400 holes/mm2, four times as large. A 240 x 240 panel therefore has 288 complete-hole equivalents, including half slots at the top/bottom.

**Horizontal seams split B slots.** A straight seam cannot sit between every 15 mm tall slot when the interleaved rows are 10 mm apart. This is intentional, not a CAD defect. Adjacent halves make full slots. Keep every panel in the same orientation; do not rotate individual panels 90 degrees or mirror them.

Current outer top/bottom edges contain half slots. Finished exterior trim/end treatment remains to be designed. Do not describe v0.1 as a finished standalone edge treatment.

## Connections and appearance

A 40 mm rhythm places pairs of exposed M2 socket-head screws along seams. Intended finish: uniform black screws against a lighter board, or stainless screws against a dark board. Hardware color is an aesthetic choice, not a modeled requirement.

Each screw passes through a 2.2 mm board hole into a blind 1.6 mm pilot in a printed rear bridge. Use M2 x 8 mm as the initial candidate. A nominal 3.2 mm locating peg on the bridge fits a 3.6 mm diameter, 0.8 mm deep rear recess; peg height is 0.6 mm. The intended 0.2 mm radial/axial clearances must be tested on the actual printer/material.

The straight H bridge connects horizontal seams. The offset V bridge follows the staggered grid across vertical seams. Their 4.4 mm widths fit the nominal 5 mm material corridors. Bridges are 6 mm thick; screw pilot depth is 4 mm. The geometric maximum rear projection is therefore 11 mm from the face.

Positive peg engagement locates panels and transfers in-plane shear; screws clamp the bridges to resist separation and face stepping. No elastic latch is required. Screw threads in printed plastic limit repeated assembly life; use finger torque and assess wear before committing to a full installation. Metal inserts are a possible later revision, but do not fit the present narrow bridge without redesign.

No strength or durability claim has been validated by print tests. The denser slots leave 5 mm webs within a column and narrow corridors between columns. Rear registers reduce the local section further. This is a light mosaic prototype, not a heavy-tool storage rating.

A nominal 3.8 mm diameter M2 socket head can fit in the 5 mm corridors. Verify the actual screw head dimensions before ordering a quantity. Do not substitute M3 heads without redesign. Corner/seam fastener pairs are deliberately offset to fit the staggered lattice.

## Future mosaic interface

Proposed pixel pitch: 10 mm. One vertical 10 x 20 mm nominal domino carries two square pixels and one hook. Alternating columns are vertically offset by 10 mm, still forming a uniform 10 mm pixel grid. A 240 mm square region corresponds to 24 x 24 pixels.

Tile face gaps, neck thickness, insertion/drop travel, anti-rotation, removal tool access and color manufacturing are not finalized. Reserve at least 3 mm between the pegboard face and the back of tile artwork as an initial clearance allowance for exposed screw heads; verify real hardware and insertion movement. Dense hooks may collide behind the board even when slot centers fit, so neighboring tile insertion must be tested.

## Parametric modeling practice

- Dedicated components for panel and connector types.
- Origin-based, dimensioned and fully constrained sketches.
- User parameters and expressions control envelope, slot seeds, cuts and feature patterns.
- Feature patterns replicate cuts instead of drawing hundreds of independent slots.
- Construction planes reference the origin and board thickness, avoiding fragile face dependencies.
- Named timeline features and no mesh-based source geometry.
- Regeneration checked at 80 x 80, 160 x 240, 280 x 280 and restored 240 x 240.
- Inspect docs/cad-validation.json for the actual CAD run result.

Only even columns/rows 4..14 and pitch 20 mm are supported for v0.1. Other parameter combinations may evaluate in Fusion but are not approved configurations. Thickness/slot changes require renewed hook-fit and connector checks.

## Remaining work after first prints

1. Validate actual IKEA hook fit, including multi-hook accessories, and adjacent custom hooks.
2. Tune pilots/registration clearance for material and real screws.
3. Validate two-axis assembly, seam flushness, stiffness and repeated assembly.
4. Add final perimeter trim, terminal screw backing and wall mounts.
5. Validate distributed wall support and mounting clearance. Use 15 mm clear space behind the board as a starting packaging target, not a tested wall-mount design.
6. Develop mosaic hook/anti-rotation and removal interface, then artwork.

Interlocks do not replace wall anchors. An arbitrarily large tiled field needs distributed support, thermal/movement allowance and a mounting design. Wall mounting is not included in this prototype.

