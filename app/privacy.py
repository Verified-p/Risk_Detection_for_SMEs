def sanitize(event):
    forbidden = ["password", "content"]
    return {k: v for k, v in event.items() if k not in forbidden}
