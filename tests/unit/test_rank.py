# pylint: skip-file
from sorter.lib.rank import rank, score_book, get_total_ratings

class TestRank(object):
    def test_rank(self, monkeypatch):
        monkeypatch.setattr("sorter.lib.rank.score_book", lambda foo, bar: foo[0])
        monkeypatch.setattr("sorter.lib.rank.get_total_ratings", lambda foo: 1234)

        fake_data = [
            (1,2,3,4,5,6,7,8,9,10,0.02),
            (9,8,7,6,5,4,3,2,1,10,0.01)
        ]

        ranked_fake_data = rank(fake_data)

        assert ranked_fake_data == [
            (9,8,7,6,5,4,3,2,1,10,0.01,9),
            (1,2,3,4,5,6,7,8,9,10,0.02,1)
        ]

    def test_score_book(self):
        fake_data = (1,2,3,4,5,6,7,8,9,10,0.2)
        foo = score_book(fake_data, 100)

        assert foo == 160.0

    def test_score_book_bad_year(self, monkeypatch):
        logger = FAKE_LOGGER()
        monkeypatch.setattr('sorter.lib.rank.LOGGER', logger)
        fake_data = (1,2,3,4,5,None,7,8,9,None,0.1)
        foo = score_book(fake_data, 100)

        assert foo == 80.0
        assert logger.called_warn == True

    def test_score_book_bad_ratings(self, monkeypatch):
        logger = FAKE_LOGGER()
        monkeypatch.setattr('sorter.lib.rank.LOGGER', logger)
        fake_data = (1,2,3,4,5,6,None,8,9,None,0.2)
        foo = score_book(fake_data, 100)

        assert foo == 160.0
        assert logger.called_warn == True

    def test_score_book_bad_avg_ratings(self, monkeypatch):
        logger = FAKE_LOGGER()
        monkeypatch.setattr('sorter.lib.rank.LOGGER', logger)
        fake_data = (1,2,3,4,5,6,7,None,9,None,0.3)
        foo = score_book(fake_data, 100)

        assert foo == 0.0
        assert logger.called_warn == True

    def test_score_book_bad_isbn_and_year(self, monkeypatch):
        logger = FAKE_LOGGER()
        monkeypatch.setattr('sorter.lib.rank.LOGGER', logger)
        fake_data = (1,None,3,4,5,None,7,8,9,None,0.4)
        foo = score_book(fake_data, 100)

        assert foo == 320.0
        assert logger.called_warn == True

    def test_score_book_bad_isbn_isbn13_and_year(self, monkeypatch):
        logger = FAKE_LOGGER()
        monkeypatch.setattr('sorter.lib.rank.LOGGER', logger)
        fake_data = (1,None,None,4,5,None,7,8,9,None,0.5)
        foo = score_book(fake_data, 100)

        assert foo == 400.0
        assert logger.called_warn == True

    def test_score_book_bad_isbn_isbn13_id_and_year(self, monkeypatch):
        logger = FAKE_LOGGER()
        monkeypatch.setattr('sorter.lib.rank.LOGGER', logger)
        fake_data = (None,None,None,4,5,None,7,8,9,None,0.6)
        foo = score_book(fake_data, 100)

        assert foo == 480.0
        assert logger.called_warn == True

    def test_get_total_ratings(self):
        fake_data = [
            (1,2,3,4,5,6,7,8,9),
            (9,8,7,6,5,4,3,2,1)
        ]

        fake_total = get_total_ratings(fake_data)

        assert fake_total == 10


class FAKE_LOGGER(object):
    def __init__(self):
        self.called_warn = False

    def warn(self, *arg):
        self.called_warn = True

