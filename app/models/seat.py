
from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Seat(Base):
    __tablename__ = "seats"
    __table_args__ = (
        UniqueConstraint(
            "section_id",
            "row_label",
            "seat_number",
            name="uq_seat_section_row_number",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    venue_id: Mapped[int] = mapped_column(
        ForeignKey("venues.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    section_id: Mapped[int] = mapped_column(
        ForeignKey("venue_sections.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    row_label: Mapped[str] = mapped_column(String(20), nullable=False)
    seat_number: Mapped[int] = mapped_column(Integer, nullable=False)
    seat_type: Mapped[str] = mapped_column(
        String(30), default="standard", nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
