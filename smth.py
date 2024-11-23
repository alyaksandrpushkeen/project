import io
import sys

from PyQt6.QtMultimedia import QVideoFrame
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6 import uic, QtGui
from pioneer_sdk import Pioneer, Camera

SIZE = WIDTH, HEIGHT = 675, 328
CAMERA_SIZE = C_WIDTH, C_HEIGHT = 480, 320
template = """<?xml version="1.0" encoding="UTF-8"?> <ui version="4.0"> <class>MainWindow</class> <widget 
class="QMainWindow" name="MainWindow"> <property name="geometry"> <rect> <x>0</x> <y>0</y> <width>790</width> 
<height>496</height> </rect> </property> <property name="windowTitle"> <string>MainWindow</string> </property> 
<widget class="QWidget" name="centralwidget"> <widget class="QLabel" name="label"> <property name="geometry"> <rect> 
<x>20</x> <y>95</y> <width>231</width> <height>131</height> </rect> </property> <property name="text"> 
<string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; 
font-size:48pt;&quot;&gt;00:00&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string> </property> </widget> 
<widget class="QProgressBar" name="progressBar"> <property name="geometry"> <rect> <x>290</x> <y>390</y> 
<width>501</width> <height>61</height> </rect> </property> <property name="value"> <number>24</number> </property> 
</widget> <widget class="QLabel" name="label_2"> <property name="geometry"> <rect> <x>20</x> <y>50</y> 
<width>241</width> <height>81</height> </rect> </property> <property name="text"> 
<string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:18pt;&quot;&gt;Время в 
полёте&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string> </property> </widget> <widget class="QTextBrowser" 
name="textBrowser"> <property name="geometry"> <rect> <x>10</x> <y>221</y> <width>256</width> <height>231</height> 
</rect> </property> <property name="html"> <string>&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; 
&quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt; &lt;html&gt;&lt;head&gt;&lt;meta 
name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt; p, li { white-space: 
pre-wrap; } &lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'MS Shell Dlg 2'; font-size:7.8pt; 
font-weight:400; font-style:normal;&quot;&gt; &lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; 
margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-size:12pt;&quot;&gt;    1 
-- arm&lt;/span&gt;&lt;/p&gt; &lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; 
margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-size:12pt;&quot;&gt;    2 
-- disarm&lt;/span&gt;&lt;/p&gt; &lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; 
margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-size:12pt;&quot;&gt;    3 
-- takeoff&lt;/span&gt;&lt;/p&gt; &lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; 
margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-size:12pt;&quot;&gt;    4 
-- land&lt;/span&gt;&lt;/p&gt; &lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; 
margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-size:12pt;&quot;&gt;    z 
-- flesh&lt;/span&gt;&lt;/p&gt; &lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; 
margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-size:12pt;&quot;&gt;    ↶q 
 w↑  e↷    i-↑&lt;/span&gt;&lt;/p&gt; &lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; 
 margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-size:12pt;&quot;&gt;    
 ←a      d→    k-↓&lt;/span&gt;&lt;/p&gt; &lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; 
 margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-size:12pt;&quot;&gt;      
      s↓&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string> </property> </widget> <widget class="QPushButton" 
      name="pushButton"> <property name="geometry"> <rect> <x>20</x> <y>10</y> <width>211</width> <height>28</height> 
      </rect> </property> <property name="text"> <string>Подключиться</string> </property> </widget> </widget> 
      <widget class="QMenuBar" name="menubar"> <property name="geometry"> <rect> <x>0</x> <y>0</y> <width>790</width> 
      <height>26</height> </rect> </property> </widget> </widget> <resources/> <connections/> </ui> """
pioneer_mini = Pioneer()
camera = Camera()


class Check(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.setWindowTitle("Панель Управления")
        self.setWindowIcon(QtGui.QIcon("1.jpg"))
        self.progressBar.setValue(0)
        self.pushButton.clicked.connect(self.check)
        self.video = QVideoFrame()

    def check(self):
        if not pioneer_mini.connected():
            QMessageBox.critical(None, 'Ошибка подключения', 'Дрон и основной хост не сопряжены. Выполните '
                                                             'подключение и повторите попытку')
            return 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Check()
    ex.show()
    sys.exit(app.exec())
