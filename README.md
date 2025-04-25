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
