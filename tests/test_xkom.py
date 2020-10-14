from json import loads

from jobs.xkom import _parse_xkom


def test_xkom_parsing(xkom_hotshot_html):
    response = _parse_xkom(loads(xkom_hotshot_html), skip_date_check=True)

    assert response.title == "TestProduct"
    assert response.image_url == "https://example.com"
