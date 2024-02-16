import pyautogui
import pygetwindow as gw

# 窗口标题是“MuMu模拟器12”
win = gw.getWindowsWithTitle("MuMu模拟器12")[0]
if win:
    win_pos = win.topleft
    win_size = win.size

else:
    print("没有找到窗口")

# 这里需要手动移动鼠标到目标位置
pyautogui.sleep(3)
absolute_pos = pyautogui.position()

relative_pos = (absolute_pos[0] - win_pos[0], absolute_pos[1] - win_pos[1])
print(relative_pos)

pyautogui.sleep(2)
relative_pos = (absolute_pos[0] - win_pos[0], absolute_pos[1] - win_pos[1])
print(relative_pos)
