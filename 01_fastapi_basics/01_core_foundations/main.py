import json
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI

from routes.task_route import router


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    app_instance.openapi_schema = None
    try:
        schema = app_instance.openapi()
        Path(__file__).parent.joinpath("openapi_dump.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    except Exception as exc:
        print("Failed to write OpenAPI dump:", exc)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/debug/routes")
def _debug_routes():
    return [
        {
            "path": getattr(r, "path", None),
            "methods": sorted(list(getattr(r, "methods", []))) if getattr(r, "methods", None) else [],
            "module": getattr(getattr(r, "endpoint", None), "__module__", None),
        }
        for r in app.routes
    ]