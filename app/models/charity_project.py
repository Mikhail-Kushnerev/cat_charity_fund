from sqlalchemy import Column, String, Text

from app.core.db import Base
from .general import General


class CharityProject(General, Base):

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
