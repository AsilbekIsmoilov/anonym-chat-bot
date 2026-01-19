from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from storage.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    location: Mapped[str] = mapped_column(String(2))
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
