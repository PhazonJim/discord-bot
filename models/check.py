import hashlib


class Check:
    def __init__(
        self,
        sphere: str,
        finder: str,
        receiver: str,
        item: str,
        location: str,
        game: str,
        **kwargs,
    ):
        self.sphere = sphere
        self.finder = finder
        self.receiver = receiver
        self.item = item
        self.location = location
        self.game = game

        self.check_id = hashlib.sha256(f"{sphere}.{finder}.{receiver}.{item}.{location}.{game}".encode()).hexdigest()

    def __str__(self) -> str:
        return f"Item: {self.item}\nPlayer: {self.receiver}"

    def as_dict(self) -> dict:
        return {
            "check_id": self.check_id,
            "sphere": self.sphere,
            "finder": self.finder,
            "receiver": self.receiver,
            "item": self.item,
            "location": self.location,
            "game": self.game,
        }
