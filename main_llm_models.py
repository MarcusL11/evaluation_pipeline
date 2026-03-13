from prompts import TEST_CASES, PROMPTS
from eval import evaluate_response, parse_judge_output
from openai_client import client
from openai_models import CHATBOT_MODELS, JUDGE_MODEL
from costs import calculate_cost
import pandas as pd
import datetime
import os


def get_career_advice(question: str, system_prompt: str, model: str):
    """Send a career question to the chatbot and return (content, cost_info)."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    usage = response.usage
    cost_usd = calculate_cost(usage.prompt_tokens, usage.completion_tokens, model)
    cost_info = {
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
        "cost_usd": cost_usd,
    }
    return response.choices[0].message.content, cost_info


def run_evaluation():
    """Run the full evaluation pipeline. Returns the output folder date string."""
    results = []
    total = len(CHATBOT_MODELS) * len(PROMPTS) * len(TEST_CASES)
    current = 0
    total_cost = 0.0

    for model_name in CHATBOT_MODELS:
        for variant_name, system_prompt in PROMPTS.items():
            for tc in TEST_CASES:
                current += 1
                print(
                    f"[{current}/{total}] {model_name} | {variant_name} — Q{tc['id']} ({tc['category']})"
                )

                # Get chatbot response
                response, chatbot_cost = get_career_advice(
                    tc["question"], system_prompt, model_name
                )

                # Judge the response
                judge_output, judge_cost = evaluate_response(
                    tc["question"], response, tc["key_aspects"]
                )
                parsed = parse_judge_output(judge_output)

                eval_total_cost = chatbot_cost["cost_usd"] + judge_cost["cost_usd"]
                total_cost += eval_total_cost

                # Store everything
                row = {
                    "model": model_name,
                    "variant": variant_name,
                    "question_id": tc["id"],
                    "category": tc["category"],
                    "difficulty": tc["difficulty"],
                    "question": tc["question"],
                    "response": response,
                    "judge_output": judge_output,
                    "reasoning": parsed["reasoning"],
                    "parse_error": parsed["parse_error"],
                    "chatbot_prompt_tokens": chatbot_cost["prompt_tokens"],
                    "chatbot_completion_tokens": chatbot_cost["completion_tokens"],
                    "chatbot_cost_usd": chatbot_cost["cost_usd"],
                    "judge_prompt_tokens": judge_cost["prompt_tokens"],
                    "judge_completion_tokens": judge_cost["completion_tokens"],
                    "judge_cost_usd": judge_cost["cost_usd"],
                    "total_cost_usd": eval_total_cost,
                }
                for dim in ["Coherence", "Relevance", "Fluency", "Consistency"]:
                    row[f"{dim}_score"] = parsed[dim]["score"]
                    row[f"{dim}_justification"] = parsed[dim]["justification"]

                results.append(row)

    df = pd.DataFrame(results)

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(f"output/{now}", exist_ok=True)
    output_path = f"output/{now}/evaluation_results.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"\nDone! {len(df)} evaluations completed.")
    print(f"Parse errors: {df['parse_error'].sum()}")

    # Cost summary
    print(f"\n{'=' * 60}")
    print("COST SUMMARY")
    print(f"{'=' * 60}")
    cost_by_model = df.groupby("model")[["chatbot_cost_usd", "judge_cost_usd", "total_cost_usd"]].sum()
    print(cost_by_model.to_string())
    print(f"\nTotal cost: ${total_cost:.6f}")
    print(f"Output saved to: {output_path}")

    return now


if __name__ == "__main__":
    run_evaluation()
