from docxtpl import DocxTemplate
import io


def format_todos(todos):
    lines: list[str] = todos.split("\n")
    lines = [line.strip().lstrip("-").lstrip() for line in lines]
    return "\n".join(["    -  " + line for line in lines])


def holiday_check(school):
    holiday = school.split("\n")[0]
    if "ferien" in holiday.lower():
        return "Ferien"
    else:
        return school

def prepare_data(content):
    point = content["point"]
    if point:
        length = len(content["todos"].split("\n"))
        point = "\n".join([point for _ in range(length)])

    return {
        "name": content["name"],
        "department": content["department"],
        "nr": str(content["berichtNummer"]),
        "kw": content["date"],
        "todo": format_todos(content["todos"]),
        "weekly": content["weekly_theme"],
        "school": holiday_check(content["school"]),
        "four": point
    }


def fill_doc(content, path):
    file_stream = io.BytesIO()
    doc = DocxTemplate(path)
    doc.render(
        prepare_data(content)
    )

    doc.save(file_stream)
    file_stream.seek(0)

    return file_stream.getvalue()
