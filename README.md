# Infinite SKADIS HD

An original Autodesk Fusion parametric pegboard system for a future pixel-art installation, printed on a Bambu Lab H2D.

**Status: v0.1 engineering / fit-test prototype. CAD validation is not physical validation.** No installation load rating, print-fit result, or universal IKEA accessory compatibility is claimed.

## Current design

- Dense staggered slots: 20 mm repeat, second lattice offset 10 mm in X and Y; nominal 5 x 15 mm obrounds.
- Four times the slot density of the assumed standard staggered 40 mm lattice, preserving a standard-spaced subset.
- Panel dimensions in 40 mm increments, from 80 mm to 280 mm for the initially checked H2D range.
- Straight butt seams; alternate slots split at horizontal seams and become complete when assembled.
- Exposed M2 socket-head screws in a deliberate 40 mm seam rhythm, with printed locating bridges behind the board.
- Intended future mosaic: vertical dominoes with two 10 mm square pixels per hook. Tiles are not modeled yet.

## Files

- [Design decisions and limitations](docs/design-brief.md)
- [MakerWorld research](docs/reference-designs.md)
- [Printing and fit-test protocol](docs/print-and-test.md)
- [Native Fusion master](models/infinite-skadis-hd-v01.f3d)
- [Four-panel coupon assembly](models/coupon-assembly-2x2-fixed80.f3d) — fixed 80 mm layout, with nominal hardware references; resize the master instead.
- [Assembly front preview](previews/assembly-front.png) and [rear preview](previews/assembly-rear.png)
- [Fusion build script](fusion/InfiniteSkadis.py)
- [User parameters](fusion/parameters.csv)
- [CAD validation results](docs/cad-validation.json)
- [Model exports](models/)

Open the F3D in Fusion and edit **Modify > Change Parameters**. Change `columns` and `rows` to even integers; each unit is 20 mm. Keep `pitch=20 mm` for the intended lattice and bridge alignment. Do not scale STL files to change panel size.

The Python script runs **inside Fusion**, creates a new document, and leaves existing documents untouched. The F3D is the editable CAD master; STEP and STL are derived exports. Do not edit exported meshes as the source of truth.

Reference models were researched but no third-party meshes, CAD, or source code were incorporated. No project redistribution license has been selected yet.
