from jobs.proline import _parse_proline


def test_proline_parsing(proline_headshot_html, monkeypatch):
    response = _parse_proline(proline_headshot_html)

    assert response.title == "TestProduct"
