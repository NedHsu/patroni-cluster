# 環境配置設定

* **ETCD_HOST**：指向 Etcd 主機的 DNS A 紀錄。
* **ETCD_HOSTS**：Etcd 主機清單，格式為 `"host1:port1","host2:port2",...,"hostN:portN"`。
* **ETCD_DISCOVERY_DOMAIN**：指向 Etcd 主機的 DNS SRV 紀錄。
* **ETCD_URL**：Etcd 主機的 URL，格式為 `http(s)://host1:port`。
* **ETCD_PROXY**：Etcd Proxy 的 URL，格式為 `http(s)://host1:port`。
* **ETCD_CACERT**：Etcd 的 CA 證書；如果有提供，將啟用驗證。
* **ETCD_CERT**：Etcd 客戶端憑證。
* **ETCD_KEY**：Etcd 客戶端憑證金鑰。如果憑證中已包含金鑰，此值可以為空。
* **PGHOME**：存放 PostgreSQL 主目錄的檔案系統路徑（預設為 `/home/postgres`）。
* **APIPORT**：Patroni API 連線所使用的 TCP 埠號（預設為 8008）。
* **BACKUP_SCHEDULE**：利用 WAL‑E 進行備份時使用的 cron 排程（若啟用 WAL‑E，預設為 `'00 01 * * *'`）。
* **CLONE_TARGET_TIMELINE**：還原備份時使用的時間軸 ID（預設為 `latest`）。
* **CRONTAB**：任何你想定期以 cron 工作執行的指令（預設為空）。
* **PGROOT**：放置 pgdata 的目錄（預設為 `/home/postgres/pgroot`）；此目錄可以依需求調整指向如 EBS 等持久性磁碟的掛載點。
* **WALE_TMPDIR**：存放 WAL‑E 暫存檔的目錄（預設為 `PGROOT/../tmp`，請確保該目錄有足夠的數 GB 空間）。
* **PGDATA**：PostgreSQL 資料目錄的位置，預設為 `PGROOT/pgdata`。
* **PGUSER_STANDBY**：用於複製使用者的帳號（預設為 `standby`）。
* **PGPASSWORD_STANDBY**：複製使用者的密碼（預設為 `standby`）。
* **STANDBY_HOST**：用於串流資料的主要主機的主機名稱或 IP 位址。
* **STANDBY_PORT**：主要主機監聽連線的 TCP 埠號；若未設定，Patroni 會使用 "5432"。
* **STANDBY_PRIMARY_SLOT_NAME**：主要主機上要使用的複製槽名稱。
* **PGUSER_ADMIN**：預設管理使用者的帳號（預設為 `admin`）。
* **PGPASSWORD_ADMIN**：預設管理使用者的密碼（預設為 `cola`）。
* **USE_ADMIN**：是否啟用管理使用者（布林值）。
* **PGUSER_SUPERUSER**：超級使用者帳號（預設為 `postgres`）。
* **PGPASSWORD_SUPERUSER**：超級使用者密碼（預設為 `zalando`）。
* **ALLOW_NOSSL**：設定此選項可允許客戶端在未啟用 SSL 的情況下連線。
* **PGPORT**：PostgreSQL 監聽客戶端連線的埠號（預設為 5432）。
* **PGVERSION**：指定 PostgreSQL 版本，此版本用於參照 bin_dir 變數（例如 `/usr/lib/postgresql/PGVERSION/bin`），前提是在 SPILO_CONFIGURATION 中未設定 postgresql.bin_dir。
* **SCOPE**：叢集名稱；同一叢集中所有 Spilo 節點的 SCOPE 值必須一致。
* **SSL_CA_FILE**：容器內部 SSL CA 證書的檔案路徑（預設為空字串）。
* **SSL_CRL_FILE**：容器內部 SSL 憑證撤銷清單的檔案路徑（預設為空字串）。
* **SSL_CERTIFICATE_FILE**：容器內部 SSL 證書的檔案路徑（預設為 `/run/certs/server.crt`）；若不存在，Spilo 會自動產生。
* **SSL_PRIVATE_KEY_FILE**：容器內部 SSL 私鑰的檔案路徑（預設為 `/run/certs/server.key`）；若不存在，Spilo 會自動產生。
* **SSL_CA**：從 SSL_CA_FILE 中讀取的 SSL CA 證書內容（預設為空字串）。
* **SSL_CRL**：從 SSL_CRL_FILE 中讀取的憑證撤銷清單內容（預設為空字串）。
* **SSL_CERTIFICATE**：從 SSL_CERTIFICATE_FILE 中讀取的 SSL 證書內容（預設為 `/run/certs/server.crt`）。
* **SSL_PRIVATE_KEY**：從 SSL_PRIVATE_KEY_FILE 中讀取的 SSL 私鑰內容（預設為 `/run/certs/server.key`）。
* **SSL_RESTAPI_CA_FILE**：容器內部 Patroni REST API 使用的 SSL CA 證書檔案路徑（預設為空字串）。
* **SSL_RESTAPI_CERTIFICATE_FILE**：容器內部 Patroni REST API 使用的 SSL 證書檔案路徑（預設為 `/run/certs/restapi.crt`）；若不存在，Spilo 會自動產生。
* **SSL_RESTAPI_PRIVATE_KEY_FILE**：容器內部 Patroni REST API 使用的 SSL 私鑰檔案路徑（預設為 `/run/certs/restapi.key`）；若不存在，Spilo 會自動產生。
* **SSL_RESTAPI_CA**：從 SSL_RESTAPI_CA_FILE 中讀取的 Patroni REST API SSL CA 證書內容（預設為空字串）。
* **SSL_RESTAPI_CERTIFICATE**：從 SSL_CERTIFICATE_FILE（預設為 `/run/certs/server.crt`）中讀取的 REST API SSL 證書內容。
* **SSL_RESTAPI_PRIVATE_KEY**：從 SSL_PRIVATE_KEY_FILE（預設為 `/run/certs/server.key`）中讀取的 REST API SSL 私鑰內容。
* **SSL_TEST_RELOAD**：檢測憑證輪換與重新加載的開關（如果已設定 SSL_PRIVATE_KEY_FILE，預設為 True）。
* **RESTAPI_CONNECT_ADDRESS**：當你以 SSL 模式配置 Patroni REST API 時，部分安全 API（例如 switchover）會進行主機名稱驗證；在此情況下，建議將 ``restapi.connect_address`` 設為主機名稱而非 IP。例如，可設為 `"$(POD_NAME).<service name>"`。
* **WALE_BACKUP_THRESHOLD_MEGABYTES**：在基底備份之後累積的 WAL 段最大大小（以 MB 為單位），超過此值時會考慮使用 WAL‑E 還原而非 pg_basebackup。
* **WALE_BACKUP_THRESHOLD_PERCENTAGE**：累積 WAL 檔案與基底備份大小的最大百分比，超過此比率時會考慮使用 WAL‑E 還原而非 pg_basebackup。
* **WALE_ENV_DIR**：存放 WAL‑E 環境變數的目錄。
* **WAL_RESTORE_TIMEOUT**：從備份位置還原單一 WAL 檔案（最多 16 MB）的超時設定（以秒計，預設為 0；設定為 0 則禁用超時）。
* **WAL_S3_BUCKET**：(可選) 用於 WAL‑E 基底備份的 S3 桶名稱。
* **AWS_ACCESS_KEY_ID**：(可選) AWS 存取金鑰 ID。
* **AWS_SECRET_ACCESS_KEY**：(可選) AWS 存取金鑰密鑰。
* **AWS_REGION**：(可選) S3 桶的區域設定。
* **AWS_ENDPOINT**：(可選) 連線格式為 `https://s3.AWS_REGION.amazonaws.com:443`；若未指定，將根據 AWS_REGION 自動計算。
* **WALE_S3_ENDPOINT**：(可選) 連線格式為 `https+path://s3.AWS_REGION.amazonaws.com:443`；若未指定，將根據 AWS_ENDPOINT 或 AWS_REGION 自動計算。
* **WALE_S3_PREFIX**：(可選) S3 備份位置的完整路徑，格式為 `s3://bucket-name/very/long/path`；若未指定，Spilo 將根據 WAL_S3_BUCKET 自動產生。
* **WAL_GS_BUCKET**：同上，適用於 Google Cloud Storage（WAL‑E 支援 S3 與 GCS）。
* **WALE_GS_PREFIX**：(可選) Google Cloud Storage 備份位置的完整路徑，格式為 `gs://bucket-name/very/long/path`；若未指定，Spilo 將根據 WAL_GS_BUCKET 自動產生。
* **GOOGLE_APPLICATION_CREDENTIALS**：在 Google Cloud 環境中運行 WAL‑E 時所需的認證憑證。
* **WAL_SWIFT_BUCKET**：適用於 OpenStack 物件存儲（Swift）的桶名稱，同上。
* **SWIFT_AUTHURL**：請參閱 WAL‑E 文件（[https://github.com/wal-e/wal-e#swift](https://github.com/wal-e/wal-e#swift)）。
* **SWIFT_TENANT**：
* **SWIFT_TENANT_ID**：
* **SWIFT_USER**：
* **SWIFT_USER_ID**：
* **SWIFT_PASSWORD**：
* **SWIFT_AUTH_VERSION**：
* **SWIFT_ENDPOINT_TYPE**：
* **SWIFT_REGION**：
* **SWIFT_DOMAIN_NAME**：
* **SWIFT_DOMAIN_ID**：
* **SWIFT_USER_DOMAIN_NAME**：
* **SWIFT_USER_DOMAIN_ID**：
* **SWIFT_PROJECT_NAME**：
* **SWIFT_PROJECT_ID**：
* **SWIFT_PROJECT_DOMAIN_NAME**：
* **SWIFT_PROJECT_DOMAIN_ID**：
* **WALE_SWIFT_PREFIX**：(可選) Swift 備份位置的完整路徑，格式為 `swift://bucket-name/very/long/path`；若未指定，Spilo 將根據 WAL_SWIFT_BUCKET 自動產生。
* **SSH_USERNAME**：(可選) 用於 WAL 備份的 SSH 使用者名稱。
* **SSH_PORT**：(可選) 用於 WAL 備份的 SSH 埠號。
* **SSH_PRIVATE_KEY_PATH**：(可選) 用於 WAL 備份的 SSH 私鑰路徑。
* **AZURE_STORAGE_ACCOUNT**：(可選) 用於 WAL 備份的 Azure 儲存帳號。
* **AZURE_STORAGE_ACCESS_KEY**：(可選) 用於 WAL 備份的 Azure 儲存帳號存取金鑰。
* **AZURE_CLIENT_ID**：(可選) 服務主體的 Client (application) ID。
* **AZURE_CLIENT_SECRET**：(可選) 服務主體的 Client secret。
* **AZURE_TENANT_ID**：(可選) 服務主體的 Tenant ID。
* **CALLBACK_SCRIPT**：在各種叢集動作（啟動、停止、重啟、角色變更）時執行的回調腳本。該腳本將接收叢集名稱、連線字串以及目前動作。詳情請參閱 Patroni 文件。
* **LOG_S3_BUCKET**：用於存放 PostgreSQL 每日日誌檔的 S3 桶路徑（例如 foobar，不包含 `s3://` 前綴）；Spilo 將在該路徑後附加 `/spilo/{LOG_BUCKET_SCOPE_PREFIX}{SCOPE}{LOG_BUCKET_SCOPE_SUFFIX}/log/`。只要設定了此變數，就會啟用日誌傳送功能。
* **LOG_S3_TAGS**：上傳到 S3 的日誌檔標籤，格式為鍵值對映射，值通常引用現有的環境變數，例如：`{"ClusterName": "SCOPE", "Namespace": "POD_NAMESPACE"}`。
* **LOG_SHIP_HOURLY**：若為 true，PostgreSQL 日誌的輪轉時間將設定為每小時（包括外部表），排程為 `1 */1 * * *`。
* **LOG_SHIP_SCHEDULE**：用於傳送 `pg_log` 中壓縮日誌檔的 cron 排程（預設為 `1 0 * * *`）。
* **LOG_ENV_DIR**：存放用於日誌傳送的環境變數的目錄。
* **LOG_TMPDIR**：用於存放臨時壓縮日誌檔的目錄（預設為 `PGROOT/../tmp`）。
* **LOG_S3_ENDPOINT**：(可選) 與 Boto3 一同使用的 S3 端點。
* **LOG_BUCKET_SCOPE_PREFIX**：(可選) 用於組成 S3 檔案路徑的前置字串，例如 `/spilo/{LOG_BUCKET_SCOPE_PREFIX}{SCOPE}{LOG_BUCKET_SCOPE_SUFFIX}/log/`。
* **LOG_BUCKET_SCOPE_SUFFIX**：(可選) 同上，用作組成 S3 檔案路徑的後置字串。
* **LOG_GROUP_BY_DATE**：(可選) 啟用依日期分組日誌。預設為 False，表示根據實例 ID 分組日誌。
* **DCS_ENABLE_KUBERNETES_API**：若設定非空值，則強制 Patroni 使用 Kubernetes 作為分散式配置儲存系統 (DCS)；預設為空。
* **KUBERNETES_USE_CONFIGMAPS**：若設定非空值，Patroni 將使用 ConfigMaps（而非 Endpoints）來存放其元資料，當在 Kubernetes 中運行時使用；預設為空。
* **KUBERNETES_ROLE_LABEL**：在 Kubernetes 中，包含 PostgreSQL 角色（例如 Spilo 使用）之標籤名稱。預設值為 `spilo-role`。
* **KUBERNETES_LEADER_LABEL_VALUE**：當 PostgreSQL 角色為 primary（主要）時，Pod 標籤的值（在 Kubernetes 中運行時預設為 `master`）。
* **KUBERNETES_STANDBY_LEADER_LABEL_VALUE**：當 PostgreSQL 角色為 standby_leader 時，Pod 標籤的值（預設為 `master`）。
* **KUBERNETES_SCOPE_LABEL**：表示叢集名稱的標籤名稱（預設為 `version`）。
* **KUBERNETES_LABELS**：以 JSON 格式描述 Patroni 在 Kubernetes 中用以定位元資料的其他標籤，預設為 `{"application": "spilo"}`。
* **INITDB_LOCALE**：資料庫叢集預設的 UTF‑8 區域設定（預設為 en_US）。
* **ENABLE_WAL_PATH_COMPAT**：舊版 Spilo 映像檔在備份存儲中產生 WAL 路徑時使用的範本為 `/spilo/{WAL_BUCKET_SCOPE_PREFIX}{SCOPE}{WAL_BUCKET_SCOPE_SUFFIX}/wal/`，而新版則在尾端額外增加一個目錄（`{PGVERSION}`）。為避免在切換至 `spilo-13` 時（不常見的情況下）還原 WAL 出現問題，請在首次以 `spilo-13` 部署舊叢集時設定 `ENABLE_WAL_PATH_COMPAT=true`；部署後此環境變數可移除。注意，WAL 路徑的改變也意味著儲存在舊位置的備份將不會自動清理。
* **WALE_DISABLE_S3_SSE, WALG_DISABLE_S3_SSE**：預設下，WAL‑E/WAL‑G 會配置對上傳至 S3 的檔案進行加密。若要禁用加密，可將此環境變數設定為 `true`。
* **USE_OLD_LOCALES**：是否在基於 Ubuntu 22.04 的映像中使用 Ubuntu 18.04 的舊版語系。預設為 false。

---

## wal‑g

wal‑g 預設用於 Azure 與 SSH 備份與還原；若使用 S3，則使用 wal‑e 進行備份，而還原則使用 wal‑g。

* **USE_WALG_BACKUP**：(可選) 強制使用 wal‑g 而非 wal‑e 進行備份（布林值）。
* **USE_WALG_RESTORE**：(可選) 強制使用 wal‑g 而非 wal‑e 進行還原（布林值）。
* **WALG_DELTA_MAX_STEPS, WALG_DELTA_ORIGIN, WALG_DOWNLOAD_CONCURRENCY, WALG_UPLOAD_CONCURRENCY, WALG_UPLOAD_DISK_CONCURRENCY, WALG_DISK_RATE_LIMIT, WALG_NETWORK_RATE_LIMIT, WALG_COMPRESSION_METHOD, WALG_BACKUP_COMPRESSION_METHOD, WALG_BACKUP_FROM_REPLICA, WALG_SENTINEL_USER_DATA, WALG_PREVENT_WAL_OVERWRITE**：(可選) wal‑g 各項配置參數。
* **WALG_S3_CA_CERT_FILE**：(可選) wal‑g 使用的 TLS CA 證書（請參閱 [wal‑g 配置](https://github.com/wal-g/wal-g#configuration)）。
* **WALG_SSH_PREFIX**：(可選) 傳送 WAL 備份時，透過 SSH 存儲的前綴路徑，格式為 `ssh://host.example.com/path/to/backups/`。詳情請參閱 wal‑g 文件。
* **WALG_LIBSODIUM_KEY, WALG_LIBSODIUM_KEY_PATH, WALG_LIBSODIUM_KEY_TRANSFORM, WALG_PGP_KEY, WALG_PGP_KEY_PATH, WALG_PGP_KEY_PASSPHRASE**：(可選) wal‑g 加密相關設定（請參閱 [wal‑g 加密](https://github.com/wal-g/wal-g#encryption)）。
* **http_proxy, https_proxy, no_proxy**：(可選) 配置 wal‑g 存取 S3 時的 HTTP(S) 代理。http_proxy 與 https_proxy 接受代理 URL，而 no_proxy 則為以逗號分隔的例外列表；均遵循業界慣例（可參閱 [wget 文件](https://www.gnu.org/software/wget/manual/html_node/Proxies.html)）。
* **AWS_ROLE_ARN, AWS_WEB_IDENTITY_TOKEN_FILE, AWS_STS_REGIONAL_ENDPOINTS**：(可選) 為 wal‑g 存取 S3 進行 AWS EKS IRSA 認證的相關配置。通常這些變數會由 AWS EKS 自動設定，目前只有 wal‑g 支持 AWS EKS IRSA 功能。

### 針對 Azure 的 WAL‑g 配置

關於 Azure 相關選項的更多資訊，請參閱  
[https://github.com/wal-g/wal-g/blob/master/docs/STORAGES.md#azure](https://github.com/wal-g/wal-g/blob/master/docs/STORAGES.md#azure)

針對 Azure 備份的一般配置選項如下：

* **WALG_AZ_PREFIX**：啟用 Azure 備份，設定備份存放在 Azure 中的前綴路徑，格式為 `azure://test-container/walg-folder`。
* **AZURE_STORAGE_ACCOUNT**
* **WALG_AZURE_BUFFER_SIZE**
* **WALG_AZURE_MAX_BUFFERS**
* **AZURE_ENVIRONMENT_NAME**

對於 Microsoft Azure Blob Storage 的認證，可選擇以下其中一種方法：

* **使用儲存帳號金鑰**：
  * AZURE_STORAGE_ACCESS_KEY
* **使用共享存取簽章 (SAS)**：
  * AZURE_STORAGE_SAS_TOKEN
* **使用服務主體**：
  * AZURE_CLIENT_ID
  * AZURE_CLIENT_SECRET
  * AZURE_TENANT_ID
* **使用 Managed Service Identity (MSI)**：無需額外配置。
