from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from flask_login import UserMixin
from sqlalchemy import DateTime, String
from datetime import datetime, timezone


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    image: Mapped[str] = mapped_column(String(50), nullable=True, default='profile_default.jpg')
    about_me: Mapped[str] = mapped_column(String(140), nullable=True)
    last_seen: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=True 
    )

    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")



    def __repr__(self):
        return f"<User {self.username}>"