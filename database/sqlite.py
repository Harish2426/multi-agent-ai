from datetime import UTC, datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker,
)

from app.config import settings


def utc_now():
    # Current schema stores naive UTC DateTime values.
    return datetime.now(UTC).replace(
        tzinfo=None
    )


DATABASE_URL = settings.database_url


engine_options = {}

if DATABASE_URL.startswith("sqlite"):
    engine_options["connect_args"] = {
        "check_same_thread": False,
    }


engine = create_engine(
    DATABASE_URL,
    **engine_options,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(
        String,
        primary_key=True,
        index=True,
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
        nullable=False,
    )

    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(
        String,
        primary_key=True,
        index=True,
    )

    title = Column(
        String,
        nullable=False,
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="conversations",
    )

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )


class Message(Base):

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    conversation_id = Column(
        String,
        ForeignKey("conversations.id"),
        nullable=False,
        index=True,
    )

    role = Column(
        String,
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    route = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=utc_now,
        nullable=False,
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )


def init_database():
    Base.metadata.create_all(bind=engine)