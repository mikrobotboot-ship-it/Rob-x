# MikroBot Pro X — ULTIMATE
Arquitetura integrada: HTML/CSS/TypeScript + Python Core + SQLite + WebSocket.

## Rodar no GitHub Codespaces
```bash
chmod +x start.sh
./start.sh
```
O servidor usa a porta 8765 e publica a pasta `web/`.

Se a porta estiver ocupada:
```bash
pkill -f "python.*8765" || true
./start.sh
```

A interface fica em `web/index.html`.
