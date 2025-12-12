from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Text, ForeignKey

class Brand(db.Model):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    phones: Mapped[list["Phone"]] = relationship("Phone", back_populates="brand")

    def __repr__(self):
        return self.name

class Phone(db.Model):
    __tablename__ = "phones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), nullable=False)
    brand: Mapped["Brand"] = relationship("Brand", back_populates="phones")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner = relationship("User", backref="phones")

    def __repr__(self):
        return f"<Phone {self.model_name}>"