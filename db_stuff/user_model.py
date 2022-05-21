import dataclasses


@dataclasses.dataclass
class User:
    id: str
    name: str
    password: str

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password
        }


def json_to_user(data):
    return User(
        id=data["id"],
        name=data["name"],
        password=data["password"]
    )
