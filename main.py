import win32gui
import win32ui
import win32con
import cv2
import time
import pyautogui
import pygetwindow as gw
import os
import numpy as np
from tensorflow.keras.models import load_model
import keyboard
import ctypes
import random

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

def get_window_size(window_title):
    win = gw.getWindowsWithTitle(window_title)[0]
    if win.isMinimized:
        print("窗口最小化，无法进行计算。")
        return None
    else:
        return (win.size.width, win.size.height)

def calculate_scale_factor(original_size, current_size):
    scale_factor_w = current_size[0] / original_size[0]
    scale_factor_h = current_size[1] / original_size[1]
    return scale_factor_w, scale_factor_h

def adjust_coordinates_for_scale(coords, scale_factor):
    adjusted_x = int(coords[0] * scale_factor[0])
    adjusted_y = int(coords[1] * scale_factor[1])
    return adjusted_x, adjusted_y

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

# 预设窗口大小
original_size = (1930, 1139)  # 预设尺寸
current_size = (1930, 1139) # assume the same

# 获取当前窗口的大小
window_title = "MuMu模拟器12"
current_size = get_window_size(window_title)  # update current size
scale_factor = calculate_scale_factor(original_size, current_size)

relative_pos_action = adjust_coordinates_for_scale((1641, 1040), scale_factor) # 开始行动
relative_pos_scene2 = adjust_coordinates_for_scale((1010, 623), scale_factor)  # 场景中间/中间造物
relative_pos_scene1 = adjust_coordinates_for_scale((605, 626), scale_factor)   # 第一个场景
relative_pos_scene1_add = adjust_coordinates_for_scale((872, 593), scale_factor)  # 第一个场景（补正）
relative_pos_scene3 = adjust_coordinates_for_scale((1355, 607), scale_factor)  # 第3个场景

relative_pos_award1 = adjust_coordinates_for_scale((731, 952), scale_factor)  # 奖励领取1
relative_pos_award2 = adjust_coordinates_for_scale((933, 952), scale_factor)  # 奖励领取2

relative_pos_tool_confirm = adjust_coordinates_for_scale((972, 1044), scale_factor)  # 确认领取造物
relative_pos_upgrade1 = adjust_coordinates_for_scale((558, 322), scale_factor)  # 强化意志1号位
relative_pos_upgrade2 = adjust_coordinates_for_scale((594, 524), scale_factor)  # 强化意志2号位
relative_pos_upgrade3 = adjust_coordinates_for_scale((608, 673), scale_factor)  # 强化意志3号位
relative_pos_upgrade4 = adjust_coordinates_for_scale((568, 844), scale_factor)  # 强化意志4号位
relative_pos_upgrade_confirm = adjust_coordinates_for_scale((1431, 1027), scale_factor)  # 确认强化意志
relative_pos_upgrade_leave = adjust_coordinates_for_scale((575, 1002), scale_factor)  # 退出强化意志

relative_pos_shop2 = adjust_coordinates_for_scale((675, 616), scale_factor)
relative_pos_shop_confirm = adjust_coordinates_for_scale((1176, 808), scale_factor)
relative_pos_pur_close = adjust_coordinates_for_scale((1588, 345), scale_factor)  # 关闭购物
relative_pos_shop_leave = adjust_coordinates_for_scale((1703, 582), scale_factor) # 关闭商店
relative_pos_shop3 = adjust_coordinates_for_scale((982, 627), scale_factor)
relative_pos_shop4 = adjust_coordinates_for_scale((1343, 623), scale_factor)
relative_pos_shop5 = adjust_coordinates_for_scale((1358, 1011), scale_factor)
relative_pos_shop6 = adjust_coordinates_for_scale((1001, 1021), scale_factor)

dialogue_options = [
    adjust_coordinates_for_scale((1633, 364), scale_factor),  # 对话1 （选项数=3）
    adjust_coordinates_for_scale((1840, 635), scale_factor),  # 对话2 （选项数=3）
    adjust_coordinates_for_scale((1757, 725), scale_factor),  # 对话3 （选项数=3）
    adjust_coordinates_for_scale((1673, 466), scale_factor),  # 对话1 （选项数=2）
    adjust_coordinates_for_scale((1422, 718), scale_factor)   # 对话2 （选项数=2）
]


try:
    while True:
        if check_for_exit():  # 检查是否需要退出
            break
        windows = gw.getWindowsWithTitle(window_title)
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
                # 选择2个对话
                selected_dialogue_i = random.sample(range(len(dialogue_options)), 2)
                for index in selected_dialogue_i:
                    pos = dialogue_options[index]
                    absolute_pos = (win_pos[0] + pos[0], win_pos[1] + pos[1])
                    # 在计算出的绝对坐标上执行双击操作
                    pyautogui.click(absolute_pos, clicks=2, interval=0.25)

            elif predicted_class_index == 2:  # 场景选择
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
                relative_pos1 = relative_pos_shop2
                relative_pos2 = relative_pos_shop_confirm
                relative_pos3 = relative_pos_pur_close
                relative_pos4 = relative_pos_shop3
                relative_pos5 = relative_pos_shop_confirm
                relative_pos6 = relative_pos_pur_close
                relative_pos7 = relative_pos_shop4
                relative_pos8 = relative_pos_shop_confirm
                relative_pos9 = relative_pos_pur_close
                relative_pos10 = relative_pos_shop_leave
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
                absolute_pos_double_click10 = (win_pos[0] + relative_pos10[0],
                                              win_pos[1] + relative_pos10[1])
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
                time.sleep(0.5)
                pyautogui.click(absolute_pos_double_click8)
                time.sleep(1)
                pyautogui.click(absolute_pos_double_click9)
                time.sleep(0.5)
                pyautogui.click(absolute_pos_double_click10)
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
                relative_pos5 = relative_pos_upgrade2
                relative_pos6 = relative_pos_upgrade_confirm
                relative_pos7 = relative_pos_upgrade1
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








