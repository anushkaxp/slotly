from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class BookingItem(Base):
    __tablename__ = "booking_items"
    __table_args__ = (
        UniqueConstraint(
            "booking_id",
            "show_seat_id",
            name="uq_booking_items_booking_seat",
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="ck_booking_items_unit_price",
        ),
        CheckConstraint(
            "fee_amount >= 0",
            name="ck_booking_items_fee",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(
        ForeignKey("bookings.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    show_seat_id: Mapped[int] = mapped_column(
        ForeignKey("show_seats.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    unit_price: Mapped[int] = mapped_column(BigInteger, nullable=False)
    fee_amount: Mapped[int] = mapped_column(
        BigInteger, default=0, nullable=False
    )
    currency: Mapped[str] = mapped_column(
        String(3), default="INR", nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )