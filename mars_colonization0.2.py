import os

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = ("txt", "pdf", "png", "jpg", "jpeg", "gif")


def allowed_file(filename):
    """Функция проверки расширения файла"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)

upload_path = "static/uploads"

app.config["UPLOAD_FOLDER"] = upload_path

files = (
    "promotion_msg.html",
    "image_msg.html",
    "form.html",
    "photo_form.html",
    "carousel.html",
)

file_nav = "./static/navigation-widget.css"

navigation_widget = ""

with open(file_nav, "r") as file:
    navigation_widget = file.read()


@app.route("/")
def greetings():
    return navigation_widget + "Миссия Колонизация Марса"


@app.route("/index")
def index():
    if request.args:
        username = request.args.get("username") or ""
        filename = request.args.get("filename") or ""
        if username and filename:
            return (
                navigation_widget
                + f'''<label>{username}</label></br>
                <img src="{filename}">
                '''
            )
    return navigation_widget + "И на Марсе будут яблони цвести!"


@app.route("/promotion")
def promotion():
    return navigation_widget + render_template(url_for("static", filename=files[0]))


@app.route("/image_mars")
def image_mars():
    return navigation_widget + render_template(url_for("static", filename=files[1]))


@app.route("/astronaut_selection", methods=["POST", "GET"])
def astronaut_selection():
    if request.method == "GET":
        return navigation_widget + render_template(url_for("static", filename=files[2]))
    elif request.method == "POST":
        print(request.form.get("user_surname"))
        print(request.form.get("user_name"))
        print(request.form.get("user_email"))
        print(request.form.get("user_education"))
        print(request.form.get("user_select"))
        print(request.form.get("user_sex"))
        print(request.form.get("user_motivation"))
        print(request.form.get("stay_on_mars"))

        return navigation_widget + "Форма отправлена"


@app.route("/results/<nickname>/<int:level>/<float:rating>")
def results(nickname, level, rating):
    return navigation_widget + f"""</br>{nickname}</br>{level}</br>{rating}"""


@app.route("/photo", methods=["POST", "GET"])
def photo_prepare():
    if request.method == "POST":
        name = request.form.get("name")
        return redirect(url_for("photo", username=name))
    return render_template(url_for("static", filename=files[3]))


@app.route("/photo/<nickname>", methods=["POST", "GET"])
def photo(nickname):
    if request.method == "POST":
        # проверим, передается ли в запросе файл
        if "file" not in request.files:
            # После перенаправления на страницу загрузки
            # покажем сообщение пользователю
            flash("Не могу прочитать файл")
            return redirect(request.url)
        file = request.files["file"]
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == "":
            flash("Нет выбранного файла")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # безопасно извлекаем оригинальное имя файла
            filename = secure_filename(file.filename)
            # сохраняем файл
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            # если все прошло успешно, то перенаправляем
            # на функцию-представление `download_file`
            # для скачивания файла
            return redirect(
                url_for(
                    "index",
                    username=nickname,
                    filename=os.path.join(app.config["UPLOAD_FOLDER"], filename),
                )
            )
    return """
    <!doctype html>
    <title>Загрузить новый файл</title>
    <h1>Загрузить новый файл</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    </html>
    """


@app.route("/carousel")
def carousel_func():
    return render_template(url_for("static", filename=files[-1]))


if __name__ == "__main__":
    app.run(port=8080, host="localhost", debug=True)
