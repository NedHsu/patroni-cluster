#!/usr/bin/env python3
import base64
import hashlib
import hmac
import secrets
import argparse
from typing import Tuple

def generate_salt() -> bytes:
    """生成隨機鹽值"""
    return secrets.token_bytes(16)

def generate_stored_key(password: str, salt: bytes, iterations: int = 4096) -> Tuple[bytes, bytes]:
    """生成 SCRAM-SHA-256 的 stored_key 和 server_key"""
    # 生成 ClientKey
    client_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations
    )
    
    # 生成 StoredKey
    stored_key = hashlib.sha256(client_key).digest()
    
    # 生成 ServerKey
    server_key = hmac.new(
        stored_key,
        b'Server Key',
        hashlib.sha256
    ).digest()
    
    return stored_key, server_key

def generate_scram_password(password: str, iterations: int = 4096) -> str:
    """生成 PostgreSQL SCRAM-SHA-256 格式的密碼"""
    salt = generate_salt()
    stored_key, server_key = generate_stored_key(password, salt, iterations)
    
    # 將二進制數據轉換為 base64
    salt_b64 = base64.b64encode(salt).decode('ascii')
    stored_key_b64 = base64.b64encode(stored_key).decode('ascii')
    server_key_b64 = base64.b64encode(server_key).decode('ascii')
    
    # 組合 SCRAM-SHA-256 格式的密碼
    return f"SCRAM-SHA-256${iterations}:{salt_b64}${stored_key_b64}:{server_key_b64}"

def main():
    parser = argparse.ArgumentParser(description='生成 PostgreSQL SCRAM-SHA-256 格式的密碼')
    parser.add_argument('--password', '-p', help='要加密的密碼')
    parser.add_argument('--iterations', '-i', type=int, default=4096, help='PBKDF2 迭代次數 (預設: 4096)')
    parser.add_argument('--env', '-e', action='store_true', help='生成 .env 格式的輸出')
    
    args = parser.parse_args()
    
    if not args.password:
        # 如果沒有提供密碼，生成一個隨機密碼
        password = secrets.token_urlsafe(16)
        print(f"生成的隨機密碼: {password}")
    else:
        password = args.password
    
    # 生成加密密碼
    encrypted_password = generate_scram_password(password, args.iterations)
    
    if args.env:
        # 生成 .env 格式的輸出
        print("\n# 將以下內容複製到 .env 檔案中：")
        print(f"POSTGRES_PASSWORD={encrypted_password}")
        print(f"PATRONI_REPLICATION_PASSWORD={encrypted_password}")
        print(f"PATRONI_ADMIN_PASSWORD={encrypted_password}")
    else:
        print(f"\n加密後的密碼: {encrypted_password}")

if __name__ == '__main__':
    main() 