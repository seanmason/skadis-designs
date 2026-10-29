# Continuous camera correction

Corrects defects in the v0.4 metallic video while retaining the assembly, materials, part motion, duration, resolution and sample settings.

The original camera's Euler angles wrapped across the ±pi boundary. Interpolation between opposite representations turned the camera away from the assembly on frames 260 and 462; motion blur smeared frames 259/261 and 461/463. An all-frame brightness scan detected both black frames. The original framing correction also applied discrete 8% distance changes, creating visible camera shifts near frames 312–313 and 342–343. These defects were missed by the previous sparse contact-sheet review.

`fix_camera.py` loads the v0.4 metallic scene, unwraps the camera orientation continuously, smooths camera distance over time, and adds a 4% distance margin. All 840 frames are checked against the bounds of all 362 components. The measured minimum border is 7.2%; maximum orientation step is 0.00703 radians instead of approximately pi. Sixteen regression frames are rendered around the failures at half resolution before starting a full render.

`run.ps1` renders the corrected scene to a separate directory, then encodes `infinite-skadis-smooth.mp4`. Encoding decodes all 840 frames and rejects black frames or large isolated brightness changes before publishing the final filename. This is stronger temporal validation than the previous spot checks; visual review of the final motion is still required. Earlier videos and frames are preserved.

Reproduction: run `fix_camera.py` in Blender with `../v04-metallic/metallic.blend` loaded, then run `run.ps1`. See `camera-validation.json` for measured camera checks. The engineering limitations of the v0.4 presentation assembly remain unchanged.
