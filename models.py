from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer,
                primary_key=True,
                autoincrement=True)
    id_user = Column(Integer,
                     unique=True)
    tg_username = Column(String,
                         default=None,
                         nullable=True)
    tg_fullname = Column(String,
                         default=None,
                         nullable=True)
    is_yoga_access = Column(Boolean,
                            default=False)
    date_end_yoga = Column(Date,
                           nullable=True,
                           default=None)
    is_last_client = Column(Boolean,
                            default=False)
    is_subscriber = Column(Boolean,
                           default=False)
    phone = Column(String,
                   nullable=True,
                   default=None)
