#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日字体专题生成器 - 启动脚本"""
import sys
sys.path.insert(0, '/Users/a1/www/freefonts1001.com/scripts')
from font_story_generator import run
path, topic, date = run()
print(f"DONE: {topic['emoji']} {date.isoformat()} → {path.name}")
