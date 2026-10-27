# Infinite SKADIS HD

An original Autodesk Fusion parametric pegboard system for a future pixel-art installation, printed on a Bambu Lab H2D.

**Status: v0.2 frame-mounted CAD prototype. CAD validation is not physical validation.** No installation load rating, print-fit result, or universal IKEA accessory compatibility is claimed.

## v0.2 frame-mounted system

- [Native parametric Fusion assembly](models/v02/frame-assembly-v02.f3d): four panels, removable registration keys, nine visible shared mounting nodes and recessed 2020 frame.
- [Design, parameters, hardware and assembly notes](docs/cad-v02.md)
- [Front view](previews/v02-front.png) and [rear view](previews/v02-rear.png)
- [Printable part and CAD exports](models/v02/)
- [Interior panel native master](models/v02/panel-interior-v02.f3d), plus left/right/top/bottom edge and standalone native variants in the same folder.
- [Assembly generator](fusion/FrameSystemV02.py), [frame joining plates](fusion/CompleteFrameV02.py), and [wall interfaces](fusion/WallBracketsV02.py)
- [Panel configuration generator](fusion/BuildPanelLibraryV02.py): independently choose internal/finished sides; resize generated native CAD with `columns` and `rows`.

This revision adds rounded slot entrances, complete-slot finished borders, rounded exterior corners, rear alignment keys, fewer visible mounting screws, and the agreed provisional 10 mm hook cavity. The assembly starts with 120 mm modules for prototyping. Hardware and extrusion bodies are nominal interface references; match them to the selected supplier before fabrication. Mosaic tiles are not modeled yet.

## Archived v0.1 design

- Dense staggered slots: 20 mm repeat, second lattice offset 10 mm in X and Y; nominal 5 x 15 mm obrounds.
- Four times the slot density of the assumed standard staggered 40 mm lattice, preserving a standard-spaced subset.
- Panel dimensions in 40 mm increments, from 80 mm to 280 mm for the initially checked H2D range.
- Straight butt seams; alternate slots split at horizontal seams and become complete when assembled.
- Exposed M2 socket-head screws in a deliberate 40 mm seam rhythm, with printed locating bridges behind the board.
- Intended future mosaic: vertical dominoes with two 10 mm square pixels per hook. Tiles are not modeled yet.

## Files

- [Original finished-edge and extrusion-frame proposal](docs/frame-architecture-v02.md) — historical design rationale; see the v0.2 CAD notes for implemented details.
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

For either revision, open the F3D in Fusion and edit **Modify > Change Parameters**. Change `columns` and `rows` to even integers; each unit is 20 mm. Keep `pitch=20 mm` for the intended lattice and connector alignment. Do not scale STL files to change panel size. Read the revision-specific notes before changing edge configurations.

The Python script runs **inside Fusion**, creates a new document, and leaves existing documents untouched. The F3D is the editable CAD master; STEP and STL are derived exports. Do not edit exported meshes as the source of truth.

Reference models were researched but no third-party meshes, CAD, or source code were incorporated. No project redistribution license has been selected yet.
