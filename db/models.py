from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
import datetime


class Order(Base):
    __tablename__ = 'order'
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[str]
    start_date: Mapped[datetime.datetime]
    end_date: Mapped[datetime.datetime]
    is_sended: Mapped[int]
    sended_notif: Mapped[int]
    client_id: Mapped[int] = mapped_column(
        ForeignKey("client.id", ondelete="CASCADE"))


class Client(Base):
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str]
    user_name: Mapped[str]
