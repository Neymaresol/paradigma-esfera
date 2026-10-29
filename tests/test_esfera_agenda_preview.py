from pathlib import Path
from html.parser import HTMLParser

PAGE = Path(__file__).resolve().parents[1] / "prototypes" / "esfera-agenda-ia-v1.html"

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.images = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "img":
            self.images.append(a)

def test_preview_keeps_core_controls():
    html = PAGE.read_text(encoding="utf-8")
    inspector = Inspector()
    inspector.feed(html)
    assert {"filters", "agenda-rail", "offer-rail", "partner-list", "wero-img", "question", "ask", "reply"}.issubset(inspector.ids)
    assert 'data-scroll="agenda-rail"' in html
    assert 'data-scroll="offer-rail"' in html
    assert "scrollBy(" in html
    assert "5000" in html

def test_preview_is_fail_closed_and_labels_examples():
    html = PAGE.read_text(encoding="utf-8")
    assert "eventos ilustrativos" in html
    assert "Links comerciais só serão habilitados" in html
    assert "Sem divulgação automática" in html
    assert "https://go.hotmart.com/" not in html
    assert "https://s.shopee.com.br/" not in html

def test_official_asset_path_is_retained():
    inspector = Inspector()
    inspector.feed(PAGE.read_text(encoding="utf-8"))
    assert any(i.get("src") == "/assets/werozinha-assistente-oficial.webp" for i in inspector.images)
