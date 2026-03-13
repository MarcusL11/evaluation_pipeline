from prompts import JUDGE_PROMPT_TEMPLATE
from openai_client import client
from openai_models import JUDGE_MODEL
from costs import calculate_cost


def evaluate_response(question: str, response: str, key_aspects: str, judge_model=None):
    """Use the LLM judge to evaluate a chatbot response.

    Returns (content, cost_info) where cost_info is a dict with token counts and cost.
    """
    model = judge_model or JUDGE_MODEL
    prompt = JUDGE_PROMPT_TEMPLATE.format(
        question=question,
        key_aspects=key_aspects,
        response=response,
    )
    result = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    usage = result.usage
    cost_usd = calculate_cost(usage.prompt_tokens, usage.completion_tokens, model)
    cost_info = {
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
        "cost_usd": cost_usd,
    }
    return result.choices[0].message.content, cost_info


def parse_judge_output(judge_output: str) -> dict:
    """Parse the judge's structured output into a dictionary of scores and justifications.

    Returns a dict like:
    {
        "Coherence": {"score": 4, "justification": "..."},
        "Relevance": {"score": 5, "justification": "..."},
        ...
        "reasoning": "...",
        "parse_error": False
    }
    """
    dimensions = ["Coherence", "Relevance", "Fluency", "Consistency"]
    result = {"reasoning": "", "parse_error": False}

    # Extract reasoning
    if "REASONING:" in judge_output:
        reasoning_start = judge_output.index("REASONING:") + len("REASONING:")
        # Find where the first dimension starts
        first_dim_pos = len(judge_output)
        for dim in dimensions:
            pos = judge_output.find(f"{dim}:")
            if pos != -1 and pos < first_dim_pos and pos > reasoning_start:
                first_dim_pos = pos
        result["reasoning"] = judge_output[reasoning_start:first_dim_pos].strip()

    # Extract each dimension score
    for dim in dimensions:
        try:
            # Find the line with this dimension
            lines = judge_output.split("\n")
            dim_line = None
            for line in lines:
                stripped = line.strip()
                if stripped.startswith(f"{dim}:") or stripped.startswith(f"**{dim}"):
                    dim_line = stripped
                    break

            if dim_line is None:
                raise ValueError(f"Dimension {dim} not found")

            # Parse "Dimension: score | justification"
            after_colon = dim_line.split(":", 1)[1].strip()
            # Remove any markdown bold markers
            after_colon = after_colon.replace("**", "")

            if "|" in after_colon:
                score_part, justification = after_colon.split("|", 1)
            else:
                score_part = after_colon.split()[0]
                justification = after_colon

            # Extract the numeric score
            score_str = "".join(c for c in score_part if c.isdigit())
            score = int(score_str)
            score = max(1, min(5, score))  # clamp to 1-5

            result[dim] = {"score": score, "justification": justification.strip()}
        except (ValueError, IndexError) as e:
            result[dim] = {"score": 3, "justification": f"PARSE ERROR: {e}"}
            result["parse_error"] = True

    return result
