# pylint: skip-file
from sorter.lib.rank import rank, score_book, get_total_ratings

class TestRank(object):
    def test_rank(self, monkeypatch):
        monkeypatch.setattr("sorter.lib.rank.score_book", lambda foo, bar: foo[0])
        monkeypatch.setattr("sorter.lib.rank.get_total_ratings", lambda foo: 1234)

        fake_data = [
            (1,2,3,4,5,6,7,8,9),
            (9,8,7,6,5,4,3,2,1)
        ]

        ranked_fake_data = rank(fake_data)

        assert ranked_fake_data == [
            (9,8,7,6,5,4,3,2,1,9),
            (1,2,3,4,5,6,7,8,9,1)
        ]

    def test_score_book(self):
        fake_data = (1,2,3,4,5,6,7,8,9)
        foo = score_book(fake_data, 100)

        assert foo == 1595.2

    def test_score_book_bad_year(self, monkeypatch):
        logger = FAKE_LOGGER()
        monkeypatch.setattr('sorter.lib.rank.LOGGER', logger)
        fake_data = (1,2,3,4,5,None,7,8,9)
        foo = score_book(fake_data, 100)

        assert foo == 0.0
        assert logger.called_warn == True

    def test_score_book_bad_ratings(self, monkeypatch):
        logger = FAKE_LOGGER()
        monkeypatch.setattr('sorter.lib.rank.LOGGER', logger)
        fake_data = (1,2,3,4,5,6,None,8,9)
        foo = score_book(fake_data, 100)

        assert foo == 1595.2
        assert logger.called_warn == True

    def test_score_book_bad_avg_ratings(self, monkeypatch):
        logger = FAKE_LOGGER()
        monkeypatch.setattr('sorter.lib.rank.LOGGER', logger)
        fake_data = (1,2,3,4,5,6,7,None,9)
        foo = score_book(fake_data, 100)

        assert foo == 0.0
        assert logger.called_warn == True

    def test_score_book_bad_isbn_and_year(self, monkeypatch):
        logger = FAKE_LOGGER()
        monkeypatch.setattr('sorter.lib.rank.LOGGER', logger)
        fake_data = (1,None,3,4,5,None,7,8,9)
        foo = score_book(fake_data, 100)

        assert foo == 0.0
        assert logger.called_warn == True

    def test_score_book_bad_isbn_isbn13_and_year(self, monkeypatch):
        logger = FAKE_LOGGER()
        monkeypatch.setattr('sorter.lib.rank.LOGGER', logger)
        fake_data = (1,None,None,4,5,None,7,8,9)
        foo = score_book(fake_data, 100)

        assert foo == 0.0
        assert logger.called_warn == True

    def test_score_book_bad_isbn_isbn13_id_and_year(self, monkeypatch):
        logger = FAKE_LOGGER()
        monkeypatch.setattr('sorter.lib.rank.LOGGER', logger)
        fake_data = (None,None,None,4,5,None,7,8,9)
        foo = score_book(fake_data, 100)

        assert foo == 0.0
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

