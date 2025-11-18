from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from fastapi.responses import StreamingResponse
from typing import List, Optional
from sqlalchemy.orm import Session
import io, csv

from database import SessionLocal, Contact as DBContact, User
from models import Contact as PydanticContact, ContactBase
from auth import get_current_active_user
from dependencies import get_db

router = APIRouter(prefix="/contacts", tags=["Contatos"])

@router.post("/", response_model=PydanticContact, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact: ContactBase,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_contact = db.query(DBContact).filter(DBContact.email == contact.email).first()
    if db_contact:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    db_contact = DBContact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/", response_model=List[PydanticContact])
async def list_contacts(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return db.query(DBContact).all()

@router.get("/{contact_id}", response_model=PydanticContact)
async def read_contact(
    contact_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    contact = db.query(DBContact).filter(DBContact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contato não encontrado.")
    return contact

@router.put("/{contact_id}", response_model=PydanticContact)
async def update_contact(
    contact_id: int,
    contact: ContactBase,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_contact = db.query(DBContact).filter(DBContact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contato não encontrado.")
    db_contact.name = contact.name
    db_contact.email = contact.email
    db_contact.phone = contact.phone
    db_contact.codExterno = contact.codExterno
    db_contact.canalPref = contact.canalPref
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    contact = db.query(DBContact).filter(DBContact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contato não encontrado.")
    db.delete(contact)
    db.commit()

# Exportar CSV
@router.get("/export/csv")
async def export_contacts(
    contact_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    contacts = db.query(DBContact).all() if not contact_id else [db.query(DBContact).get(contact_id)]
    if not contacts:
        raise HTTPException(status_code=404, detail="Nenhum contato encontrado.")
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "name", "email", "phone", "canalPref", "codExterno"])
    writer.writeheader()
    for c in contacts:
        writer.writerow(c.__dict__)
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]),
                             media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=contacts.csv"})

# Importar CSV
@router.post("/import/csv")
async def import_contacts(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Envie um arquivo CSV válido.")
    reader = csv.DictReader(io.StringIO(file.file.read().decode("utf-8")))
    imported = 0
    for row in reader:
        db.add(DBContact(**row))
        imported += 1
    db.commit()
    return {"status": "sucesso", "importados": imported}

