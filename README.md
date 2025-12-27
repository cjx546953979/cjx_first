# 桌面清理工具 Desktop Cleanup Tool

一个自动清理桌面临时文件和目录的工具集合，提供Python和Shell两种实现版本。

## Recent Updates

- Added more test content.
- Created a simple Python script.
- Added desktop cleanup script with scheduled task (Python version).
- Added Shell script version with configuration support.

## 版本说明

本项目提供两个版本的清理工具：

1. **Python版本** (`cleanup_desktop.py`) - 推荐使用
   - 跨平台支持更好
   - 功能更丰富，支持预览模式
   - 使用launchd定时任务（macOS）

2. **Shell版本** (`cleanup_desktop.sh`) - 轻量级
   - 无需Python环境
   - 支持配置文件
   - 使用crontab定时任务

---

## Python版本使用说明

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

---

## Shell版本使用说明

### 功能特性

- 🗂️ 自动清理桌面临时目录
- 🗑️ 删除指定类型的临时文件
- 📁 可选清理下载文件夹中的旧文件
- 🗑️ 自动清空回收站（macOS）
- 📝 详细的操作日志记录
- ⏰ 支持定时任务自动执行

### 安装使用

#### 快速安装
```bash
# 克隆仓库
git clone https://github.com/cjx546953979/cjx_first.git
cd cjx_first

# 运行安装脚本
chmod +x install_cleanup.sh
./install_cleanup.sh
```

#### 手动使用
```bash
# 给脚本添加执行权限
chmod +x cleanup_desktop.sh

# 手动执行清理
./cleanup_desktop.sh
```

### 配置说明

编辑 `config.conf` 文件可以自定义清理规则：

- `TEMP_DIRECTORIES`: 需要清理的目录名称
- `TEMP_FILE_EXTENSIONS`: 需要清理的文件扩展名
- `DOWNLOADS_RETENTION_DAYS`: 下载文件保留天数
- `EMPTY_TRASH`: 是否清空回收站

### 定时任务

安装脚本会自动设置每天早上9点执行清理任务。你可以通过以下命令管理定时任务：

```bash
# 查看当前定时任务
crontab -l

# 编辑定时任务
crontab -e

# 删除清理任务
crontab -l | grep -v 'cleanup_desktop.sh' | crontab -
```

### 日志查看

清理日志保存在桌面的 `cleanup.log` 文件中：

```bash
# 查看最新日志
tail -f ~/Desktop/cleanup.log

# 查看所有日志
cat ~/Desktop/cleanup.log
```

### 注意事项

- 脚本会永久删除文件，请谨慎使用
- 建议先在测试环境中验证
- 可以设置 `DRY_RUN=true` 进行模拟运行
- 支持macOS和Linux系统

---

## 许可证

MIT License
