# cjx_first

This is a test repository.
Created for testing purposes.

## Recent Updates
- Added more test content.
- Created a simple Python script.
- Added desktop cleanup script with scheduled task.

## 桌面临时文件清理脚本

这是一个自动清理桌面临时文件和目录的Python脚本，支持定时执行。

### 功能特性

- 自动识别临时文件（.tmp, .log, .cache等）
- 清理超过指定天数的旧临时文件（默认7天）
- 支持预览模式，可以先查看将要删除的文件
- 统计清理结果和释放的空间

### 使用方法

#### 1. 手动执行

```bash
# 预览模式（不会实际删除文件）
python3 cleanup_desktop.py --dry-run

# 执行清理
python3 cleanup_desktop.py
```

#### 2. 设置定时任务（macOS）

使用 launchd 设置每天凌晨2点自动清理：

```bash
# 1. 复制plist文件到LaunchAgents目录
cp com.cjx.cleanup.desktop.plist ~/Library/LaunchAgents/

# 2. 修改plist文件中的路径（如果需要）
# 编辑 ~/Library/LaunchAgents/com.cjx.cleanup.desktop.plist
# 将脚本路径改为你的实际路径

# 3. 加载定时任务
launchctl load ~/Library/LaunchAgents/com.cjx.cleanup.desktop.plist

# 4. 立即测试执行（可选）
launchctl start com.cjx.cleanup.desktop

# 5. 查看日志
tail -f cleanup.log
```

#### 3. 管理定时任务

```bash
# 卸载定时任务
launchctl unload ~/Library/LaunchAgents/com.cjx.cleanup.desktop.plist

# 查看任务状态
launchctl list | grep cleanup

# 停止任务
launchctl stop com.cjx.cleanup.desktop

# 重新加载任务（修改配置后）
launchctl unload ~/Library/LaunchAgents/com.cjx.cleanup.desktop.plist
launchctl load ~/Library/LaunchAgents/com.cjx.cleanup.desktop.plist
```

### 配置说明

- **临时文件扩展名**: 脚本会自动识别 `.tmp`, `.temp`, `.log`, `.cache`, `.bak`, `.swp` 等扩展名
- **保留期限**: 默认保留7天内的临时文件，可在脚本中修改 `MAX_AGE_DAYS` 变量
- **执行时间**: 默认每天凌晨2点执行，可在 `com.cjx.cleanup.desktop.plist` 中修改 `StartCalendarInterval`

### 注意事项

- 脚本会跳过隐藏的系统文件（除了 `.DS_Store`）
- 建议先使用 `--dry-run` 模式预览将要删除的文件
- 确保脚本有执行权限：`chmod +x cleanup_desktop.py`
