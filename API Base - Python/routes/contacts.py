from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from fastapi.responses import StreamingResponse
from typing import List, Optional
from sqlalchemy.orm import Session
import io, csv
from datetime import datetime

from database import SessionLocal, Contact, User
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
    db_contact = db.query(Contact).filter(Contact.email == contact.email).first()
    if db_contact:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/", response_model=List[PydanticContact])
async def list_contacts(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return db.query(Contact).all()

@router.get("/{contact_id}", response_model=PydanticContact)
async def read_contact(
    contact_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
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
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
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
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contato não encontrado.")
    db.delete(contact)
    db.commit()

# Exportar CSV
@router.get("/export/csv")
async def export_contacts(
    contact_id: Optional[int] = None,
    cliente_id: Optional[int] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        print(f"Iniciando exportação de contatos. Filtros - cliente_id: {cliente_id}, search: {search}")
        
        # Inicia a query
        query = db.query(Contact)
        print(f"Query inicial criada")
        
        # Aplica filtros
        if contact_id is not None:
            print(f"Filtrando por contact_id: {contact_id}")
            query = query.filter(Contact.id == contact_id)
        else:
            if cliente_id is not None:
                print(f"Aplicando filtro de cliente_id: {cliente_id}")
                query = query.filter(Contact.cliente_id == cliente_id)
            
            if search:
                search_term = f"%{search}%"
                print(f"Aplicando filtro de busca: {search}")
                query = query.filter(
                    (Contact.name.ilike(search_term)) | 
                    (Contact.email.ilike(search_term)) |
                    (Contact.phone.ilike(search_term))
                )
        
        # Executa a query
        print("Executando query...")
        contacts = query.all()
        print(f"Encontrados {len(contacts)} contatos")
        
        if not contacts:
            print("Nenhum contato encontrado com os filtros fornecidos")
            raise HTTPException(status_code=404, detail="Nenhum contato encontrado com os filtros fornecidos.")
        
        # Prepara o CSV
        print("Preparando CSV...")
        output = io.StringIO()
        fieldnames = ["id", "name", "email", "phone", "canalPref", "codExterno", "cliente_id"]
        
        try:
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            # Escreve os dados
            for contact in contacts:
                writer.writerow({
                    "id": contact.id,
                    "name": contact.name,
                    "email": contact.email,
                    "phone": contact.phone or "",
                    "canalPref": contact.canalPref or "",
                    "codExterno": contact.codExterno or "",
                    "cliente_id": contact.cliente_id or ""
                })
            
            output.seek(0)
            csv_content = output.getvalue()
            print(f"CSV gerado com sucesso. Tamanho: {len(csv_content)} bytes")
            
            # Gera o nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"contatos_{timestamp}.csv"
            
            return StreamingResponse(
                iter([csv_content]),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
            
        except Exception as e:
            print(f"Erro ao gerar CSV: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao gerar o arquivo CSV: {str(e)}")
            
    except HTTPException:
        # Re-lança exceções HTTP que já foram tratadas
        raise
        
    except Exception as e:
        print(f"Erro inesperado ao exportar contatos: {str(e)}")
        import traceback
        traceback.print_exc()  # Isso vai imprimir o traceback completo no console
        raise HTTPException(
            status_code=500,
            detail=f"Ocorreu um erro inesperado: {str(e)}"
        )

# Importar CSV
@router.post("/import/csv")
async def import_contacts(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        print(f"Iniciando importação de contatos do arquivo: {file.filename}")
        
        # Verifica o tipo do arquivo
        if file.content_type != "text/csv" and not file.filename.lower().endswith('.csv'):
            raise HTTPException(status_code=400, detail="O arquivo deve ser um CSV válido.")
        
        # Lê o conteúdo do arquivo
        content = await file.read()
        try:
            # Tenta decodificar como UTF-8
            content_str = content.decode('utf-8')
        except UnicodeDecodeError:
            # Se falhar, tenta com outro encoding comum
            try:
                content_str = content.decode('latin-1')
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Erro ao ler o arquivo: {str(e)}")
        
        # Cria o leitor CSV
        reader = csv.DictReader(io.StringIO(content_str))
        
        # Verifica se os campos obrigatórios estão presentes
        required_fields = {'name', 'email'}
        if not required_fields.issubset(reader.fieldnames):
            missing = required_fields - set(reader.fieldnames)
            raise HTTPException(
                status_code=400, 
                detail=f"Campos obrigatórios ausentes no CSV: {', '.join(missing)}"
            )
        
        imported = 0
        errors = []
        
        # Processa cada linha do CSV
        for i, row in enumerate(reader, 2):  # Começa da linha 2 (cabeçalho é a linha 1)
            try:
                # Remove espaços em branco extras dos valores
                row = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
                
                # Cria o dicionário de dados para o contato
                contact_data = {
                    'name': row.get('name', '').strip(),
                    'email': row.get('email', '').strip().lower(),
                    'phone': row.get('phone', '').strip() or None,
                    'canalPref': row.get('canalPref', '').strip().lower() or None,
                    'codExterno': row.get('codExterno', '').strip() or None,
                }
                
                # Converte cliente_id para inteiro se existir
                if 'cliente_id' in row and row['cliente_id'].strip():
                    try:
                        contact_data['cliente_id'] = int(row['cliente_id'])
                    except (ValueError, TypeError):
                        contact_data['cliente_id'] = None
                
                # Verifica se o email já existe
                if db.query(Contact).filter(Contact.email == contact_data['email']).first():
                    print(f"Aviso: Email {contact_data['email']} já existe, pulando...")
                    errors.append(f"Linha {i}: Email {contact_data['email']} já existe")
                    continue
                
                # Cria e adiciona o contato
                db_contact = Contact(**contact_data)
                db.add(db_contact)
                imported += 1
                
                # Faz commit a cada 10 registros para evitar perda de dados em caso de erro
                if imported % 10 == 0:
                    db.commit()
            
            except Exception as e:
                error_msg = f"Erro na linha {i}: {str(e)}"
                print(error_msg)
                errors.append(error_msg)
                # Continua processando as próximas linhas mesmo em caso de erro
                continue
        
        # Faz o commit final
        db.commit()
        
        # Prepara a resposta
        response = {
            "status": "sucesso",
            "importados": imported,
            "total_linhas": imported + len(errors)
        }
        
        if errors:
            response["erros"] = errors
            response["status"] = "parcial" if imported > 0 else "erro"
        
        print(f"Importação concluída. {imported} contatos importados com sucesso.")
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro inesperado durante a importação: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Ocorreu um erro durante a importação: {str(e)}"
        )

