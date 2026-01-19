def detect_location(phone: str) -> str | None:
    phone = phone.replace(" ", "").replace("-", "")

    if phone.startswith("+998"):
        return "uz"
    if phone.startswith("+996"):
        return "kyr"
    if phone.startswith("+7"):
        return "ru"
    return None
