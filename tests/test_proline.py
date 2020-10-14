from jobs.proline import URL, _get_response, _parse_proline


def test_proline_scraping():
    response = _get_response()

    assert response.status_code == 200


def test_proline_parsing(proline_headshot_html, monkeypatch):
    response = _parse_proline(proline_headshot_html)

    assert response.title == "TestProduct"
    assert response.description == "~~100.00zł~~ → 50.00zł (-50.00zł/-50%)"
    assert response.offer_url == f"{URL}/product"
    assert response.image_url == f"{URL}/image.jpg"
