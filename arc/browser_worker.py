"""Browser worker using Playwright to capture screenshots."""
from __future__ import annotations

import random
from pathlib import Path

from faker import Faker
from playwright.sync_api import sync_playwright


def run_browser_task(output: Path) -> None:
    """Start an HTTP server, seed data, and take a screenshot."""
    fake = Faker()
    port = random.randint(8000, 9000)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(f"<h1>Hello {fake.name()}</h1>")
        page.screenshot(path=str(output))
        browser.close()
