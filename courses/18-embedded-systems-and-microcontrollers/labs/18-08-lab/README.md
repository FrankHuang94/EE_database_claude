# Lab 18-08 · Power Cuts During Firmware Updates

Chapter: [18-08 · Boot, Bootloaders and Firmware Update](../../chapters/18-08-boot-and-firmware-update.md)

## Objective

- Model flash as sectors that are erased and written one at a time, with power able to fail during any operation.
- Implement in-place, overwrite and swap installations with a bootloader that verifies SHA-256 digests and resumes from atomic progress records.
- Cut power during every operation and count the outcomes: new image, old image or no bootable image.
- Show that an unconfirmed image is reverted, and that the revert itself survives power cuts.

## Background

An update is power-safe if every interrupted state can be finished or undone at the next boot (§3.4): never destroy the only good copy, record progress atomically with repeatable steps, and boot new images on test until the application confirms them.

The model is deliberately small (six 64-byte sectors per image) so that exhaustive cut injection runs in seconds; the logic, not the size, is what is tested. Real bootloaders add per-slot trailers, alternating status records with CRCs, and signatures, which the model replaces by an atomic status variable and a SHA-256 digest.

## Files

- `bootsim.py`: `make_image`, `validate`, `Flash` (with `cut_at`), `Device` (`download`, `boot`, `confirm`), `run_with_cut`, `count_ops`, `campaign`, `revert_test`, `revert_campaign`, `swap_time`, `outage_probability`.
- `18-08-boot-lab.ipynb`: the guided notebook.

## Procedure

1. **Count the operations** of each scheme for a six-sector image; check with `count_ops`.
2. **Cut everywhere.** Predict how many cut positions leave the new image, the old image or nothing; run `campaign` for each scheme.
3. **Break the bootloader.** In a copy of `Device.boot`, drop the condition that resumes a swap whose progress record is nonzero (keep only "the secondary slot validates"); rerun the swap campaign and find the bricking cut.
4. **Revert.** Boot the new image without confirming it, reset, and check which image runs; then run `revert_campaign`.
5. **Budgets.** Tabulate installation time with `swap_time` for images of 128 KiB to 1 MiB, one and three copies per sector, and the risk of Example 18-08.4 with `outage_probability`.

## Expected results

- Parts 1 and 2: in-place 14 operations, of which 12 cuts brick; overwrite 32 operations, 0 bricked (13 keep the old image, 19 finish the new); swap 69 operations, 0 bricked (14 keep or return to the old image, 55 finish the new).
- Part 3: the broken rule bricks 44 of the 69 cut positions, every cut from the erase of the secondary slot's first sector (operation 20 of 69) to operation 63; cuts at operations 64 to 69 do not brick, because by then the primary is complete or the secondary is intact. Once the secondary holds part of the old image it no longer validates, so a resume conditioned on it never happens; the progress record, not the slot's contents, must decide.
- Part 4: the unconfirmed image is reverted to version 1; each of the revert's 56 operations can be cut without bricking, and every cut ends with the old image.
- Part 5: installation time grows linearly with image size and with copies per sector, as in Example 18-08.2.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 18-08.a | in-place operations, six sectors | 14 | — |
| Lab 18-08.b | overwrite operations | 32 | — |
| Lab 18-08.c | overwrite cuts keeping the old image | 13 | — |
| Lab 18-08.d | swap operations | 69 | — |
| Lab 18-08.e | swap cuts completing the new image | 55 | — |
| Lab 18-08.f | revert operations | 56 | — |
| Lab 18-08.g | swap cuts that brick with the broken resume rule | 44 | — |
| Lab 18-08.h | first bricking operation (1-based) with the broken rule | 20 | — |

## Discussion

1. Why does the overwrite scheme never brick even though it destroys the old image?
2. Why must the status record be atomic, and how does a real bootloader make a flash write atomic?
3. In the swap campaign, the cut during the final confirmation ends with the *old* image. Is that a failure?

## Answers

1. Its secondary slot keeps a complete, verified copy of the new image until installation finishes, and the progress record (or the still-valid secondary) tells the bootloader to finish the copy. There is always a complete image somewhere. What is lost is rollback: if the new image is bad, nothing older remains.
2. If a torn status write could produce a plausible but wrong record, the bootloader could resume the wrong step, for example copying from a sector that was already overwritten. Real bootloaders write records with sequence numbers and CRCs into alternating locations (or use flash words that program atomically), and trust only the newest record whose CRC is correct.
3. No. The new image had not confirmed itself when power failed, so the bootloader cannot know it is healthy, and the design's rule is to revert. The update is simply retried later. This is the intended trade: occasionally redoing an update to never running an unproven image.

## Optional hardware

On a development board with MCUboot (for example under Zephyr), build two signed images that differ in a printed version string, start a swap upgrade, and remove power at random moments with a relay driven by a second board, logging which version boots each time. Then build an image that never confirms itself, and watch MCUboot revert it at the next reset.
