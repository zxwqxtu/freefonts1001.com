#!/usr/bin/env python3
"""设置每日字体专题定时任务（使用 crontab）"""
import subprocess, datetime, os

CRON_LINE = "0 9 * * * cd /Users/a1/www/freefonts1001.com && /usr/bin/python3 scripts/font_story_generator.py >> /Users/a1/www/freefonts1001.com/scripts/cron.log 2>&1\n"

def get_crontab():
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    if result.returncode != 0:
        return ''
    return result.stdout

def set_cron():
    current = get_crontab()
    # 移除旧的 freefonts 相关任务（避免重复）
    lines = [l for l in current.splitlines() if 'freefonts1001' not in l]
    # 追加新任务
    lines.append(CRON_LINE.strip())
    new_cron = '\n'.join(lines).strip() + '\n'
    # 写入
    proc = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate(input=new_cron.encode())
    if proc.returncode == 0:
        print(f"✅ Crontab 已更新，每天 09:00 运行字体专题生成器")
        print(f"   当前 crontab:\n{new_cron}")
    else:
        print(f"❌ crontab 设置失败: {err.decode()}")

if __name__ == '__main__':
    set_cron()
