from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class ShowSeat(Base):
    __tablename__ = "show_seats"
    __table_args__ = (
        UniqueConstraint(
            "show_id",
            "seat_id",
            name="uq_show_seats_show_seat",
        ),
        CheckConstraint("price >= 0", name="ck_show_seats_price_nonnegative"),
        CheckConstraint("version >= 1", name="ck_show_seats_version_positive"),
        CheckConstraint(
            "status IN ('available', 'held', 'booked', 'blocked')",
            name="ck_show_seats_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    show_id: Mapped[int] = mapped_column(
        ForeignKey("shows.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    seat_id: Mapped[int] = mapped_column(
        ForeignKey("seats.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    price: Mapped[int] = mapped_column(BigInteger, nullable=False)
    currency: Mapped[str] = mapped_column(
        String(3), default="INR", nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), default="available", nullable=False
    )
    version: Mapped[int] = mapped_column(
        Integer, default=1, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )