# 桌面清理工具 Desktop Cleanup Tool

一个自动清理桌面临时文件和目录的Shell脚本工具。

## 功能特性

- 🗂️ 自动清理桌面临时目录
- 🗑️ 删除指定类型的临时文件
- 📁 可选清理下载文件夹中的旧文件
- 🗑️ 自动清空回收站（macOS）
- 📝 详细的操作日志记录
- ⏰ 支持定时任务自动执行

## 安装使用

### 快速安装
```bash
# 克隆仓库
git clone https://github.com/cjx546953979/cjx_first.git
cd cjx_first

# 运行安装脚本
chmod +x install_cleanup.sh
./install_cleanup.sh
```

### 手动使用
```bash
# 给脚本添加执行权限
chmod +x cleanup_desktop.sh

# 手动执行清理
./cleanup_desktop.sh
```

## 配置说明

编辑 `config.conf` 文件可以自定义清理规则：

- `TEMP_DIRECTORIES`: 需要清理的目录名称
- `TEMP_FILE_EXTENSIONS`: 需要清理的文件扩展名
- `DOWNLOADS_RETENTION_DAYS`: 下载文件保留天数
- `EMPTY_TRASH`: 是否清空回收站

## 定时任务

安装脚本会自动设置每天早上9点执行清理任务。你可以通过以下命令管理定时任务：

```bash
# 查看当前定时任务
crontab -l

# 编辑定时任务
crontab -e

# 删除清理任务
crontab -l | grep -v 'cleanup_desktop.sh' | crontab -
```

## 日志查看

清理日志保存在桌面的 `cleanup.log` 文件中：

```bash
# 查看最新日志
tail -f ~/Desktop/cleanup.log

# 查看所有日志
cat ~/Desktop/cleanup.log
```

## 注意事项

- 脚本会永久删除文件，请谨慎使用
- 建议先在测试环境中验证
- 可以设置 `DRY_RUN=true` 进行模拟运行
- 支持macOS和Linux系统

## 许可证

MIT License
