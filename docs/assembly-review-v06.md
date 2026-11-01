# v0.6 centered M2 prototype

The user selected the middle mounting option on 2026-10-31: retain every slot and move each M2 screw toward the equal-clearance point between three neighboring slot outlines. This supersedes the pending mounting-layout choice in the mounting study. Filament and working-load targets remain unspecified.

## Coupled interface revision

The offset is `(slotHeight-slotWidth)^2/(4*pitch)`, or 1.25 mm for the established 20 mm pitch and 5 x 15 mm slots. All sixteen screw axes move in negative model X, including the right-hand stations; the stagger has the same phase at every station. Native panel bores/countersinks, screw references, captive nuts, nut tracks and integral nut-retaining springs follow the offset parameter. The alignment jig's screw holes follow it too.

The compression blade and registration pads deliberately retain their original axes. Moving the whole blade would obstruct more of the adjacent hook column. The offset 2.4 mm passage opens the left side of the existing 3.2 mm blade, leaving a nominal 1.65 mm spine on the right at the passage center. The complete blade is not a closed sleeve. The remaining front bearing footprint and two registration pads support the board on the original axis; this makes the clamp eccentric by 1.25 mm and needs a physical test. Do not compensate by tightening harder.

Front countersink-to-slot ligament is 1.35 mm, versus 0.10 mm in v0.5. Bore-to-slot-throat ligament is 2.55 mm. These figures do not account for printing errors, countersink variation, or the rear registration recess and are not strength ratings. The 4 mm countersink leaves 4.2 mm axial board thickness below its 0.8 mm deep cut away from other recesses.

## Hook compatibility boundary

The nominal 2 mm screw shank reaches X=7.75 mm at the first station; a continuous 5 mm hook column centered at X=5 ends at X=7.50, leaving only 0.25 mm. The earlier 6 mm provisional envelope reaches X=8 and therefore overlaps the shank by 0.25 mm. Keeping the old 6 mm check is essential: it must report the incompatibility rather than silently shrinking the requirement to obtain a pass.

The 10 mm cavity depth remains. It is not fully unobstructed for every possible hook: the shifted screws constrain local width at mounting stations. Actual IKEA hook samples, their insertion sweep, and printed mosaic clips must be tested next to a mounting station. No universal SKADIS hook compatibility is claimed. Mosaic spring width in the separate v0.5 concept is 5.4 mm; a static width alone does not establish collision-free insertion or spring deformation.

## Assembly and physical sanity check

Completed CAD checks on the 480 x 480 assembly: 143 component occurrences, 850 healthy timeline features, fully constrained sketches; zero static part collisions; zero collisions at seven sampled axial removal positions; 52 frame tool envelopes clear; no front protrusions or parts behind the wall plane. All 1,128 whole hook slots are retained. The 6 mm corridor check reports exactly 16 screw-shank overlaps and no carrier overlaps. See [combined validation](validation-v06.json). This is a conditional geometric result, not an overall compatibility pass.

The delivered native archive was reopened and recomputed with the same healthy feature/sketch counts and 1.25 mm offset. All nine exported STL files (four panels, four carrier seed parts and the jig) passed closed-edge and positive-volume checks. Lower panel bounds are 239.65 x 249.65 x 5 mm, upper panel bounds 239.65 x 239.65 x 5 mm. See [archive verification](archive-validation-v06.json) and [mesh audit](mesh-validation-v06.json). The repeated single-carrier seed exports have different assembly coordinates but the same physical shape. Historical v0.5 tooling and animations are not updated implicitly.

1. Trial actual metal channel nuts in the measured extrusion; confirm bearing, anti-rotation and no screw bottoming. The metal hardware references remain provisional.
2. Load frame nuts and assemble the flush-wall frame with the established front/side tool access.
3. Load M2 nuts into the revised carriers and test integral spring retention outside the frame.
4. Locate carriers with the **v0.6** jig; tighten the M5 carrier fasteners through its access openings. Do not use the old jig or old carriers with revised panels.
5. Fit a panel onto the unchanged rear registration pads. Insert the offset M2 screws from the face and tighten only enough to seat the head flush. Nominal M2 x 20 screw/nut engagement remains unchanged in Z.
6. Test adjacent hooks and mosaic insertion/removal. Inspect the narrow front web and open-sided blade for cracks, whitening or distortion.
7. Test a complete mounting station, then a populated panel, in vertical shear and outward pull. Apply the intended service load and lever arm for a sustained period in the intended environment, measuring creep and checking retention after repeated assembly. Establish a load target and margin before calling the system qualified.

The four-panel 480 mm assembly remains a prototype. Larger wall frames, anchors and loads require their own checks. Existing v0.5 animations and prototype panels are historical and do not show this revision.
