#!/bin/bash

# 桌面临时目录清理脚本
# Desktop Temporary Directory Cleanup Script

# 设置日志文件
LOG_FILE="$HOME/Desktop/cleanup.log"

# 记录日志函数
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# 开始清理
log_message "开始清理桌面临时目录"

# 定义需要清理的目录和文件类型
DESKTOP_PATH="$HOME/Desktop"
TEMP_DIRS=("temp" "tmp" "临时文件" "临时")
TEMP_EXTENSIONS=("*.tmp" "*.temp" "*.cache" "*.log" "*.bak" "*.old")

# 清理临时目录
for dir in "${TEMP_DIRS[@]}"; do
    if [ -d "$DESKTOP_PATH/$dir" ]; then
        log_message "清理目录: $DESKTOP_PATH/$dir"
        rm -rf "$DESKTOP_PATH/$dir"/*
        log_message "目录 $dir 清理完成"
    fi
done

# 清理临时文件
for ext in "${TEMP_EXTENSIONS[@]}"; do
    files_found=$(find "$DESKTOP_PATH" -maxdepth 1 -name "$ext" 2>/dev/null)
    if [ -n "$files_found" ]; then
        log_message "清理文件类型: $ext"
        find "$DESKTOP_PATH" -maxdepth 1 -name "$ext" -delete 2>/dev/null
        log_message "文件类型 $ext 清理完成"
    fi
done

# 清理超过7天的下载文件（可选）
DOWNLOADS_PATH="$HOME/Downloads"
if [ -d "$DOWNLOADS_PATH" ]; then
    log_message "清理超过7天的下载文件"
    find "$DOWNLOADS_PATH" -type f -mtime +7 -delete 2>/dev/null
    log_message "下载文件清理完成"
fi

# 清理回收站（macOS）
if command -v osascript >/dev/null 2>&1; then
    log_message "清理回收站"
    osascript -e 'tell application "Finder" to empty trash'
    log_message "回收站清理完成"
fi

log_message "桌面清理任务完成"
echo "清理完成！查看日志: $LOG_FILE"