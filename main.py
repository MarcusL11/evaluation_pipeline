from main_llm_models import run_evaluation
from visualize import run_visualization
from difficulty_breakdown import run_difficulty_analysis


print("=" * 60)
print("CAREER ADVICE CHATBOT — FULL EVALUATION PIPELINE")
print("=" * 60)

# Step 1: Run evaluations across all models and prompts
print("\n[1/3] Running evaluations...")
date = run_evaluation()

# Step 2: Generate visualization plots
print("\n" + "=" * 60)
print("[2/3] Generating visualizations...")
run_visualization(date)

# Step 3: Generate difficulty breakdown analysis
print("\n" + "=" * 60)
print("[3/3] Generating difficulty breakdown...")
run_difficulty_analysis(date)

print("\n" + "=" * 60)
print("PIPELINE COMPLETE")
print(f"All outputs saved to: output/{date}/")
print("=" * 60)
