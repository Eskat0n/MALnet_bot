import unittest

import mal


class MalClientTests(unittest.TestCase):
    def test_search(self):
        results = mal.search('full metal alchemist')

        print(results)


if __name__ == '__main__':
    unittest.main()
