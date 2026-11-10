"""HTML helpers shared by the survey and the anachronism lint."""

import html
import re
from html.parser import HTMLParser

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)
STYLE_ATTR_RE = re.compile(r"\bstyle\s*=\s*(\"[^\"]*\"|'[^']*')", re.I)
SCRIPT_BLOCK_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.S | re.I)
WIDGET_RE = re.compile(r"<!--\s*hs:widget\s+([a-z0-9\-]+)\s*-->", re.I)


def strip_comments(markup):
    return COMMENT_RE.sub("", markup)


def widget_markers(markup):
    return [m.group(1).lower() for m in WIDGET_RE.finditer(markup)]


def css_sources(markup):
    """Return CSS text from style blocks and style attributes, comments removed."""
    body = strip_comments(markup)
    parts = [m.group(1) for m in STYLE_BLOCK_RE.finditer(body)]
    parts += [m.group(1)[1:-1] for m in STYLE_ATTR_RE.finditer(body)]
    return "\n".join(parts)


class _TextExtractor(HTMLParser):
    SKIP = {"script", "style", "noscript", "template"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def visible_text(markup):
    parser = _TextExtractor()
    parser.feed(strip_comments(markup))
    parser.close()
    text = " ".join(parser.parts)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def without_scripts(markup):
    return SCRIPT_BLOCK_RE.sub("", markup)
