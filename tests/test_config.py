"""Environment configuration tests; no database connection or real credentials."""
import os
import tempfile
import unittest
from unittest.mock import patch

from private.config import Configurator

ENV = {
    'DB_USER': 'test_user', 'DB_PASSWORD': 'synthetic@:/password',
    'DB_NAME': 'test_database', 'FLASK_SECRET': 'synthetic-test-only-' * 3,
}


class ConfigTests(unittest.TestCase):
    def test_dev_defaults(self):
        with patch.dict(os.environ, ENV, clear=True):
            Configurator.configure_resources()
        self.assertEqual(Configurator.db['host'], '127.0.0.1')
        self.assertEqual(Configurator.db['port'], 5432)
        self.assertTrue(Configurator.app_config['images_folder'].endswith('/pictures'))

    def test_missing_variables_report_names_only(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, 'DB_USER, DB_PASSWORD, DB_NAME, FLASK_SECRET'):
                Configurator.configure_resources()

    def test_prod_requires_explicit_host_and_path(self):
        with patch.dict(os.environ, dict(ENV, SERVER_MODE='PROD'), clear=True):
            with self.assertRaisesRegex(ValueError, 'DB_HOST, IMAGES_FOLDER'):
                Configurator.configure_resources()

    def test_prod_overrides(self):
        env = dict(ENV, SERVER_MODE='PROD', DB_HOST='db', DB_PORT='5433', IMAGES_FOLDER='/tmp/test-images')
        with patch.dict(os.environ, env, clear=True):
            Configurator.configure_resources()
        self.assertEqual(Configurator.db['host'], 'db')
        self.assertEqual(Configurator.db['port'], 5433)
        self.assertEqual(Configurator.app_config['images_folder'], '/tmp/test-images')

    def test_invalid_mode(self):
        with patch.dict(os.environ, dict(ENV, SERVER_MODE='PRODD'), clear=True):
            with self.assertRaisesRegex(ValueError, 'SERVER_MODE'):
                Configurator.configure_resources()

    def test_invalid_port(self):
        for value in ['not-a-port', '0', '65536']:
            with self.subTest(value=value), patch.dict(os.environ, dict(ENV, DB_PORT=value), clear=True):
                with self.assertRaisesRegex(ValueError, 'DB_PORT'):
                    Configurator.configure_resources()

    def test_short_secret(self):
        with patch.dict(os.environ, dict(ENV, FLASK_SECRET='short'), clear=True):
            with self.assertRaisesRegex(ValueError, 'at least 32'):
                Configurator.configure_resources()

    def test_config_path_is_independent_of_working_directory(self):
        previous = os.getcwd()
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, ENV, clear=True):
            try:
                os.chdir(directory)
                Configurator.configure_resources()
            finally:
                os.chdir(previous)
