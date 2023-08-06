from dataclasses import dataclass
from src.ballyregan.providers import FreeProxyListProvider


@dataclass
class SSLProxiesProvider(FreeProxyListProvider):
    url: str = "https://www.sslproxies.org/"
