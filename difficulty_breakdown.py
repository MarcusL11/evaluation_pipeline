import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def run_difficulty_analysis(date):
    """Generate difficulty breakdown analysis for the given evaluation run."""
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

    # Mean scores per variant
    summary = df.groupby("variant")[score_cols].mean().round(2)
    summary["Overall"] = summary[score_cols].mean(axis=1).round(2)
    summary.columns = [c.replace("_score", "") for c in summary.columns]
    print(summary.to_string())
    print()

    # Average overall score by variant and difficulty
    df["Overall_score"] = df[score_cols].mean(axis=1)

    difficulty_breakdown = df.pivot_table(
        values="Overall_score",
        index="difficulty",
        columns="variant",
        aggfunc="mean",
    ).round(2)

    # Order rows logically
    difficulty_order = ["easy", "medium", "hard", "edge_case"]
    difficulty_breakdown = difficulty_breakdown.reindex(
        [d for d in difficulty_order if d in difficulty_breakdown.index]
    )

    print("Overall Score by Variant x Difficulty")
    print(difficulty_breakdown.to_string())

    # --- Chart 1: Variant x Difficulty heatmap ---
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    im = ax1.imshow(difficulty_breakdown.values, cmap="RdYlGn", aspect="auto", vmin=1, vmax=5)
    ax1.set_xticks(range(len(difficulty_breakdown.columns)))
    ax1.set_xticklabels(difficulty_breakdown.columns, rotation=30, ha="right")
    ax1.set_yticks(range(len(difficulty_breakdown.index)))
    ax1.set_yticklabels(difficulty_breakdown.index)
    for i in range(len(difficulty_breakdown.index)):
        for j in range(len(difficulty_breakdown.columns)):
            val = difficulty_breakdown.iloc[i, j]
            ax1.text(j, i, f"{val:.2f}", ha="center", va="center", fontweight="bold",
                     color="white" if val < 2.5 else "black")
    ax1.set_title("Overall Score by Variant x Difficulty")
    fig1.colorbar(im, ax=ax1, label="Mean Score (1-5)")
    plt.tight_layout()
    heatmap_path = f"output/{date}/variant_difficulty_heatmap.png"
    plt.savefig(heatmap_path)
    plt.show()
    print(f"Saved: {heatmap_path}")

    # Model x difficulty pivot table
    if "model" in df.columns:
        print("\n" + "=" * 60)
        print("Overall Score by Model x Difficulty")
        model_difficulty = df.pivot_table(
            values="Overall_score",
            index="difficulty",
            columns="model",
            aggfunc="mean",
        ).round(2)
        model_difficulty = model_difficulty.reindex(
            [d for d in difficulty_order if d in model_difficulty.index]
        )
        print(model_difficulty.to_string())

        # --- Chart 2: Model x Difficulty grouped bar chart ---
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        models = list(model_difficulty.columns)
        difficulties = list(model_difficulty.index)
        x = np.arange(len(difficulties))
        width = 0.8 / len(models)
        colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]
        for i, model in enumerate(models):
            offset = (i - len(models) / 2 + 0.5) * width
            scores = [model_difficulty.loc[d, model] for d in difficulties]
            bars = ax2.bar(x + offset, scores, width, label=model, color=colors[i % len(colors)])
            for bar, score in zip(bars, scores):
                ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03,
                         f"{score:.2f}", ha="center", va="bottom", fontsize=8)
        ax2.set_xticks(x)
        ax2.set_xticklabels(difficulties)
        ax2.set_ylabel("Mean Overall Score (1-5)")
        ax2.set_ylim(1, 5.5)
        ax2.set_title("Model Performance by Difficulty Level")
        ax2.legend()
        plt.tight_layout()
        model_diff_path = f"output/{date}/model_difficulty_bars.png"
        plt.savefig(model_diff_path)
        plt.show()
        print(f"Saved: {model_diff_path}")

    # Cost summary by model
    if "model" in df.columns and "total_cost_usd" in df.columns:
        print("\n" + "=" * 60)
        print("Cost Summary by Model")
        cost_summary = df.groupby("model").agg(
            total_cost=("total_cost_usd", "sum"),
            mean_cost_per_eval=("total_cost_usd", "mean"),
            num_evals=("total_cost_usd", "count"),
        ).round(6)
        print(cost_summary.to_string())

        # --- Chart 3: Cost efficiency bar chart ---
        fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(12, 5))
        models = cost_summary.index.tolist()
        colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]

        # Total cost per model
        bars_total = ax3a.bar(models, cost_summary["total_cost"], color=colors[: len(models)])
        for bar, val in zip(bars_total, cost_summary["total_cost"]):
            ax3a.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.0001,
                      f"${val:.4f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
        ax3a.set_ylabel("Total Cost (USD)")
        ax3a.set_title("Total Cost by Model")
        ax3a.tick_params(axis="x", rotation=15)

        # Mean cost per eval
        bars_mean = ax3b.bar(models, cost_summary["mean_cost_per_eval"], color=colors[: len(models)])
        for bar, val in zip(bars_mean, cost_summary["mean_cost_per_eval"]):
            ax3b.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.00001,
                      f"${val:.6f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
        ax3b.set_ylabel("Mean Cost per Evaluation (USD)")
        ax3b.set_title("Mean Cost per Evaluation by Model")
        ax3b.tick_params(axis="x", rotation=15)

        plt.tight_layout()
        cost_path = f"output/{date}/cost_efficiency_bars.png"
        plt.savefig(cost_path)
        plt.show()
        print(f"Saved: {cost_path}")

    # Best case
    best_idx = df["Overall_score"].idxmax()
    best_row = df.loc[best_idx]
    print("=" * 60)
    print(f"BEST CASE — {best_row['variant']} on Q{best_row['question_id']}")
    print(f"Overall Score: {best_row['Overall_score']:.2f}")
    print(f"Question: {best_row['question']}")
    print(f"\nResponse (first 400 chars):\n{best_row['response'][:400]}...")
    print(f"\nJudge Reasoning: {best_row['reasoning'][:300]}...")

    print("\n" + "=" * 60)

    # Worst case
    worst_idx = df["Overall_score"].idxmin()
    worst_row = df.loc[worst_idx]
    print(f"WORST CASE — {worst_row['variant']} on Q{worst_row['question_id']}")
    print(f"Overall Score: {worst_row['Overall_score']:.2f}")
    print(f"Question: {worst_row['question']}")
    print(f"\nResponse (first 400 chars):\n{worst_row['response'][:400]}...")
    print(f"\nJudge Reasoning: {worst_row['reasoning'][:300]}...")

    off_topic = df[df["category"] == "off_topic"]

    for _, row in off_topic.iterrows():
        print(f"\n{'=' * 60}")
        print(f"Variant: {row['variant']}")
        print(
            f"Scores — Coherence: {row['Coherence_score']}, Relevance: {row['Relevance_score']}, "
            f"Fluency: {row['Fluency_score']}, Consistency: {row['Consistency_score']}"
        )
        print(f"Overall: {row['Overall_score']:.2f}")
        print(f"\nResponse:\n{row['response'][:400]}")
        print(f"\nJudge Reasoning: {row['reasoning'][:200]}")

    print(f"\nTotal evaluations: {len(df)}")
    print(f"Variants tested: {df['variant'].nunique()}")
    print(f"Parse errors: {df['parse_error'].sum()}")
    print(f"\nBest variant: {summary['Overall'].idxmax()} ({summary['Overall'].max():.2f})")
    print("\n--- Summary ---")
    print(summary.to_string())


if __name__ == "__main__":
    date = input("date of csv file to analyze (e.g. 2024-06-01_12-00-00): ")
    run_difficulty_analysis(date)
