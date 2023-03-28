
import cv2
# 读入灰度图
img=cv2.imread('/media/ztc/Data/temp/batch4/vsm_1/background.bmp', cv2.IMREAD_GRAYSCALE)
# 定义鼠标回调函数
def on_mouse(event, x, y, flags, param):
    if event==cv2.EVENT_LBUTTONDOWN:
# 如果鼠标按下，获取当前位置的像素值并输出 if event == cv2.EVENT_LBUTTONDOWN:
        value = img[y,x]
        print(f'({x},{y}):{value}')
#使用setMouseCal1back设置鼠标回调函数 cv2.setMouseCallback('Image', onmouse)
cv2.namedWindow('background', cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback('background',on_mouse)
# 显示图像
cv2.imshow('background',img)
cv2.waitKey(0)
