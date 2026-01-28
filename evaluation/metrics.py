def check_follow_up(response: str) -> bool:
    return response.strip().endswith("?")

def check_min_length(response: str, min_chars=200) -> bool:
    return len(response.strip()) >= min_chars

def check_code_blocks(response: str) -> bool:
    return "```" in response
