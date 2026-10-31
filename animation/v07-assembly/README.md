# v0.5 features and assembly animation

60-second, silent, captioned product/assembly film using the actual [v0.5 Fusion assembly](../../models/v05/frame-assembly-v05.f3d) and its [prototype parts](../../models/v05/prototypes/README.md). Source CAD commit: `62f24f6`.

Deliverables: [MP4](skadis-v05-assembly.mp4), [poster](poster.jpg), [contact sheet](contact-sheet.jpg), [editable Blender scene](assembly.blend), and [delivery checks](delivery-validation.json).

## Sequence

| Time | Demonstration |
|---|---|
| 0–4 s | Finished 480 mm assembly, 240 mm modules and sample mosaic |
| 4–9 s | Exploded overview of the 143 actual CAD instances |
| 9–13 s | Loading a channel nut through an open vertical rail end |
| 13–18 s | Frame ties, preloaded side nuts, brackets, side screws and flush wall tabs |
| 18–24 s | Shared carrier, M5 fixing, top-loaded M2 nuts and illustrative spring capture |
| 24–29 s | Reusable carrier-positioning jig, temporary screws and M5 driver access |
| 29–37 s | Four panels approach axially from the front; four flush screws retain each |
| 37–40 s | Whole slots, rounded entrances and stepped seams close-up |
| 40–43 s | Side view and dimension ticks for the provisional 10 mm hook cavity |
| 43–47 s | Actual two-pixel tile geometry with illustrative axial snap action |
| 47–50 s | A 288-tile abstract mosaic builds across the panels |
| 50–53 s | Five access tiles are removed; handling keys insert vertically and turn 90° |
| 53–57 s | Four panel screws withdraw; one panel, its remaining artwork and the handle move forward |
| 57–60 s | Finished assembly reveal |

The five cleared tile sites are `(185,190)`, `(225,190)`, `(225,210)`, `(225,230)` and `(235,220)` in CAD millimeters. Two expose the handle slots; three expose the otherwise covered upper-right fastener of the lower-left panel. B-column tiles on the horizontal seam belong to the lower panel and move with it. Neighboring panels remain stationary.

## What the animation does and does not establish

The geometry comes from 49 unique native CAD component meshes and the 143 occurrence transforms, plus exported native jig, mosaic and handling-tool parts. The assembled positions at frames 96, 888 and 1440 and independent panel-service pose are checked by the scene builder. The camera uses explicit cuts and quaternion-based, continuous motion within shots. [Scene checks](scene-validation.json) record the result.

The opening explosion is a parts overview, not an installation trajectory. Hardware is the same provisional reference geometry as the CAD; wall anchors and supplier-specific joints are not qualified by the film. Metallic panel finishes are presentation styling for the intended printed panels.

Spring and snap deformations are illustrative shape keys, not a structural simulation or a verified force/fit result. The handling tool is still a print-test concept. Access-tile removal is shown schematically; a dense-mosaic extraction method remains to be tested. The separate metal compression-clamp study is deliberately not installed in this assembly.

## Reproduction

1. Run `fusion/ExportAnimationV05.py` in Fusion to export the native instances and unique meshes. It leaves the CAD unchanged.
2. Run `prepare.py` with Python/Pillow on Windows to copy the prototype assets and generate the caption overlays. The text and timings are in `shots.json`; Segoe UI is used to rasterize text, without redistributing the font.
3. Run Blender 4.5 with `--background --python-exit-code 1 --python build_scene.py` to rebuild `assembly.blend`.
4. The established Ubuntu container renders with OptiX on the RTX 3080, GPU denoising, 32 samples, 1080p and 24 fps. `run_remote.sh` starts a fresh Blender process every 96 frames and records a completion exit code. Credentials and pinned host keys remain outside the repository.
5. `finish_remote.py` retrieves the frame sequence and runs `encode.py`. Captions are composited before H.264 encoding. The encoder decodes all 1,440 frames and checks dimensions, duration, black frames and isolated within-shot brightness/image discontinuities. Intended shot cuts are excluded from the discontinuity test. Representative decoded frames still require visual review.

The raw frame sequence, intermediate preview frames and logs are excluded from Git. No other rendering project is stopped or modified.
