from datetime import datetime

from pwdlib import PasswordHash
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models import Base


password_hash = PasswordHash.recommended()


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100))
    _password: Mapped[str] = mapped_column("password", String(200))

    def __init__(self, password: str, **kwargs):
        super().__init__(**kwargs)
        self.password = password

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, raw_password: str) -> None:
        self._password = password_hash.hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        return password_hash.verify(raw_password, self.password)


class EmailCode(Base):
    __tablename__ = "email_code"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    code: Mapped[str] = mapped_column(String(10))
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
