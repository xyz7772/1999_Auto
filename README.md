# 1999_Auto
用于1999肉鸽模式，自动化流程 （弱智版）

## 操作系统要求
Windows
## 软件和代码解释器要求
MuMu模拟器12: 用于运行重返未来1999。
Python 3.9: 由于最新TensorFlow2.x版本与Python 3.12不兼容，请确保使用Python 3.9。可以从Python官网下载。
python 3.6之前可以使用tensorflow1.x版本，用法是from keras.models import load_model  替换main.py中的from tensorflow.keras.models import load_model


## 使用方法
1.准备工作:

确保已安装Python 3.9。
安装所需的Python库。可以通过在命令行中运行以下命令来安装：

pip install pywin32 opencv-python numpy pyautogui pygetwindow tensorflow keyboard scikit-image

2.运行游戏:

打开MuMu模拟器，并启动1999肉鸽模式。建议选择低难度。

3.运行脚本:

使用PyCharm（推荐）或其他Python IDE打开main.py脚本。
确保MuMu模拟器窗口处于打开状态，并且游戏已经进入肉鸽模式。
在PyCharm中运行main.py。

4.适用：

懒人专用，解放双手，萌新慎入（打不过不负责）

5.建议配队：

主c放4号位，副c放3号位，强烈建议带上一个盾和奶妈（小叶优先）

6.备注:
*似乎一些人出现了关于模拟器适配问题而点击无效，首先是调整模拟器分辨率设置为1920x1080,280DPI， 如果设置后依然点击无效，请调整一下窗口大小（点击超出范围则调大，小于范围则缩小）。这几天比较忙，之后想办法优化这里。


运行时尽量保证模拟器在前台，后台运行可能会操作失败
确保模型文件1999auto.keras与脚本处于同一目录下
使用Find_pos.py手动寻找新的点击位置并替换代码中Relative_pos_xxxx部分
出现运行问题/卡住 请重启脚本并截图评论（页面上方issue）或发送到2248389930@qq.com




