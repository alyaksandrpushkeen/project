import io
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6 import uic
from pioneer_sdk import Pioneer, Camera

SIZE = WIDTH, HEIGHT = 675, 328
CAMERA_SIZE = C_WIDTH, C_HEIGHT = 480, 320
template = """<?xml version="1.0" encoding="UTF-8"?> <ui version="4.0"> <class>MainWindow</class> <widget 
class="QMainWindow" name="MainWindow"> <property name="geometry"> <rect> <x>0</x> <y>0</y> <width>790</width> 
<height>496</height> </rect> </property> <property name="windowTitle"> <string>MainWindow</string> </property> 
<widget class="QWidget" name="centralwidget"> <widget class="QGraphicsView" name="graphicsView"> <property 
name="geometry"> <rect> <x>20</x> <y>220</y> <width>256</width> <height>231</height> </rect> </property> </widget> 
<widget class="QLabel" name="label"> <property name="geometry"> <rect> <x>20</x> <y>95</y> <width>231</width> 
<height>131</height> </rect> </property> <property name="text"> 
<string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; 
font-size:48pt;&quot;&gt;00:00&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string> </property> </widget> 
<widget class="QProgressBar" name="progressBar"> <property name="geometry"> <rect> <x>290</x> <y>390</y> 
<width>501</width> <height>61</height> </rect> </property> <property name="value"> <number>24</number> </property> 
</widget> <widget class="QLabel" name="label_2"> <property name="geometry"> <rect> <x>20</x> <y>20</y> 
<width>241</width> <height>81</height> </rect> </property> <property name="text"> 
<string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;&lt;span style=&quot; font-size:18pt;&quot;&gt;Время в 
полёте&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string> </property> </widget> </widget> <widget 
class="QMenuBar" name="menubar"> <property name="geometry"> <rect> <x>0</x> <y>0</y> <width>790</width> 
<height>26</height> </rect> </property> </widget> </widget> <resources/> <connections/> </ui> """
pioneer_mini = Pioneer()
camera = Camera()


class Check(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        check = self.check()
        if check == 0:
            exit()

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
