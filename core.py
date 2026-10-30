import ipaddress, socket
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

def is_safe_url(url: str) -> bool:
    """Allow only public http(s) URLs (prevents SSRF)."""
    p = urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        return False
    try:
        # check every IP the host resolves to, not just the first
        for info in socket.getaddrinfo(p.hostname, None):
            ip = ipaddress.ip_address(info[4][0])
            if not ip.is_global:
                return False
        return True
    except Exception:
        return False

def fetch_page(url: str) -> dict:
    """Fetch a page and return title, meta description, h1s and clean text."""
    for _ in range(5):                      # follow redirects, re-checking each hop
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 AuditBot"},
                         timeout=15, allow_redirects=False)
        if not r.is_redirect:
            break
        url = urljoin(url, r.headers["Location"])
        if not is_safe_url(url):
            raise ValueError(f"Redirect to unsafe URL blocked: {url}")
    else:
        raise ValueError("Too many redirects")
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    meta = soup.find("meta", attrs={"name": "description"})
    title = soup.title.get_text(strip=True) if soup.title else ""
    h1 = [h.get_text(strip=True) for h in soup.find_all("h1")]
    for tag in soup(["script", "style", "noscript"]):    # drop non-visible text
        tag.decompose()
    return {
        "title": title,
        "meta": (meta.get("content") or "").strip() if meta else "",
        "h1": h1,
        "text": " ".join(soup.get_text(" ").split()),
    }
