import sys
from PyQt5.QtWidgets import (QWidget, QLabel,QTextEdit,QComboBox, QApplication,QPushButton,QGridLayout,QMainWindow)
from PyQt5.QtGui import QPalette, QBrush, QPixmap,QFont
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
import requests
import random
import hashlib
import json
from PIL import Image
# 接口文件
from get_chinese import pic2word

# 1,只需要在get_Chinese的文件中有一个名为:pic2word(pic)的函数即可
# 2,pic为表示图片的矩阵变量，用imread导入的
# 3,识别之后的文本文件应该保存为'word.txt'
# 4,翻译只能翻译单段文字，不能有换行符!!!!!
# 5,显示尽量显示较少的文本，较多的文本Label显示不下，没有特别处理!!!!!
# 满足1,3条件就可以直接通过GUI操作，无需管内部怎么运行


class OCR_GUI(QWidget):
    def __init__(self):
        self.pic=np.ndarray(())
        self.word=''
        self.translation=''
        super().__init__()
        self.initUI()
        
    def initUI(self):
        
        self.setFixedWidth(1180) # 设置窗口大小
        self.setFixedHeight(553)
        
        # 建立GUI所有用到的对象
        self.label_pic = QLabel()
        self.label_word = QLabel()
        self.label_translation = QLabel()
        self.label_word.setWordWrap(True)
        self.label_translation.setWordWrap(True)
        
        self.btn_in = QPushButton('导入图片',self)
        self.btn_ORC = QPushButton('文本识别',self)
        self.btn_Trans = QPushButton('文本翻译',self)
        
        # 设置各个部件在窗口上的位置
        layout = QGridLayout(self)
        layout.setSpacing(10)
        layout.addWidget(self.label_pic,1,1,3,3)
        layout.addWidget(self.label_word,1,4,3,3)
        layout.addWidget(self.label_translation,1,7,3,3)
        layout.addWidget(self.btn_in,4,2,1,1)
        layout.addWidget(self.btn_ORC,4,5,1,1)
        layout.addWidget(self.btn_Trans,4,8,1,1)
        
        # 设置各个对象的样式
        self.setStyleSheet("QLabel{background:white;}") # 设定所有Label的颜色为白色
        
        self.label_pic.setFixedWidth(350) 
        self.label_pic.setFixedHeight(260)
        self.label_pic.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.label_word.setFixedWidth(350) 
        self.label_word.setFixedHeight(260)
        self.label_word.setFont(QFont("Roman times",10,QFont.Bold))
        self.label_word.setAlignment(Qt.AlignTop | Qt.AlignLeft)
     
        self.label_translation.setFixedWidth(350) 
        self.label_translation.setFixedHeight(320)
        self.label_translation.setFont(QFont("Roman times",9,QFont.Bold))
        self.label_translation.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        self.btn_in.setStyleSheet("QPushButton{color:black}" "QPushButton:hover{color:red}" "QPushButton{background-color:lightblue}")
        self.btn_in.setFixedHeight(75)
        self.btn_in.setFixedWidth(120)
        self.btn_in.setFont(QFont("Roman times",18,QFont.Bold))
        
        self.btn_ORC.setStyleSheet("QPushButton{color:black}" "QPushButton:hover{color:red}" "QPushButton{background-color:lightblue}") 
        self.btn_ORC.setFixedHeight(75)
        self.btn_ORC.setFixedWidth(120)
        self.btn_ORC.setFont(QFont("Roman times",18,QFont.Bold))
        
        self.btn_Trans.setStyleSheet("QPushButton{color:black}" "QPushButton:hover{color:red}" "QPushButton{background-color:lightblue}")
        self.btn_Trans.setFixedHeight(75)
        self.btn_Trans.setFixedWidth(120)
        self.btn_Trans.setFont(QFont("Roman times",18,QFont.Bold))
        
        
        #信号与槽链接
        self.btn_in.clicked.connect(self.PicIn)
        self.btn_ORC.clicked.connect(self.OCR)
        self.btn_Trans.clicked.connect(self.Translate)
        
        
        #窗口外观设置
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('background2.jpg')))
        self.setPalette(palette1)
        self.setWindowTitle('文本识别翻译')
        
        self.show() #窗口显示
        
        
    def PicIn(self):
        # 从电脑的文件中选择一张图片导入
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
       
        Pixmap = QPixmap(imgName) #得到要加载的图片名
        scaredPixmap = Pixmap.scaled(350, 260, aspectRatioMode=Qt.KeepAspectRatio) #调整图片使其适应Label
        # self.pic = mpimg.imread(imgName) #读入图片
        self.pic = (Image.open(imgName).convert('RGB'))
        self.label_pic.setPixmap(scaredPixmap) #在label上显示图片
       
    def OCR(self):
        # 调用主文件中的函数进行文本识别
        pic2word(self.pic)
        f = open('word.txt')
        self.word = f.read()
        self.label_word.setText(self.word)
        
    def Translate(self):
        # 调用API,翻译文本
        T = trans()
        f2 = open('to_english.txt')
        self.to_english = f2.read()
        self.translation = T.translate(self.to_english)
        self.label_translation.setText(self.translation)
        
        
class trans():
    def __init__(self):
        # API接口所需的参数
        self.appid = '20190307000274854'
        self.key = 'WWBPRjInI96ehr8d4qCw'
        self.url = 'http://api.fanyi.baidu.com/api/trans/vip/translate?'
        self.from_language = 'zh'
        self.to_language = 'en'

    # 改变待翻译文本的语言
    def change_fl(self, fl):
        self.from_language = fl

    # 改变翻译出的文本的语言
    def change_tl(self, tl):
        self.to_language = tl

    def translate(self, qMax, salt=random.randint(32768, 65536)):
        # qMax为待翻译文本
        # 拼接字符串appid+q+salt+key
        final_translate_result=''  # 由于API翻译的字符串中不能有换行符
        qlist = qMax.split('\n')   # 因此先利用换行符把原字符串分割
        for q in qlist:
            salt=random.randint(32768, 65536)
            sign = self.appid + q + str(salt) + self.key
            # 计算md5加密前，需将字符串更改为utf-8编码
            sign = sign.encode('utf-8')
            # md5加密得到签名sign
            sign_new = hashlib.md5(sign).hexdigest()
            new_url = self.url + 'q=' + q + '&from=' + self.from_language + '&to=' + self.to_language + '&appid=' + \
            self.appid + '&salt=' + str(salt) + '&sign=' + sign_new
            res = requests.get(new_url)
            json_data = json.loads(res.text)
            translate_result = json_data["trans_result"][0]["dst"] # 这一段文字的翻译结果
            
            final_translate_result = final_translate_result + translate_result+'\n' # 合并最后的话
            
        return final_translate_result

 
if __name__ == '__main__':
    # 主函数
    if(not QApplication.instance()):
       app = QApplication(sys.argv)
    else:
       app= QApplication.instance()
    
    ex = OCR_GUI()
    sys.exit(app.exec_())
