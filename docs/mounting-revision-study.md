# Mounting revision decision and CAD comparison

2026-10-31. This study identifies a real weakness in v0.5; it is not a released replacement assembly or a load rating.

The 4 mm countersink in the current panel has only 0.10 mm of front-face material to the neighboring rounded slot entrance. The 2.4 mm bore has 1.30 mm to that slot's 5 mm throat. Moving vertically to the visual column midpoint does not fix the narrow web.

For the 20 mm pitch, 10 mm stagger, 5 x 15 mm throat and 0.4 mm entrance radius, the largest inter-slot circle at a current screw row is centered 1.25 mm toward the column whose two rounded ends straddle the screw. Example: (10,20) becomes (8.75,20) mm. The slot-centerline distance is 6.25 mm to all three neighboring segments. Therefore the front-face ligament is 6.25 - 2.5 - 0.4 - 2 = 1.35 mm, and bore-to-throat ligament is 6.25 - 2.5 - 1.2 = 2.55 mm. These are nominal geometric distances, not print tolerances or strengths.

The offset is coupled to the complete interface. Shifting the original 3.2 mm compression blade would intrude into the prior conservative 6 mm continuous hook corridor; even the nominal M2 shank at X=8.75 reaches X=7.75, whereas that corridor ends at X=8. A clean front view alone therefore cannot qualify a simple whole-carrier translation. Carrier support, hook insertion sweep, nut position and jig must be reconsidered together.

A more substantial option replaces four individual hook slots per panel with solid mounting lands and flush M3 screws. The comparison uses a 6.2 mm seat and 3.4 mm bore centered at the omitted slot. At an interior land, the nearest retained entrance is sqrt(10^2+5^2)-2.5-0.4-3.1 = 5.18 mm from the seat perimeter. The underlying bore ligament is 6.98 mm and 3.6 mm of the 5 mm plate remains below the countersink. This is not a 5.18/1.35 strength multiplier. Final edge placement must preserve edge distances, follow the stagger, and align redesigned carriers.

## Native study

[Open Fusion comparison](../models/mounting-study/mounting-comparison.f3d). It contains three 60 x 60 x 5 mm coupons with native, fully constrained sketches. [Front view](../models/mounting-study/comparison.png) shows **left: M3 solid land; middle: centered M2; right: original M2**, because the front-facing CAD camera reverses model X. Separate STL files are provided for comparative prints. The model has 156 healthy timeline features. The main v0.5 assembly, its prototypes and its animation have not been silently changed.

## Pending requirements

Update 2026-10-31: the user selected the centered M2 (middle) option. See [v0.6 implementation and checks](assembly-review-v06.md). The following paragraph records the earlier decision state; filament and service load remain pending.

The user has been asked whether to preserve every slot or accept four solid M3 mounting lands, and for the load target and intended filament. No answer has been received at the time of this study. These choices affect the full assembly and purchase specification.

No allowable load is asserted. Strength qualification needs actual filament/print orientation and settings, screw-head measurements and preload, panel dead weight, accessory weight and lever arm, sustained creep duration/temperature, and tests of panel bearing/pull-through, registration pads, carriers, nuts and wall anchorage. A suitable next specimen is a complete mounting station loaded in vertical shear and outward pull, followed by a populated panel test; a flat coupon alone cannot qualify the complete load path.
