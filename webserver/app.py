from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import json
import os

app = FastAPI(title="CubeSat Telemetry Dashboard")

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

LOG_FILE = os.path.join(os.path.dirname(__file__), "sensor_log.json")

@app.get("/api/readings")
async def get_readings():
    """
    Reads the latest sensor data from sensor_log.json
    and returns it.
    """
    from fastapi.responses import FileResponse
    
    if not os.path.exists(LOG_FILE):
        return JSONResponse(content={"error": "Log file not found", "data": []}, status_code=404)
        
    return FileResponse(LOG_FILE, media_type="application/json")

@app.get("/")
async def root():
    """
    Redirect root to static/index.html handled by StaticFiles
    """
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8008, reload=True)
