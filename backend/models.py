import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True)
    content = Column(Text)
    folder = Column(String, default="")

    outgoing = relationship("Reference", back_populates="source", foreign_keys='Reference.source_id')
    incoming = relationship("Reference", back_populates="target", foreign_keys='Reference.target_id')

class Reference(Base):
    __tablename__ = "references"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String, ForeignKey("notes.id"))
    target_id = Column(String, ForeignKey("notes.id"))

    source = relationship("Note", foreign_keys=[source_id], back_populates="outgoing")
    target = relationship("Note", foreign_keys=[target_id], back_populates="incoming")
