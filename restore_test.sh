#!/bin/bash

# 設置變量
RESTORE_DIR="/home/postgres/pgroot/restore"
LOG_FILE="/home/postgres/pgroot/log/restore_test.log"

# 創建日誌目錄
mkdir -p $(dirname $LOG_FILE)

# 記錄開始時間
echo "$(date): 開始還原測試" >> $LOG_FILE

# 創建還原目錄
echo "$(date): 創建還原目錄" >> $LOG_FILE
mkdir -p ${RESTORE_DIR}

# 獲取最新的備份
echo "$(date): 獲取最新的備份" >> $LOG_FILE
LATEST_BACKUP=$(wal-g backup-list | grep -v "name" | head -n 1 | awk '{print $1}')

if [ -z "$LATEST_BACKUP" ]; then
    echo "$(date): 沒有找到可用的備份" >> $LOG_FILE
    exit 1
fi

# 還原備份
echo "$(date): 開始還原備份 $LATEST_BACKUP" >> $LOG_FILE
wal-g backup-fetch ${RESTORE_DIR} $LATEST_BACKUP >> $LOG_FILE 2>&1

if [ $? -ne 0 ]; then
    echo "$(date): 還原備份失敗" >> $LOG_FILE
    exit 1
fi

# 配置還原參數
echo "$(date): 配置還原參數" >> $LOG_FILE
cat > ${RESTORE_DIR}/postgresql.conf << EOF
port = 5436
data_directory = '${RESTORE_DIR}'
hba_file = '${RESTORE_DIR}/pg_hba.conf'
ident_file = '${RESTORE_DIR}/pg_ident.conf'
external_pid_file = '${RESTORE_DIR}/postgresql.pid'
restore_command = 'wal-g wal-fetch %f %p'
recovery_target_timeline = 'latest'
EOF

# 創建還原標記文件
echo "$(date): 創建還原標記文件" >> $LOG_FILE
touch ${RESTORE_DIR}/recovery.signal

# 啟動還原實例
echo "$(date): 啟動還原實例" >> $LOG_FILE
pg_ctl -D ${RESTORE_DIR} start >> $LOG_FILE 2>&1

if [ $? -eq 0 ]; then
    echo "$(date): 還原實例啟動成功" >> $LOG_FILE
else
    echo "$(date): 還原實例啟動失敗" >> $LOG_FILE
    exit 1
fi

# 等待還原完成
echo "$(date): 等待還原完成" >> $LOG_FILE
sleep 30

# 檢查還原狀態
echo "$(date): 檢查還原狀態" >> $LOG_FILE
psql -h localhost -p 5436 -U postgres -c "SELECT pg_is_in_recovery();" >> $LOG_FILE 2>&1

# 停止還原實例
echo "$(date): 停止還原實例" >> $LOG_FILE
pg_ctl -D ${RESTORE_DIR} stop >> $LOG_FILE 2>&1

# 清理還原目錄
echo "$(date): 清理還原目錄" >> $LOG_FILE
rm -rf ${RESTORE_DIR}

echo "$(date): 還原測試完成" >> $LOG_FILE
exit 0 