# pylint: skip-file
from sorter.lib.asset_handler import asset

class TestAssetHandler(object):
    def test_asset_exists_js(self):      
        asset_data, header = asset("tests/fixtures/fake.js")

        assert header == "application/javascript; charset=utf-8"
        assert "Fake JS file" in asset_data


    def test_asset_exists_css(self):
        asset_data, header = asset("tests/fixtures/fake.css")

        assert header == "text/css; charset=utf-8"
        assert "Fake CSS file" in asset_data

    def test_asset_exists_plain(self):
        asset_data, header = asset("tests/fixtures/fake.txt")

        assert header == "text/plain; charset=utf-8"
        assert "Fake Text File" in asset_data

    def test_asset_absent_js(self):
        asset_data, header = asset("tests/fixtures/missing.js")

        assert header == "text/plain; charset=utf-8"
        assert asset_data is None

    def test_asset_absent_css(self):
        asset_data, header = asset("tests/fixtures/missing.css")

        assert header == "text/plain; charset=utf-8"
        assert asset_data is None

    def test_asset_absent_plain(self):
        asset_data, header = asset("tests/fixtures/missing.txt")

        assert header == "text/plain; charset=utf-8"
        assert asset_data is None
