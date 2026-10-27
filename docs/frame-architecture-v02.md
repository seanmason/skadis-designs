# Wall-supported extrusion frame: v0.2 proposal

Recorded 2026-10-27. This is a design proposal and requirements update, not a revised CAD model or a structural load rating. The exported v0.1 models remain unchanged.

## Requirements carried forward

- Reduce the excessive v0.1 screw-hole count; place visible fasteners intentionally.
- Add positive panel edge registration instead of relying solely on rear bridges.
- Add parameterized slot-entry rounding while preserving a defined minimum slot throat and hook-bearing section.
- Configure each side as Internal or Finished. Finished edges suppress intersected slots, have a continuous border and rounded exposed corners/edges.
- Preserve complete dense-lattice spacing across internal seams, including split slots where needed. Do not move the entire grid to solve an outside-edge condition.
- Add optional mounting to a wall-supported 2020 extrusion grid. The possible ultimate installation is roughly 20 ft x 8 ft (6096 x 2438.4 mm).
- Preserve as many usable mosaic/hook positions as practical, including above rails.

## Recommended architecture to prototype

Separate the jobs: metal frame and wall fixings carry the installation; each panel is supported directly; panel-to-panel keys register the faces and resist local shear. The artwork should not hang through a long chain of printed edge connectors.

Use 240 mm nominal panel module pitch for a first prototype, vertical 2020 rails behind every vertical panel seam, and horizontal ties nominally every 480 mm. Horizontal ties fit between continuous vertical rails, keeping the front faces of both rail directions coplanar. Keep joining hardware behind or beside that front datum where possible. Frame joints, wall anchors and panel mounts are separate interfaces.

This 240 x 480 mm frame grid is a prototype geometry, not an approved structural support spacing. Wall-anchor spacing must be determined independently from the wall construction, rail profile, joint design and full loads. Larger profiles (2040 or 4040) are options for primary members or unavoidable long unsupported spans. Orient the deep dimension of a rectangular profile to resist the relevant bending direction. A large wall made of short supported bays is different from a 6 m unsupported beam.

Mount the pegboard approximately 10 mm forward of the nearest frame/bracket obstruction, measured from the panel BACK. The user selected this provisional hook-clearance value on 2026-10-27, replacing the initial 20 mm proposal. Physical testing is deferred; this is not a verified minimum or a universal SKADIS clearance. Check both seated hooks and the full insertion/tilt/drop/removal envelope. A rail can lie behind a slot in front elevation without making that slot unusable if it is outside the hook envelope.

Depth budget for a coplanar 2020 grid: 5 mm panel + 10 mm clear hook cavity + 20 mm extrusion = 35 mm from the board face to the back of the extrusion. Add wall levelling/anchor clearance and the mosaic stand-off/face thickness separately. Brackets or bolt heads projecting in front of the extrusion reduce the cavity and must be included in the clearance model.

## Visible shared mounting nodes

Prototype one decorative front clamp/rosette at each four-panel intersection, bolted through a metal compression spacer into a compatible metal T-nut. The spacer controls depth and avoids making plastic carry the bolt's entire clamping preload. A rear bearing/locating seat supports the panel corners; the cap retains them. Include positive restraint against panel lift and outward pull, not just friction.

An interior node can support/retain four panel corners with one visible bolt. Perimeter nodes have two-panel and one-panel variants. This replaces the repeated M2 seam-bridge screws in frame-mounted mode; it is not an additional layer of screws. Frame mode and freestanding/interconnected panel mode may need different connector options.

Use a small intentionally reserved area at each node. Suppress any slots that collide with the cap, spacer, screw, rear seat or tool-access envelope. The exact number of lost hook/pixel positions is not yet known: report it from the detailed CAD, rather than promising zero blocked holes. A whole extrusion-width strip of blank slots is unnecessary. M4/M5 hardware is a candidate for the frame interface; exact T-nut, head and spacer sizes depend on the selected extrusion system.

The cap must distribute load into reinforced panel corners. If a cap bridges multiple corners, loosening it also releases those neighboring corners: other mounts must continue to support the adjacent panels during maintenance. Four-corner support and local edge keys need testing for panel midspan deflection, not just frame strength.

## Serviceability, appearance and movement

- Require removal of one interior panel from the front. Avoid a permanently trapped four-sided dovetail grid; use removable alignment keys or another explicitly tested release sequence.
- Use metal T-nuts, bolts and spacers for primary attachment. Printed seats/keys are replaceable interface parts, with bearing area, creep and repeated-use tests.
- Keep visible fastener heads/caps in a consistent pattern and finish. A black or matching extrusion frame plus rounded outer trim can conceal incidental bracket hardware while retaining the deliberate screw detail.
- Wall unevenness should be corrected at adjustable/shimmed mounts, not by bending the artwork to the wall.
- Segment a very large installation into manageable supported bays, with accessible splices and controlled movement joints. Provide a defined datum and designed sliding accommodation rather than forcing every printed panel and aluminum rail into one rigid 6 m tolerance chain. Do not merely loosen gravity-bearing bolts to allow motion.
- Panel module pitch, physical panel width and seam clearance must be separate variables. Changing seam clearance must not accumulate unwanted changes in hole pitch across the wall.

## Scale check, not a bill of materials

A nominal 6000 x 2400 mm field uses 25 x 10 = 250 modules at 240 mm pitch. This is approximately 19.69 x 7.87 ft; it is not exactly 20 x 8 ft. Treat trim, seams, mounting margins and actual frame outer dimensions separately.

A full shared-node grid contains (25+1)*(10+1) = 286 visible mounting nodes. Most interior nodes serve four corners. Compare this to 24 potential edge screw holes per v0.1 240 mm panel. Node count is not a wall-anchor count, and a node is not necessarily a connection between frame rails.

A dense example has 26 vertical rail lines at 240 mm pitch and 6 horizontal lines at 480 mm pitch. Centerline bookkeeping gives 26*2.4 + 6*6 = 98.4 m of extrusion. At 20 mm square with continuous verticals extending 10 mm past the outer line at each end and 150 horizontal pieces at 220 mm clear span, an illustrative member sum is 26*2.42 + 150*0.22 = 95.92 m. Connections, bay segmentation, perimeter choices and cutting waste will change this.

The cited MISUMI HFS5-2020 profile is 0.5 kg/m, so that dense frame alone is about 48 kg before joints, wall brackets, panels, tiles and fasteners. This is why a coarser support layout may be worth testing after the small assembly works. A 480 x 480 mm grid would require deliberately designed panel carriers/reinforcement; simply deleting alternate supports is not equivalent.

No anchor quantity, hardware purchase list or allowable installation load is established. Needed before full-scale design: wall substrate/stud arrangement, exact extrusion brand/profile, total measured panel/tile/hardware mass, intended accessory loads and pull-out/cantilever loads, and allowed projection from the wall.

## Proposed Fusion parameters and checks

| Parameter / option | Initial proposal |
|---|---|
| mountingMode | Frame / panel-to-panel |
| panelModuleX, panelModuleY | 240 mm nominal pitch |
| seamGap | Fit-test value; panel envelope shrinks around fixed lattice datum |
| left/right/top/bottomEdge | Internal / Finished |
| finishedBorderWidth, outerCornerRadius, faceEdgeRadius | Separate from slot throat geometry |
| slotEntryRadius | Trial 0.5 mm; compare with actual hooks before increasing |
| frameProfile | Exact manufacturer profile, not generic interchangeable 2020 |
| framePitchX, framePitchY | 240 / 480 mm prototype |
| hookClearance | 10 mm provisional cavity behind panel; insertion/removal testing pending |
| bracketKeepout, hookInsertionEnvelope | Actual component envelopes |
| mountPattern | Shared corner nodes, configurable spacing only with support checks |
| nodeReservedArea | Derived from real cap, screw, spacer, seat and tool geometry |
| wallOffset / bay segmentation | Determined from installation conditions |

Next CAD prototype: 2 x 2 panels with two finished sides represented, one central shared node plus perimeter mounts, actual extrusion cross-section/compatible T-nuts, recessed frame and a representative hook envelope. Validate front removal, node access with mosaic tiles installed, no unintended blocked slots, joint flushness, edge treatment and stiffness before scaling.

## Primary references

- [80/20 20-2020](https://8020.net/20-2020.html): 20 x 20 mm profile with four slots; compatible with its own 20-series fasteners; IX/IY 0.6826 cm4. Manufacturer lists panel racks/displays as applications. This is profile information, not approval of the proposed wall.
- [MISUMI HFS5 20/40 mm profiles and hardware](https://sg.misumi-ec.com/pdf/fa/2013/p1839.pdf): 20 mm square, 6 mm slot family with M3/M4/M5 nut options, HFS5-2020 mass 0.5 kg/m and I=0.742*10^4 mm4; 2040/4040 alternatives and bracket types. Verify the current purchased SKU before detailed design.
- [IKEA SKADIS pegboard](https://www.ikea.com/us/en/p/skadis-pegboard-white-10321618/): manufacturer product context and wall mounting hardware context. This source does not establish the proposed 10 mm cavity or custom system load capacity.

All dimensions and architecture choices not expressly attributed above are design proposals or arithmetic derived from the proposed layout. No third-party CAD was copied.
