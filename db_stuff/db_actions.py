import dataclasses
from tinydb import TinyDB, Query
from datetime import date

db = TinyDB("db.json")

user_db = db.table("user")
file_db = db.table("file")


def save_file(file_name: str, author):
    parts = file_name.split(".")
    d = date.today().strftime("%d.%m")
    file = File(id="aslndla", name=parts[0], full_name=file_name, date=d, author=author, ending=parts[-1])

    file_db.insert(file.to_json())
    return file


def get_user(user_name, password):
    user = user_db.search(Query().fragment({"name": user_name, "password": password}))
    if any(user):
        return True
    else:
        return False


def del_file(name):
    res = file_db.remove(Query().full_name == name)
    return any(res)


def get_files():
    return file_db.all()


def add_users():
    users = [User(name="justin", password="9_eWSuyna*9+ym7CMMZc-wV-_+7zEx", id="3"), User(name="justin_r", password="tobi", id="_5&m-QpHdxmE_=S^bJxw6@w97e*AtH")]

    for u in users:
        user_db.insert(u.to_json())


@dataclasses.dataclass
class File:
    id: str
    name: str
    full_name: str
    date: str
    author: str
    ending: str

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "full_name": self.full_name,
            "ending": self.ending
        }


def json_to_file(data):
    return File(
        id=data["id"],
        name=data["name"],
        full_name=data["full_name"],
        date=data["date"],
        author=data["author"],
        ending=data["ending"]
    )

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
