import json
import os
import sqlite3
import Database
import base64

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.keywrap import aes_key_wrap_with_padding, aes_key_unwrap_with_padding, InvalidUnwrap
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import padding


class MaasserUserDatabase(Database.DatabaseHelper):
    def initialize(self):
        self.table_name = 'maasser_users'
        self.table_schema = '''
            CREATE TABLE %s (
               id                       INTEGER     PRIMARY KEY     AUTOINCREMENT,
               telegram_id              TEXT        UNIQUE,
               public_key               TEXT        NOT NULL,
               encrypted_private_key    TEXT        NOT NULL,
               encrypted_data           TEXT        NOT NULL
            );'''

    @staticmethod
    def __encrypt_data(telegram_id, data):
        dek = AESGCM.generate_key(bit_length=128)

        aesgcm = AESGCM(dek)
        nonce = os.urandom(12)

        associated_data = str(telegram_id).encode()

        encrypted_data = aesgcm.encrypt(nonce, json.dumps(data).encode(), associated_data)

        return dek, nonce, encrypted_data

    @staticmethod
    def __decrypt_data(telegram_id, dek, nonce, encrypted_data):
        aesgcm = AESGCM(dek)

        associated_data = str(telegram_id).encode()

        data = aesgcm.decrypt(nonce, encrypted_data, associated_data)

        return data

    @staticmethod
    def __wrap_key(key, public_key):
        wrapped_key = public_key.encrypt(
            key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return wrapped_key

    @staticmethod
    def __unwrap_key(wrapped_key, private_key):
        key = private_key.decrypt(
            wrapped_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return key

    @staticmethod
    def __dump_private_key(private_key, password):
        return private_key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.BestAvailableEncryption(password.encode())
        )

    @staticmethod
    def __dump_public_key(public_key):
        return public_key.public_bytes(
            crypto_serialization.Encoding.PEM,
            format=crypto_serialization.PublicFormat.SubjectPublicKeyInfo
        )

    @staticmethod
    def __load_private_key(private_key_str, password):
        try:
            return crypto_serialization.load_pem_private_key(
                        private_key_str,
                        password=password.encode(),
                    )
        except ValueError:
            return None

    @staticmethod
    def __load_public_key(public_key_str):
        return crypto_serialization.load_pem_public_key(public_key_str)

    @staticmethod
    def __generate_asymetric_key():
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=3072
        )

        return key

    def init(self, telegram_id, password):
        key = MaasserUserDatabase.__generate_asymetric_key()

        encrypted_private_key = MaasserUserDatabase.__dump_private_key(key, password)

        public_key = MaasserUserDatabase.__dump_public_key(key.public_key())

        encrypted_data = json.dumps(
            {
                'consolidated': [],
                'unconsolidated': []
            }
        )

        row = self.cur.execute(
            'INSERT INTO  %s'
            ' (telegram_id, public_key, encrypted_private_key, encrypted_data)'
            ' VALUES (?, ?, ?, ?);' % self.table_name,
            (telegram_id, public_key, encrypted_private_key, encrypted_data)
        )
        self.con.commit()

        return row

    def add_data(self, telegram_id, data):
        maasser_user = self.get(telegram_id)

        public_key = MaasserUserDatabase.__load_public_key(maasser_user.public_key)

        dek, nonce, encrypted_data_sub = MaasserUserDatabase.__encrypt_data(telegram_id, data)

        encrypted_dek = MaasserUserDatabase.__wrap_key(dek, public_key)

        encrypted_data = json.loads(maasser_user.encrypted_data)

        encrypted_data['unconsolidated'] += [
                [
                    encrypted_dek.hex(),
                    nonce.hex(),
                    encrypted_data_sub.hex()
                ]
            ]

        encrypted_data = json.dumps(encrypted_data)

        row = self.cur.execute(
            'UPDATE %s'
            ' SET'
            ' encrypted_data = ?'
            ' WHERE telegram_id = ?;' % self.table_name,
            (encrypted_data, telegram_id)
        )
        self.con.commit()

        return row

    def consolidate(self, telegram_id, password):
        maasser_user = self.get(telegram_id)

        private_key = MaasserUserDatabase.__load_private_key(maasser_user.encrypted_private_key, password)
        if private_key is None:
            return None

        encrypted_data = json.loads(maasser_user.encrypted_data)

        public_key = MaasserUserDatabase.__load_public_key(maasser_user.public_key)

        decrypted_data = []
        if len(encrypted_data['consolidated']) > 0:
            [encrypted_dek, nonce, encrypted_data_sub] = encrypted_data['consolidated']
            [encrypted_dek, nonce, encrypted_data_sub] = [
                bytes.fromhex(encrypted_dek),
                bytes.fromhex(nonce),
                bytes.fromhex(encrypted_data_sub)
            ]
            dek = MaasserUserDatabase.__unwrap_key(encrypted_dek, private_key)
            decrypted_data_sub = MaasserUserDatabase.__decrypt_data(telegram_id, dek, nonce, encrypted_data_sub)
            decrypted_data_sub = json.loads(decrypted_data_sub)
            decrypted_data += decrypted_data_sub

        if len(encrypted_data['unconsolidated']) > 0:
            for e_d in encrypted_data['unconsolidated']:
                [encrypted_dek, nonce, encrypted_data_sub] = e_d
                [encrypted_dek, nonce, encrypted_data_sub] = [
                    bytes.fromhex(encrypted_dek),
                    bytes.fromhex(nonce),
                    bytes.fromhex(encrypted_data_sub)
                ]
                dek = MaasserUserDatabase.__unwrap_key(encrypted_dek, private_key)
                decrypted_data_sub = MaasserUserDatabase.__decrypt_data(telegram_id, dek, nonce, encrypted_data_sub)
                decrypted_data_sub = json.loads(decrypted_data_sub)
                decrypted_data += [decrypted_data_sub]

        if decrypted_data:
            dek, nonce, encrypted_data_sub = MaasserUserDatabase.__encrypt_data(telegram_id, decrypted_data)

            encrypted_dek = MaasserUserDatabase.__wrap_key(dek, public_key)

            encrypted_data = json.dumps(
                {
                    'consolidated': [encrypted_dek.hex(), nonce.hex(), encrypted_data_sub.hex()],
                    'unconsolidated': []
                }
            )

            row = self.cur.execute(
                'UPDATE %s'
                ' SET'
                ' encrypted_data = ?'
                ' WHERE telegram_id = ?;' % self.table_name,
                (encrypted_data, telegram_id)
            )
            self.con.commit()

        return decrypted_data

    def get(self, telegram_id):
        from Unit import MaasserUser
        rows = self.cur.execute("SELECT * FROM %s WHERE telegram_id = ?;" % self.table_name, (str(telegram_id), ))

        row = rows.fetchone()

        if not row:
            return None

        maasser_user = MaasserUser()

        row_id, telegram_id, public_key, encrypted_private_key, encrypted_data = row

        if telegram_id is not None:
            maasser_user.telegram_id = telegram_id
        if public_key is not None:
            maasser_user.public_key = public_key
        if encrypted_private_key is not None:
            maasser_user.encrypted_private_key = encrypted_private_key
        if encrypted_data is not None:
            maasser_user.encrypted_data = encrypted_data

        return maasser_user