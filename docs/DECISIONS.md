# Decisions

- SSE is used for the dashboard because the browser only needs server-to-client updates and it is simpler to operate than WebSockets.
- The first runnable scaffold uses FastAPI startup-created tables; Alembic is the next migration step before production deployment.
- Tenant context is resolved once in `current_actor`, and tenant-owned queries require its tenant id.
- Webhook delivery ids are unique to make retries idempotent; webhook processing is intentionally small and can move to a worker.
- A compact cookie session is used for the demo; production should use signed, rotating sessions with a server-side revocation path.
