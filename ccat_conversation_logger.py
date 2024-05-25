import hashlib
import datetime
import socket

from cat.log import log
from cat.mad_hatter.decorators import hook, plugin

from pydantic import BaseModel, Field
from sqlalchemy import ForeignKey, String, Text, DateTime, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


### Cheshire Cat AI Settings section

DEFAULT_SQLITE_FILEPATH = 'sqlite:///cat/data/conv_log.db'

class PluginSettings(BaseModel):
    db_dsn: str = Field(
        default=DEFAULT_SQLITE_FILEPATH,
        title="Sqlite filepath. Change it only if you know what you are doing!",
    )

@plugin
def settings_model():
    return PluginSettings


### Conversation Logger DB Model section

class Base(DeclarativeBase):
    pass

class ConvLogDocument(Base):
    __tablename__= 'ccat_conversations'
    id: Mapped[int] = mapped_column(primary_key=True)
    instance: Mapped[str] = mapped_column(String(256))
    username: Mapped[str] = mapped_column(String(256))
    input: Mapped[str] = mapped_column(Text)
    output: Mapped[str] = mapped_column(Text)
    ts: Mapped[DateTime] = mapped_column(DateTime, server_default=func.CURRENT_TIMESTAMP(), nullable=False)


### The Real Code :-)

engine = None

@hook  # default priority = 1
def before_cat_sends_message(message, cat):
    global engine
    DSN = cat.mad_hatter.get_plugin().load_settings()["db_dsn"]
    engine = create_engine(DSN)
    Base.metadata.create_all(engine, checkfirst=True)
    if message.type == 'chat':
        log.info(f"CCat Conversation Logger is logging a message from: {message.user_id}")
        with Session(engine) as session:
            try:
                db_doc = ConvLogDocument(instance=socket.getfqdn(),
                                        username=message.user_id,
                                        input=message.why.input,
                                        output=message.content
                                        )
                session.add(db_doc)
                session.commit()
            except Exception as e:
                session.rollback()
                log.error(f"Something weird happened: {str(e)}. Conversation NOT logged to DSN {DSN}")
                return message

    return message
