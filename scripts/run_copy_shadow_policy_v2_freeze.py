#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from voice2task.copy_shadow_policy_v2_freeze import (
    DEFAULT_FREEZE_DIR,
    DEFAULT_FROZEN_POLICY_PATH,
    DEFAULT_PROPOSED_POLICY_PATH,
    write_copy_shadow_policy_v2_freeze_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_FREEZE_DIR)
    parser.add_argument("--proposed-policy-path", type=Path, default=DEFAULT_PROPOSED_POLICY_PATH)
    parser.add_argument("--frozen-policy-path", type=Path, default=DEFAULT_FROZEN_POLICY_PATH)
    args = parser.parse_args()

    result = write_copy_shadow_policy_v2_freeze_report(
        args.repo_root,
        output_dir=args.output_dir,
        proposed_policy_path=args.proposed_policy_path,
        frozen_policy_path=args.frozen_policy_path,
    )
    print(
        json.dumps(
            {
                "decision_label": result["summary"]["decision_label"],
                "output_dir": args.output_dir.as_posix(),
                "frozen_policy_path": args.frozen_policy_path.as_posix(),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
