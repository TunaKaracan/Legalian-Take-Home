from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Node(Base):
    __tablename__ = 'nodes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
