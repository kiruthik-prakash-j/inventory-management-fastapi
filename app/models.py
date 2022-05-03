
from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, nullable=False)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, server_default='0')
    row_no = Column(Integer, nullable=False)
    column_no = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    is_empty = Column(Boolean, nullable=False, server_default='TRUE')