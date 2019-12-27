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
