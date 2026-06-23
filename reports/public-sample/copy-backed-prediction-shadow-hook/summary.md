# Copy-backed prediction shadow hook

- Decision: `PREDICTION_SHADOW_HOOK_READY_OBSERVE_ONLY`
- Canonical entrypoint: `voice2task-train sft-predict -> voice2task.training.run_sft_prediction_export`
- Feature flag default: disabled
- Sidecar default: hash-and-offset-only
- Policy: `copy-backed-scope-policy-v1` version `1.0.0` hash `5dc14efb8ded13dc048ddb067c7c63a1a62b6c03896950e861303973d505cbc7`
- Prediction output hashes equal: `True`
- Runtime enforcement: not enabled
- Recommended next change: `evaluate-frozen-copy-shadow-policy-on-template-disjoint-challenge-set`
