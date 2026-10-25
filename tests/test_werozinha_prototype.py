"""Regression contract for the Werozinha prototype. Run: pytest -q tests/test_werozinha_prototype.py
Static checks only; browser E2E and integration tests remain pending.
"""
from pathlib import Path

HTML = (Path(__file__).resolve().parents[1] / "prototypes" / "werozinha-idle-v1.html").read_text(encoding="utf-8")

def test_has_mobile_viewport_and_responsive_layout():
    assert 'name="viewport"' in HTML
    assert '@media(max-width:650px)' in HTML

def test_idle_rotation_and_pause():
    assert "setInterval(tick,250)" in HTML
    assert "5-Math.floor((Date.now()-last)/1000)" in HTML
    assert "paused=!paused" in HTML
    assert "prefers-reduced-motion: reduce" in HTML

def test_chat_opens_from_center_stage():
    assert "$('pose').onclick=openChat" in HTML
    assert "$('pose').onkeydown" in HTML
    assert "$('chat').hidden=false" in HTML

def test_search_autocomplete_and_safe_text():
    assert 'role="listbox"' in HTML
    assert "addEventListener('input'" in HTML
    assert "textContent=item.name" in HTML
    assert "replaceChildren()" in HTML

def test_no_fake_sales_or_external_checkout():
    assert "Link de compra não cadastrado" in HTML
    assert "Ainda não estou conectada a uma IA externa" in HTML
    assert "window.open(" not in HTML
    assert "localStorage" not in HTML
