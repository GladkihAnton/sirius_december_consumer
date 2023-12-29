from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.meta import Base, DEFAULT_SCHEMA


class File(Base):
    __tablename__ = 'file'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    url: Mapped[str] = mapped_column(Text)
    task_id: Mapped[str] = mapped_column(String)
