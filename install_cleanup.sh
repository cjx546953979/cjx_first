#!/bin/bash

# 安装桌面清理脚本的安装程序
# Installation script for desktop cleanup

echo "正在安装桌面清理脚本..."

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLEANUP_SCRIPT="$SCRIPT_DIR/cleanup_desktop.sh"

# 检查清理脚本是否存在
if [ ! -f "$CLEANUP_SCRIPT" ]; then
    echo "错误: 找不到 cleanup_desktop.sh 脚本"
    exit 1
fi

# 给脚本添加执行权限
chmod +x "$CLEANUP_SCRIPT"

# 创建定时任务
echo "设置定时任务..."

# 检查是否已存在相同的定时任务
if crontab -l 2>/dev/null | grep -q "cleanup_desktop.sh"; then
    echo "定时任务已存在，正在更新..."
    # 移除旧的定时任务
    crontab -l 2>/dev/null | grep -v "cleanup_desktop.sh" | crontab -
fi

# 添加新的定时任务（每天早上9点执行）
(crontab -l 2>/dev/null; echo "0 9 * * * $CLEANUP_SCRIPT") | crontab -

echo "定时任务设置完成！"
echo "脚本将在每天早上9点自动执行"
echo ""
echo "你也可以手动运行清理脚本："
echo "  $CLEANUP_SCRIPT"
echo ""
echo "查看当前定时任务："
echo "  crontab -l"
echo ""
echo "卸载定时任务："
echo "  crontab -l | grep -v 'cleanup_desktop.sh' | crontab -"