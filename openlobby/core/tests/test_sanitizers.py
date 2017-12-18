import pytest

from ..sanitizers import strip_all_tags, extract_text


@pytest.mark.parametrize('input, text', [
    ('foo', 'foo'),
    ('has multiple words', 'has multiple words'),
    ('has <b>some</b> tags', 'has some tags'),
    ("<IMG SRC=j&#X41vascript:alert('test2')>", ''),
])
def test_strip_all_tags(input, text):
    assert strip_all_tags(input) == text


@pytest.mark.parametrize('input, text', [
    ('foo', 'foo'),
    ('has multiple words', 'has multiple words'),
    ('has <b>some</b> tags', 'has some tags'),
    ('x" onload="alert()"', 'x onload alert'),
    ("'; drop database; x='y", 'drop database x y'),
    ("<IMG SRC=j&#X41vascript:alert('test2')>", ''),
    ('=/*-+.', ''),
])
def test_extract_text(input, text):
    assert extract_text(input) == text
