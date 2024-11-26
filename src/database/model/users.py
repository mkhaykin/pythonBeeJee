from flask_login import UserMixin
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from src.database.model.base import BaseModel


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=False,
        server_default="f",
    )

    __table_args__ = (UniqueConstraint("name", name="uc_name"),)

    def __repr__(self) -> str:
        return self.name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def change_password(self, password_old: str, password_new: str) -> None:
        if self.check_password(password_old):
            self.set_password(password_new)
