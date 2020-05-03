import unittest

from private.config import Configurator

if __name__ == '__main__':
    Configurator.configure_resources()
    from tests.base_test import TestEdu
    unittest.main()


