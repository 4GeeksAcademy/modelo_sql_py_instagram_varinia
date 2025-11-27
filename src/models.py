from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from sqlalchemy import Enum
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firts_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    comentarios: Mapped[List["Comment"]] = relationship()
    publicaciones: Mapped[List["Post"]] = relationship()
    seguidores: Mapped[List["Follower"]] = relationship()


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_name": self.user_name,
            "firts_name": self.firts_name,
            "last_name": self.last_name,
            # do not serialize the password, its a security breach
        }
class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=True)
    comentarios: Mapped["User"] = relationship(back_populates="Comment")
    opinion: Mapped["Post"] = relationship(back_populates="Comment")

    def serialize(self):
        return {
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    publicaciones: Mapped["User"] = relationship(back_populates="Post")
    opinion: Mapped[List["Comment"]] = relationship()
    archivos: Mapped[List["Media"]] = relationship()

    def serialize(self):
        return {
            "user_id": self.user_id,
            
        }
class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    seguidores: Mapped["User"] = relationship(back_populates="Follower")

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
        }
class MediaType (enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    GIFT =  "gift"

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(200), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=True)
    archivos: Mapped["Post"] = relationship(back_populates="Media")

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "type": self.type,
            "post_id": self.post_id,
        }
