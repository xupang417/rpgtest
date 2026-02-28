def validate_required_dict_keys(obj: dict, keys: list[str], prefix: str = ""):
    missing = [k for k in keys if k not in obj]
    if missing:
        raise ValueError(f"{prefix} missing keys: {missing}")