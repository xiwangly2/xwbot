# CQ
class MessageBuilder:
    @staticmethod
    def text(text):
        return {
            "type": "text",
            "data": {
                "text": text
            }
        }

    @staticmethod
    def face(face_id):
        return {
            "type": "face",
            "data": {
                "id": face_id
            }
        }

    @staticmethod
    def image(file, name="", summary="", sub_type="", file_id="", url="", path="", file_size="", file_unique=""):
        return {
            "type": "image",
            "data": {
                "name": name,
                "summary": summary,
                "file": file,
                "sub_type": sub_type,
                "file_id": file_id,
                "url": url,
                "path": path,
                "file_size": file_size,
                "file_unique": file_unique
            }
        }

    @staticmethod
    def record(file, name="", url="", path="", file_id="", file_size="", file_unique=""):
        return {
            "type": "record",
            "data": {
                "file": file,
                "name": name,
                "url": url,
                "path": path,
                "file_id": file_id,
                "file_size": file_size,
                "file_unique": file_unique
            }
        }

    @staticmethod
    def video(file, name="", thumb="", url="", path="", file_id="", file_size="", file_unique=""):
        return {
            "type": "video",
            "data": {
                "file": file,
                "name": name,
                "thumb": thumb,
                "url": url,
                "path": path,
                "file_id": file_id,
                "file_size": file_size,
                "file_unique": file_unique
            }
        }

    @staticmethod
    def at(qq):
        return {
            "type": "at",
            "data": {
                "qq": qq
            }
        }

    @staticmethod
    def rps(result):
        return {
            "type": "rps",
            "data": {
                "result": result
            }
        }

    @staticmethod
    def dice(result):
        return {
            "type": "dice",
            "data": {
                "result": result
            }
        }

    @staticmethod
    def contact(contact_type, contact_id):
        return {
            "type": "contact",
            "data": {
                "type": contact_type,
                "id": contact_id
            }
        }

    @staticmethod
    def music(music_type, music_id="", url="", audio="", title="", image="", singer=""):
        return {
            "type": "music",
            "data": {
                "type": music_type,
                "id": music_id,
                "url": url,
                "audio": audio,
                "title": title,
                "image": image,
                "singer": singer
            }
        }

    @staticmethod
    def reply(reply_id):
        return {
            "type": "reply",
            "data": {
                "id": reply_id
            }
        }

    @staticmethod
    def forward(forward_id, content=None):
        if content is None:
            content = []
        return {
            "type": "forward",
            "data": {
                "id": forward_id,
                "content": content
            }
        }

    @staticmethod
    def node(node_id="", content=None, user_id="", nickname=""):
        if content is None:
            content = []
        return {
            "type": "node",
            "data": {
                "id": node_id,
                "content": content,
                "user_id": user_id,
                "nickname": nickname
            }
        }

    @staticmethod
    def json(data):
        return {
            "type": "json",
            "data": {
                "data": data
            }
        }

    @staticmethod
    def mface(emoji_id, emoji_package_id, key, summary=""):
        return {
            "type": "mface",
            "data": {
                "emoji_id": emoji_id,
                "emoji_package_id": emoji_package_id,
                "key": key,
                "summary": summary
            }
        }

    @staticmethod
    def file(name="", file="empty", path="empty", url="empty", file_id="empty", file_size="empty", file_unique="empty"):
        return {
            "type": "file",
            "data": {
                "name": name,
                "file": file,
                "path": path,
                "url": url,
                "file_id": file_id,
                "file_size": file_size,
                "file_unique": file_unique
            }
        }

    @staticmethod
    def xml(data):
        return {
            "type": "xml",
            "data": {
                "data": data
            }
        }
