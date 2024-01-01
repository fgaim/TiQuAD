# The official evaluation script for TiQuAD Benchmark
# Inspired by the evaluation script for SQuAD v2.0, but adapted for the TiQuAD benchmark.
# Part of the TiQuAD benchmark: https://github.com/fgaim/tiquad, Gaim et al. 2023.

import re
import string
import json
import argparse

from datasets import load_dataset


class TiQuADEvaluator:
    """Extractive QA evaluation metrics for the TiQuAD benchmark."""

    def __init__(
        self, preds_path: str, eval_set_path: str = None, use_hf_dataset: bool = False, split: str = "validation"
    ):
        self.predictions: dict[str, str] = {}
        with open(preds_path, "r") as fin:
            self.predictions = json.load(fin)

        if use_hf_dataset:
            print(f"Loading {split} set from HF dataset...")
            _tiquad_eval = load_dataset("fgaim/tiquad", trust_remote_code=True, split=split)
            self.references = {entry["id"]: entry["answers"]["text"] for entry in _tiquad_eval}
        elif eval_set_path:
            print("Loading evaluation set from local file...")
            with open(eval_set_path, "r") as fin:
                _tiquad_eval = json.load(fin)
            self.references: dict[str, list[str]] = {}
            for article in _tiquad_eval["data"]:
                for paragraph in article["paragraphs"]:
                    for qa in paragraph["qas"]:
                        self.references[qa["id"]] = [answer["text"] for answer in qa["answers"]]
        else:
            raise Exception("No evaluation option provided! Either use --eval-set-path or --use-hf-dataset!")

        _tiquad_geez_puncs = "፡፣፥፤፦።፧፨፠“”‘’‚‛„‟"
        self.re_all_puncs = re.compile(r"([" + string.punctuation.replace("-", "") + _tiquad_geez_puncs + r"])")
        self.excluded_articles = {"a", "an", "the", "ብ", "ናይ", "ኣብ", "እዩ", "ናብ", "ካብ", "እቲ"}

    def normalize_answer(self, text: str):
        """Lower text and remove punctuation, articles and extra whitespace."""

        def clean_text(text: str) -> list[str]:
            """
            Cleans Ge'ez or English text for evaluation purposes.
             - Lowercase, remove punctuation, and extra whitespace
            """
            text = self.re_all_puncs.sub(" ", text.lower())
            return " ".join(text.split()).strip()

        def remove_articles(text):
            return " ".join([w for w in text.split() if w not in self.excluded_articles])

        return remove_articles(clean_text(text))

    def _compute_em(self, a_true: str, a_pred: str):
        return int(self.normalize_answer(a_true) == self.normalize_answer(a_pred))

    def _compute_f1(self, a_true: str, a_pred: str):
        """Custom F1 score for token-level evaluation."""
        pred_tokens = self.normalize_answer(a_pred).split()
        true_tokens = self.normalize_answer(a_true).split()
        common = set(pred_tokens) & set(true_tokens)
        num_same = sum(min(pred_tokens.count(w), true_tokens.count(w)) for w in common)
        if len(pred_tokens) == 0 or len(true_tokens) == 0:
            return int(pred_tokens == true_tokens)
        if num_same == 0:
            return 0
        precision = num_same / len(pred_tokens)
        recall = num_same / len(true_tokens)
        f1 = 2 * precision * recall / (precision + recall)
        return f1

    def _compute_max_em_f1(self, prediction: str, references: list[str]) -> tuple[float, float]:
        """Compute EM and F1 scores considering all reference alternatives."""
        max_em = 0
        max_f1 = 0
        for y_true in references:
            _em_score = self._compute_em(a_true=y_true, a_pred=prediction)
            _f1_score = self._compute_f1(a_true=y_true, a_pred=prediction)
            max_em = max(max_em, _em_score)
            max_f1 = max(max_f1, _f1_score)
        return max_em, max_f1

    def score(self) -> dict[str, float]:
        """Computes token-level EM and F1 scores using loaded predictions and references, aligned by question ID."""

        common_qids = set(self.predictions.keys()) & set(self.references.keys())
        if not common_qids:
            raise ValueError("No common question IDs found between predictions and references!")

        missing_preds = set(self.references.keys()) - set(self.predictions.keys())
        missing_refs = set(self.predictions.keys()) - set(self.references.keys())
        if missing_preds:
            print(f"Warning: {len(missing_preds)} question IDs have references but no predictions!")
        if missing_refs:
            print(f"Warning: {len(missing_refs)} question IDs have predictions but no references!")

        em_scores = []
        f1_scores = []
        for qid in common_qids:
            prediction = self.predictions[qid]
            references = self.references[qid]
            em, f1 = self._compute_max_em_f1(prediction, references)
            em_scores.append(em)
            f1_scores.append(f1)

        return {
            "em": sum(em_scores) / len(em_scores),
            "f1": sum(f1_scores) / len(f1_scores),
            "num_evaluated": len(common_qids),
            "total_predictions": len(self.predictions),
            "total_references": len(self.references),
        }


def parse_cli_args():
    """Parse arguments for TiQuAD evaluation."""
    parser = argparse.ArgumentParser(description="Evaluate on the TiQuAD benchmark")
    parser.add_argument("preds_path", type=str, help="Path to JSON file containing predictions in format {qid: text}")
    parser.add_argument("--eval-set-path", type=str, default=None, help="Path to local evaluation dataset JSON file")
    parser.add_argument("--use-hf-dataset", action="store_true", help="Use HF dataset (fgaim/tiquad)")
    parser.add_argument("--split", default="validation", choices=["test", "validation", "train"], help="Dataset split")
    parser.add_argument("--verbose", action="store_true", help="Print detailed evaluation information")
    return parser.parse_args()


def main():
    """TiQuAD Evaluation."""

    try:
        args = parse_cli_args()
        print(f"Loading predictions from: {args.preds_path}")
        evaluator = TiQuADEvaluator(
            preds_path=args.preds_path,
            eval_set_path=args.eval_set_path,
            use_hf_dataset=args.use_hf_dataset,
            split=args.split,
        )

        if args.verbose:
            print(f"Loaded {len(evaluator.predictions)} predictions")
            print(f"Loaded {len(evaluator.references)} references")

        print("Computing evaluation scores...")
        results = evaluator.score()

        print("\n" + "=" * 35)
        print("TiQuAD EVALUATION RESULTS")
        print("=" * 35)
        print(f"Exact Match (EM): {results['em']:.4f} ({results['em'] * 100:.2f}%)")
        print(f"F1 Score:         {results['f1']:.4f} ({results['f1'] * 100:.2f}%)")
        print(f"Questions evaluated: {results['num_evaluated']}")

        if args.verbose:
            print(f"Total predictions: {results['total_predictions']}")
            print(f"Total references:  {results['total_references']}")
            if results["num_evaluated"] != results["total_predictions"]:
                missing_refs = results["total_predictions"] - results["num_evaluated"]
                print(f"Missing references: {missing_refs}")
            if results["num_evaluated"] != results["total_references"]:
                missing_preds = results["total_references"] - results["num_evaluated"]
                print(f"Missing predictions: {missing_preds}")

        print("=" * 35)
    except Exception as e:
        print(f"Error during evaluation: {e}")
        exit(1)


if __name__ == "__main__":
    main()
