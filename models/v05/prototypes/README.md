# v0.5 prototype library

These are editable native Fusion models. Matching STEP, STL and preview PNG files share each model's filename prefix. Read the [assembly and test notes](../../../docs/assembly-review-v05.md) before printing. Physical fit and load capacity are unverified.

| Purpose | Native Fusion model |
|---|---|
| 240 mm whole-slot interior panel | [240 mm](panel-interior-240-gap-0.35.f3d) |
| Larger comparison panel | [280 mm](panel-interior-280-gap-0.35.f3d) |
| Finished perimeter variants | [Left](panel-left-edge-240-gap-0.35.f3d), [right](panel-right-edge-240-gap-0.35.f3d), [bottom](panel-bottom-edge-240-gap-0.35.f3d), [top](panel-top-edge-240-gap-0.35.f3d), [standalone](panel-standalone-240-gap-0.35.f3d) |
| Fully surrounded 80 mm seam coupons | [0.20 mm gap](seam-array-3x3-gap-0.2.f3d), [0.35 mm](seam-array-3x3-gap-0.35.f3d), [0.50 mm](seam-array-3x3-gap-0.5.f3d) |
| Carrier positioning and M5 access | [240 mm alignment jig](carrier-jig-240.f3d) |
| Two-pixel axial retention trial | [Tile and slot coupon](axial-mosaic-tile.f3d) |
| Three-pixel straight-edge terminals | [Top](axial-mosaic-tile-top-terminal.f3d), [bottom](axial-mosaic-tile-bottom-terminal.f3d) |
| Front panel handling concept | [Two-slot quarter-turn tool](panel-handling-tool-concept.f3d) |
| Controlled carrier compression study | [Metal sleeve and washer study](metal-clamp-study.f3d) |

For a seam array, print nine copies of its individual coupon STL, not the assembled STEP as a fused object. Native occurrence patterns position the nine coupons; the one exported coupon mesh is intentionally reused.

For mosaic printing, import the core and COLOR pixel regions as one registered multipart object, using compatible materials. Their mating faces are intended to fuse during printing. They are not detachable caps. Print the separate fit coupon as a separate object. Terminal variants have three pixels to fill a straight outer border; rounded artwork corners still require development.

Parts labeled METAL, CUSTOM METAL or REFERENCE are hardware/study geometry, not instructions to print hardware in plastic. The handling tool requires two M2×6 screws; its printed pilots and bearing tabs need physical tests. The clamp study requires actual metal parts and a tolerance/torque assessment, and is not installed in the main assembly.

STL exports retain model coordinates. Center ordinary individual parts on the build plate; preserve the shared coordinates of mosaic color regions. The 240 and 280 mm interior panel envelopes are approximately 239.65×249.65×5 and 279.65×289.65×5 mm respectively.
