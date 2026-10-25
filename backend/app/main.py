import json
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .config import settings
from .db import Base, engine, get_db
from .models import Event, Membership, Tenant, User
from .security import new_state, valid_signature
from .tenant import Actor, current_actor

app = FastAPI(title="OpsPilot", version="0.1.0")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    await db.execute(select(1)); return {"status": "ok"}

@app.get("/auth/github")
async def github_login():
    state = new_state()
    response = RedirectResponse("https://github.com/login/oauth/authorize?client_id=" + settings.github_client_id + "&state=" + state)
    response.set_cookie("opspilot_oauth_state", state, httponly=True, samesite="lax")
    return response

@app.get("/auth/github/callback")
async def github_callback(request: Request):
    error = request.query_params.get("error")
    if error:
        return HTMLResponse(f"<h1>GitHub sign-in was cancelled</h1><p>{error}</p>", status_code=400)
    state = request.query_params.get("state")
    expected = request.cookies.get("opspilot_oauth_state")
    if not state or not expected or state != expected:
        raise HTTPException(400, "Invalid or expired OAuth state")
    if not request.query_params.get("code"):
        raise HTTPException(400, "Missing GitHub authorization code")
    # Token exchange and user provisioning are intentionally kept behind this boundary.
    return HTMLResponse("<h1>GitHub callback received</h1><p>OAuth token exchange is not configured yet. Add GitHub credentials to .env.</p>")

@app.get("/api/events")
async def events(actor: Actor = Depends(current_actor), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Event).where(Event.tenant_id == actor.tenant_id).order_by(Event.created_at.desc()).limit(50))).scalars()
    return [{"type": e.event_type, "status": e.status, "created_at": e.created_at.isoformat()} for e in rows]

@app.get("/api/events/stream")
async def event_stream(actor: Actor = Depends(current_actor), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Event).where(Event.tenant_id == actor.tenant_id).order_by(Event.created_at.desc()).limit(20))).scalars()
    async def generate():
        for e in rows: yield f"data: {json.dumps({'type': e.event_type, 'status': e.status})}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/webhooks/github")
async def github_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    body = await request.body()
    if not valid_signature(body, request.headers.get("x-hub-signature-256"), settings.github_client_secret): raise HTTPException(401, "Invalid signature")
    delivery = request.headers.get("x-github-delivery")
    if not delivery: raise HTTPException(400, "Missing delivery id")
    if (await db.execute(select(Event).where(Event.delivery_id == delivery))).scalar_one_or_none(): return {"status": "duplicate"}
    event = Event(tenant_id=1, delivery_id=delivery, event_type=request.headers.get("x-github-event", "unknown"), payload=body.decode())
    db.add(event); await db.commit(); return {"status": "accepted"}
