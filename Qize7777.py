from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *
from tkinter import messagebox
import os.path
import math


## 함수 선언 부분 ##
def func_open():
    global inImage, canvas, paper, window, XSIZE, YSIZE

    # 파일 --> 메모리
    filename = askopenfilename(parent=window, filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))

    if filename == "":  # 파일을 불러오는 중 취소
        return
    if canvas != None:  # 두 번 이상 새로운 파일을 불러오는 경우 실행
        canvas.destroy()

    # 캔버스 생성 (아직 점을 찍을 종이만 생성, 아직 사진 삽입X)
    canvas = Canvas(window, height=XSIZE, width=YSIZE)
    paper = PhotoImage(width=XSIZE, height=YSIZE)
    canvas.create_image((XSIZE / 2, YSIZE / 2), image=paper, state="normal")

    loadImage(filename)  # RAW 파일 데이터 저장
    displayImage()  # 메모리 --> 화면

    canvas.pack()

def loadImage(fname):
    global inImage, XSIZE, YSIZE
    inImage = []

    fsize = os.path.getsize(fname)  # 파일의 크키
    XSIZE = YSIZE = int(math.sqrt(fsize))  # 사진의 행과 열이 같다고 가정 (256 X 256)
    fp = open(fname, 'rb')

    for i in range(0, XSIZE):
        tmpList = []  # inImage의 한 행을 구성할 리스트
        for k in range(0, YSIZE):
            data = int(ord(fp.read(1)))  # 파일을 1byte씩 읽은 후, 고유값을 int형으로 변경
            tmpList.append(data)  # tmpLIst에 순차적으로 추가
        inImage.append(tmpList)  # tmpList가 한 행을 구성했다는 그 리스트를 inimage에 주가하여 행렬 구성

    fp.close()

def displayImage():
    global XSIZE, YSIZE, inImage, paper
    rgbString = ""
    for i in range(0, XSIZE):
        tmpString = ""
        for k in range(0, YSIZE):
            data = inImage[i][k]
            tmpString += "#%02x%02x%02x " % (data, data, data)  # x 뒤에 한칸 공백
        rgbString += "{" + tmpString + "} "  # } 뒤에 한칸 공백
    paper.put(rgbString)  # 사용자에게 사진을 보여줌


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
                    data = inImage[i][k] + 128
                    if data > 255:  # 최대 범위인 255를 넘어가는 데이터의 값을 255로 설정
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
                    data = inImage[i][k] - 128
                    if data < 0:  # 최소 범위인 0보다 작은 데이터의 값을 0으로 설정
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
                    data = 255 - inImage[i][k]  # 흑백 반전
                    tmpString += "#%02x%02x%02x " % (data, data, data)  # x 뒤에 한칸 공백
                rgbString += "{" + tmpString + "} "  # } 뒤에 한칸 공백
            paper.put(rgbString)
    except IndexError:
        messagebox.showinfo(title="ERROR!", message="사진을 먼저 추가해주세요.")


## 전역 변수 선언 부분 ##
window, canvas, paper = None, None, None  # 세 개의 변수를 None으로 설정
XSIZE, YSIZE = 256, 256
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
