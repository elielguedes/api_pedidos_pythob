from fastapi import APIRouter
from models import usuario , db
from sqlalchemy.orm import sessionmaker

auth_router = APIRouter(prefix = "/auth" , tags =["autenticão"])

@auth_router.get("/")
async def home():
    return {"mensagem":"voce acessou rota padrao de autenticação " , "autenticação":True}

@auth_router.post("/criar_usuario")
async def crair_conta(email:str , senha:str , nome:str):
    SessionLocal = sessionmaker(bind = db) #conecta meu banco para ligar e desligar 
    db_session = SessionLocal()
    usuarios = db_session.query(usuario).filter_by(email=email).first() #consulta meu banco
    if usuarios:
        #ja existe
        db_session.close()
        return {"mensagem":"usuario ja existe", "criado":False}
    else:
        novo_usuario = usuario(nome=nome, email=email, senha=senha, ativo=True)
        db_session.add(novo_usuario)
        db_session.commit()
        db_session.refresh(novo_usuario)
        db_session.close()
        return {"mensagem":"usuario criado", "criado":True, "usuario_id": getattr(novo_usuario, "id", None)}


