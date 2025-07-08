from sqlalchemy.orm import Session
from . import models


def create_note(db: Session, title: str, content: str, folder: str = ""):
    note = models.Note(title=title, content=content, folder=folder)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_note(db: Session, note_id: str):
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def get_notes(db: Session):
    return db.query(models.Note).all()


def delete_note(db: Session, note_id: str):
    note = get_note(db, note_id)
    if note:
        db.delete(note)
        db.commit()
    return note


def update_note(db: Session, note_id: str, title: str, content: str, folder: str = ""):
    note = get_note(db, note_id)
    if not note:
        return None
    note.title = title
    note.content = content
    note.folder = folder
    db.commit()
    db.refresh(note)
    return note


def create_reference(db: Session, source_id: str, target_id: str):
    ref = models.Reference(source_id=source_id, target_id=target_id)
    db.add(ref)
    db.commit()
    db.refresh(ref)
    return ref


def delete_reference(db: Session, source_id: str, target_id: str):
    ref = db.query(models.Reference).filter_by(source_id=source_id, target_id=target_id).first()
    if ref:
        db.delete(ref)
        db.commit()
    return ref


def get_incoming(db: Session, note_id: str):
    return db.query(models.Reference).filter(models.Reference.target_id == note_id).all()


def get_outgoing(db: Session, note_id: str):
    return db.query(models.Reference).filter(models.Reference.source_id == note_id).all()
