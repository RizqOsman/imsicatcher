from fastapi import FastAPI, WebSocket
from app.models import IMSIRecord, IMSIBlacklistEntry, IMSIStats
from app.database import (
    init_db, save_imsi, get_all_imsis,
    add_to_blacklist, get_blacklisted_imsis,
    get_statistics
)
from app.utils import estimate_distance, scan_bts_arfcn
from typing import List
from datetime import datetime

app = FastAPI()
websocket_clients = []

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/imsi", response_model=List[IMSIRecord])
def get_imsis():
    rows = get_all_imsis()
    return [
        IMSIRecord(
            imsi=r[0],
            timestamp=datetime.fromisoformat(r[1]),
            signal_strength=r[2],
            estimated_distance=estimate_distance(r[2])
        ) for r in rows
    ]

@app.post("/imsi")
def add_imsi(record: IMSIRecord):
    save_imsi(record.imsi, record.signal_strength)
    data = {
        "imsi": record.imsi,
        "timestamp": record.timestamp.isoformat(),
        "signal_strength": record.signal_strength,
        "estimated_distance": estimate_distance(record.signal_strength)
    }
    for client in websocket_clients:
        try:
            import asyncio
            asyncio.create_task(client.send_json(data))
        except Exception:
            pass
    return {"message": "IMSI logged"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # dummy listener
    except Exception:
        websocket_clients.remove(websocket)

@app.post("/blacklist")
def blacklist_imsi(entry: IMSIBlacklistEntry):
    add_to_blacklist(entry.imsi, entry.label)
    return {"message": f"IMSI {entry.imsi} added to blacklist"}

@app.get("/alerts", response_model=List[IMSIBlacklistEntry])
def get_alerts():
    return [IMSIBlacklistEntry(imsi=imsi, label=label) for imsi, label in get_blacklisted_imsis()]

@app.get("/stats", response_model=IMSIStats)
def get_stats():
    total, avg_signal, most_common = get_statistics()
    return IMSIStats(total=total, average_signal=avg_signal, top_imsis=most_common)

@app.get("/bts-scan")
def get_bts_scan():
    return {"results": scan_bts_arfcn()}