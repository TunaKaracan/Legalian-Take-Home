from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Edge(Base):
	__tablename__ = 'edges'

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	from_node_id: Mapped[int] = mapped_column(Integer, ForeignKey('nodes.id', ondelete='CASCADE'))
	to_node_id: Mapped[int] = mapped_column(Integer, ForeignKey('nodes.id', ondelete='CASCADE'))
