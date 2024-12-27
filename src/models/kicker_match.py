from sqlalchemy import Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .member import Member

class KickerMatch(Base):
    __tablename__ = "kicker_matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    team_a_score: Mapped[int] = mapped_column(Integer, nullable=False)
    team_b_score: Mapped[int] = mapped_column(Integer, nullable=False)

    team_a_player_1: Mapped[str] = mapped_column(String, ForeignKey("members.user_sub"), nullable=False)
    team_a_player_1_member: Mapped[Member] = relationship("Member", foreign_keys=[team_a_player_1])
    team_a_player_2: Mapped[str] = mapped_column(String, ForeignKey("members.user_sub"), nullable=True)
    team_a_player_2_member: Mapped[Member] = relationship("Member", foreign_keys=[team_a_player_2])

    team_b_player_1: Mapped[str] = mapped_column(String, ForeignKey("members.user_sub"), nullable=False)
    team_b_player_1_member: Mapped[Member] = relationship("Member", foreign_keys=[team_b_player_1])
    team_b_player_2: Mapped[str] = mapped_column(String, ForeignKey("members.user_sub"), nullable=True)
    team_b_player_2_member: Mapped[Member] = relationship("Member", foreign_keys=[team_b_player_2])
    start_time: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    end_time: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    history: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
