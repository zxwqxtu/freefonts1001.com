#!/bin/bash
# 每日字体专题定时任务安装脚本（macOS launchd）
# 用法: bash setup_daily_story.sh

AGENT_NAME="com.freefonts1001.dailystory"
PLIST_PATH="$HOME/Library/LaunchAgents/${AGENT_NAME}.plist"

mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PLIST_PATH" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.freefonts1001.dailystory</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/a1/www/freefonts1001.com/scripts/font_story_generator.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/a1/www/freefonts1001.com</string>
    <key>StandardOutPath</key>
    <string>/Users/a1/www/freefonts1001.com/scripts/cron.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/a1/www/freefonts1001.com/scripts/cron_error.log</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

echo "✅ LaunchAgent plist 已创建: $PLIST_PATH"
echo "加载定时任务..."
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"
echo "✅ 定时任务已启动！每天 09:00 (Asia/Shanghai) 自动生成字体专题页"
echo ""
echo "管理命令:"
echo "  查看状态: launchctl list | grep freefonts"
echo "  立即执行: launchctl kickstart -k gui/$(id -u)/com.freefonts1001.dailystory"
echo "  停止任务: launchctl unload $PLIST_PATH"
echo "  删除任务: launchctl remove com.freefonts1001.dailystory && rm $PLIST_PATH"
