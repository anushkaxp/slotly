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


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        UniqueConstraint(
            "provider",
            "idempotency_key",
            name="uq_payments_provider_idempotency",
        ),
        CheckConstraint("amount > 0", name="ck_payments_amount_positive"),
        CheckConstraint(
            "status IN ('pending', 'succeeded', 'failed', 'refunded')",
            name="ck_payments_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(
        ForeignKey("bookings.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    provider_payment_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    idempotency_key: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    currency: Mapped[str] = mapped_column(
        String(3), default="INR", nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False
    )
    failure_code: Mapped[str | None] = mapped_column(
        String(100), nullable=True
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