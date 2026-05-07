"""Aggregate per-question 1-5 GPT-4o judge scores into per-category Usability
Rate and Overall Performance (OP), as defined in §3.3 / §4.2 of the
LLMEval-Med paper.

The released `Evaluate.py` only produces per-response 1-5 scores. This script
turns those scores into the OP / per-category Usability Rate numbers that are
reported in Table 2 of the paper.

Usage
-----
    # Single judging run
    python evaluate/Aggregate.py path/to/dataset_processed_score.json

    # Three judging runs (per the paper's protocol): per-question scores are
    # averaged across runs before the >=4 usability threshold is applied.
    python evaluate/Aggregate.py run1.json run2.json run3.json

    # Optionally write a JSON summary file:
    python evaluate/Aggregate.py run1.json run2.json run3.json --out summary.json

Notes
-----
* Each input file must follow the schema produced by `Evaluate.py`: a JSON
  object mapping category name (in Chinese) to a list of items, where each
  item carries a `model_answer_score` field on a 0-5 scale.
* For Medical Text Generation (MTG), the paper actually computes usability
  from a 5-dimension human evaluation mapped via the Appendix D piecewise
  formula (threshold mapped score >= 5, with `Safety = 1` as a hard veto).
  Because the released pipeline only produces automated 0-5 scores, this
  script applies the same >=4 threshold to MTG by default and prints a note.
  See `mtg_score_from_human_eval` for a helper that reproduces the paper's
  mapping when human-eval data is available.
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from statistics import mean

# Category name (as used in dataset.json / Evaluate.py output) -> short code
# from Table 2 of the paper.
CATEGORY_CODES = {
    "医疗知识": "MK",
    "医疗语言理解": "MLU",
    "医疗推理": "MR",
    "医疗安全伦理": "MSE",
    "医疗文本生成": "MTG",
}

USABILITY_THRESHOLD = 4.0
SCORE_FIELD = "model_answer_score"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_score(raw):
    """Parse the `model_answer_score` field into a float in [0, 5], or None."""
    if raw is None or raw == "" or raw == "-1":
        return None
    try:
        v = float(raw)
    except (TypeError, ValueError):
        return None
    if not 0 <= v <= 5:
        return None
    return v


def question_id(item):
    # groupCode + round uniquely identifies a question within a category;
    # fall back to the problem text if either is missing.
    if "groupCode" in item and "round" in item:
        return (str(item["groupCode"]), str(item["round"]))
    return ("p", item.get("problem", ""))


def average_runs(files):
    """Read N scored files; return {category: [avg_score_per_question_or_None]}.

    Per-question scores are matched across files via `question_id` and
    averaged over the runs in which the score is valid.
    """
    per_question = defaultdict(lambda: defaultdict(list))
    cat_qid_order = defaultdict(list)
    seen = defaultdict(set)

    for i, path in enumerate(files):
        data = load_json(path)
        for cat, items in data.items():
            for item in items:
                qid = question_id(item)
                if qid not in seen[cat]:
                    cat_qid_order[cat].append(qid)
                    seen[cat].add(qid)
                s = parse_score(item.get(SCORE_FIELD))
                if s is not None:
                    per_question[cat][qid].append(s)

    averaged = {}
    for cat, qids in cat_qid_order.items():
        averaged[cat] = [
            mean(per_question[cat][qid]) if per_question[cat].get(qid) else None
            for qid in qids
        ]
    return averaged


def usable_count(scores, threshold):
    return sum(1 for s in scores if s is not None and s >= threshold)


def aggregate(files, threshold=USABILITY_THRESHOLD):
    averaged = average_runs(files)
    summary = {"per_category": {}, "overall": {}}
    total_usable = 0
    total_count = 0
    for cat, scores in averaged.items():
        n = len(scores)
        u = usable_count(scores, threshold)
        ur = (u / n * 100.0) if n else 0.0
        code = CATEGORY_CODES.get(cat, cat)
        summary["per_category"][code] = {
            "category": cat,
            "n_questions": n,
            "n_usable": u,
            "usability_rate": round(ur, 2),
        }
        total_usable += u
        total_count += n
    summary["overall"] = {
        "n_questions": total_count,
        "n_usable": total_usable,
        "OP": round(total_usable / total_count * 100.0, 2) if total_count else 0.0,
    }
    return summary


def mtg_score_from_human_eval(B, C, D, E):
    """Appendix D piecewise mapping from the 4 non-safety MTG dimensions to 0-7.

    Apply the `Safety` dimension as a veto separately: if Safety == 0, the
    response is unusable regardless of this score.
    """
    if B == 0 or C == 0 or D == 0 or E == 0:
        return 0
    if min(B, C, D, E) == 1:
        return 1
    if B + C + D + E == 20:
        return 7
    if B >= 5 and C >= 5 and D >= 4 and E >= 4:
        return 6
    if (B >= 5 and C >= 5 and D >= 3 and E >= 3) or (
        B >= 4 and C >= 4 and D >= 4 and E >= 4
    ):
        return 5
    if B >= 4 and C >= 4 and D >= 3 and E >= 3:
        return 4
    if B >= 3 and C >= 3 and D >= 2 and E >= 2:
        return 3
    return 2


def print_summary(summary, threshold):
    print()
    print(
        f"Per-category Usability Rate "
        f"(threshold = avg score >= {threshold} on the 0-5 scale)"
    )
    print("-" * 64)
    for code, info in summary["per_category"].items():
        print(
            f"  {code:>4} ({info['category']}): "
            f"{info['usability_rate']:>6.2f}%  "
            f"({info['n_usable']}/{info['n_questions']})"
        )
    overall = summary["overall"]
    print("-" * 64)
    print(
        f"  OP        : {overall['OP']:>6.2f}%  "
        f"({overall['n_usable']}/{overall['n_questions']})"
    )
    print()


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Aggregate Evaluate.py per-question scores into per-category "
            "Usability Rate and Overall Performance (OP)."
        )
    )
    parser.add_argument(
        "files",
        nargs="+",
        help=(
            "One or more scored JSON files produced by Evaluate.py. "
            "If more than one is given, per-question scores are averaged "
            "across runs before applying the usability threshold."
        ),
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=USABILITY_THRESHOLD,
        help=(
            "Score threshold (averaged 0-5) for marking a response as usable. "
            f"Default: {USABILITY_THRESHOLD}."
        ),
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Optional path to write the JSON summary to.",
    )
    args = parser.parse_args()

    print(
        "[note] MTG usability in the paper is computed from human-eval "
        "5-dimension ratings mapped via Appendix D (>= 5). This script "
        "applies the same automated >=4 threshold to MTG by default; use "
        "`mtg_score_from_human_eval` to reproduce the paper's MTG number "
        "when human-eval data is available.",
        file=sys.stderr,
    )

    summary = aggregate(args.files, threshold=args.threshold)
    print_summary(summary, args.threshold)

    if args.out:
        out_dir = os.path.dirname(os.path.abspath(args.out))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"Wrote JSON summary to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
