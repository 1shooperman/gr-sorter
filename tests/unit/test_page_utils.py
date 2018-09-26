# pylint: skip-file
from sorter.lib.page_utils import page_loop, page_vars, query_vars

class Flags(object):
    def __init__(self):
        self.called_parse = False
        self.called_store_data = False
        self.called_bootstrap = False
        self.called_dump_data = False

    def truthy_parse(self, *args):
        self.called_parse = True

    def truthy_store_data(self, *args):
        self.called_store_data = True

    def truthy_dump_data(self, *args):
        self.called_dump_data = True

    def truthy_bootstrap(self, *args):
        self.called_bootstrap = True

class Logger(object):
    def __init__(self):
        self.message = []
    
    def warn(self, message, key, *args):
        self.message.append(message % key)


class TestPageUtils(object):
    def test_page_loop(self, monkeypatch):
        flags = Flags()

        monkeypatch.setattr("sorter.lib.page_utils.os.path.abspath", lambda foo: "")
        monkeypatch.setattr("sorter.lib.page_utils.parse", flags.truthy_parse)
        monkeypatch.setattr("sorter.lib.page_utils.store_data", flags.truthy_store_data)
        monkeypatch.setattr("sorter.lib.page_utils.dump_data", flags.truthy_dump_data)
        monkeypatch.setattr("sorter.lib.page_utils.bootstrap", flags.truthy_bootstrap)

        page_loop(None, None, False)

        assert flags.called_parse == True
        assert flags.called_store_data == True
        assert flags.called_bootstrap == False
        assert flags.called_dump_data == False

    def test_page_loop_new(self, monkeypatch):
        flags = Flags()

        monkeypatch.setattr("sorter.lib.page_utils.os.path.abspath", lambda foo: "")
        monkeypatch.setattr("sorter.lib.page_utils.parse", flags.truthy_parse)
        monkeypatch.setattr("sorter.lib.page_utils.store_data", flags.truthy_store_data)
        monkeypatch.setattr("sorter.lib.page_utils.dump_data", flags.truthy_dump_data)
        monkeypatch.setattr("sorter.lib.page_utils.bootstrap", flags.truthy_bootstrap)

        page_loop(None, None, True)

        assert flags.called_parse == True
        assert flags.called_store_data == True
        assert flags.called_bootstrap == True
        assert flags.called_dump_data == True

    def test_page_vars(self):
        new_data, per_page, api_key, user_id = page_vars("www.fake.gtld/foo?user_id=1234&new=1&api_key=fakerkey&per_page=42")

        assert new_data == True
        assert per_page == 42
        assert api_key == "fakerkey"
        assert user_id == "1234"

    def test_page_vars_catches_valueerror(self, monkeypatch):
        logger = Logger()
        monkeypatch.setattr("sorter.lib.page_utils.LOGGER", logger)
        new_data, per_page, api_key, user_id = page_vars("www.fake.gtld/foo?new=boom&per_page=foo&api_key=2&user_id=3")

        assert logger.message == [
            "ValueError with message: invalid literal for int() with base 10: 'boom'",
            "ValueError with message: invalid literal for int() with base 10: 'foo'"
        ]

    def test_page_vars_catches_keyerror(self, monkeypatch):
        logger = Logger()
        monkeypatch.setattr("sorter.lib.page_utils.LOGGER", logger)
        new_data, per_page, api_key, user_id = page_vars("www.fake.gtld/foo")

        assert logger.message == [
            "KeyError for key 'new'", 
            "KeyError for key 'per_page'", 
            "KeyError for key 'api_key'", 
            "KeyError for key 'user_id'"
        ]

    def test_query_vars(self):
        class Storage:          
            def __init__(self):
                self.api_key = 'foo'
        
        api_key, foo = query_vars(Storage())

        assert api_key == 'foo'
        assert foo is None

