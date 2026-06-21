from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from voice2task.slot_error_analysis import generate_slot_error_mechanism_analysis  # noqa: E402

DEFAULT_RAW_INPUTS = REPO_ROOT / "reports/public-sample/step-matched-canonical-slot-ablation/raw-inputs"
DEFAULT_OUTPUT = REPO_ROOT / "reports/public-sample/slot-error-mechanism-analysis"


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze recovered step-matched slot error mechanisms.")
    parser.add_argument("--raw-inputs-dir", type=Path, default=DEFAULT_RAW_INPUTS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    raw_inputs_dir = args.raw_inputs_dir.resolve()
    output_dir = args.output_dir.resolve()
    if raw_inputs_dir != DEFAULT_RAW_INPUTS.resolve():
        raise SystemExit(f"refusing unapproved raw inputs dir: {raw_inputs_dir}")
    if output_dir != DEFAULT_OUTPUT.resolve():
        raise SystemExit(f"refusing unapproved output dir: {output_dir}")
    result = generate_slot_error_mechanism_analysis(args.raw_inputs_dir, args.output_dir)
    print(result["decision_label"])
    return 0 if result["decision_label"] != "ANALYSIS_BLOCKED_INVALID_INPUT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
