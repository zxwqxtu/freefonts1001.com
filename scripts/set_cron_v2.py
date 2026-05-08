#!/usr/bin/env python3
"""使用 launchd 或 crontab 设置每日字体专题定时任务"""
import subprocess, sys, os, datetime

CRON_LINE = "0 9 * * * cd /Users/a1/www/freefonts1001.com && /usr/bin/python3 scripts/font_story_generator.py >> /Users/a1/www/freefonts1001.com/scripts/cron.log 2>&1"

def run_cmd(cmd, shell=True):
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=15)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, '', 'timeout'
    except Exception as e:
        return -2, '', str(e)

def set_cron_via_file():
    """先写入临时文件，再喂给 crontab"""
    import tempfile
    # 获取现有 crontab
    rc, out, err = run_cmd('crontab -l')
    existing = out if rc == 0 else ''
    # 过滤掉旧的 freefonts 任务
    lines = [l for l in existing.splitlines() if 'freefonts1001' not in l]
    lines.append(CRON_LINE)
    content = '\n'.join(lines) + '\n'
    # 写到临时文件
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.cron', delete=False)
    tmp.write(content)
    tmp.close()
    # 用 crontab 读取该文件
    rc2, out2, err2 = run_cmd(f'crontab {tmp.name}')
    os.unlink(tmp.name)
    return rc2, out2, err2

if __name__ == '__main__':
    print(f"[{datetime.datetime.now()}] 开始设置定时任务...")
    rc, out, err = set_cron_via_file()
    print(f"rc={rc} out={out.strip()} err={err.strip()}")
    if rc == 0:
        print("✅ 定时任务设置成功！每天 09:00 自动生成并推送字体专题")
    else:
        print(f"❌ 设置失败: {err}")
        # 回退：只显示 crontab 内容，让用户手动处理
        rc3, out3, _ = run_cmd('crontab -l')
        print(f"\n当前 crontab 内容:\n{out3}")
        print(f"\n请手动添加以下行到 crontab:\n{CRON_LINE}")
