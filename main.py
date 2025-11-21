from mcp.server.fastmcp import FastMCP
from tools.tools import register_tools
from mcp.server.auth.provider import TokenVerifier, AccessToken
from mcp.server.auth.settings import AuthSettings

from datetime import datetime
import os, asyncio
import nest_asyncio

from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


class VerificadorPermanente(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        print(f"Verificando token: {token}")
        print(f"Verificando secret: {SECRET_KEY}")
        # Compara con el token fijo
        if token == SECRET_KEY:
            # Crea y retorna el AccessToken
            return AccessToken(
                token=token,
                client_id="cliente_permanente",
                scopes=["read", "write"],  # define los scopes que quieres
                expires_at=None  # indica que no hay expiración (permanente)
            )
        else:
            return None

auth_settings = AuthSettings(
    issuer_url="https://mi-issuer-ficticio",
    resource_server_url="http://localhost:5001",
    required_scopes=["read", "write"]
)

def json_serializer(obj):
    """Helper function to convert non-serializable objects for JSON serialization."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="replace")
    # Add other non-serializable types as needed
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

auth = VerificadorPermanente()
mcp = FastMCP("myanimelist", auth=auth_settings, token_verifier=VerificadorPermanente(), host="0.0.0.0", port=5001)

register_tools(mcp)

if __name__ == "__main__":
    nest_asyncio.apply()

    async def main() -> None:
        try:
            await mcp.run_streamable_http_async()
        except Exception as e:
            print(f"Error starting client: {e}")

    asyncio.run(main())
