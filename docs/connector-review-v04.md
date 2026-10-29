# Connector review: protect the artwork and hook paths

2026-10-29. The user returned from animation work and identified intrusive front connectors and lost hook space. This review supersedes the v0.3 mounting direction; v0.3 remains archived as a prototype. The new native file is a clearance study, not a completed replacement assembly or a print-ready connector.

## Findings in the existing design

- The v0.3 cap is 18 mm diameter and 5 mm thick. Its reference button head adds another 3 mm, for 8 mm front projection. The old mosaic brief reserved only 3 mm behind artwork for screw heads: these specifications conflict.
- Each panel pattern deliberately omits four slot positions near its mounting nodes (some positions represent half slots at internal horizontal seams). These omissions interrupt the art grid. Additional entire outer rows/columns are omitted for v0.3's wide finished border; this is a separate source of lost positions.
- The shared cap, 18 mm rear seat, 8 mm shoulder and 12 mm spacer base were designed around the mount rather than around a hook's insertion/removal path. The earlier interference checks established solid part separation and frame tool access. They did not certify hook access or mosaic compatibility.
- Shared caps release neighboring panel corners during maintenance and require temporary studs to retain loose spacer stacks. This is needlessly awkward for a large installation.

## Revised design rules

1. The artwork-facing surface must be flat. Remove large caps and button heads from the active field.
2. Do not omit extra lattice positions for connectors. A finished outer edge may omit split slots; edge border width is a separate strength/aesthetic decision.
3. Check the full provisional hook insertion corridor, not just whether a mount overlaps the slot aperture.
4. Keep broad carriers, frame screw heads, nuts and any latch bodies at or behind the rear limit of the hook cavity.
5. Supports passing through the cavity should occupy the narrow solid corridors between slot columns. Align every mount to the lattice before arranging extrusion rails.
6. Aim for independent straight-forward panel removal with neighbors supported. Do not rely on four-sided sliding dovetails, hidden screws requiring wall removal, or magnets alone as the primary positive retention.
7. Separate the functions: frame attachment, panel registration, panel retention and release. A visual clearance model must not be presented as proof that the retention mechanism works.

## Geometry and tradeoffs

Slot columns occur every 10 mm in X; slots remain 5 × 15 mm on the staggered 20 mm repeat. For this study, reserve a 6 mm-wide, 10 mm-deep continuous rear corridor at every slot column. This includes 0.5 mm lateral allowance on either side of the nominal slot and conservatively covers every vertical position, including a provisional 8 mm hook lift. Actual accessory width, tilt and rear depth still require physical measurements.

Only 4 mm-wide continuous support corridors remain between those envelopes. A 3 mm support centered between columns leaves 0.5 mm on each side. Round 5.5 mm posts may fit the static gaps between slot ends but do not fit this conservative insertion envelope; simply shrinking the old round mounts is not sufficient.

Small flush M2 screws were considered. Manufacturer dimensions show approximately 4.09 mm actual head diameter for an ISO 10642 M2 example. Allowing a printable countersink and neighboring slot entrance radii makes placement in the continuous web tight, and a coaxial rear post/insert introduces further interference. A head can fit a staggered pocket while its support blocks hook travel. This option is not accepted without a complete interface check. [Würth M2 example](https://eshop.wuerth.de/Countersunk-screw-with-hexagon-socket-head-ISO-10642-steel-109-plain-SCR-CS-ISO10642-0109-HS15-M2X4/00892%20%204.sku/en/US/EUR/).

The user subsequently confirmed that **small flush screw heads are acceptable between the slots**. The preferred retention approach is therefore front-accessible flush screws, with rear registration/supports arranged around the hook corridors. Concealed latches are a fallback if a screw arrangement cannot meet the clearance requirements. This preference does not resolve the coaxial screw/post interference described above: the full screw, threaded receiver, registration support and tool access must be checked together. Screw size, placement, receiver geometry and load capacity have NOT been selected or validated.

The depth allowance becomes 5 mm panel + 10 mm hook cavity + 4 mm rear carrier + 20 mm extrusion = **39 mm face to wall**, with no designed air gap behind the extrusion. Keeping exactly 35 mm would require fitting the carriers within the profile or reducing the cavity; neither is assumed here.

## Native Fusion clearance study

`models/v04-study/connector-clearance-study.f3d` contains two nominal 120 mm panels with restored slot fields, complete finished top/bottom slots, exterior corner rounds, rounded slot entrances, eight narrow support envelopes, six rear carrier envelopes, three reference extrusion rails and 24 hidden hook-corridor reference solids. Components explicitly identify unfinished connector envelopes. The finished edge treatment is narrower than v0.3 and needs edge-strength testing.

The panel geometry uses native sketches, feature patterns and user-parameter expressions. The study's reference-corridor count and layout are generated specifically for this 240 × 120 mm arrangement; do not treat arbitrary resizing of the complete study as validated. Retention details, frame joints, wall brackets, hardware and mosaic tiles are deliberately not represented as completed parts.

`docs/connector-clearance-v04.json` records native feature health and the dimensional clearance calculation. No STL is released for the carrier/blade envelopes because they are not finished printable connectors.

## Updated extrusion evidence

The latest relevant message in **Design Quiet DIY Air Purifier** says the revised printed T-nut carriers fit the slot. The subsequent hardware selection used M5 thin nuts, 8 mm across flats and 2.7 mm thick. This advances the physical fit evidence beyond v0.3's notes. It does not establish clamped capacity or make the printed carriers approved structural frame nuts; preserve the measured mouth/cavity/floor cautions and use appropriate metal load paths for the wall frame.

## Next engineering checks

- User preference resolved: small flush screw heads are acceptable. Heads must sit at or slightly below the board face, without large decorative caps or additional omitted slot positions.
- Design the complete screw/receiver/support interface and prove front removal with adjacent panels installed. Retain the narrow rear support corridors; do not assume the previous round-post proposal now fits because flush heads are acceptable.
- Test adjacent hooks and a pair of two-pixel tile hooks at regular slots, seams, support locations and rail-backed positions, including lift/tilt/removal.
- Confirm front artwork clearance at all connector locations; keep the pegboard face unobstructed.
- Validate printed blade fatigue/creep or specify a suitable metal spring/load member. The 3 mm envelope is a geometric allocation, not a strength result.
- Revisit large-frame bay spacing and load paths separately from these small connector/interface coupons.
