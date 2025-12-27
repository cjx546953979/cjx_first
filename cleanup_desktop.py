#!/usr/bin/env python3
"""
桌面临时文件清理脚本
自动清理桌面上的临时文件和目录
"""

import os
import shutil
import time
from pathlib import Path
from datetime import datetime, timedelta

# 临时文件扩展名列表
TEMP_EXTENSIONS = {
    '.tmp', '.temp', '.log', '.cache', '.bak', '.swp', 
    '.~', '.DS_Store', '.Thumbs.db'
}

# 临时目录名称模式
TEMP_DIR_PATTERNS = [
    'tmp', 'temp', 'cache', '临时', 'temporary'
]

# 文件最大保留天数（超过此天数的临时文件将被删除）
MAX_AGE_DAYS = 7


def is_temp_file(filepath: Path) -> bool:
    """判断是否为临时文件"""
    # 检查扩展名
    if filepath.suffix.lower() in TEMP_EXTENSIONS:
        return True
    
    # 检查文件名是否以 ~ 开头或结尾
    name = filepath.name
    if name.startswith('~') or name.startswith('.~'):
        return True
    
    # 检查是否包含临时文件关键词
    name_lower = name.lower()
    for pattern in TEMP_DIR_PATTERNS:
        if pattern in name_lower:
            return True
    
    return False


def is_old_file(filepath: Path, max_age_days: int) -> bool:
    """判断文件是否超过最大保留天数"""
    try:
        mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
        age = datetime.now() - mtime
        return age > timedelta(days=max_age_days)
    except (OSError, ValueError):
        return False


def cleanup_desktop(desktop_path: str = None, dry_run: bool = False):
    """
    清理桌面临时文件
    
    Args:
        desktop_path: 桌面路径，默认为 ~/Desktop
        dry_run: 如果为True，只显示将要删除的文件，不实际删除
    """
    if desktop_path is None:
        desktop_path = os.path.expanduser("~/Desktop")
    
    desktop = Path(desktop_path)
    
    if not desktop.exists():
        print(f"错误: 桌面路径不存在: {desktop_path}")
        return
    
    print(f"开始清理桌面: {desktop_path}")
    print(f"模式: {'预览模式（不会实际删除）' if dry_run else '执行模式'}")
    print("-" * 50)
    
    deleted_files = []
    deleted_dirs = []
    total_size = 0
    
    try:
        # 遍历桌面上的所有文件和目录
        for item in desktop.iterdir():
            try:
                # 跳过隐藏的系统文件（除了我们明确要删除的）
                if item.name.startswith('.') and item.name not in ['.DS_Store']:
                    continue
                
                should_delete = False
                reason = ""
                
                # 检查是否为临时文件
                if is_temp_file(item):
                    should_delete = True
                    reason = "临时文件"
                # 检查是否超过保留期限
                elif is_old_file(item, MAX_AGE_DAYS) and is_temp_file(item):
                    should_delete = True
                    reason = f"超过{MAX_AGE_DAYS}天的临时文件"
                
                if should_delete:
                    size = 0
                    if item.is_file():
                        size = item.stat().st_size
                        if not dry_run:
                            item.unlink()
                        deleted_files.append((item.name, size, reason))
                    elif item.is_dir():
                        # 计算目录大小
                        for root, dirs, files in os.walk(item):
                            for f in files:
                                try:
                                    size += os.path.getsize(os.path.join(root, f))
                                except (OSError, ValueError):
                                    pass
                        if not dry_run:
                            shutil.rmtree(item)
                        deleted_dirs.append((item.name, size, reason))
                    
                    total_size += size
                    print(f"{'[预览] ' if dry_run else ''}删除: {item.name} ({reason})")
                    
            except (OSError, PermissionError) as e:
                print(f"警告: 无法处理 {item.name}: {e}")
                continue
    
    except Exception as e:
        print(f"错误: 清理过程中发生异常: {e}")
        return
    
    # 输出统计信息
    print("-" * 50)
    print(f"清理完成!")
    print(f"删除文件数: {len(deleted_files)}")
    print(f"删除目录数: {len(deleted_dirs)}")
    print(f"释放空间: {format_size(total_size)}")
    
    if dry_run:
        print("\n这是预览模式，实际未删除任何文件。")
        print("要执行实际清理，请运行: python cleanup_desktop.py")


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def main():
    """主函数"""
    import sys
    
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    
    if '--help' in sys.argv or '-h' in sys.argv:
        print("桌面临时文件清理脚本")
        print("\n用法:")
        print("  python cleanup_desktop.py          # 执行清理")
        print("  python cleanup_desktop.py --dry-run # 预览模式（不实际删除）")
        print("  python cleanup_desktop.py -h       # 显示帮助")
        return
    
    cleanup_desktop(dry_run=dry_run)


if __name__ == "__main__":
    main()

