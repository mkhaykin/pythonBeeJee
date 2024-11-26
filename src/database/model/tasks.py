from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from src.database.model.base import BaseModel
from src.database.model.mixin_id import MixinID
from src.database.model.mixin_ts import MixinTimeStamp


class Task(BaseModel, MixinID, MixinTimeStamp):
    __tablename__ = "tasks"
    user_name: Mapped[str] = mapped_column(
        String(30),
        unique=False,
        index=True,
        nullable=False,
    )

    user_email: Mapped[str] = mapped_column(
        String(100),
        unique=False,
        index=True,
        nullable=False,
    )

    text: Mapped[str] = mapped_column(
        TEXT,
        unique=False,
        index=False,
        nullable=False,
    )

    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
