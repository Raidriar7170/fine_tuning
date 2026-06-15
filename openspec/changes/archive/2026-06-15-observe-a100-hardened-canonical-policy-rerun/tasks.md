## 1. Evidence Path And Tests

- [x] 1.1 Add regression coverage that hardened rerun diagnostic artifacts follow the requested output directory.
- [x] 1.2 Add an observed evidence directory check that does not overwrite the earlier blocked report.
- [x] 1.3 Keep existing blocked evidence public-safe and historically readable.

## 2. Remote Prediction-Only Rerun

- [x] 2.1 Re-check SSH, approved remote root, dependency environment, source adapter files, and GPU occupancy.
- [x] 2.2 Create private prediction overrides outside git for train/dev/test.
- [x] 2.3 Run train/dev/test prediction-only rerun on the selected safe GPU.
- [x] 2.4 Verify prediction metadata proves hardened canonical prompt flags for each split.

## 3. Evidence, Review, Archive

- [x] 3.1 Generate sanitized observed rerun evidence and leak-scan result.
- [x] 3.2 Generate the Chinese Human Brief.
- [x] 3.3 Run local validation and Reviewer pass.
- [x] 3.4 Archive the OpenSpec change and guarded commit.
