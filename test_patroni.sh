#!/bin/bash

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 測試函數
test_connection() {
    echo -e "${YELLOW}測試連接...${NC}"
    
    # 測試 HAProxy 連接
    echo "測試 HAProxy 連接..."
    PGPASSWORD=${POSTGRES_PASSWORD} psql -h localhost -p 5435 -U postgres -d postgres -c "SELECT version();" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}HAProxy 連接成功${NC}"
    else
        echo -e "${RED}HAProxy 連接失敗${NC}"
        return 1
    fi

    # 測試各個節點連接
    for port in 5432 5433 5434; do
        echo "測試節點端口 $port 連接..."
        PGPASSWORD=${POSTGRES_PASSWORD} psql -h localhost -p $port -U postgres -d postgres -c "SELECT version();" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}端口 $port 連接成功${NC}"
        else
            echo -e "${RED}端口 $port 連接失敗${NC}"
            return 1
        fi
    done
}

test_authentication() {
    echo -e "${YELLOW}測試認證...${NC}"
    
    # 測試 superuser
    echo "測試 superuser 認證..."
    PGPASSWORD=${POSTGRES_PASSWORD} psql -h localhost -p 5435 -U postgres -d postgres -c "SELECT current_user;" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}superuser 認證成功${NC}"
    else
        echo -e "${RED}superuser 認證失敗${NC}"
        return 1
    fi

    # 測試 admin 用戶
    echo "測試 admin 用戶認證..."
    PGPASSWORD=${PATRONI_ADMIN_PASSWORD} psql -h localhost -p 5435 -U admin -d postgres -c "SELECT current_user;" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}admin 用戶認證成功${NC}"
    else
        echo -e "${RED}admin 用戶認證失敗${NC}"
        return 1
    fi
}

test_replication() {
    echo -e "${YELLOW}測試複製...${NC}"
    
    # 在 primary 創建測試表
    echo "在 primary 創建測試表..."
    PGPASSWORD=${POSTGRES_PASSWORD} psql -h localhost -p 5435 -U postgres -d postgres -c "
        CREATE TABLE IF NOT EXISTS test_replication (id serial PRIMARY KEY, data text);
        INSERT INTO test_replication (data) VALUES ('test data');
    " > /dev/null 2>&1

    # 等待複製
    sleep 2

    # 檢查所有節點是否都有數據
    for port in 5432 5433 5434; do
        echo "檢查節點端口 $port 的數據..."
        PGPASSWORD=${POSTGRES_PASSWORD} psql -h localhost -p $port -U postgres -d postgres -c "SELECT COUNT(*) FROM test_replication;" | grep -q "1"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}端口 $port 數據同步成功${NC}"
        else
            echo -e "${RED}端口 $port 數據同步失敗${NC}"
            return 1
        fi
    done
}

test_failover() {
    echo -e "${YELLOW}測試故障轉移...${NC}"
    
    # 獲取當前 primary
    PRIMARY_PORT=$(PGPASSWORD=${POSTGRES_PASSWORD} psql -h localhost -p 5435 -U postgres -d postgres -c "SELECT port FROM pg_stat_replication;" | grep -o '[0-9]*' | head -1)
    
    if [ -z "$PRIMARY_PORT" ]; then
        echo -e "${RED}無法獲取 primary 端口${NC}"
        return 1
    fi

    echo "當前 primary 端口: $PRIMARY_PORT"
    
    # 停止 primary
    echo "停止 primary 節點..."
    docker stop patroni-$(echo $PRIMARY_PORT | sed 's/543//')
    
    # 等待故障轉移
    echo "等待故障轉移..."
    sleep 10
    
    # 檢查新的 primary
    NEW_PRIMARY_PORT=$(PGPASSWORD=${POSTGRES_PASSWORD} psql -h localhost -p 5435 -U postgres -d postgres -c "SELECT port FROM pg_stat_replication;" | grep -o '[0-9]*' | head -1)
    
    if [ -z "$NEW_PRIMARY_PORT" ]; then
        echo -e "${RED}無法獲取新的 primary 端口${NC}"
        return 1
    fi

    echo "新的 primary 端口: $NEW_PRIMARY_PORT"
    
    if [ "$PRIMARY_PORT" != "$NEW_PRIMARY_PORT" ]; then
        echo -e "${GREEN}故障轉移成功${NC}"
    else
        echo -e "${RED}故障轉移失敗${NC}"
        return 1
    fi
    
    # 恢復停止的節點
    echo "恢復停止的節點..."
    docker start patroni-$(echo $PRIMARY_PORT | sed 's/543//')
}

# 主測試流程
echo -e "${YELLOW}開始 Patroni 集群測試...${NC}"

# 檢查環境變數
if [ -z "$POSTGRES_PASSWORD" ] || [ -z "$PATRONI_ADMIN_PASSWORD" ]; then
    echo -e "${RED}錯誤: 請先設置必要的環境變數${NC}"
    echo "請確保以下環境變數已設置:"
    echo "- POSTGRES_PASSWORD"
    echo "- PATRONI_ADMIN_PASSWORD"
    exit 1
fi

# 執行測試
test_connection
if [ $? -eq 0 ]; then
    test_authentication
    if [ $? -eq 0 ]; then
        test_replication
        if [ $? -eq 0 ]; then
            test_failover
        fi
    fi
fi

echo -e "${YELLOW}測試完成${NC}" 