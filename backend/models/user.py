from models import Base
from pwdlib import PasswordHash
from sqlalchemy import Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

password_hash = PasswordHash.recommended()


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    username: Mapped[str] = mapped_column(String(100))
    _password: Mapped[str] = mapped_column(String(200))

    def __init__(self, **kw):
        super().__init__(**kw)
        password = kw.pop("password")
        if password:
            self.password = password

    @property
    def password(self):
        return self._password

    @property.setter
    def password(self, rawpassword):
        self._password = password_hash.hash(rawpassword)
    
    def verify_password(self,rawpassword):
        return password_hash.verify(rawpassword,self.password)
    
class EmailCode(Base):
    __tablename__= 'emailcode'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    code: Mapped[int] = mapped_column(Integer(10))
    create_time: Mapped[datetime] = mapped_column(DateTime)