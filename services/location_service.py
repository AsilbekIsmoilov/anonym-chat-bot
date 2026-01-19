class LocationService:
    GROUPS = {
        "uz": {
            "group_id": -1001111111111,
            "invite": "https://t.me/+xxxx"
        },
        "ru": {
            "group_id": -1002222222222,
            "invite": "https://t.me/+yyyy"
        },
        "kz": {
            "group_id": -1003333333333,
            "invite": "https://t.me/+zzzz"
        },
        "kr": {
            "group_id": -1004444444444,
            "invite": "https://t.me/+aaaa"
        },
    }

    @classmethod
    def get_group(cls, location: str):
        return cls.GROUPS[location]
