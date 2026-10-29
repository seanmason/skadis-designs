# Infinite SKADIS HD — product reveal

A 25-second silent, 1280 × 720, 24 fps presentation animation. Warm white panels, champagne-colored caps, graphite rails and a dark blue studio backdrop. The movie rotates the assembled board, separates its 120 modeled components, and returns to the assembled design. Opening and closing shots hold briefly for the titles.

- [Watch or download the MP4](infinite-skadis-reveal.mp4)
- [Opening poster](poster.png) and [decoded video contact sheet](qa-contact-sheet.jpg)
- [Editable Blender scene](reveal.blend) and [native 480 mm Fusion assembly](assembly-480.f3d)
- [Delivery validation](delivery-validation.json)

## Grounding in the CAD

- The source is a **separate native Fusion assembly**, `assembly-480.f3d`, regenerated from v0.3 with `columns=12`, `rows=12`: four nominal 240 mm panels form a 480 × 480 mm installation. Hole pitch, slot geometry, board thickness, frame profile and hardware dimensions are not scaled.
- `manifest.json` records every exported component, its bounds, volume and native model health. `meshes/` contains the actual Fusion tessellations used by the renderer.
- `reveal.blend` is the self-contained editable presentation scene. Fusion remains the engineering source of truth. Materials and lighting are illustrative; fasteners retain the simplified reference envelopes in the CAD, including unmodeled threads and drive recesses.
- The 10 mm hook cavity and 35 mm nominal board-face-to-wall stack are retained. The render floats the assembly away from a studio floor; it is not a wall installation view.
- Explosion paths are **presentation transforms**, not a collision-free installation procedure. Refer to `../../docs/assembly-review-v03.md` for the actual assembly sequence and the unresolved profile fit, hardware capacity and anchoring questions. No mosaic tiles have been invented for this animation.

## Storyboard

| Time | Shot |
|---|---|
| 0–3 s | Finished-board title reveal |
| 3–8 s | Rotation exposes the front, edges and rear frame |
| 8–13 s | Layered separation of caps, panels, locating seats, spacers, fasteners and frame |
| 13–16 s | Exploded assembly turns to show depth |
| 16–21 s | Components return in staggered groups |
| 21–25 s | Finished-board end card |

## Reproduce or edit

1. Run `../../fusion/ExportAnimationV03.py` inside Fusion to regenerate the separate source and 120 STL files. It preserves existing open documents.
2. With Blender 4.5 LTS, run `blender --background --factory-startup --python build_scene.py` from this directory. This creates `reveal.blend` with the editable animation, camera and materials.
3. Run `blender --background reveal.blend --python check_and_render.py` to verify framing throughout the full timeline and the assembled end positions. Add `-- --stills` for representative stills.
4. Run `blender --background reveal.blend --python render_movie.py` for the moving shots. It resumes from existing frames. Opening and closing editorial holds reuse frames 72 and 504, avoiding duplicate rendering.
5. In Python with Pillow, NumPy and `imageio-ffmpeg`, run `finish_movie.py`. It applies the titles, encodes the H.264 MP4, makes a poster/contact sheet, and decodes the delivery to verify all 600 frames. Fonts currently reference Windows Segoe UI; substitute equivalent local font paths on another OS.

The scene uses Cycles CPU rendering with denoising and 12 samples. For a higher-quality render, increase samples and resolution in `build_scene.py` and update the finishing script's dimensions. Generated working frames, logs and temporary Blender backups are ignored by Git; the source scene, geometry, final movie and validation records are retained.

## Geometry and framing checks

`geometry-validation.json` compares all 120 imported mesh volumes to Fusion's analytic body volumes. The largest difference is approximately 0.2073%, caused by tessellation of the small round reference fasteners. Imported coordinates use metres and preserve the CAD dimensions. All parts occupy the same assembled local positions at the editorial opening and closing poses.

`animation-validation.json` checks the projected part bounds throughout all 600 timeline frames: every part stays within the camera's safe border. It does not certify collision-free exploded motion. `delivery-validation.json` is generated after video encoding and records the actual decoded frame count and format.
