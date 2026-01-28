from evaluation.metrics import *

def score_response(response: str) -> dict:
    return {
        "has_follow_up": check_follow_up(response),
        "sufficient_detail": check_min_length(response),
        "contains_code": check_code_blocks(response),
    }