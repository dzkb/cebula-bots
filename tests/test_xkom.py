from json import loads

from jobs.xkom import _get_response, _parse_xkom


def test_xkom_scraping():
    response = _get_response()

    assert response.status_code == 200
    assert type(response.json()) == dict


def test_xkom_parsing(xkom_hotshot_html):
    response = _parse_xkom(loads(xkom_hotshot_html), skip_date_check=True)

    assert response.title == "TestProduct"
    assert (
        response.description
        == "~~100.00zł~~ → 50.00zł (-50.00zł/-50%)\nSprzedano 69 z 420 szt."
    )
    assert response.image_url == "https://example.com"
