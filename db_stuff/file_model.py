import dataclasses


@dataclasses.dataclass
class File:
    id: str
    name: str
    date: str
    ending: str

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "ending": self.ending
        }


def json_to_file(data):
    return File(
        id=data["id"],
        name=data["name"],
        date=data["date"],
        ending=data["ending"]
    )
