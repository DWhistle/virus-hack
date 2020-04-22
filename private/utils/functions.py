import os
import re

from private.utils.constants import VIDEO_REQUIRED_FIELDS, POSSIBLE_VIDEO_FORMATS


def extract_info_fields(info: dict):
    return {k: v for k, v in info.items() if k in VIDEO_REQUIRED_FIELDS}


def clean_tags(tags: list):
    return [re.sub(r"[;,]", '', tag) for tag in tags]


def resolve_video_path(path: str):
    """
    Если видео смерджилось и первоначальный формат поменялся - ищет новый файл
    :param path: путь к видео
    :return:
    """
    if os.path.isfile(path):
        return path
    splitted_path, extension = list(os.path.splitext(path))
    for ext in POSSIBLE_VIDEO_FORMATS:
        new_file = os.path.join(splitted_path + ext)
        if os.path.isfile(new_file):
            return new_file
    raise FileNotFoundError("Видеоролик не существует или был сконвертирован в неподдерживаемый формат")


def is_response_valid(response_id):
    if type(response_id) is not str:
        return False
    else:
        return True if re.match("^[a-zA-Z0-9_-]{11}$", response_id) else False

