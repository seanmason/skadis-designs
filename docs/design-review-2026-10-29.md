# Critical design review — 29 October 2026

Status: design review and proposed next revision. The v0.4 CAD has NOT been changed by this review. It remains a geometrically checked prototype, not a production-qualified wall system.

The main agent and an independent extra-high-reasoning subagent reviewed the repository and debated the design. The review began at 17:34 PDT (00:34 UTC on 30 October). Conclusions below distinguish current evidence, preferred candidates and unresolved physical tests.

## Conclusion

Keep the 20 mm staggered slot lattice, the 240 mm nominal panel size as the first production candidate, front-accessible removable panels, and a flush-backed frame. Keep 240 mm vertical rail / 480 mm crossmember spacing as the prototype baseline, not an established structural optimum. The next revision should address mosaic serviceability, real fastener selection and repeatable assembly before adding more frame detail.

The preferred new interior horizontal seam candidate is a stepped contour following pixel boundaries. It gives whole slots and panel-owned mosaic tiles, but must compete against the simpler straight seam in a real assembly/removal test. It is not ready to replace the released prototype exports yet.

## What changed through debate

| Issue | Initial position / challenge | Agreed result |
| --- | --- | --- |
| Interlocking | Reviewer challenged the absence of direct panel interlocks. | Frame-mediated registration can satisfy the evolved wall-mounted requirement. Describe that architecture explicitly; it is not a free-standing snap-together board. |
| Small countersink lip | Reviewer identified a nominal 0.1 mm front ligament beside a slot. | Main showed that it grows to about 0.465 mm at 0.1 mm depth and 0.646 mm at 0.2 mm depth. It is a real cosmetic/clamping test point, not evidence that the entire panel connection is 0.1 mm thick. |
| Offset front screws | Main proposed moving the axis away from the neighboring slot. | Reviewer showed that this consumes the rear hook-envelope tolerance. Retain centered M2 screws for the first comparison coupon; do not remodel all mounts on an unproven offset. |
| Recessed socket heads | Considered eliminating the countersink's wedging action. | A deep cylindrical pocket at the same location extends the thin ligament farther into the board. It is not an automatic improvement. |
| Permanent carrier strips | Reviewer proposed linking carrier stations into long printed strips. | Main challenged extra material, warping and thermal constraint. Prefer a reusable positioning jig with driver windows and short independent carriers. |
| M5 carrier clamp | Main and reviewer traced the load path through compressed plastic. | Investigate a supplier-matched metal clamp insert/compression limiter, positive carrier bearing and a broad foot spanning the extrusion mouth. A loose sleeve that merely unloads the plastic can reduce retention; a small tube can also concentrate load on the lips. |
| Artwork service | Initially considered removing seam-spanning tiles before pulling a panel. | Reviewer proposed stepped seams; both checked the lattice phase. Prefer testing this approach because it assigns the interior slots and centered tile faces to individual panels. |
| Panel handling | Existing notes suggested a suction cup. | Reviewer correctly rejected this as a dependable bare-panel grip. Provide a reusable positively engaged through-slot handling tool; a cup on artwork may pull off a tile rather than hold the panel. |
| Sparse frame | Main challenged the approximately 95 m of extrusion in a large example. | A 480 mm square grid leaves intermediate 240 mm panel mounts unsupported. Do not replace aluminum with untested long printed bridges. Compare a real secondary metal support alternative if full-wall cost warrants it. |

## Preferred next-revision architecture

### 1. Whole-slot interior seams

For each 20 mm horizontal period, place the horizontal seam at y=0 over x=0..10 (A tile column), and at y=10 over x=10..20 (B tile column). The transitions lie in the solid corridors between slots. Repeat this profile at a 240 mm vertical pitch.

An interior panel then owns A-slot centers y=10..230 and B-slot centers y=20..240: 288 whole slots for 12 columns of each family. Both top and bottom ownership must change; simply adding top teeth to the current panel would be wrong. The nominal bounding box is approximately 240 × 250 mm, before clearance offsets. The edge remains a planar extrusion, so it has no inherent Z undercut.

Apply clearance as a true two-dimensional contour offset, including the vertical step walls. Add appropriate XY corner radii and test 0.2, 0.35 and 0.5 mm nominal seam gaps. The nominal closest slot-to-contour distance is 2.5 mm; subtracting two 0.4 mm face rounds and a 0.1 mm contour inset leaves about 1.6 mm of front-face web at the closest parallel sections. This arithmetic is not a strength result.

The costs are a visible stepped shadow line, more edge topology, handling-sensitive teeth, and more simultaneous fits during panel withdrawal. Test a fully surrounded center panel in a 3×3 coupon array, then test full-size warped/printed panels. A 2×2 array does not surround a center panel on all sides. If teeth bind or chip, retain straight seams and explicitly make seam artwork removable before panel service.

Keep straight finished outer boundaries and rounded outside corners. Alternate mosaic columns still need an intentional top/bottom artwork termination. Candidate solutions include an independently colored perimeter clip or a special terminal carrier; do not pretend the missing boundary half-domino is solved by rounding the board.

### 2. Separate compatibility from artwork retention

Preserve the IKEA-compatible center-spacing subset and test real accessories. Do not assume their lift/drop motion is suitable for a tightly filled mosaic. Prototype a custom axial push/pull tile connection, with a gravity-bearing feature and a demonstrated release/pickup tool. Printed resilient retention is the first candidate; magnets are an alternative only if their cost and handling are justified.

Test neighboring tiles, rear hooks, panel seams and perimeter tiles together. An empty-panel clearance box cannot prove this interface. With current centered 10×20 mm faces, a screw at (10,20) is at a junction of three tile faces. Four screws can therefore require removing up to twelve tiles for access. Straight horizontal seams can add twelve bridging dominoes at each edge of a 240 mm panel. Stepped seams remove that bridging requirement, but do not make the screws magically accessible through completed artwork.

Two pixels must be independently colorable if full 10 mm image resolution is intended. Printing each domino in one color constrains the artwork. Compare ordered two-color prints against separate colored faces, including the additional part count. Do not silently double manufacturing parts by assuming separate face caps.

### 3. Simplify and strengthen the rear mounting workflow

- Select and measure actual M5 channel hardware first. The current 8.8×12×2.7 mm rectangular nut is a reference envelope without a selected matching SKU. Stock M2×20 screws exist; the channel-nut interface is the more important sourcing uncertainty.
- Match the in-bay metal angles and wall tabs to purchased parts or explicit fabrication drawings too. Their current dimensions and hole positions are custom reference geometry, not a purchasable bill of materials. Supplier choices may change clearances and tool access.
- The user's thin M5 nut / printed anti-rotation-carrier approach is a candidate, not a qualified structural joint. Check actual lip thickness, complete cavity shape, metal bearing area, screw engagement and bottoming clearance. Printed nut-carrier fit alone is insufficient.
- Replace the loose M2 keeper plugs with integral captive-nut retention if the print trial succeeds. The nut must remain near its current axial position; letting it slide to the rail face can prevent the M2×20 screw from reaching it.
- Add a reusable carrier-positioning jig with access to tighten the M5 fixings while alignment is held.
- Develop a metal-reinforced M5 clamp with controlled plastic compression and positive bearing into the carrier. Keep it behind the hook cavity. Choose real components and an appropriate tolerance stack before freezing thickness or screw length.
- Retain four small front M2 screws for the initial prototype. A full panel latch redesign is not justified by the review alone.
- Provide a positively retained temporary handling tool before removing the last screw from a loaded panel. Demonstrate its engagement and withdrawal within the hook cavity and around neighboring hooks.

[SPIROL's compression-limiter guide](https://www.spirol.com/assets/files/cmpl-compression-limiter-design-guide-us.pdf) supports controlling plastic compression and maintaining the bolted joint. It also requires adequate bearing surfaces, appropriate host geometry and application-specific tolerances. It does not validate a particular limiter for this extrusion or justify completely removing plastic retention from the joint.

### 4. Keep the grid provisional and cost the whole system

240 mm square panels remain a sensible starting point. A 280 mm panel reduces panel/fastener count per area by about 26.5%, but requires a larger, flatter print and increases unsupported span. Proposed stepped versions have approximately 250 and 290 mm bounding heights, respectively. A 240×120 mm panel is a useful flatness/stiffness fallback but doubles panel count relative to 240 mm square.

Keep the initial 240 mm vertical rail spacing and 480 mm horizontal crossmember spacing. These are a convenient support layout, not allowable spans or an anchor schedule. A 960 mm planning block is not automatically a separately boxed cassette. Shared rails, splice access, thermal movement and wall anchors remain to be designed around the actual wall and stock lengths. Do not assume an unmeasured center bore accepts a particular tapped end fastener.

For the hypothetical 6000×2400 mm wall, the proposed layout has approximately 95.2 m of extrusion, 150 crossmembers and 300 two-screw L brackets. It also has 520 carrier mount stations. These counts assume the current connection approach extrapolated over the grid; they are a warning about manufacturing complexity, not a released BOM. Supplier-matched lower-part-count joints deserve comparison before full-wall fabrication.

Full 10 mm pixel coverage means 144,000 pixels, or about 72,000 two-pixel tile equivalents, with special perimeter treatment. At an assumed 5–10 seconds solely to place each tile, that is 100–200 hours. Sparse artwork scales these figures by coverage. Measure a 100-tile trial rather than treating those times as actual production data.

The current 120 mm interior STL encloses 46,478.572 mm³ of solid geometry. Extrapolating its volume per area over 14.4 m² and using [Bambu PLA Basic's 1.24 g/cm³ density](https://store.bblcdn.com/s7/default/b189de92249a4b9ebed28b8ea1f080f0/Bambu_PLA_Basic_Technical_Data_Sheet.pdf) gives about 57.6 kg if that geometry were fully solid. This is not sliced panel mass. Separately, hypothetical full-coverage 2 mm solid PLA artwork faces alone would add about 35.7 kg. Neither assumption specifies the intended print; obtain slicer and measured masses before selecting wall anchors. Individual tile loads are small, but a fully populated wall is not weightless.

## Prototype and release sequence

1. **Interface coupon:** actual IKEA accessories, neighboring custom mosaic tiles, a finished edge, both seam candidates and the existing screw/support geometry. Prove insertion, retention and removal with nearby sites populated. Record forces, damage and repeated-use behavior.
2. **Carrier coupon:** real extrusion/nuts/screws, proposed captive nut retention, jig and metal clamp. Measure torque/engagement/clearance and check sustained load, slip and relaxation over time at the intended environment. Do not extrapolate supplier material-strength numbers to a printed assembly.
3. **Panel comparison:** slice and print 240 mm and 280 mm candidates; record mass, time, flatness and center/edge deflection under the same measured test force. Test repeated fitting without forcing holes into alignment. Budget print variation and temperature movement before selecting the final gap. Four countersunk screws are not a floating mount; simply slotting rear sockets does not change that.
4. **Service demonstration:** a fully surrounded panel with populated artwork, the actual driver and handling tool. Remove it from the front without releasing neighboring panels, damaging teeth or losing captive nuts. Use a 3×3 small-coupon array for topology and a full-size assembly for warp/stiffness.
5. **Frame scale-up:** after the above, choose actual rail lengths, joints, splices, wall attachment pattern and load cases. Compatibility with accessory locations does not imply a heavy-tool load rating.

The existing 80/120 mm CAD interference checks, 280 mm regeneration, constrained sketches and manifold exports remain valuable. They do not establish printed fit, a real hook's motion, material durability, artwork access, supplier hardware availability or a completed full-wall structure. This review changes the next design direction without relabeling those earlier tests as proof of production readiness.

## Review closure and documentation handoff

The final red-team exchange accepted this sequence: inexpensive interface and hardware coupons first, full-size panel comparisons second, then a 480 mm frame and populated service trial. The reviewer retained the condition that neither stepped seams nor axial clips become production defaults before those trials; the main agent agreed. There was no remaining substantive disagreement on this next-design direction.

The review also found that README linked to `print-and-test.md`, which described v0.1 M2×8 screws in printed pilots. That file is now explicitly marked historical and points to current v0.4 assembly notes and this test sequence. The underlying old instructions are preserved as history, not silently converted into an untested new manufacturing profile.
