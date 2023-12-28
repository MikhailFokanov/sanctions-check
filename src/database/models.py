from datetime import datetime

from sqlalchemy import func, JSON, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SearchLog(Base):
    __tablename__ = 'search_log'

    id: Mapped[int] = mapped_column(primary_key=True)
    create_date: Mapped[datetime] = mapped_column(server_default=func.now()) 
    index: Mapped[str] = mapped_column(nullable=False)
    search_query: Mapped[dict] = mapped_column(JSON, nullable=True)
    search_result: Mapped[list] = mapped_column(ARRAY(JSON), nullable=True)


class GPTResponse(Base):
    __tablename__ = 'gpt_response'

    id: Mapped[int] = mapped_column(primary_key=True)
    create_date: Mapped[datetime] = mapped_column(server_default=func.now()) 
    keyword: Mapped[str] = mapped_column(unique=True)
    normalized: Mapped[str] = mapped_column(nullable=False)


### -------------------------------------------
# class User(Base):
#     __tablename__ = "users"
# 
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(unique=True)
#     is_block: Mapped[bool] = mapped_column(default=False)
#     is_admin: Mapped[bool] = mapped_column(server_default=false())
#     todoist_email: Mapped[str] = mapped_column(nullable=True)
# 
#     tickets: Mapped[List["Ticket"]] = relationship("Ticket")
# 
# 
# class Ticket(Base):
#     __tablename__ = "tickets"
# 
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(nullable=True)
#     sync_id: Mapped[str] = mapped_column(nullable=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey(column="users.id", ondelete="CASCADE"))
#     create_date: Mapped[datetime] = mapped_column(server_default=func.now())
#     close_data: Mapped[datetime] = mapped_column(nullable=True)
#     resolved: Mapped[bool] = mapped_column(nullable=True, server_default=false())
# 
#     logs: Mapped[List["Log"]] = relationship("Log")
# 
#     def __repr__(self):
#         return f"{self.name}"
# 
# 
# class Log(Base):
#     __tablename__ = "logs"
# 
#     id: Mapped[int] = mapped_column(primary_key=True)
#     status: Mapped[str] = mapped_column()
#     create_date: Mapped[datetime] = mapped_column(server_default=func.now())
#     ticket_id: Mapped[int] = mapped_column(ForeignKey(column="tickets.id"))
# 
#     def __repr__(self):
#         return f"{self.status}"
