from tokencost import calculate_cost_by_tokens


def calculate_cost(prompt_tokens, completion_tokens, model):
    """Calculate the USD cost for a given API call using tokencost."""
    try:
        prompt_cost = calculate_cost_by_tokens(prompt_tokens, model, "input")
        completion_cost = calculate_cost_by_tokens(completion_tokens, model, "output")
        return float(prompt_cost + completion_cost)
    except Exception:
        return 0.0
