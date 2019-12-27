from jobs.xkom import _parse_xkom


def test_xkom_parsing(xkom_hotshot_html):
    response = _parse_xkom(xkom_hotshot_html)

    assert response.title == "TestProduct"
    assert response.image_url == "https://example.com"
