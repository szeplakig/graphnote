from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, crud
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/notes")
def create_note(title: str, content: str, folder: str = "", db: Session = Depends(get_db)):
    return crud.create_note(db, title=title, content=content, folder=folder)


@app.get("/notes")
def list_notes(db: Session = Depends(get_db)):
    return crud.get_notes(db)


@app.get("/notes/{note_id}")
def read_note(note_id: str, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.put("/notes/{note_id}")
def update_note(note_id: str, title: str, content: str, folder: str = "", db: Session = Depends(get_db)):
    note = crud.update_note(db, note_id, title, content, folder)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.delete("/notes/{note_id}")
def remove_note(note_id: str, db: Session = Depends(get_db)):
    note = crud.delete_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"status": "deleted"}


@app.post("/notes/{source_id}/link/{target_id}")
def link_notes(source_id: str, target_id: str, db: Session = Depends(get_db)):
    return crud.create_reference(db, source_id, target_id)


@app.delete("/notes/{source_id}/link/{target_id}")
def unlink_notes(source_id: str, target_id: str, db: Session = Depends(get_db)):
    ref = crud.delete_reference(db, source_id, target_id)
    if not ref:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"status": "deleted"}


@app.get("/notes/{note_id}/references/incoming")
def incoming_refs(note_id: str, db: Session = Depends(get_db)):
    return crud.get_incoming(db, note_id)


@app.get("/notes/{note_id}/references/outgoing")
def outgoing_refs(note_id: str, db: Session = Depends(get_db)):
    return crud.get_outgoing(db, note_id)
