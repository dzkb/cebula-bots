import pytest


@pytest.fixture
def xkom_hotshot_html():
    return r"""
<div class="container">
    <script type="module" src="..."></script>
    <script>
      window.__ENV = {};
      
      window.__INITIAL_STATE__ = window.__INITIAL_STATE__ || {}; window.__INITIAL_STATE__['app'] = {'productsLists': {'recommendedProducts': [{'type': 'Promotion', 'extend': {'promotionId': '0000005597970002', 'title': 'Apple iPhone SE 128GB Black', 'html': None, 'photo': {'url': 'https://cdn.x-kom.pl/i/setup/images/prod/big/product-large,,2020/4/pr_2020_4_15_19_27_7_398_03.jpg', 'thumbnailUrl': 'https://cdn.x-kom.pl/i/setup/images/prod/big/product-small,,2020/4/pr_2020_4_15_19_27_7_398_03.jpg', 'urlTemplate': 'https://cdn.x-kom.pl/i/setup/images/prod/big/{SIZE},,2020/4/pr_2020_4_15_19_27_7_398_03.jpg'}, 'type': 'Recommended'}, 'id': '559797'}], 'hotShot': [{'type': 'HotShot', 'extend': {'id': '22106', 'price': 39, 'oldPrice': 59, 'promotionGainText': 'Oszczędź 34%', 'promotionGainTextLines': ['Oszczędź', '34 %'], 'promotionGainValue': 20, 'promotionTotalCount': 1000, 'saleCount': 1000, 'maxBuyCount': 0, 'promotionName': 'Samsung 64GB microSDXC Evo Plus', 'promotionEnd': '2020-07-03T20:00:00Z', 'htmlContent': None, 'promotionPhoto': {'url': 'https://cdn.x-kom.pl/i/img/promotions/hot-shot-large,,hs_2020_7_3_8_56_41.PNG', 'thumbnailUrl': 'https://cdn.x-kom.pl/i/img/promotions/hot-shot-large,,hs_2020_7_3_8_56_41.PNG', 'urlTemplate': None}, 'isActive': True, 'isSuspended': False, 'minimumInstallmentValue': None, 'hotShotBuyOffers': [{'customer': 'ra...pl', 'count': 1, 'date': '2020-07-03T08:18:11Z'}]}, 'id': '360784'}], 'complementaryProducts360784': [{'type': 'Base', 'id': '550477'}]}};
      window.__NEWWEB_SSR_VERSION = window.__NEWWEB_SSR_VERSION || {}; window.__NEWWEB_SSR_VERSION['app'] = "20200630.01";
      window.__MAINAPP__ = true;
    </script>
</div>
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
