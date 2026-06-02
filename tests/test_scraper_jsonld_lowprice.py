from app.scraper.scraper import fetch_price


def test_fetch_price_jsonld_lowprice(requests_mock):

    html = """
    <html>
      <body>

        <div id="sub-main">
          <script type="application/ld+json">
          {
            "offers": {
              "lowPrice": "2980"
            }
          }
          </script>
        </div>

      </body>
    </html>
    """

    requests_mock.get(
        "http://example.com",
        text=html
    )

    assert fetch_price("http://example.com") == 2980