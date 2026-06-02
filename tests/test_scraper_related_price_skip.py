from app.scraper.scraper import fetch_price


def test_fetch_price_skip_related_price(requests_mock):

    html = """
    <html>
      <body>

        <div id="sub-main">

            <div class="related-products">
                <span class="price">
                    99999円
                </span>
            </div>

            <span class="price">
                3980円
            </span>

        </div>

      </body>
    </html>
    """

    requests_mock.get(
        "http://example.com",
        text=html
    )

    assert fetch_price("http://example.com") == 3980