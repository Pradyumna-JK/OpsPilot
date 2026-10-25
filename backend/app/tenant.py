from dataclasses import dataclass
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_db
from .models import Membership

@dataclass(frozen=True)
class Actor:
    user_id: int
    tenant_id: int
    role: str

async def current_actor(request: Request, db: AsyncSession = Depends(get_db)) -> Actor:
    # Signed-cookie session decoding is intentionally centralized here; production deployments
    # should replace this compact demo decoder with its server-side session store.
    raw = request.cookies.get("opspilot_session")
    if not raw or ":" not in raw: raise HTTPException(401, "Authentication required")
    user, tenant = raw.split(":", 1)
    membership = (await db.execute(select(Membership).where(Membership.user_id == int(user), Membership.tenant_id == int(tenant)))).scalar_one_or_none()
    if not membership: raise HTTPException(403, "Tenant access denied")
    return Actor(int(user), int(tenant), membership.role)

def require_admin(actor: Actor = Depends(current_actor)) -> Actor:
    if actor.role != "admin": raise HTTPException(403, "Admin role required")
    return actor
