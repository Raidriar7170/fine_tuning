# Voice2Task SFT contract learning-signal evidence

This local diagnostic inspects public-sample SFT contract learning signal only. It does not train, run prediction, download models, load private adapters, or repair outputs.

## Boundary

- This is not a model recovery claim.
- This is not a checkpoint release.
- This is not an adapter release.
- This is not held-out or private-corpus generalization evidence.
- This makes no production-readiness claim.
- This is not a live-browser benchmark or benchmark-improvement claim.

## Summary

- Rows inspected: `30`
- Split counts: `{'dev': 6, 'test': 6, 'train': 18}`
- Task type counts: `{'blocked': 6, 'clarify': 6, 'extract': 3, 'form_fill': 6, 'navigate': 6, 'search': 3}`
- All rows have assistant target span: `True`
- True runtime label-mask status: `unavailable`

## Target Pressure

- Max training text characters: `2005`
- Max assistant target characters: `244`
- Min assistant target char ratio: `0.11371571072319202`
- Max assistant target char ratio: `0.12248995983935743`
- Rows over 2048 chars: `[]`
- Tokenizer-specific token counts available: `False`

## Runtime label-mask evidence

- Status: `labels_unavailable`
- True label-mask status: `unavailable`
- Evidence gaps: `['real_training_labels_not_inspected', 'real_training_label_provenance_missing']`

## Prior Repair Evidence

- Available: `True`
- Overall interpretation: `public_heldout_residual_repair_failed`
- Split exact match: `{'dev': 0.0, 'test': 0.0, 'train': 0.3333333333333333}`

## Recommended Next Step

- `run_bounded_runtime_label_or_tiny_overfit_diagnostic`

## Row Evidence

### `seed-search-weather`

- Split: `train`
- Task type: `search`
- Route: `search_web`
- Assistant target span found: `True`
- Training text characters: `1972`
- Assistant target characters: `226`
- Assistant target char ratio: `0.11460446247464504`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `76e1bf198472001cfcfa4d46b1cf189df2c92ef7385450823ed9d9753c31c1c9`
- Assistant target SHA-256: `dbeec084022d6dcbf8673f9450e0adde10628015e6b01737f3c5064a69d41e63`

### `seed-search-weather-aug-1`

- Split: `train`
- Task type: `search`
- Route: `search_web`
- Assistant target span found: `True`
- Training text characters: `1970`
- Assistant target characters: `226`
- Assistant target char ratio: `0.11472081218274112`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `38de9a249f18c0fb16d7f4704554db1f441e414132bb2a87b22b8c650061a884`
- Assistant target SHA-256: `dbeec084022d6dcbf8673f9450e0adde10628015e6b01737f3c5064a69d41e63`

### `seed-search-weather-aug-2`

- Split: `train`
- Task type: `search`
- Route: `search_web`
- Assistant target span found: `True`
- Training text characters: `1969`
- Assistant target characters: `226`
- Assistant target char ratio: `0.11477907567293043`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `242c19bfe2a17dee372c63626c4c138c38a246172c18e8b79f445c1d4490a068`
- Assistant target SHA-256: `dbeec084022d6dcbf8673f9450e0adde10628015e6b01737f3c5064a69d41e63`

### `seed-open-example`

- Split: `dev`
- Task type: `navigate`
- Route: `open_url`
- Assistant target span found: `True`
- Training text characters: `1991`
- Assistant target characters: `235`
- Assistant target char ratio: `0.11803114013058764`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `8cb85045d8c3f8eca4cecd78a5f867e785d855676815465be8b22f468aaa4c53`
- Assistant target SHA-256: `a495fa41ba975e04e0acf484b9aad1b553c8fa7d1808100a4479f6a391c113fd`

### `seed-open-example-aug-1`

- Split: `dev`
- Task type: `navigate`
- Route: `open_url`
- Assistant target span found: `True`
- Training text characters: `1985`
- Assistant target characters: `235`
- Assistant target char ratio: `0.11838790931989925`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `13f8cf2180f4311761d2fc1c85448935a3f2d56b7437d74f38835663334e372c`
- Assistant target SHA-256: `a495fa41ba975e04e0acf484b9aad1b553c8fa7d1808100a4479f6a391c113fd`

### `seed-open-example-aug-2`

- Split: `dev`
- Task type: `navigate`
- Route: `open_url`
- Assistant target span found: `True`
- Training text characters: `1990`
- Assistant target characters: `235`
- Assistant target char ratio: `0.11809045226130653`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `2123fdc08f165bac070313097157671f763deeccc8be7195825bdca00cf53ab6`
- Assistant target SHA-256: `a495fa41ba975e04e0acf484b9aad1b553c8fa7d1808100a4479f6a391c113fd`

### `seed-form-email`

- Split: `test`
- Task type: `form_fill`
- Route: `fill_form`
- Assistant target span found: `True`
- Training text characters: `1986`
- Assistant target characters: `228`
- Assistant target char ratio: `0.1148036253776435`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `6e6767b796b37a02e30444b4f459464394bbec4c9dbf4a1e36526194f63567fa`
- Assistant target SHA-256: `65783bfbf86df22daa201777124708a2ef75ddc5f098d3f93fdb4a76f22cb125`

### `seed-form-email-aug-1`

- Split: `test`
- Task type: `form_fill`
- Route: `fill_form`
- Assistant target span found: `True`
- Training text characters: `1983`
- Assistant target characters: `228`
- Assistant target char ratio: `0.11497730711043873`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `4038b9f964bc6f08cdb4237bfb126f84183e3ed74c1d2d23f1a97d124bf9e046`
- Assistant target SHA-256: `65783bfbf86df22daa201777124708a2ef75ddc5f098d3f93fdb4a76f22cb125`

### `seed-form-email-aug-2`

- Split: `test`
- Task type: `form_fill`
- Route: `fill_form`
- Assistant target span found: `True`
- Training text characters: `1983`
- Assistant target characters: `228`
- Assistant target char ratio: `0.11497730711043873`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `9f3905702bdab097d256093f83600bd081a40c024c96704ab284aaa4903f5f2e`
- Assistant target SHA-256: `65783bfbf86df22daa201777124708a2ef75ddc5f098d3f93fdb4a76f22cb125`

### `seed-block-purchase`

- Split: `test`
- Task type: `blocked`
- Route: `deny`
- Assistant target span found: `True`
- Training text characters: `2001`
- Assistant target characters: `244`
- Assistant target char ratio: `0.12193903048475763`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `3281820c4f50b3c0f2d4035da06cc3a9422f98f2b33f415da46cf27ada942903`
- Assistant target SHA-256: `5423e8f410500ae0a3b174ba07e3ec940300f92e817eb62d7825cebe947bff3d`

### `seed-block-purchase-aug-1`

- Split: `test`
- Task type: `blocked`
- Route: `deny`
- Assistant target span found: `True`
- Training text characters: `1995`
- Assistant target characters: `244`
- Assistant target char ratio: `0.12230576441102757`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `707739d574594c73b9b87c5be205cb6f258acab28edff1453efc75d7df8a3f21`
- Assistant target SHA-256: `5423e8f410500ae0a3b174ba07e3ec940300f92e817eb62d7825cebe947bff3d`

### `seed-block-purchase-aug-2`

- Split: `test`
- Task type: `blocked`
- Route: `deny`
- Assistant target span found: `True`
- Training text characters: `1993`
- Assistant target characters: `244`
- Assistant target char ratio: `0.12242849974912193`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `d0023cd1a3bf0c8cbc31617bfd2c4c5a0cf42bce2fb76bef8f612b1d860f6dab`
- Assistant target SHA-256: `5423e8f410500ae0a3b174ba07e3ec940300f92e817eb62d7825cebe947bff3d`

### `seed-extract-price`

- Split: `train`
- Task type: `extract`
- Route: `extract_page`
- Assistant target span found: `True`
- Training text characters: `2005`
- Assistant target characters: `228`
- Assistant target char ratio: `0.11371571072319202`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `7d909c3cf78f85c9db1399e6661832939b4ab28ad82609453b90744190f6955b`
- Assistant target SHA-256: `720ed5fcbce721b7a4b1cfebcf464cf1a10a2563f74b0d6af098db61e16a0e35`

### `seed-extract-price-aug-1`

- Split: `train`
- Task type: `extract`
- Route: `extract_page`
- Assistant target span found: `True`
- Training text characters: `2005`
- Assistant target characters: `228`
- Assistant target char ratio: `0.11371571072319202`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `1cd5a7a1690cb98c3cf03a6eacc7ad1aa0e9db054957a43c8939541cc014893c`
- Assistant target SHA-256: `720ed5fcbce721b7a4b1cfebcf464cf1a10a2563f74b0d6af098db61e16a0e35`

### `seed-extract-price-aug-2`

- Split: `train`
- Task type: `extract`
- Route: `extract_page`
- Assistant target span found: `True`
- Training text characters: `2000`
- Assistant target characters: `228`
- Assistant target char ratio: `0.114`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `6f68a3b439960924a9f2748c78e8eba323b9e509228a81bfb087a3f98bd58941`
- Assistant target SHA-256: `720ed5fcbce721b7a4b1cfebcf464cf1a10a2563f74b0d6af098db61e16a0e35`

### `seed-clarify-ambiguous`

- Split: `dev`
- Task type: `clarify`
- Route: `clarify`
- Assistant target span found: `True`
- Training text characters: `1985`
- Assistant target characters: `237`
- Assistant target char ratio: `0.11939546599496222`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `007e54ce212e1816d385511c51278a5fb650f9f560aa979a1c0ec1c9dddc6dc9`
- Assistant target SHA-256: `61ec738cb26adf4cf605e9a08d1613418342c9ab4b248b6fee5cbf5d38002a99`

### `seed-clarify-ambiguous-aug-1`

- Split: `dev`
- Task type: `clarify`
- Route: `clarify`
- Assistant target span found: `True`
- Training text characters: `1986`
- Assistant target characters: `237`
- Assistant target char ratio: `0.11933534743202417`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `0f6d8fe780403350afc47247363ed1f3aa9eaa2402538d207f0538d3ce33458d`
- Assistant target SHA-256: `61ec738cb26adf4cf605e9a08d1613418342c9ab4b248b6fee5cbf5d38002a99`

### `seed-clarify-ambiguous-aug-2`

- Split: `dev`
- Task type: `clarify`
- Route: `clarify`
- Assistant target span found: `True`
- Training text characters: `1983`
- Assistant target characters: `237`
- Assistant target char ratio: `0.11951588502269289`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `eca66678187888b3a33faec2db64fb769ab84ff6c2163bf9964f2902bc1d98e9`
- Assistant target SHA-256: `61ec738cb26adf4cf605e9a08d1613418342c9ab4b248b6fee5cbf5d38002a99`

### `seed-open-help`

- Split: `train`
- Task type: `navigate`
- Route: `open_url`
- Assistant target span found: `True`
- Training text characters: `1988`
- Assistant target characters: `240`
- Assistant target char ratio: `0.12072434607645875`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `9449d86650c49da627185b6f1a6c2eeea6b7ae5432622dce8d34ed60cffe2026`
- Assistant target SHA-256: `0748d2b7cb50164b6dea1df0e9e9fb38a8dd2b0bc7b0de08e149006ca45caaac`

### `seed-open-help-aug-1`

- Split: `train`
- Task type: `navigate`
- Route: `open_url`
- Assistant target span found: `True`
- Training text characters: `1987`
- Assistant target characters: `240`
- Assistant target char ratio: `0.12078510317060896`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `45b618769ce5c6258d89527621fe982a6b348ce4d35100fdb13f4067c2a9dd05`
- Assistant target SHA-256: `0748d2b7cb50164b6dea1df0e9e9fb38a8dd2b0bc7b0de08e149006ca45caaac`

### `seed-open-help-aug-2`

- Split: `train`
- Task type: `navigate`
- Route: `open_url`
- Assistant target span found: `True`
- Training text characters: `1988`
- Assistant target characters: `240`
- Assistant target char ratio: `0.12072434607645875`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `f389f6503a8ceecead93d8bd7ccfe11e96d61b2a4750b196588e02f43fd45d34`
- Assistant target SHA-256: `0748d2b7cb50164b6dea1df0e9e9fb38a8dd2b0bc7b0de08e149006ca45caaac`

### `seed-clarify-target`

- Split: `train`
- Task type: `clarify`
- Route: `clarify`
- Assistant target span found: `True`
- Training text characters: `1984`
- Assistant target characters: `234`
- Assistant target char ratio: `0.11794354838709678`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `83c6acad4dce8de1c593afde276c69fb9e6bc711bb4a852026ec2fced5cbb36a`
- Assistant target SHA-256: `bef90fb78b35d80d414e5bb48b1e14b8aae82e7121b59697aa67aa40a56f5e99`

### `seed-clarify-target-aug-1`

- Split: `train`
- Task type: `clarify`
- Route: `clarify`
- Assistant target span found: `True`
- Training text characters: `1984`
- Assistant target characters: `234`
- Assistant target char ratio: `0.11794354838709678`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `e026f0e076ab099edf7154fc3ae3e7d7c88b94c2ae7e052af2cb71957267075f`
- Assistant target SHA-256: `bef90fb78b35d80d414e5bb48b1e14b8aae82e7121b59697aa67aa40a56f5e99`

### `seed-clarify-target-aug-2`

- Split: `train`
- Task type: `clarify`
- Route: `clarify`
- Assistant target span found: `True`
- Training text characters: `1983`
- Assistant target characters: `234`
- Assistant target char ratio: `0.11800302571860817`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `82e19ca5c4c7a71aca79134591e4027dec44c7e35a7a455bfbb7f366a75305fe`
- Assistant target SHA-256: `bef90fb78b35d80d414e5bb48b1e14b8aae82e7121b59697aa67aa40a56f5e99`

### `seed-form-nickname`

- Split: `train`
- Task type: `form_fill`
- Route: `fill_form`
- Assistant target span found: `True`
- Training text characters: `1986`
- Assistant target characters: `228`
- Assistant target char ratio: `0.1148036253776435`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `94ca907cfba3f79851451d1ede30e84692a56585b725c2e865cc9b45d33e17fe`
- Assistant target SHA-256: `9e64d13380c3ff594ea6cd1a526c708822855ebbfc8152a84b5653d7b8e638c8`

### `seed-form-nickname-aug-1`

- Split: `train`
- Task type: `form_fill`
- Route: `fill_form`
- Assistant target span found: `True`
- Training text characters: `1984`
- Assistant target characters: `228`
- Assistant target char ratio: `0.11491935483870967`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `190cad6db430cdaa6c7d83a2f1e0e9b007ead2bf0ae37b0147ace3565143ee9b`
- Assistant target SHA-256: `9e64d13380c3ff594ea6cd1a526c708822855ebbfc8152a84b5653d7b8e638c8`

### `seed-form-nickname-aug-2`

- Split: `train`
- Task type: `form_fill`
- Route: `fill_form`
- Assistant target span found: `True`
- Training text characters: `1981`
- Assistant target characters: `228`
- Assistant target char ratio: `0.11509338717819283`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `7af098dd370837971b10e3893e6a55a87d7403354c7120a4caffb13ce5b24770`
- Assistant target SHA-256: `9e64d13380c3ff594ea6cd1a526c708822855ebbfc8152a84b5653d7b8e638c8`

### `seed-block-transfer`

- Split: `train`
- Task type: `blocked`
- Route: `deny`
- Assistant target span found: `True`
- Training text characters: `1998`
- Assistant target characters: `244`
- Assistant target char ratio: `0.12212212212212212`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `d5ccbb0b050d7f5f37a8412a2df6b96ccd2e327d12268afaf5f30efab0f96421`
- Assistant target SHA-256: `4ae8f2b4a3b5d6e2f3d6b90aca13589b67a08d4beaaf366748d3efe6c8d0cbb3`

### `seed-block-transfer-aug-1`

- Split: `train`
- Task type: `blocked`
- Route: `deny`
- Assistant target span found: `True`
- Training text characters: `1992`
- Assistant target characters: `244`
- Assistant target char ratio: `0.12248995983935743`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `558629786e16dab3587e38b84fe7ac08504417a5dfae6058a29b8689752c4810`
- Assistant target SHA-256: `4ae8f2b4a3b5d6e2f3d6b90aca13589b67a08d4beaaf366748d3efe6c8d0cbb3`

### `seed-block-transfer-aug-2`

- Split: `train`
- Task type: `blocked`
- Route: `deny`
- Assistant target span found: `True`
- Training text characters: `1996`
- Assistant target characters: `244`
- Assistant target char ratio: `0.12224448897795591`
- Target fields: `8`
- Target slots: `1`
- Training text SHA-256: `b29f19cbc0de37db1db1f0be9dd6ef27c75d4911255eff363193f4e04ade6140`
- Assistant target SHA-256: `4ae8f2b4a3b5d6e2f3d6b90aca13589b67a08d4beaaf366748d3efe6c8d0cbb3`
