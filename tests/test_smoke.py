"""Import the actual app and exercise DB-free routes; no PostgreSQL required."""
import importlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import jwt
from tests.test_config import ENV


class AppSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with patch.dict(os.environ, ENV, clear=True):
            cls.app = importlib.import_module('main').app
        cls.app.config['TESTING'] = True

    def test_registered_modules_and_static_dashboard(self):
        self.assertEqual(set(self.app.blueprints), {'user', 'teacher', 'calendar', 'assessment', 'dashboard', 'classes'})
        response = self.app.test_client().get('/dashboard/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 1)
        self.assertEqual(len(response.json['dashboards']), 2)

    def test_database_password_is_not_url_interpreted(self):
        from private.db.models import db_connection
        self.assertEqual(db_connection.url.password, ENV['DB_PASSWORD'])

    def test_image_directory_override(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(self.app.config, IMAGES_FOLDER=directory):
            Path(directory, '123.jpg').write_bytes(b'synthetic-image-test')
            response = self.app.test_client().get('/assessment/123')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'synthetic-image-test')
            response.close()

    def test_jwt_roundtrip_and_invalid_signature(self):
        from private.service.auth import TokenAuth
        with self.app.app_context():
            auth = TokenAuth()
            token = auth.create_auth_token(123, 4)
            self.assertIsInstance(token, str)
            self.assertEqual(auth.verify_token(token), (123, 4))
            forged = jwt.encode({'sub': '123', 'class': 4}, 'different-test-key-' * 3, algorithm='HS256')
            with self.assertRaises(jwt.InvalidSignatureError):
                auth.verify_token(forged)

    def test_schema_cli_can_locate_app(self):
        from click.testing import CliRunner
        from commands import client, meta
        with patch.object(meta, 'create_all') as create:
            result = CliRunner().invoke(client, ['create_db'])
        self.assertEqual(result.exit_code, 0, result.output)
        create.assert_called_once_with()
