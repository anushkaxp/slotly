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


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        UniqueConstraint("booking_reference", name="uq_bookings_reference"),
        UniqueConstraint("hold_id", name="uq_bookings_hold"),
        CheckConstraint(
            "status IN ('pending', 'confirmed', 'cancelled', 'failed')",
            name="ck_bookings_status",
        ),
        CheckConstraint("subtotal >= 0", name="ck_bookings_subtotal"),
        CheckConstraint(
            "convenience_fee >= 0",
            name="ck_bookings_convenience_fee",
        ),
        CheckConstraint(
            "discount_amount >= 0",
            name="ck_bookings_discount_amount",
        ),
        CheckConstraint("total_amount >= 0", name="ck_bookings_total"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_reference: Mapped[str] = mapped_column(
        String(30), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    hold_id: Mapped[int] = mapped_column(
        ForeignKey("seat_holds.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False
    )
    subtotal: Mapped[int] = mapped_column(BigInteger, nullable=False)
    convenience_fee: Mapped[int] = mapped_column(
        BigInteger, default=0, nullable=False
    )
    discount_amount: Mapped[int] = mapped_column(
        BigInteger, default=0, nullable=False
    )
    total_amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    currency: Mapped[str] = mapped_column(
        String(3), default="INR", nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    confirmed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )