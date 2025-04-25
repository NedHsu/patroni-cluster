這是一個穩定的 PostgreSQL 高可用叢集架構

---

## 📦 三節點 Patroni + etcd + Redis + pgAdmin 架構

### 🧱 服務總覽：

| 服務 | 描述 |
|------|------|
| `etcd` | 共識系統，負責 leader 選舉與註冊資訊 |
| `patroni-1` | 初始主節點（primary） |
| `patroni-2` | 副本節點（replica） |
| `patroni-3` | 備援副本節點（replica） |
| `redis` | 你的 Redis server |
| `pgadmin` | PostgreSQL Web 管理工具 |

---

## ⚙️ 提供項目：

- ✅ `docker-compose.yml`
- ✅ 每個 Patroni 節點的設定（`patroni.yml`）
- ✅ etcd 預設配置
- ✅ pg_hba.conf 設定
- ✅ Redis 預設配置
- ✅ pgAdmin 預設帳號密碼
- ✅ 對外連線設定（可選 nginx）

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
├── data/
│   ├── patroni-1/
│   ├── patroni-2/
│   └── patroni-3/
```

---

### ✨ 功能說明：

- **自動主從切換（Patroni + etcd）**
- **pgAdmin 可視化管理**
- **Redis 可由其他應用連接使用**
- **所有資料都儲存在本地 `./data/` 下**


---

## 🤔 是否需要多台實體伺服器？

### ✅ **開發/測試環境**
你**不需要**多台實體主機，可以：
- 用一台機器啟動所有容器（如你現在用的 docker-compose 架構）
- 模擬 failover、同步、主從切換流程

👉 適合你目前的階段：**本地測試與學習**

---

### ✅ **生產環境 / 真正高可用需求**

你**應該要**使用 **多台實體伺服器**（或 VM）來達成真正的高可用性：

#### 多台機器的優點：
| 好處 | 說明 |
|------|------|
| 🎯 故障隔離 | 一台主機掛掉不會影響整個叢集 |
| 🌍 分散部署 | 可跨資料中心或不同 zone |
| 🚦 真正自動故障轉移 | 不依賴同一台主機上其他容器運作 |
| 🧠 etcd 更安全 | 共識節點應部署在不同主機才能有效運作 |

---

### 💡 一個典型的 HA 架構長這樣：

```text
實體機 A:
  - etcd
  - Patroni-1 (Primary)

實體機 B:
  - etcd
  - Patroni-2 (Replica)

實體機 C:
  - etcd
  - Patroni-3 (Replica)

實體機 D:
  - Redis / pgAdmin / nginx / client apps
```

---

### 🛡️ 最佳建議（生產部署）：

- 至少部署在 **3 台不同主機**（或雲端 VM）
- 每個主機跑一個 `etcd + Patroni` 節點
- 使用 `HAProxy` 或 `pgbouncer` 當作連線路由器
- `pgAdmin` 可以跑在任意伺服器上（甚至筆電）
