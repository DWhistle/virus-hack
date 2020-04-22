class YoutubeUploadException(Exception):
    """
    Кидается в случае, если выгрузка видео на ютуб не удалась
    """
    pass


class DbException(Exception):
    """
    Кидается в случае, если проблема с базой
    """
    pass
