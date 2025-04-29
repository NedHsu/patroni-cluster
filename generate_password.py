#!/usr/bin/env python3
import base64
import hashlib
import hmac
import secrets
import argparse
import re
import json
import os
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

def generate_md5_password(password: str, username: str) -> str:
    """生成 PostgreSQL MD5 格式的密碼"""
    # MD5 格式：md5 + MD5(password + username)
    md5_hash = hashlib.md5((password + username).encode('utf-8')).hexdigest()
    return f"md5{md5_hash}"

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

def generate_servers_json(password: str) -> dict:
    """生成 pgAdmin servers.json 內容"""
    return {
        "Servers": {
            "1": {
                "Name": "Patroni Cluster (HAProxy)",
                "Group": "Patroni",
                "Host": "haproxy",
                "Port": 5435,
                "MaintenanceDB": "postgres",
                "Username": "postgres",
                "Password": password,
                "SSLMode": "prefer"
            },
            "2": {
                "Name": "Patroni-1 (Primary)",
                "Group": "Patroni",
                "Host": "patroni-1",
                "Port": 5432,
                "MaintenanceDB": "postgres",
                "Username": "postgres",
                "Password": password,
                "SSLMode": "prefer"
            },
            "3": {
                "Name": "Patroni-2 (Replica)",
                "Group": "Patroni",
                "Host": "patroni-2",
                "Port": 5432,
                "MaintenanceDB": "postgres",
                "Username": "postgres",
                "Password": password,
                "SSLMode": "prefer"
            },
            "4": {
                "Name": "Patroni-3 (Replica)",
                "Group": "Patroni",
                "Host": "patroni-3",
                "Port": 5432,
                "MaintenanceDB": "postgres",
                "Username": "postgres",
                "Password": password,
                "SSLMode": "prefer"
            }
        }
    }

def main():
    parser = argparse.ArgumentParser(description='生成 PostgreSQL 密碼')
    parser.add_argument('--password', '-p', help='要使用的密碼')
    parser.add_argument('--iterations', '-i', type=int, default=4096, help='PBKDF2 迭代次數 (預設: 4096)')
    parser.add_argument('--env', '-e', action='store_true', help='生成 .env 格式的輸出')
    parser.add_argument('--prefix', help='密碼前綴')
    parser.add_argument('--output-dir', '-o', default='.', help='輸出目錄')
    parser.add_argument('--method', '-m', choices=['scram-sha-256', 'md5'], default='scram-sha-256',
                      help='密碼加密方式 (預設: scram-sha-256)')
    
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
    
    if args.env:
        # 根據加密方式生成密碼
        if args.method == 'md5':
            postgres_password = generate_md5_password(postgres_password, 'postgres')
            replication_password = generate_md5_password(replication_password, 'replicator')
            admin_password = generate_md5_password(admin_password, 'admin')
        else:
            postgres_password = generate_scram_password(postgres_password, args.iterations)
            replication_password = generate_scram_password(replication_password, args.iterations)
            admin_password = generate_scram_password(admin_password, args.iterations)
        
        # 生成 .env 格式的輸出
        print("\n# 將以下內容複製到 .env 檔案中：")
        print(f"POSTGRES_PASSWORD={escape_env_value(postgres_password)}")
        print(f"PATRONI_REPLICATION_PASSWORD={escape_env_value(replication_password)}")
        print(f"PATRONI_ADMIN_PASSWORD={escape_env_value(admin_password)}")
        
        # 生成 servers.json，使用相同的密碼
        servers_json = generate_servers_json(postgres_password)
        servers_json_path = os.path.join(args.output_dir, 'pgadmin', 'servers.json')
        os.makedirs(os.path.dirname(servers_json_path), exist_ok=True)
        with open(servers_json_path, 'w') as f:
            json.dump(servers_json, f, indent=4)
        print(f"\n已生成 servers.json 到 {servers_json_path}")
    else:
        print("\n生成的密碼:")
        print(f"PostgreSQL: {postgres_password}")
        print(f"Replication: {replication_password}")
        print(f"Admin: {admin_password}")

if __name__ == '__main__':
    main() 