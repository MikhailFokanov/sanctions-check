from datetime import datetime

from sqlalchemy import func, JSON, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SearchLog(Base):
    __tablename__ = "search_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    create_date: Mapped[datetime] = mapped_column(server_default=func.now())
    name_search_pattern: Mapped[str] = mapped_column(nullable=False)
    address_search_pattern: Mapped[str] = mapped_column(nullable=False)
    n_results: Mapped[int] = mapped_column(nullable=False)
    index: Mapped[str] = mapped_column(nullable=False)
    search_query: Mapped[dict] = mapped_column(JSON, nullable=True)
    search_result: Mapped[list] = mapped_column(ARRAY(JSON), nullable=True)


class LLMResponse(Base):
    __tablename__ = "llm_response"

    id: Mapped[int] = mapped_column(primary_key=True)
    create_date: Mapped[datetime] = mapped_column(server_default=func.now())
    keyword: Mapped[str] = mapped_column(unique=True)
    normalized: Mapped[str] = mapped_column(nullable=False)
