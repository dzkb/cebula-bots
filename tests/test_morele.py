from jobs.morele import _get_response, _parse_morele


def test_morele_scraping():
    response = _get_response()

    assert response.status_code == 200


def test_morele_parsing(morele_alert_html):
    response = _parse_morele(morele_alert_html)

    assert response.title == "TestProduct"
    assert response.description == "~~100.00zł~~ → 50.00zł (-50.00zł/-50%)\nkod: COUPON"
    assert response.image_url == "https://example.com/image"
    assert response.offer_url == "https://example.com"
