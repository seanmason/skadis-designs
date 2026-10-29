# All-metallic product reveal

[Watch the completed 1080p movie](infinite-skadis-metallic.mp4) · [Decoded contact sheet](contact-sheet.jpg) · [Delivery validation](delivery-validation.json)

Completed delivery: 35 seconds, 840 decoded frames, 24 fps, 1920 × 1080. All frames rendered successfully; the interrupted packaging step was rerun and the decoded contact sheet visually reviewed. FFmpeg progress now goes directly to a log file to avoid PowerShell stderr handling during future encodes.

The approved 35-second, text-free whirlwind animation with metallic teal, blue, bronze, copper and gunmetal panels. There are no white panel finishes. Metallic appearances are illustrative finishes for the printed designs.

The assembly and motion come from `../v04-review/review.blend`: 24 nominal 120 mm panels, 720 × 480 mm overall, 362 components. Existing CAD provenance and limitations in the review README still apply; this does not certify the expanded layout as a native Fusion assembly.

Rendering uses Cycles CPU, 24 threads on the upgraded VM, 1920 × 1080, 24 fps, 840 frames, 32 samples with adaptive sampling and denoising, and a quarter-frame motion-blur shutter. Exposure is reduced by 0.7 stops to retain metallic color. The review's linear animation keys are retimed to 24 fps without changing choreography.

Run `prepare.py` in Blender with the review scene loaded to regenerate `metallic.blend` and two representative full-resolution stills. Run `run.ps1` to render missing frames and then encode and decode-check `infinite-skadis-metallic.mp4`. Encoding requires Pillow and imageio-ffmpeg. Working frames are ignored by Git. `render-progress.json` records completed frames. `delivery-validation.json` and `contact-sheet.jpg` are created only after successful encoding and decoding. A final visual review is separate from that automated check.

The render is resumable. Use a new frames folder after scene changes to avoid mixing renders. Source scripts and stills are retained in the repository; the completed video and delivery records should be committed after visual review.
