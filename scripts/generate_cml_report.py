import json
import os
from pathlib import Path
from typing import Dict, List


METRICS_DIR = Path("metrics")
REPORTS_DIR = Path("reports")
OUTPUT_PATH = REPORTS_DIR / "cml_report.md"


def load_json(path: Path) -> Dict:
    with path.open() as f:
        return json.load(f)


def parse_classification_report(report_str: str) -> List[Dict[str, str]]:
    """Parse the sklearn classification report string into rows."""
    rows: List[Dict[str, str]] = []
    for line in report_str.splitlines():
        stripped = line.strip()
        # Skip headers or blank lines
        if not stripped or stripped.startswith("precision") or stripped.startswith("accuracy"):
            continue
        parts = stripped.split()
        # Expect rows like: class precision recall f1-score support
        if len(parts) >= 5 and parts[0].replace(".", "", 1).isdigit():
            label, precision, recall, f1_score, support = parts[:5]
            rows.append(
                {
                    "label": label,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1_score,
                    "support": support,
                }
            )
        elif len(parts) >= 5 and parts[0] in {"macro", "weighted"}:
            # macro avg, weighted avg
            label = f"{parts[0]} {parts[1]}"
            precision, recall, f1_score, support = parts[2:6]
            rows.append(
                {
                    "label": label,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1_score,
                    "support": support,
                }
            )
    return rows


def build_markdown(train_metrics: Dict, eval_metrics: Dict) -> str:
    eval_accuracy = eval_metrics.get("accuracy_full_data")
    test_accuracy = train_metrics.get("accuracy_test")
    classification_report = eval_metrics.get("classification_report", "")

    lines: List[str] = ["# Rapport CML", ""]

    lines.append("## Métriques globales")
    if eval_accuracy is not None:
        lines.append(f"- Training accuracy: **{eval_accuracy:.3f}**")
    if test_accuracy is not None:
        lines.append(f"- Test accuracy: **{test_accuracy:.3f}**")
    lines.append("")

    rows = parse_classification_report(classification_report)
    if rows:
        lines.append("## Métriques par classe")
        lines.append("| Classe | Précision | Rappel | F1-score | Effectif |")
        lines.append("| --- | --- | --- | --- | --- |")
        for row in rows:
            lines.append(
                f"| {row['label']} | {row['precision']} | {row['recall']} | {row['f1_score']} | {row['support']} |"
            )
        lines.append("")

    lines.append("## Configuration d'entraînement")
    for key in ["n_estimators", "max_depth", "test_size", "random_state"]:
        if key in train_metrics:
            lines.append(f"- {key}: `{train_metrics[key]}`")

    return "\n".join(lines) + "\n"


def main() -> None:
    train_metrics = load_json(METRICS_DIR / "train_metrics.json")
    eval_metrics = load_json(METRICS_DIR / "eval_metrics.json")

    report_text = build_markdown(train_metrics, eval_metrics)

    os.makedirs(REPORTS_DIR, exist_ok=True)
    OUTPUT_PATH.write_text(report_text)
    print(f"Report written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
