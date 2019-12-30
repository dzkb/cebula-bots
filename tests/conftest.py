import pytest


@pytest.fixture
def xkom_hotshot_html():
    return """
<div id="hotShot" class="hot-shot  mainpage-gs" data-products-list-name="Hot Shot">
    <div class="row">
        <div class="col-md-12 col-sm-6 product-impression">
            <img class="img-responsive center-block"
                src="https://example.com"
                alt="TestProduct">
            <p class="product-name">TestProduct</p>
        </div>
        <div class="col-md-12 col-sm-6">
            <div class="clearfix price">
                <div class="old-price">100,00 zł</div>
                <div class="new-price">50,00 zł</div>
            </div>
        </div>
    </div>
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
