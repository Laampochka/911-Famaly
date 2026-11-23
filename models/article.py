# from services.db import Db

from models.active_record_entity import ActiveRecordEntity
from models.user import User
import cgi
import os
import uuid
import mimetypes

from exceptions import InvalidArgumentException


MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_MIME_TYPES = {'image/png', 'image/jpeg', 'image/gif', 'image/webp'}

class Article(ActiveRecordEntity):
    __tablename__ = 'articles'
    _id = None
    _author_id = None
    _name = None
    _text = None
    _created_at = None
    _img = None

    def get_author_id(self):
        return self._author_id



    def get_author(self):
        return User.get_by_id(self._author_id)
    
    def get_text(self):
        return self._text

    def get_img(self):
        return getattr(self, '_img', None)

    def get_name(self):
        return self._name

    def get_created_at(self):
        return self._created_at

    def set_author_id(self,_author_id):
        self._author_id = _author_id

    def set_name(self,name):
        self._name = name

    def set_text(self,text):
        self._text = text

    def set_created_at(self,created_at):
        self._created_at = created_at


    @staticmethod
    def get_table_name():
        return 'articles'
    
    @staticmethod
    def search_by_name(search_string):
        return __class__.search('name', search_string)



    # @staticmethod
    # def create(fields, img_file, author):
    #     if not fields['name']:
    #         raise InvalidArgumentException('не передано название статьи')

    #     if not fields['text']:
    #         raise InvalidArgumentException('не передан текст статьи')

    #     if __class__.check_file_size(img_file, MAX_FILE_SIZE)[0] == False :
    #         raise InvalidArgumentException('Слишком большой файл! Должно быть не более 5МБ')


    #     article = Article()
    #     article._name = fields['name']
    #     article._text = fields['text']
    #     article._author_id = author.get_id()

    #     if img_file.filename:
    #         file_path = 'uploads/' +  img_file.filename
    #         article._img = file_path
    #         os.makedirs('/uploads', exist_ok=True)
    #         with open(file_path, 'wb') as f:
    #             while True:
    #                 chunk = img_file.file.read(8192)  # Читаем файл по частям
    #                 if not chunk:
    #                     break
    #                 f.write(chunk)

    #     article.save()
    #     return article

    @staticmethod
    def create(fields, img_file, author):
        if not fields.get('name'):
            raise InvalidArgumentException('не передано название статьи')

        if not fields.get('text'):
            raise InvalidArgumentException('не передан текст статьи')

        # --- проверки файла ---
        # ВАЖНО: не "if img_file:", а "if img_file is not None"
        if img_file is not None and getattr(img_file, 'filename', ''):
            # 1) расширение
            if not __class__.check_file_extension(img_file.filename):
                raise InvalidArgumentException(
                    'Недопустимый формат. Разрешены: png, jpg, jpeg, gif, webp'
                )

            # 2) MIME по сигнатуре
            if not __class__.check_file_mime(img_file):
                raise InvalidArgumentException(
                    'Содержимое файла не является изображением'
                )

            # 3) размер
            ok, size = __class__.check_file_size(img_file, MAX_FILE_SIZE)
            if not ok:
                raise InvalidArgumentException(
                    f'Слишком большой файл ({size // 1024} КБ). Максимум 5 МБ'
                )

        article = Article()
        article._name = fields['name']
        article._text = fields['text']
        article._author_id = author.get_id()

        if img_file is not None and getattr(img_file, 'filename', ''):
            upload_dir = os.path.join(os.getcwd(), 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            safe_name = __class__.generate_safe_filename(img_file.filename)
            file_path = os.path.join(upload_dir, safe_name)

            img_file.file.seek(0)
            with open(file_path, 'wb') as f:
                while True:
                    chunk = img_file.file.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)

            article._img = 'uploads/' + safe_name

        article.save()
        return article


    @staticmethod
    def check_file_extension(filename: str) -> bool:
        """Проверка расширения файла."""
        if not filename or '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in ALLOWED_EXTENSIONS


    @staticmethod
    def check_file_mime(file_item) -> bool:
        """Проверка MIME-типа по содержимому (первые байты)."""
        current_pos = file_item.file.tell()
        try:
            file_item.file.seek(0)
            header = file_item.file.read(32)
        finally:
            file_item.file.seek(current_pos)

        
        if header.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'image/png' in ALLOWED_MIME_TYPES
        if header.startswith(b'\xff\xd8\xff'):
            return 'image/jpeg' in ALLOWED_MIME_TYPES
        if header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
            return 'image/gif' in ALLOWED_MIME_TYPES
        if header[:4] == b'RIFF' and header[8:12] == b'WEBP':
            return 'image/webp' in ALLOWED_MIME_TYPES
        return False


    @staticmethod
    def check_file_size(file_item, max_size):
        """
        Проверка размера файла без загрузки всего файла в память.
        Читает файл по частям и суммирует их размер.
        """
        total_size = 0
        chunk_size = 8192  # Читаем по 8KB

        # Сохраняем текущую позицию, чтобы потом вернуться
        current_pos = file_item.file.tell()

        try:
            # Перемещаемся в начало файла
            file_item.file.seek(0)

            # Читаем файл по частям и суммируем размер
            while True:
                chunk = file_item.file.read(chunk_size)
                if not chunk:
                    break
                total_size += len(chunk)

                # Если уже превысили лимит, можно прервать проверку
                if total_size > max_size:
                    break
        finally:
            # Возвращаемся на исходную позицию для последующего чтения
            file_item.file.seek(current_pos)
        print(total_size)
        return total_size <= max_size, total_size



    @staticmethod
    def generate_safe_filename(original_name: str) -> str:
        """
        Генерирует безопасное имя файла:
        - сохраняет расширение (только из ALLOWED_EXTENSIONS)
        - заменяет имя на UUID, чтобы избежать path traversal
          ('../../etc/passwd'), коллизий и проблем с юникодом/пробелами
        """
        if not original_name or '.' not in original_name:
            raise InvalidArgumentException('Недопустимое имя файла')

        ext = original_name.rsplit('.', 1)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise InvalidArgumentException('Недопустимый формат файла')

        return f"{uuid.uuid4().hex}.{ext}"    