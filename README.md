# 1999_Auto
用于1999肉鸽模式，自动化流程 （弱智版）。

2/20 更新：优化了窗口适配问题，会自动根据用户的模拟器窗口大小与预设的窗口大小对比，缩放点击位置。增加了对话逻辑，以及防止对话卡死和误触。

2/18 更新：新增新角色入队判定
## 操作系统要求
Windows

## 软件和代码解释器要求

MuMu模拟器12: 用于运行重返未来1999。 

Python 3.9: 请确保使用Python 3.9（防止出现某些库不兼容的问题）。可以从Python官网下载。

## 使用方法
1.准备工作:

确保已安装Python 3.9。
安装PyCharm（推荐）或其他Python IDE
安装所需的Python库。可以通过在命令行（pyCharm 按alt+F12）中运行以下命令来安装：

pip install pywin32 opencv-python numpy pyautogui pygetwindow tensorflow==2.15 keyboard scikit-image

2.运行游戏:

打开MuMu模拟器，并启动1999肉鸽模式。建议选择低难度。

3.运行脚本:
确保MuMu模拟器窗口处于打开状态（不要开全屏），并且游戏已经进入肉鸽模式。 
运行main.py。

4.适用：

懒人专用，解放双手，萌新慎入（打不过不负责）

5.建议配队：

主c放4号位，副c放3号位，强烈建议带上一个盾和奶妈

6.备注:

运行时尽量保证模拟器在前台，后台运行可能会操作失败。
确保模型文件1999auto.keras与脚本处于同一目录下。 

出现点击无效情况，先调整模拟器分辨率设置为1920x1080,280DPI，并重启脚本
如果依然出现点击无效的情况，运行问题/卡住， 请截图评论（页面上方issue） 或者使用Find_pos.py手动校准位置 

PPS.已经尽力优化适配问题了（QAQ）



