#!/usr/bin/env python3
import os
import time
import psycopg2
import docker
from typing import Optional, Tuple
import sys
from colorama import init, Fore, Style

# 初始化 colorama
init()

class PatroniTester:
    def __init__(self):
        self.postgres_password = os.getenv('POSTGRES_PASSWORD')
        self.admin_password = os.getenv('PATRONI_ADMIN_PASSWORD')
        self.docker_client = docker.from_env()
        
        if not self.postgres_password or not self.admin_password:
            print(f"{Fore.RED}錯誤: 請先設置必要的環境變數{Style.RESET_ALL}")
            print("請確保以下環境變數已設置:")
            print("- POSTGRES_PASSWORD")
            print("- PATRONI_ADMIN_PASSWORD")
            sys.exit(1)

    def connect_db(self, host: str, port: int, user: str, password: str) -> Optional[psycopg2.extensions.connection]:
        """建立資料庫連接"""
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database='postgres'
            )
            return conn
        except Exception as e:
            print(f"{Fore.RED}連接失敗: {e}{Style.RESET_ALL}")
            return None

    def test_connection(self) -> bool:
        """測試連接"""
        print(f"{Fore.YELLOW}測試連接...{Style.RESET_ALL}")
        
        # 測試 HAProxy 連接
        print("測試 HAProxy 連接...")
        conn = self.connect_db('localhost', 5435, 'postgres', self.postgres_password)
        if conn:
            print(f"{Fore.GREEN}HAProxy 連接成功{Style.RESET_ALL}")
            conn.close()
        else:
            print(f"{Fore.RED}HAProxy 連接失敗{Style.RESET_ALL}")
            return False

        # 測試各個節點連接
        for port in [5432, 5433, 5434]:
            print(f"測試節點端口 {port} 連接...")
            conn = self.connect_db('localhost', port, 'postgres', self.postgres_password)
            if conn:
                print(f"{Fore.GREEN}端口 {port} 連接成功{Style.RESET_ALL}")
                conn.close()
            else:
                print(f"{Fore.RED}端口 {port} 連接失敗{Style.RESET_ALL}")
                return False
        
        return True

    def test_authentication(self) -> bool:
        """測試認證"""
        print(f"{Fore.YELLOW}測試認證...{Style.RESET_ALL}")
        
        # 測試 superuser
        print("測試 superuser 認證...")
        conn = self.connect_db('localhost', 5435, 'postgres', self.postgres_password)
        if conn:
            with conn.cursor() as cur:
                cur.execute("SELECT current_user;")
                user = cur.fetchone()[0]
                if user == 'postgres':
                    print(f"{Fore.GREEN}superuser 認證成功{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}superuser 認證失敗{Style.RESET_ALL}")
                    return False
            conn.close()
        else:
            return False

        # 測試 admin 用戶
        print("測試 admin 用戶認證...")
        conn = self.connect_db('localhost', 5435, 'admin', self.admin_password)
        if conn:
            with conn.cursor() as cur:
                cur.execute("SELECT current_user;")
                user = cur.fetchone()[0]
                if user == 'admin':
                    print(f"{Fore.GREEN}admin 用戶認證成功{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}admin 用戶認證失敗{Style.RESET_ALL}")
                    return False
            conn.close()
        else:
            return False
        
        return True

    def test_replication(self) -> bool:
        """測試複製"""
        print(f"{Fore.YELLOW}測試複製...{Style.RESET_ALL}")
        
        # 在 primary 創建測試表
        print("在 primary 創建測試表...")
        conn = self.connect_db('localhost', 5435, 'postgres', self.postgres_password)
        if not conn:
            return False

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS test_replication (
                        id serial PRIMARY KEY,
                        data text
                    );
                    INSERT INTO test_replication (data) VALUES ('test data');
                """)
            conn.commit()
        except Exception as e:
            print(f"{Fore.RED}創建測試表失敗: {e}{Style.RESET_ALL}")
            return False
        finally:
            conn.close()

        # 等待複製
        time.sleep(2)

        # 檢查所有節點是否都有數據
        for port in [5432, 5433, 5434]:
            print(f"檢查節點端口 {port} 的數據...")
            conn = self.connect_db('localhost', port, 'postgres', self.postgres_password)
            if not conn:
                return False

            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) FROM test_replication;")
                    count = cur.fetchone()[0]
                    if count == 1:
                        print(f"{Fore.GREEN}端口 {port} 數據同步成功{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}端口 {port} 數據同步失敗{Style.RESET_ALL}")
                        return False
            except Exception as e:
                print(f"{Fore.RED}檢查數據失敗: {e}{Style.RESET_ALL}")
                return False
            finally:
                conn.close()
        
        return True

    def get_primary_port(self) -> Optional[int]:
        """獲取當前 primary 端口"""
        conn = self.connect_db('localhost', 5435, 'postgres', self.postgres_password)
        if not conn:
            return None

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT port FROM pg_stat_replication;")
                result = cur.fetchone()
                if result:
                    return result[0]
        except Exception as e:
            print(f"{Fore.RED}獲取 primary 端口失敗: {e}{Style.RESET_ALL}")
        finally:
            conn.close()
        return None

    def test_failover(self) -> bool:
        """測試故障轉移"""
        print(f"{Fore.YELLOW}測試故障轉移...{Style.RESET_ALL}")
        
        # 獲取當前 primary
        primary_port = self.get_primary_port()
        if not primary_port:
            print(f"{Fore.RED}無法獲取 primary 端口{Style.RESET_ALL}")
            return False

        print(f"當前 primary 端口: {primary_port}")
        
        # 停止 primary
        print("停止 primary 節點...")
        container_name = f"patroni-{primary_port - 5430}"
        try:
            container = self.docker_client.containers.get(container_name)
            container.stop()
        except Exception as e:
            print(f"{Fore.RED}停止節點失敗: {e}{Style.RESET_ALL}")
            return False
        
        # 等待故障轉移
        print("等待故障轉移...")
        time.sleep(10)
        
        # 檢查新的 primary
        new_primary_port = self.get_primary_port()
        if not new_primary_port:
            print(f"{Fore.RED}無法獲取新的 primary 端口{Style.RESET_ALL}")
            return False

        print(f"新的 primary 端口: {new_primary_port}")
        
        if primary_port != new_primary_port:
            print(f"{Fore.GREEN}故障轉移成功{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}故障轉移失敗{Style.RESET_ALL}")
            return False
        
        # 恢復停止的節點
        print("恢復停止的節點...")
        try:
            container = self.docker_client.containers.get(container_name)
            container.start()
        except Exception as e:
            print(f"{Fore.RED}恢復節點失敗: {e}{Style.RESET_ALL}")
            return False
        
        return True

def main():
    tester = PatroniTester()
    
    print(f"{Fore.YELLOW}開始 Patroni 集群測試...{Style.RESET_ALL}")
    
    if tester.test_connection():
        if tester.test_authentication():
            if tester.test_replication():
                tester.test_failover()
    
    print(f"{Fore.YELLOW}測試完成{Style.RESET_ALL}")

if __name__ == '__main__':
    main() 