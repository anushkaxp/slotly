from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class SeatHoldItem(Base):
    __tablename__ = "seat_hold_items"
    __table_args__ = (
        UniqueConstraint(
            "hold_id",
            "show_seat_id",
            name="uq_seat_hold_items_hold_seat",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    hold_id: Mapped[int] = mapped_column(
        ForeignKey("seat_holds.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    show_seat_id: Mapped[int] = mapped_column(
        ForeignKey("show_seats.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )