# MK4S fit-kit print preparation — 2026-11-02

- PrusaSlicer 2.9.6; Original Prusa MK4S MMU3, standard 0.4 mm nozzle profile.
- User-loaded black Bambu PLA Basic in MMU slot 1. Generic PLA @MK4S is the slicing base; no Bambu-specific calibration is claimed.
- 0.20 mm STRUCTURAL, four perimeters, four top/bottom layers, 20% infill.
- Automatic supports from build plate only, 0.20 mm contact gap; all model/support extrusion assigned to slot 1 (T0). No wipe tower.
- Five pieces: mounting coupon, seam mate, single carrier, two mosaic tiles. Original CAD geometry and plate orientations retained.
- GUI slice estimate: 55 minutes, 14.09 g. CLI G-code estimate: 54m48s, 14.08 g.
- Configured project: skadis-fit-mk4s-04.3mf; settings: mk4s-04.ini; standalone G-code: skadis-fit-mk4s-04-slot1.gcode.
- Slice preview reviewed; support generation enabled for the carrier rear face. Physical cleanup and spring/slot fit remain experimental.

## Status

Prepared, not started. Prusa Connect reports the MK4S idle but configured for a 0.6 mm high-flow nozzle, conflicting with the installed 0.4 mm nozzle reported by the user. Requested that the printer hardware setting be updated before launch. No successful upload/start is claimed.
