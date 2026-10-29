# Infinite SKADIS HD

An original Autodesk Fusion parametric pegboard system for a future pixel-art installation, printed on a Bambu Lab H2D.

**Status: v0.4 flush-screw CAD prototype. CAD validation is not physical validation.** No installation load rating, print-fit result, or universal IKEA accessory compatibility is claimed.

## v0.4 clean-face revision

- [Assembly sequence, hardware and prototype limitations](docs/assembly-review-v04.md)
- [Native Fusion assembly](models/v04/frame-assembly-v04.f3d), [STEP](models/v04/frame-assembly-v04.step), and [printable prototype parts](models/v04/)
- [Front](models/v04/front.png) and [rear](models/v04/rear.png) previews
- [Parametric generator](fusion/FrameSystemV04.py) and [geometric validation](docs/validation-v04.json)
- [Native interior, edge and standalone panel library](models/v04/panels/), [80 mm clearance checks](docs/validation-v04-80.json), [resize checks](docs/resize-validation-v04.json) and [mesh checks](docs/mesh-validation-v04.json)

Four small flush M2 heads retain each panel independently. Integrated support blades and captive metal nuts replace the large front caps, restoring the mounting-node slots. Shared rear carriers register vertical seams and bolt to the extrusion with recessed M5 fixings. The 10 mm provisional hook cavity is preserved; the revised carrier stack gives a 42 mm face-to-wall distance with the extrusion rear against the wall. This supersedes the earlier v0.4 clearance-only study.

## Product-reveal animation

[Animation source and production notes](animation/v03-reveal/README.md) for a 480 × 480 mm parameterization: four 240 mm panels and 120 actual CAD components, presented with rotation, an exploded view and reassembly. Includes a separate native Fusion assembly and an editable Blender scene; materials and exploded paths are illustrative.

[Watch the 25-second MP4](animation/v03-reveal/infinite-skadis-reveal.mp4) · [Poster](animation/v03-reveal/poster.png) · [Editable Blender scene](animation/v03-reveal/reveal.blend)

## v0.3 flush-wall revision

- [Assembly review, measured profile, hardware cautions and installation sequence](docs/assembly-review-v03.md)
- [Parametric Fusion generator](fusion/FrameSystemV03.py)
- [Native Fusion assembly](models/v03/frame-assembly-v03.f3d) and [assembly STEP](models/v03/frame-assembly-v03.step)
- [Panel library, printable parts and metal reference parts](models/v03/)
- [Bare frame](previews/v03-bare-frame.png), [front](previews/v03-front.png), [rear](previews/v03-rear.png) and [side](previews/v03-side.png) previews
- [120 mm clearance checks](docs/validation-v03.json), [80 mm clearance checks](docs/validation-v03-80.json) and [native resize checks](docs/resize-validation-v03.json)

This revision removes the designed gap behind the extrusion, keeps the provisional 10 mm hook cavity, and replaces rear bridges with shared locating seats so panels can withdraw forward independently. Side-mounted metal angles and wall tabs are accessible through the open frame bays. The extrusion approximation uses the user's updated measurements, including its narrowing inner cavity. Metal nut fit remains unverified; the failed rectangular carriers from the separate purifier project are not used as structural hardware.

## Archived v0.2 frame-mounted system

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
