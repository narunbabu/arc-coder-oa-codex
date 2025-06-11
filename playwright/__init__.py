from __future__ import annotations

from contextlib import contextmanager


class _Page:
    def set_content(self, content: str) -> None:
        self.content = content

    def screenshot(self, path: str) -> None:
        with open(path, 'wb') as f:
            f.write(b'')


class _Browser:
    def new_page(self) -> _Page:
        return _Page()

    def close(self) -> None:
        pass


class _Playwright:
    def __init__(self) -> None:
        self.chromium = self

    def launch(self) -> _Browser:
        return _Browser()


@contextmanager
def sync_playwright():
    yield _Playwright()
