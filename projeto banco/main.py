import duckdb
import fastapi
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import pymongo
import json
from fastapi import Request
import redis

r = redis.Redis(
    host='redis-19985.c345.samerica-east1-1.gce.cloud.redislabs.com',
    port=19985,
    decode_responses=True,
    username="default",
    password="xIT62jHUaYCoO8zk6BVpDluhISY16TgU",
)

app = fastapi.FastAPI()


@app.middleware("http")
async def no_cache_middleware(request: Request, call_next):
    response = await call_next(request)
    try:
        path = request.url.path
        if path.startswith("/static") or path == "/dados":
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
    except Exception:
        pass
    return response

# Conectar ao banco de dados
con = duckdb.connect("./bancoProjeto.duckdb")
client = pymongo.MongoClient("mongodb+srv://dudifhorta_db_user:5RFIaJ4LVEPjTOqV@databasebancos.fppym0m.mongodb.net/")


db = client["databaseBancos"]
colecao = db["carros"]

# Servir arquivos estáticos
static_path = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Modelo de dados
class Usuario(BaseModel):
    nome: str
    senha: str

# Rota para servir o index.html
@app.get("/")
async def root():
    return FileResponse(os.path.join(static_path, "index.html"))
@app.post("/login")
async def login(usuario: Usuario):
    try:
        # Verificar se o usuário já existe
        resultado = con.execute(
            "SELECT COUNT(*) FROM client WHERE nome = ?",
            [usuario.nome]
        ).fetchall()
        
        if resultado[0][0] <= 0:
            return {"success": False, "message": "Usuário não existe!"}
        if resultado[0][0] > 0:
            senha_verificada = con.execute(
                "SELECT senha FROM client WHERE nome = ?",
                [usuario.nome]
            ).fetchall()
            if senha_verificada[0][0] == usuario.senha:
                return {"success": True, "message": "Login realizado com sucesso!"}
         
            else:
                return {"success": False, "message": "Senha incorreta!"}
        
       
        con.commit()
        
    except Exception as e:
        return {"success": False, "message": f"Erro ao realizar login: {str(e)}"}
    
    
# Rota de cadastro
@app.post("/cadastro")
async def cadastro(usuario: Usuario):
    try:
        # Verificar se o usuário já existe
        resultado = con.execute(
            "SELECT COUNT(*) FROM client WHERE nome = ?",
            [usuario.nome]
        ).fetchall()
        
        if resultado[0][0] > 0:
            return {"success": False, "message": "Usuário já existe!"}
        
        # Inserir novo usuário
        con.execute(
            "INSERT INTO client (nome, senha) VALUES (?, ?)",
            [usuario.nome, usuario.senha]
        )
        con.commit()
        
        return {"success": True, "message": "Cadastro realizado com sucesso!"}
    except Exception as e:
        return {"success": False, "message": f"Erro ao cadastrar: {str(e)}"}


@app.get("/catalogo")
async def catalogo():
    return FileResponse(os.path.join(static_path, "./catalogo.html"))

@app.get("/dados")
async def dados():
    resultado = []
    for doc in colecao.find({}):
        try:
            doc["_id"] = str(doc.get("_id"))
        except Exception:
            pass
        resultado.append(doc)
    return resultado

# adicionar carro
@app.post("/adicionar")
async def adicionar_carro(carro: dict):
    for doc in colecao.find({}):
        if doc.get("nome do carro") == carro.get("nome do carro"):
            return {"success": False, "message": "Carro já existe no catálogo!"}
    try:
        resultado = colecao.insert_one(carro)
        
        return {"success": True, "message": "Carro adicionado com sucesso!", "id": str(resultado.inserted_id)}
    except Exception as e:
        return {"success": False, "message": f"Erro ao adicionar carro: {str(e)}"}
#deletar carro
@app.post("/deletar")
async def deletar_carro(carro: dict):
    for doc in colecao.find({}):
        if doc.get("nome do carro") == carro.get("nome do carro"):
            break
    else:
        return {"success": False, "message": "Carro não encontrado no catálogo!"}
    try:
        resultado = colecao.delete_one({"nome do carro": carro.get("nome do carro")})
        if resultado.deleted_count > 0:
           
            return {"success": True, "message": "Carro deletado com sucesso!"}
        else:
            return {"success": False, "message": "Carro não encontrado!"}
    except Exception as e:
        return {"success": False, "message": f"Erro ao deletar carro: {str(e)}"}
@app.get("/pedido")
async def pedido():
    return FileResponse(os.path.join(static_path, "./pedido.html"))

#lista de pedidos
@app.get("/pedidos")
async def pedidos():
    pedidos = []
    for key in r.scan_iter("pedido:*"): 
        pedidos.append(r.hgetall(key))
    return pedidos
#fazer pedido
@app.post("/fazer_pedido")
async def fazer_pedido(pedido: dict):
    # validar dados mínimos
    carro = (pedido.get("carro") or "").strip()
    quantidade = str(pedido.get("quantidade") or "").strip()
    local = (pedido.get("cidade") or "").strip()
    if not carro or not quantidade or not local:
        return {"success": False, "message": "Campos obrigatórios: carro, quantidade, local."}

    # verificar se o carro existe no catálogo
    encontrado = False
    for doc in colecao.find({}):
        if doc.get("nome do carro") == carro:
            encontrado = True
            break
    if not encontrado:
        return {"success": False, "message": "Carro não encontrado no catálogo!"}

    try:
        
        pedido_id = r.incr("pedido_id")
        chave = f"pedido:{pedido_id}"
        mapping = {
            "id": chave,
            "carro": carro,
            "quantidade": quantidade,
            "cidade": local,
            "status": "em andamento"
        }
        for k, v in mapping.items():
            r.hset(chave, k, v)
        return {"success": True, "message": "Pedido realizado com sucesso!", "id": pedido_id}
    except Exception as e:
        return {"success": False, "message": f"Erro ao realizar pedido: {str(e)}"}
#cancelar pedido
@app.post("/cancelar_pedido")
async def cancelar_pedido(body: dict):
    pedido = (body.get("pedido") or "").strip()
    if not pedido:
        return {"success": False, "message": "Número do pedido é obrigatório."}

    chave = f"pedido:{pedido}"
    if not r.exists(chave):
        return {"success": False, "message": "Pedido não encontrado!"}
    if r.hget(chave, "status") == "entregue":
        return {"success": False, "message": "Pedido já foi entregue e não pode ser cancelado!"}
    try:
        r.delete(chave)
        return {"success": True, "message": "Pedido cancelado com sucesso!"}
    except Exception as e:
        return {"success": False, "message": f"Erro ao cancelar pedido: {str(e)}"}
@app.post("/atualizar_pedido")
async def atualizar_pedido(body: dict):
    pedido = (body.get("pedido") or "").strip()
    if not pedido:
        return {"success": False, "message": "Número do pedido é obrigatório."}

    chave = f"pedido:{pedido}"
    if not r.exists(chave):
        return {"success": False, "message": "Pedido não encontrado!"}
    if r.hget(chave, "status") == "entregue":
        return {"success": False, "message": "Pedido já foi entregue!"}
    try:
        r.hset(chave, "status", "entregue")
        return {"success": True, "message": "Pedido atualizado com sucesso!"}
    except Exception as e:
        return {"success": False, "message": f"Erro ao atualizar pedido: {str(e)}"}


  
   
# Rodar servidor
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
