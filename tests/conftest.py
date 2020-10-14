import pytest


@pytest.fixture
def xkom_hotshot_html():
    return """
{
    "Id": "12345",
    "Product": null,
    "Price": 50.0,
    "OldPrice": 100.0,
    "PromotionGainText": "Oszczędź 50 zł",
    "PromotionGainTextLines": [
        "Oszczędź",
        "50 zł"
    ],
    "PromotionGainValue": 50.0,
    "PromotionTotalCount": 420,
    "SaleCount": 69,
    "MaxBuyCount": 0,
    "PromotionName": "TestProduct",
    "PromotionEnd": "2020-10-14T08:00:00Z",
    "HtmlContent": null,
    "PromotionPhoto": {
        "Url": "https://example.com",
        "ThumbnailUrl": "https://example.com",
        "UrlTemplate": null
    },
    "IsActive": true,
    "IsSuspended": false,
    "MinimumInstallmentValue": null
}
"""


@pytest.fixture
def morele_alert_html():
    return """
<div class="promotion-box card ">
    <div class="prom-box-content">
        <div class="prom-box-top">
            <a href="https://example.com"
                title="TestProduct" class="prom-box-image">
                <img src="https://example.com/image" alt="TestProduct">
            </a>
            <div class="prom-box-mobile-right">
                <div class="promo-box-price">
                    <div class="promo-box-old-price">100 zł</div>
                    <div class="promo-box-new-price">50 zł</div>
                </div>
                <div class="promo-box-name">
                    <a href="https://example.com"
                        title="TestProduct">TestProduct</a>
                </div>
            </div>
        </div>
        <div class="promo-box-actions">
            <div class="promo-box-code">
                <div class="promo-box-code-value">COUPON</div>
                <div class="promo-box-code-button" data-clipboard-text="COUPON">SKOPIUJ KOD</div>
            </div>
        </div>
    </div>
</div>
    """


@pytest.fixture()
def proline_headshot_html():
    return """
<div id="headshot">
    <a class="fotka"
        href="/product"
        title="TestProduct"><img
            src="/image.jpg"
            title="TestProduct"
            alt="TestProduct"></a>
    <table id="karta">
        <tbody>
            <tr>
                <td class="cena_old"><b>100,00</b>&nbsp;zł</td>
                <td class="cena_new"><b>50,00</b>&nbsp;zł</td>
            </tr>
        </tbody>
    </table>
</div>
    """
