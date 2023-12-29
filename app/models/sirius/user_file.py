from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.meta import Base, DEFAULT_SCHEMA


class UserFile(Base):
    __tablename__ = 'user_file'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[str] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.user.id'))

    file_id: Mapped[str] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.file.id'))
