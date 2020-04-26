import unittest

from private.config import configure_resources

if __name__ == '__main__':
    configure_resources()
    from tests.base_test import TestEdu
    unittest.main()


