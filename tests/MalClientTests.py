import unittest

import mal


class MalClientTests(unittest.TestCase):
    def test_search_anime(self):
        entries = mal.search_anime('full metal alchemist')

        print(entries)

    def test_search_manga(self):
        entries = mal.search_manga('full metal alchemist')

        print(entries)


if __name__ == '__main__':
    unittest.main()
