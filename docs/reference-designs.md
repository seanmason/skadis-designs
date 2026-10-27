# Reference designs

Research date: 2026-10-27. MakerWorld descriptions were opened directly in the browser after the web retrieval tool could not fetch the pages. No model files were downloaded or reused. Creator claims below are reference observations, not independent validation.

| Reference | What the creator provides | Design lesson |
|---|---|---|
| [KAIZEN PEGBOARD Modular System, Pavan](https://makerworld.com/en/models/1750905-kaizen-pegboard-modular-system-skadis-compatible) | Modular panels, printed connectors/fasteners and concealed mounting; 160 and 240 mm panels plus other sizes | Treat panel, connectors and wall support as a system; separate printable parts. Our visible screw treatment intentionally differs. |
| [Any Size Customize Infinite Seamless Skadis Board](https://makerworld.com/en/models/1970526) | Parametric board dimensions, margins and thickness; continuous slot alignment across panels | Derive module dimensions and seam phase from the lattice, not arbitrary margins. |
| [Parametric Ikea Skadis Generator for OpenSCAD, tommusrhodus](https://makerworld.com/en/models/1194912) | Row/column sizing, configurable slot size/pitch and corner holes; small slot chamfer | Keep interface dimensions distinct from panel dimensions; test a small panel before a large one. This project uses native Fusion features instead. |
| [Parametric Ikea Skadis Pegboard, Roland Deschain](https://makerworld.com/en/models/1576279) | Custom sizing and an included Fusion file; mounting hardware is separate | Preserve an editable Fusion master and distinguish pegboard design from wall-mounting design. |

The MakerWorld listings display restrictive standard-file licenses in the research results. We use these as references only and do not redistribute them. Check the current original listing before any future reuse.

## Dimensions and evidence

The working SKADIS interface is **nominal 5 x 15 mm slots, 5 mm panel thickness, two 40 mm square lattices offset 20 mm in X and Y**. These are provisional community-CAD dimensions, not an IKEA manufacturing specification verified in this project. [Community dimensional summary](https://pegboardly.com/skadis/skadis-sizes-and-dimensions) was a discovery aid; physical caliper measurement and actual IKEA hooks remain the acceptance criteria. An additional Printables primary-reference lookup could not be completed because browser access was declined; no content from that lookup was used.

[IKEA buying guide](https://www.ikea.com/ie/en/files/pdf/12/3d/123db3ba/skadis_buying_guide_aug_20.pdf) provides product/system context, not a tolerance-controlled slot drawing.

[Bambu H2D specification sheet](https://cdn1.bambulab.com/documentation/h2d/en/H2D_Laser_Full_Combo_20250305.pdf): single nozzle 325 x 320 x 325 mm; dual-nozzle overlap 300 x 320 x 325 mm; combined two-nozzle volume 350 x 320 x 325 mm. The 350 mm advertised width must not be treated as a single-nozzle width. Our initial maximum 280 x 280 mm leaves room within the overlap envelope; slicing, brim and purge-tower arrangements still need checking.

## Fusion API sources consulted

- [User parameters](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/fusion_UserParameters.htm)
- [Center-to-center slot](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/fusion_Sketch_addCenterToCenterSlot.htm)
- [Rectangular feature patterns](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/RectangularPatternFeatureSample_Sample.htm)
- [Export manager](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ExportManager_Sample.htm)

An implementation detail discovered in this Fusion session: rectangle geometry did not automatically receive horizontal/vertical constraints; slot reference lines needed explicit constraints, and generated slot dimensions needed their expressions explicitly rebound. The build script includes these constraints instead of fixing sketch geometry.

