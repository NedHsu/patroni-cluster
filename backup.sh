#!/bin/bash

# 設置變量
LOG_FILE="/home/postgres/pgroot/log/backup.log"
DATE=$(date +%Y%m%d_%H%M%S)

# 創建日誌目錄
mkdir -p $(dirname $LOG_FILE)

# 記錄開始時間
echo "$(date): 開始備份" >> $LOG_FILE

# 創建基礎備份
echo "$(date): 開始創建基礎備份" >> $LOG_FILE
wal-g backup-push /home/postgres/pgroot/pgdata >> $LOG_FILE 2>&1

if [ $? -eq 0 ]; then
    echo "$(date): 基礎備份完成" >> $LOG_FILE
else
    echo "$(date): 基礎備份失敗" >> $LOG_FILE
    exit 1
fi

# 清理舊的備份（保留最近 7 天的備份）
echo "$(date): 開始清理舊備份" >> $LOG_FILE
wal-g delete retain 7 --confirm >> $LOG_FILE 2>&1

# 驗證備份完整性
echo "$(date): 開始驗證備份完整性" >> $LOG_FILE
wal-g backup-list >> $LOG_FILE 2>&1

if [ $? -eq 0 ]; then
    echo "$(date): 備份驗證成功" >> $LOG_FILE
else
    echo "$(date): 備份驗證失敗" >> $LOG_FILE
    exit 1
fi

echo "$(date): 備份完成" >> $LOG_FILE
exit 0 