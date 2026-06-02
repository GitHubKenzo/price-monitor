from app.scraper.scraper import fetch_price


def test_fetch_price_jsonld_invalid(requests_mock):

    html = """
    <html>
      <body>

        <div id="sub-main">
          <script type="application/ld+json">
          invalid json
          </script>

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