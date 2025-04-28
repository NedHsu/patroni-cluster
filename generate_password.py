#!/usr/bin/env python3
import base64
import hashlib
import hmac
import secrets
import argparse
import re
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

def escape_env_value(value: str) -> str:
    """處理 .env 檔案中的特殊符號"""
    # 如果值包含特殊符號，用雙引號包起來
    if any(c in value for c in ' $#"\'\\'):
        # 轉義雙引號和反斜線
        value = value.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{value}"'
    return value

def generate_password(prefix: str = "", length: int = 16) -> str:
    """生成隨機密碼"""
    if prefix:
        return f"{prefix}_{secrets.token_urlsafe(length)}"
    return secrets.token_urlsafe(length)

def main():
    parser = argparse.ArgumentParser(description='生成 PostgreSQL SCRAM-SHA-256 格式的密碼')
    parser.add_argument('--password', '-p', help='要加密的密碼')
    parser.add_argument('--iterations', '-i', type=int, default=4096, help='PBKDF2 迭代次數 (預設: 4096)')
    parser.add_argument('--env', '-e', action='store_true', help='生成 .env 格式的輸出')
    parser.add_argument('--prefix', help='密碼前綴')
    
    args = parser.parse_args()
    
    if not args.password:
        # 如果沒有提供密碼，生成不同的隨機密碼
        postgres_password = generate_password("postgres", 16)
        replication_password = generate_password("repl", 16)
        admin_password = generate_password("admin", 16)
        
        print("生成的隨機密碼:")
        print(f"PostgreSQL: {postgres_password}")
        print(f"Replication: {replication_password}")
        print(f"Admin: {admin_password}")
    else:
        # 如果提供了密碼，使用它作為基礎生成不同的密碼
        base_password = args.password
        postgres_password = f"{base_password}_postgres"
        replication_password = f"{base_password}_repl"
        admin_password = f"{base_password}_admin"
    
    # 生成加密密碼
    postgres_encrypted = generate_scram_password(postgres_password, args.iterations)
    replication_encrypted = generate_scram_password(replication_password, args.iterations)
    admin_encrypted = generate_scram_password(admin_password, args.iterations)
    
    if args.env:
        # 生成 .env 格式的輸出，處理特殊符號
        print("\n# 將以下內容複製到 .env 檔案中：")
        print(f"POSTGRES_PASSWORD={escape_env_value(postgres_encrypted)}")
        print(f"PATRONI_REPLICATION_PASSWORD={escape_env_value(replication_encrypted)}")
        print(f"PATRONI_ADMIN_PASSWORD={escape_env_value(admin_encrypted)}")
    else:
        print("\n加密後的密碼:")
        print(f"PostgreSQL: {postgres_encrypted}")
        print(f"Replication: {replication_encrypted}")
        print(f"Admin: {admin_encrypted}")

if __name__ == '__main__':
    main() 