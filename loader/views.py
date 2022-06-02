import os
import random
from flask import Blueprint, render_template, request, current_app
from classes.data_manager import DataManager
from . import upload_manager
from .exceptions import OutOffFreeNamesError, PictureFormatNotSupportedError, PictureNotUploadedError
from .upload_manager import UploadManager

loader_blueprint = Blueprint("loader_blueprint", __name__, template_folder="/templates")



@loader_blueprint.route('/post/', methods=["GET"])
def page_form():
    return render_template("post_form.html")

@loader_blueprint.route('/post/', methods=["POST"])
def page_create_posts():

    path = current_app.config.get("POST_PATH")
    data_manager = DataManager(path)
    upload_manager = UploadManager()

    
    #  Получаем данные
    picture = request.files.get('picture', None)
    content = request.values.get('content', '')

    #  Сохраняем картинку с помощью менеджера загрузок

    filename_saved = upload_manager.save_with_random_name(picture)

    #  Получаем путь для браузера клиента
    web_path = f"/uploads/images/{filename_saved}"

    post = {"pic": web_path, "content": content}

    data_manager.add(post)

    return render_template("post_uploaded.html", pic=web_path, content=content)

@loader_blueprint.errorhandler(OutOffFreeNamesError)
def error_out_of_free_names(e):
    return  "Закончились свободные имена для загрузки картинок, обратитесь к администратору"

@loader_blueprint.errorhandler(PictureFormatNotSupportedError)
def error_format_not_supported(e):
    return  "Формат картинки не поддерживается"

@loader_blueprint.errorhandler(PictureNotUploadedError)
def error_load_file(e):
    return  "Не удалось загрузить картинку"