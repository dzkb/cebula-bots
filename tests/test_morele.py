import pytest

from jobs.morele import _parse_morele


def test_morele_parsing(morele_alert_html):
    response = _parse_morele(morele_alert_html)

    assert response.title == "TestProduct"
    assert response.image_url == "https://example.com/image"
    assert response.offer_url == "https://example.com"
