from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *
from tkinter import messagebox
import os.path
import math


## 함수 선언 부분 ##
def loadImage(fname):
    global filename, inImage, canvas, paper, window, XSIZE, YSIZE

    inImage = []
    fsize = os.path.getsize(fname)
    XSIZE = YSIZE = int(math.sqrt(fsize))

    fp = open(fname, 'rb')

    for i in range(0, XSIZE):
        tmpList = []
        for k in range(0, YSIZE):
            data = int(ord(fp.read(1)))
            tmpList.append(data)
        inImage.append(tmpList)

    fp.close()


def displayImage():
    global XSIZE, YSIZE, inImage
    rgbString = ""
    for i in range(0, XSIZE):
        tmpString = ""
        for k in range(0, YSIZE):
            data = inImage[i][k]
            tmpString += "#%02x%02x%02x " % (data, data, data)  # x 뒤에 한칸 공백
        rgbString += "{" + tmpString + "} "  # } 뒤에 한칸 공백
    paper.put(rgbString)


def func_open():
    global filename, inImage, canvas, paper, window, XSIZE, YSIZE

    # 파일 --> 메모리
    filename = askopenfilename(parent=window, filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))

    if filename == "":
        return
    if canvas != None:
        canvas.destroy()

    canvas = Canvas(window, height=XSIZE, width=YSIZE)
    paper = PhotoImage(width=XSIZE, height=YSIZE)
    canvas.create_image((XSIZE / 2, YSIZE / 2), image=paper, state="normal")

    loadImage(filename)

    # 메모리 --> 화면
    displayImage()

    canvas.pack()


def func_exit():
    window.quit()
    window.destroy()


def Make_B():
    try:
        while True:
            global XSIZE, YSIZE, inImage
            rgbString = ""
            for i in range(0, XSIZE):
                tmpString = ""
                for k in range(0, YSIZE):
                    data = inImage[i][k]
                    if (data + 128) > 256 > 0:
                        data = 255
                    tmpString += "#%02x%02x%02x " % (data, data, data)  # x 뒤에 한칸 공백
                rgbString += "{" + tmpString + "} "  # } 뒤에 한칸 공백
            paper.put(rgbString)
    except IndexError:
        messagebox.showinfo(title="ERROR!", message="사진을 먼저 추가해주세요.")


def Make_D():
    try:
        while True:
            global XSIZE, YSIZE, inImage
            rgbString = ""
            for i in range(0, XSIZE):
                tmpString = ""
                for k in range(0, YSIZE):
                    data = inImage[i][k]
                    if (data - 128) < 0:
                        data = 0
                    tmpString += "#%02x%02x%02x " % (data, data, data)  # x 뒤에 한칸 공백
                rgbString += "{" + tmpString + "} "  # } 뒤에 한칸 공백
            paper.put(rgbString)
    except IndexError:
        messagebox.showinfo(title="ERROR!", message="사진을 먼저 추가해주세요.")


def Make_deca():
    try:
        while True:
            global XSIZE, YSIZE, inImage
            rgbString = ""
            for i in range(0, XSIZE):
                tmpString = ""
                for k in range(0, YSIZE):
                    data = inImage[i][k]
                    tmpString += "#%02x%02x%02x " % (255 - data, 255 - data, 255 - data)  # x 뒤에 한칸 공백
                rgbString += "{" + tmpString + "} "  # } 뒤에 한칸 공백
            paper.put(rgbString)
    except IndexError:
        messagebox.showinfo(title="ERROR!", message="사진을 먼저 추가해주세요.")


## 전역 변수 선언 부분 ##
window = None
canvas = None
XSIZE, YSIZE = 255, 255
inImage = []  # 2차원 리스트 (메모리)

## 메인 코드 부분 ##
if __name__ == "__main__":
    window = Tk()
    window.title("흑백 사진 보기")
    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu1 = Menu(mainMenu)
    mainMenu.add_cascade(label="파일", menu=fileMenu1)
    fileMenu1.add_cascade(label="열기", command=func_open)
    fileMenu1.add_separator()
    fileMenu1.add_cascade(label="종료", command=func_exit)

    fileMenu2 = Menu(mainMenu)
    mainMenu.add_cascade(label="사진효과", menu=fileMenu2)
    fileMenu2.add_cascade(label="밝게하기", command=Make_B)
    fileMenu2.add_separator()
    fileMenu2.add_cascade(label="어둡게하기", command=Make_D)
    fileMenu2.add_separator()
    fileMenu2.add_cascade(label="반전이미지", command=Make_deca)

    window.mainloop()
