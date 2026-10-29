# Infinite SKADIS HD — motion review draft

A silent, text-free 35-second CPU preview at 640 × 360 and 12 fps. This draft reviews the proposed larger assembly, panel colors and whirlwind choreography before a full-quality render.

- [Review movie](infinite-skadis-motion-review.mp4)
- [Assembled](assembled.png), [exploded](exploded.png), [whirlwind](whirlwind.png)
- [Decoded contact sheet](review-contact-sheet.jpg)
- [Editable scene](review.blend)

## Proposed configuration

Six columns and four rows of nominal 120 mm panels form a 720 × 480 mm assembly. There are **362 modeled components**: 24 panels, 175 node parts (35 nodes × 5), 19 rails/ties, 120 corner-joint parts (24 × 5), and 24 wall-tab parts (4 × 6).

Panel appearances alternate deep teal, midnight blue, warm ivory, copper and satin aluminum. Caps retain champagne coloring and rails graphite. Metallic appearances are illustrative finishes, not a change to the printed panel construction.

The panels use the existing v0.3 120 mm Fusion-exported corner, edge and interior meshes. Hardware and vertical rails reuse the actual v0.3 reveal meshes. Horizontal ties retain the same constant cross-section with cut lengths adjusted to 88 mm in the outer bays and 100 mm in the inner bays. No holes or hardware are scaled. The 10 mm provisional hook cavity and 35 mm face-to-wall stack are retained.

This expanded layout is assembled in Blender for quick review; it has not yet been regenerated and engineering-validated as a complete native Fusion assembly. Fusion remains the engineering source. The underlying profile approximations and physical fit/load cautions still apply. No mosaic tiles are included.

## Choreography

| Seconds | Motion |
|---|---|
| 0–5 | Finished assembly rotates |
| 5–10 | Layered explosion |
| 10–14 | Camera sweep around separated parts |
| 14–23 | Parts blend into a rotating spiral with individual rotation |
| 23–30 | Spiral sweeps back into the rotating assembly |
| 30–35 | Finished assembly settles into the final view |

Paths are presentation motion, not a collision-free installation sequence. All 420 frames are checked for camera containment; the final component positions and rotations are verified against the assembled pose. Two samples and denoising keep the review fast but can soften holes, wash out material differences and cause temporal noise. These are not final render settings.

## Reproduction

1. `blender --background ../v03-reveal/reveal.blend --python build_review.py`
2. `blender --background review.blend --python render_review.py`
3. `python encode_review.py` (requires Pillow and imageio-ffmpeg)

Run from this directory. The scene is self-contained after building; source paths are resolved relative to the script. Rendering resumes from existing frames, so clear or relocate working frames before rendering a changed scene. Encoding verifies the decoded frame count, duration, dimensions and frame rate. Working frames/logs are ignored by Git.
