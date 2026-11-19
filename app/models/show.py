from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Show(Base):
    __tablename__ = "shows"
    __table_args__ = (
        CheckConstraint(
            "ends_at > starts_at",
            name="ck_shows_end_after_start",
        ),
        CheckConstraint(
            "booking_closes_at >= booking_opens_at",
            name="ck_shows_booking_window_valid",
        ),
        CheckConstraint(
            "status IN ('draft', 'scheduled', 'cancelled', 'completed')",
            name="ck_shows_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    venue_id: Mapped[int] = mapped_column(
        ForeignKey("venues.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    ends_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    booking_opens_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    booking_closes_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(30), default="scheduled", nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )