import win32gui
import win32ui
import win32con
import cv2
import time
import pyautogui
import pygetwindow as gw
import ctypes
import os
import numpy as np
from tensorflow.keras.models import load_model
import keyboard

ctypes.windll.user32.SetProcessDPIAware()

def capture_screenshot(hwnd):
    window_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(window_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width, height = right - left, bot - top
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)
    save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
    bmpinfo = save_bitmap.GetInfo()
    bmpstr = save_bitmap.GetBitmapBits(True)
    img = np.frombuffer(bmpstr, dtype='uint8')
    img.shape = (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, window_dc)
    return img[:, :, :3]

def find_model_file(filename="1999_auto_v2.keras"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, filename)
    if os.path.exists(model_path):
        print(f"模型文件地址：{model_path}")
        return model_path
    else:
        print(f"未能找到文件：{model_path}")
        return None

def check_for_exit():
    if keyboard.is_pressed('F7'):
        print("程序即将停止...")
        return True
    return False

# 加载模型
model_file_path = find_model_file()
if model_file_path:
    model = load_model(model_file_path)
else:
    print("错误：模型文件不存在。")

# class_indices：
train_class_indices = {'award': 0, 'dialogs': 1, 'scene': 2, 'shop': 3, 'start': 4, 'upgrade': 5, 'wait': 6,
                       'wait_action': 7, 'wait_sub': 8}

# 从索引映射回类别名称
label_map = dict((v, k) for k, v in train_class_indices.items())

# 预先获取的相对位置
relative_pos_action = (1641, 1040)  #开始行动
relative_pos_scene2 = (1010, 623) #场景中间/中间造物

relative_pos_scene1 = (605, 626) #第一个场景
relative_pos_scene1_add = (872, 593) #第一个场景（补正）
relative_pos_scene3 = (1355, 607) #第3个场景

relative_pos_award1 = (731, 952) #战斗奖励1
relative_pos_award2 = (933, 952) #战斗奖励2/强化意志
relative_pos_tool_confirm = (972, 1044) #确认领取造物
relative_pos_upgrade1 = (558, 322)#强化意志1号位
relative_pos_upgrade2 = (594, 524)#强化意志2号位
relative_pos_upgrade3 = (608, 673)#强化意志3号位
relative_pos_upgrade4 = (568, 844) #强化意志4号位
relative_pos_upgrade_confirm = (1431, 1027) #确认强化意志
relative_pos_upgrade_leave = (575, 1002) #退出强化意志

relative_pos_dialogue3 = (1757, 725) #对话3 （双击）
relative_pos_dialogue3_add = (1806, 858)#对话3 （补正）

relative_pos_shop2 = (675, 616)
relative_pos_shop_confirm = (1176, 808)
relative_pos_pur_close = (1588, 345) #关闭购物
relative_pos_shop_leave = (1703, 582)
relative_pos_shop3 = (982, 627)
relative_pos_shop4 = (1343, 623)
relative_pos_shop5 = (1358, 1011)
relative_pos_shop6 = (1001, 1021)

try:
    while True:
        if check_for_exit():  # 检查是否需要退出
            break
        windows = gw.getWindowsWithTitle('MuMu模拟器12') #模拟器分辨率设置 1920x1080 280DPI
        if windows:
            window = windows[0]
            hwnd = window._hWnd
            current_screenshot = capture_screenshot(hwnd)

            # 将OpenCV格式的图像转换为适合模型预测的格式
            img_array = cv2.resize(current_screenshot, (150, 250))  # 调整图像大小
            img_array = img_array.astype('float32') / 255.0  # 归一化
            img_array = np.expand_dims(img_array, axis=0)  # 增加批次维度

            # 预测并获取类别名称
            prediction = model.predict(img_array)
            predicted_class_index = np.argmax(prediction[0])
            predicted_class_name = label_map[predicted_class_index]
            print(f"current state: {predicted_class_name}")
            time.sleep(1)
            # 根据预测结果执行特定操作的代码
            if predicted_class_index == 6:
                time.sleep(2)
                continue
            elif predicted_class_index == 0:
                win_pos = window.topleft
                relative_pos1 = relative_pos_award1
                relative_pos2 = relative_pos_award2
                relative_pos3 = relative_pos_tool_confirm
                # 计算出绝对坐标
                absolute_pos_double_click1 = (win_pos[0] + relative_pos1[0],
                                              win_pos[1] + relative_pos1[1])

                absolute_pos_double_click2 = (win_pos[0] + relative_pos2[0],
                                              win_pos[1] + relative_pos2[1])

                absolute_pos_double_click3 = (win_pos[0] + relative_pos3[0],
                                              win_pos[1] + relative_pos3[1])
                # 点击
                pyautogui.click(absolute_pos_double_click1)
                time.sleep(0.5)
                pyautogui.click(absolute_pos_double_click2)
                time.sleep(0.5)
                pyautogui.click(absolute_pos_double_click3)
                time.sleep(0.5)

            elif predicted_class_index == 1:
                win_pos = window.topleft
                relative_pos1 = relative_pos_action
                relative_pos2 = relative_pos_dialogue3
                relative_pos3 = relative_pos_dialogue3_add
                relative_pos4 = (1736, 593) #补正位置
                absolute_pos_double_click1 = (win_pos[0] + relative_pos1[0],
                                              win_pos[1] + relative_pos1[1])
                absolute_pos_double_click2 = (win_pos[0] + relative_pos2[0],
                                              win_pos[1] + relative_pos2[1])
                absolute_pos_double_click3 = (win_pos[0] + relative_pos3[0],
                                              win_pos[1] + relative_pos3[1])
                absolute_pos_double_click4 = (win_pos[0] + relative_pos4[0],
                                              win_pos[1] + relative_pos4[1])
                # 点击
                pyautogui.click(absolute_pos_double_click1)
                pyautogui.click(absolute_pos_double_click2, clicks=2, interval=0.25)
                pyautogui.click(absolute_pos_double_click3, clicks=2, interval=0.25)
                pyautogui.click(absolute_pos_double_click4, clicks=2, interval=0.25)
                time.sleep(2)
            elif predicted_class_index == 2:
                win_pos = window.topleft
                relative_pos1 = relative_pos_scene2
                relative_pos2 = relative_pos_action
                relative_pos3 = relative_pos_scene3
                # 计算出绝对坐标
                absolute_pos_double_click1 = (win_pos[0] + relative_pos1[0],
                                              win_pos[1] + relative_pos1[1])
                absolute_pos_double_click2 = (win_pos[0] + relative_pos2[0],
                                              win_pos[1] + relative_pos2[1])
                absolute_pos_double_click3 = (win_pos[0] + relative_pos3[0],
                                              win_pos[1] + relative_pos3[1])
                # 点击
                pyautogui.click(absolute_pos_double_click1, clicks=2, interval=0.5)
                time.sleep(1)
                pyautogui.click(absolute_pos_double_click3)
                pyautogui.click(absolute_pos_double_click2, clicks=2, interval=0.5)
                time.sleep(1)

            elif predicted_class_index == 3:
                win_pos = window.topleft
                relative_pos1 = relative_pos_shop3
                relative_pos2 = relative_pos_shop_confirm
                relative_pos3 = relative_pos_pur_close
                relative_pos4 = relative_pos_shop2
                relative_pos5 = relative_pos_shop_confirm
                relative_pos6 = relative_pos_pur_close
                relative_pos7 = relative_pos_shop_leave
                absolute_pos_double_click1 = (win_pos[0] + relative_pos1[0],
                                              win_pos[1] + relative_pos1[1])
                absolute_pos_double_click2 = (win_pos[0] + relative_pos2[0],
                                              win_pos[1] + relative_pos2[1])
                absolute_pos_double_click3 = (win_pos[0] + relative_pos3[0],
                                              win_pos[1] + relative_pos3[1])
                absolute_pos_double_click4 = (win_pos[0] + relative_pos4[0],
                                              win_pos[1] + relative_pos4[1])
                absolute_pos_double_click5 = (win_pos[0] + relative_pos5[0],
                                              win_pos[1] + relative_pos5[1])
                absolute_pos_double_click6 = (win_pos[0] + relative_pos6[0],
                                              win_pos[1] + relative_pos6[1])
                absolute_pos_double_click7 = (win_pos[0] + relative_pos7[0],
                                              win_pos[1] + relative_pos7[1])
                # 点击
                pyautogui.click(absolute_pos_double_click1)
                time.sleep(0.5)
                pyautogui.click(absolute_pos_double_click2)
                time.sleep(1)
                pyautogui.click(absolute_pos_double_click3)
                time.sleep(0.5)
                pyautogui.click(absolute_pos_double_click4)
                time.sleep(0.5)
                pyautogui.click(absolute_pos_double_click5)
                time.sleep(1)
                pyautogui.click(absolute_pos_double_click6)
                time.sleep(0.5)
                pyautogui.click(absolute_pos_double_click7)
                time.sleep(1)
            elif predicted_class_index == 4:
                win_pos = window.topleft
                relative_pos1 = relative_pos_action
                absolute_pos_double_click1 = (win_pos[0] + relative_pos1[0],
                                              win_pos[1] + relative_pos1[1])
                # 点击
                pyautogui.click(absolute_pos_double_click1, clicks=2, interval=0.5)
                time.sleep(1)
            elif predicted_class_index == 5:
                win_pos = window.topleft
                relative_pos1 = relative_pos_upgrade4
                relative_pos2 = relative_pos_upgrade_confirm
                relative_pos3 = relative_pos_upgrade3
                relative_pos4 = relative_pos_upgrade_confirm
                relative_pos5 = relative_pos_upgrade1
                relative_pos6 = relative_pos_upgrade_confirm
                relative_pos7 = relative_pos_upgrade2
                relative_pos8 = relative_pos_upgrade_confirm
                relative_pos9 = relative_pos_upgrade_leave
                # 计算出绝对坐标
                absolute_pos_double_click1 = (win_pos[0] + relative_pos1[0],
                                              win_pos[1] + relative_pos1[1])
                absolute_pos_double_click2 = (win_pos[0] + relative_pos2[0],
                                              win_pos[1] + relative_pos2[1])
                absolute_pos_double_click3 = (win_pos[0] + relative_pos3[0],
                                              win_pos[1] + relative_pos3[1])
                absolute_pos_double_click4 = (win_pos[0] + relative_pos4[0],
                                              win_pos[1] + relative_pos4[1])
                absolute_pos_double_click5 = (win_pos[0] + relative_pos5[0],
                                              win_pos[1] + relative_pos5[1])
                absolute_pos_double_click6 = (win_pos[0] + relative_pos6[0],
                                              win_pos[1] + relative_pos6[1])
                absolute_pos_double_click7 = (win_pos[0] + relative_pos7[0],
                                              win_pos[1] + relative_pos7[1])
                absolute_pos_double_click8 = (win_pos[0] + relative_pos8[0],
                                              win_pos[1] + relative_pos8[1])
                absolute_pos_double_click9 = (win_pos[0] + relative_pos9[0],
                                              win_pos[1] + relative_pos9[1])
                # 点击
                pyautogui.click(absolute_pos_double_click1)
                pyautogui.click(absolute_pos_double_click2, clicks=2, interval=1)
                pyautogui.click(absolute_pos_double_click3)
                pyautogui.click(absolute_pos_double_click4, clicks=2, interval=1)
                pyautogui.click(absolute_pos_double_click5)
                pyautogui.click(absolute_pos_double_click6, clicks=2, interval=1)
                pyautogui.click(absolute_pos_double_click7)
                pyautogui.click(absolute_pos_double_click8, clicks=2, interval=1)
                pyautogui.click(absolute_pos_double_click9)
                time.sleep(1)
            elif predicted_class_index == 7:
                win_pos = window.topleft
                relative_pos1 = relative_pos_action
                absolute_pos_double_click1 = (win_pos[0] + relative_pos1[0],
                                              win_pos[1] + relative_pos1[1])
                # 点击
                pyautogui.click(absolute_pos_double_click1, clicks=2, interval=0.75)
                time.sleep(2)
            elif predicted_class_index == 8:
                win_pos = window.topleft
                relative_pos1 = relative_pos_action
                absolute_pos_double_click1 = (win_pos[0] + relative_pos1[0],
                                              win_pos[1] + relative_pos1[1])
                # 点击
                pyautogui.click(absolute_pos_double_click1)
                time.sleep(2)
        else:
            print("没有找到窗口")
            time.sleep(2)

except Exception as e:
    print(f"发生错误：{e}")
finally:
    print("程序已停止")








