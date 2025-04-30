這是一個穩定的 PostgreSQL 高可用叢集架構

---

## 📦 三節點 Patroni + etcd + Redis + pgAdmin + HAProxy 架構

### 🧱 服務總覽：

| 服務 | 描述 |
|------|------|
| `etcd` | 共識系統，負責 leader 選舉與註冊資訊 |
| `patroni-1` | 初始主節點（primary） |
| `patroni-2` | 副本節點（replica） |
| `patroni-3` | 備援副本節點（replica） |
| `redis` | 你的 Redis server |
| `pgadmin` | PostgreSQL Web 管理工具 |
| `haproxy` | 負載均衡器 |

---

## ⚙️ 提供項目：

- ✅ `docker-compose.yml`
- ✅ 每個 Patroni 節點的設定（`patroni.yml`）
- ✅ etcd 預設配置
- ✅ pg_hba.conf 設定
- ✅ Redis 預設配置
- ✅ pgAdmin 預設帳號密碼
- ✅ HAProxy 負載均衡設定
- ✅ 健康檢查配置
- ✅ 密碼生成工具

---

## ✅ 三節點 Patroni 自動主從切換架構（本地資料夾）

資料夾架構：

```
patroni-cluster/
├── docker-compose.yml
├── etcd/
│   └── docker-entrypoint.sh
├── patroni/
│   ├── patroni-1.yml
│   ├── patroni-2.yml
│   ├── patroni-3.yml
│   └── pg_hba.conf
├── redis/
│   └── redis.conf
├── pgadmin/
│   └── servers.json（或環境變數）
├── haproxy/
│   └── haproxy.cfg
├── data/
│   ├── patroni-1/
│   ├── patroni-2/
│   └── patroni-3/
├── generate_password.py
└── .env
```

---

### ✨ 功能說明：

- **自動主從切換（Patroni + etcd）**
- **pgAdmin 可視化管理**
- **Redis 可由其他應用連接使用**
- **HAProxy 負載均衡**
- **健康檢查監控**
- **所有資料都儲存在本地 `./data/` 下**

---

## 🔐 環境變數設定

### 密碼生成工具

我們提供了一個跨平台的密碼生成工具 `generate_password.py`，可以生成 PostgreSQL 的 SCRAM-SHA-256 加密密碼。

#### 使用方法：

1. **生成隨機密碼**：
```bash
python generate_password.py
```

2. **使用指定密碼**：
```bash
python generate_password.py -p "your_password"
```

3. **生成 .env 格式輸出**：
```bash
python generate_password.py -p "your_password" -e
```

4. **指定迭代次數**：
```bash
python generate_password.py -p "your_password" -i 10000
```

#### 參數說明：
- `-p, --password`: 要加密的密碼（如果不提供，會生成隨機密碼）
- `-i, --iterations`: PBKDF2 迭代次數（預設：4096）
- `-e, --env`: 生成 .env 格式的輸出

#### 輸出範例：
```bash
# 生成隨機密碼
python generate_password.py
生成的隨機密碼: XhdZE2WAUyibYjqLbo8Iug
加密後的密碼: SCRAM-SHA-256$4096:...

# 生成 .env 格式
python generate_password.py -p "test123" -e
# 將以下內容複製到 .env 檔案中：
POSTGRES_PASSWORD=SCRAM-SHA-256$4096:...
PATRONI_REPLICATION_PASSWORD=SCRAM-SHA-256$4096:...
PATRONI_ADMIN_PASSWORD=SCRAM-SHA-256$4096:...
```

### 環境變數設定

創建 `.env` 檔案並設定以下環境變數：

```env
# PostgreSQL 密碼 (已使用 SCRAM-SHA-256 加密)
POSTGRES_PASSWORD=your_encrypted_password

# Redis 密碼
REDIS_PASSWORD=your_redis_password

# pgAdmin 設定
PGADMIN_EMAIL=your_email@example.com
PGADMIN_PASSWORD=your_pgadmin_password

# Patroni 複製密碼
PATRONI_REPLICATION_PASSWORD=your_encrypted_password

# Patroni 管理員密碼
PATRONI_ADMIN_PASSWORD=your_encrypted_password
```

---

## 🚀 部署步驟

1. 設定環境變數：
   ```bash
   # 使用密碼生成工具生成密碼
   python generate_password.py -p "your_password" -e > .env
   # 編輯 .env 檔案設定其他環境變數
   ```

2. 啟動服務：
   ```bash
   docker-compose up -d
   ```

3. 檢查服務狀態：
   ```bash
   docker-compose ps
   ```

4. 查看日誌：
   ```bash
   docker-compose logs -f
   ```

---

## 📊 pgAdmin 連線設置

### 1. 訪問 pgAdmin

1. 打開瀏覽器，訪問：
```
http://localhost:5050
```

2. 使用以下憑證登入：
```
Email: ${PGADMIN_EMAIL}
Password: ${PGADMIN_PASSWORD}
```

3. 自動導入設定
   我們提供了自動導入的伺服器設定檔 `pgadmin/servers.json`，它會自動配置：
   - HAProxy 負載均衡連線
   - 所有 Patroni 節點的直接連線
   - 適當的 SSL 設定
   登入後，你應該能看到以下伺服器：
   - Patroni Cluster (HAProxy)
   - Patroni-1 (Primary)
   - Patroni-2 (Replica)
   - Patroni-3 (Replica)

### 2. 添加新伺服器

1. 右鍵點擊 "Servers" -> "Register" -> "Server"

2. 在 "General" 標籤頁：
   - Name: Patroni Cluster（或任何你喜歡的名稱）

3. 在 "Connection" 標籤頁：
   - Host name/address: localhost
   - Port: 5435（HAProxy 端口）
   - Maintenance database: postgres
   - Username: postgres
   - Password: ${POSTGRES_PASSWORD}

4. 在 "SSL" 標籤頁：
   - SSL mode: Prefer

5. 點擊 "Save" 保存設定

### 3. 驗證連線

1. 展開伺服器列表，應該能看到：
   - Databases
   - Login/Group Roles
   - Tablespaces
   - Catalogs

2. 檢查複製狀態：
   - 展開 "Databases" -> "postgres" -> "Statistics"
   - 查看 "Replication" 標籤頁

### 4. 常見問題

1. **連線被拒絕**：
   - 檢查 HAProxy 是否正常運行
   - 確認端口 5435 是否開放
   - 驗證密碼是否正確

2. **無法看到複製資訊**：
   - 確認 Patroni 叢集是否正常運行
   - 檢查 etcd 是否正常運行
   - 查看 Patroni 日誌

3. **SSL 錯誤**：
   - 將 SSL mode 改為 "Prefer" 或 "Disable"
   - 檢查 SSL 證書設定

### 5. 安全建議

1. 使用強密碼
2. 定期更換密碼
3. 限制 pgAdmin 的訪問 IP
4. 啟用 SSL/TLS
5. 定期備份 pgAdmin 設定

---

## 🛡️ 安全建議

1. 定期更換密碼
2. 限制網路訪問
3. 啟用 SSL/TLS
4. 定期備份資料
5. 監控系統狀態

---

## 🔍 故障排除

1. 檢查服務狀態：
   ```bash
   docker-compose ps
   ```

2. 查看服務日誌：
   ```bash
   docker-compose logs -f [service_name]
   ```

3. 檢查健康狀態：
   ```bash
   curl http://localhost:8008/health
   ```

4. 常見問題：
   - 如果 Patroni 無法啟動，檢查 etcd 是否正常運行
   - 如果複製失敗，檢查 pg_hba.conf 設定
   - 如果 HAProxy 無法連接，檢查 Patroni 健康狀態

5. 文件:
   - [spilo 環境變數](https://github.com/zalando/spilo/blob/master/ENVIRONMENT.rst)
---

## 📊 監控建議

1. 使用 Prometheus + Grafana 監控：
   - PostgreSQL 指標
   - Patroni 狀態
   - 系統資源使用率

2. 設定警報：
   - 主從切換事件
   - 複製延遲
   - 系統資源警告

---

## 🔄 備份策略

1. 定期備份：
   ```bash
   pg_basebackup -h localhost -p 5435 -U postgres -D /backup
   ```

2. WAL 歸檔：
   - 設定 WAL 歸檔目錄
   - 定期清理舊的 WAL 檔案

3. 備份驗證：
   - 定期測試備份還原
   - 驗證資料完整性

## 備份和還原

### WAL 歸檔配置

1. 在 `docker-compose.yml` 中添加 WAL 歸檔目錄：
```yaml
volumes:
  - ./wal_archive:/home/postgres/pgdata/pgroot/wal_archive
```

2. 在 Patroni 配置文件中添加 WAL 歸檔設定：
```yaml
postgresql:
  parameters:
    archive_mode: "on"
    archive_command: 'test ! -f /home/postgres/pgdata/pgroot/wal_archive/%f && cp %p /home/postgres/pgdata/pgroot/wal_archive/%f'
    archive_timeout: 60
    wal_level: replica
```

### 備份策略

1. **基礎備份**：
```bash
# 使用 pg_basebackup 創建基礎備份
pg_basebackup -h localhost -p 5435 -U postgres -D /backup/pg_basebackup -Ft -z -P
```

2. **WAL 歸檔**：
- WAL 文件會自動歸檔到 `./wal_archive` 目錄
- 建議定期將歸檔文件備份到異地存儲

3. **備份驗證**：
```bash
# 驗證 WAL 文件完整性
pg_waldump /path/to/wal_archive/000000010000000000000001
```

### 還原步驟

1. **準備還原環境**：
```bash
# 創建還原目錄
mkdir -p /restore
# 解壓基礎備份
tar -xzf /backup/pg_basebackup/base.tar.gz -C /restore
```

2. **配置還原參數**：
在 `/restore/postgresql.conf` 中添加：
```conf
restore_command = 'cp /path/to/wal_archive/%f %p'
recovery_target_timeline = 'latest'
```

3. **創建還原標記文件**：
```bash
touch /restore/recovery.signal
```

4. **啟動還原實例**：
```bash
# 修改端口避免衝突
sed -i 's/port = 5432/port = 5436/' /restore/postgresql.conf
# 啟動 PostgreSQL
pg_ctl -D /restore start
```

### 自動化備份腳本

創建 `backup.sh` 腳本：
```bash
#!/bin/bash

# 設置變量
BACKUP_DIR="/backup"
WAL_ARCHIVE_DIR="./wal_archive"
DATE=$(date +%Y%m%d_%H%M%S)

# 創建基礎備份
pg_basebackup -h localhost -p 5435 -U postgres \
    -D ${BACKUP_DIR}/pg_basebackup_${DATE} \
    -Ft -z -P

# 壓縮 WAL 歸檔
tar -czf ${BACKUP_DIR}/wal_archive_${DATE}.tar.gz ${WAL_ARCHIVE_DIR}

# 清理舊的備份（保留最近 7 天的備份）
find ${BACKUP_DIR} -name "pg_basebackup_*" -mtime +7 -delete
find ${BACKUP_DIR} -name "wal_archive_*" -mtime +7 -delete
```

### 監控備份狀態

1. **檢查 WAL 歸檔狀態**：
```sql
SELECT * FROM pg_stat_archiver;
```

2. **檢查備份進度**：
```sql
SELECT * FROM pg_stat_progress_basebackup;
```

3. **設置備份監控告警**：
- 監控 WAL 歸檔目錄大小
- 檢查備份文件完整性
- 設置備份失敗通知

### 最佳實踐

1. **備份策略**：
- 每日進行基礎備份
- 實時 WAL 歸檔
- 定期異地備份
- 定期備份驗證

2. **存儲管理**：
- 定期清理舊的 WAL 文件
- 監控磁盤使用情況
- 設置存儲告警閾值

3. **安全考慮**：
- 加密備份文件
- 限制備份目錄訪問權限
- 定期測試還原流程

4. **性能優化**：
- 使用並行備份
- 調整 WAL 歸檔參數
- 優化備份時間窗口
