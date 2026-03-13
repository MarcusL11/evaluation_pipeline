import pandas as pd
import os
import matplotlib.pyplot as plt
from prompts import PROMPTS


def run_visualization(date):
    """Generate visualization plots for the given evaluation run."""
    full_path = f"output/{date}/evaluation_results.csv"

    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        return

    df = pd.read_csv(full_path)

    score_cols = [
        "Coherence_score",
        "Relevance_score",
        "Fluency_score",
        "Consistency_score",
    ]

    # Include model in score table if available
    display_cols = ["variant", "question_id"]
    if "model" in df.columns:
        display_cols = ["model"] + display_cols
    display_cols += score_cols

    print(df[display_cols].to_string(index=False))

    # Mean scores per variant
    summary = df.groupby("variant")[score_cols].mean().round(2)
    summary["Overall"] = summary[score_cols].mean(axis=1).round(2)
    summary.columns = [c.replace("_score", "") for c in summary.columns]
    print(summary.to_string())
    print()

    # Highlight the winner
    best = summary["Overall"].idxmax()
    print(f"Best overall variant: {best} (Overall = {summary.loc[best, 'Overall']})")

    dimensions = ["Coherence", "Relevance", "Fluency", "Consistency"]
    variants = list(PROMPTS.keys())

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # --- Plot 1: Overall scores ---
    overall_scores = [summary.loc[v, "Overall"] for v in variants]
    colors = ["#4C72B0", "#55A868", "#C44E52"]
    bars = axes[0].bar(variants, overall_scores, color=colors[: len(variants)])
    axes[0].set_ylabel("Mean Score (1-5)")
    axes[0].set_title("Overall Score by Variant")
    axes[0].set_ylim(1, 5.3)
    for bar, score in zip(bars, overall_scores):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            f"{score:.2f}",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    # --- Plot 2: Per-dimension grouped bar chart ---
    x = range(len(dimensions))
    width = 0.25
    for i, variant in enumerate(variants):
        scores = [summary.loc[variant, dim] for dim in dimensions]
        offset = (i - len(variants) / 2 + 0.5) * width
        axes[1].bar(
            [xi + offset for xi in x],
            scores,
            width,
            label=variant,
            color=colors[i % len(colors)],
        )

    axes[1].set_xticks(x)
    axes[1].set_xticklabels(dimensions)
    axes[1].set_ylabel("Mean Score (1-5)")
    axes[1].set_title("Per-Dimension Scores by Variant")
    axes[1].set_ylim(1, 5.3)
    axes[1].legend()

    plt.tight_layout()
    # Save plot to folder
    path = f"output/{date}/summary_plot.png"
    plt.savefig(path)
    plt.show()

    # --- Cost vs Performance scatter plot ---
    if "model" in df.columns and "total_cost_usd" in df.columns:
        df["Overall_score"] = df[
            ["Coherence_score", "Relevance_score", "Fluency_score", "Consistency_score"]
        ].mean(axis=1)

        model_stats = df.groupby("model").agg(
            mean_cost=("total_cost_usd", "mean"),
            mean_score=("Overall_score", "mean"),
        )

        fig2, ax2 = plt.subplots(figsize=(8, 6))
        ax2.scatter(model_stats["mean_cost"], model_stats["mean_score"], s=100, zorder=5)

        for model_name, row in model_stats.iterrows():
            ax2.annotate(
                model_name,
                (row["mean_cost"], row["mean_score"]),
                textcoords="offset points",
                xytext=(10, 5),
                fontsize=10,
                fontweight="bold",
            )

        ax2.set_xlabel("Mean Cost per Evaluation (USD)")
        ax2.set_ylabel("Mean Overall Score (1-5)")
        ax2.set_title("Cost vs Performance by Model")
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        cost_path = f"output/{date}/cost_vs_performance.png"
        plt.savefig(cost_path)
        plt.show()
        print(f"Cost vs performance plot saved to: {cost_path}")


if __name__ == "__main__":
    date = input("date of csv file to analyze (e.g. 2024-06-01_12-00-00): ")
    run_visualization(date)
