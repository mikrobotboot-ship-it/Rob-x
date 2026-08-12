from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import sqlite3, platform, socket, time

BASE = Path(__file__).resolve().parent
WEB = BASE / "web"
DB = BASE / "mikrobot.db"

app = FastAPI(title="MikroBot Pro X Ultimate")
app.mount("/assets", StaticFiles(directory=WEB / "assets"), name="assets")

def db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS events(ts REAL, kind TEXT, data TEXT)")
    con.commit()
    return con

@app.get("/")
def index():
    return FileResponse(WEB / "index.html")

@app.get("/api/status")
def status():
    return {
        "online": True,
        "time": time.strftime("%H:%M:%S"),
        "platform": platform.system(),
        "python": platform.python_version(),
        "hostname": socket.gethostname()
    }

@app.post("/api/diagnostic")
def diagnostic():
    result = {
        "internet": "verificação pelo navegador/API",
        "core": "ONLINE",
        "python": platform.python_version(),
        "platform": platform.system()
    }
    con = db()
    con.execute("INSERT INTO events VALUES(?,?,?)", (time.time(), "diagnostic", str(result)))
    con.commit(); con.close()
    return result

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"type":"hello","message":"MikroBot Core conectado"})
    while True:
        msg = await websocket.receive_json()
        action = msg.get("action")
        if action == "status":
            await websocket.send_json({"type":"status","data":status()})
        elif action == "diagnostic":
            await websocket.send_json({"type":"diagnostic","data":diagnostic()})
        else:
            await websocket.send_json({"type":"error","message":"Ação desconhecida"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)
