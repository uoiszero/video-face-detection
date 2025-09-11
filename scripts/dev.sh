#!/bin/bash
# 每次开发前激活虚拟环境
source venv/bin/activate

# 确认环境正确
which python  # 应该指向 venv/bin/python
pip list      # 查看已安装的包

# 运行GUI应用
python gui_mosaic_pyqt.py