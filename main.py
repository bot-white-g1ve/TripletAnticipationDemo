import os
import sys
import data
from PyQt5.QtCore import Qt, QTimer, QDir
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget, QSlider

def d_print(func, str):
    print(f"(In {func}) {str}")

app_width = 1600
app_height = 800
button_width = 90
button_height = 30
frameSlider_width = 290
video_width = (int)((app_width-40)/2)
video_height = (int)(video_width*2/3)
video_vertical = 10
label_width = video_width
label_height = 30*4
description_label_vertical = video_vertical + video_height + 10
label_vertical = video_vertical + video_height + 10 + 30
last_line_vertical = app_height - 50
last3_line_vertical = app_height - 200
last_column_horizontal = app_width -10

mapping_file = "label_mapping.json"

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SurgAnt')
        self.setGeometry(100, 100, app_width, app_height)
        
        self.currentImageLabel = QLabel(self)
        self.currentImageLabel.setGeometry(10, video_vertical, video_width, video_height)

        self.futureImageLabel = QLabel(self)
        self.futureImageLabel.setGeometry(30+video_width, video_vertical, video_width, video_height)

        self.currentLabelDescription = QLabel("Current Frame's label", self)
        self.currentLabelDescription.setGeometry(10, description_label_vertical, label_width, label_height)
        self.currentLabelDescription.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.currentLabelDescription.setStyleSheet("font-size: 12pt")

        self.currentLabelLabel = QLabel(self)
        self.currentLabelLabel.setGeometry(10, label_vertical, label_width, label_height)
        self.currentLabelLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.currentLabelLabel.setStyleSheet("font-size: 12pt")

        self.futureLabelDescription = QLabel("Future Frame's label", self)
        self.futureLabelDescription.setGeometry(30+video_width, description_label_vertical, label_width, label_height)
        self.futureLabelDescription.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.futureLabelDescription.setStyleSheet("font-size: 12pt")

        self.futureLabelLabel = QLabel(self)
        self.futureLabelLabel.setGeometry(30+video_width, label_vertical, label_width, label_height)
        self.futureLabelLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.futureLabelLabel.setStyleSheet("font-size: 12pt")

        self.predictionLabelDescription = QLabel("Prediction", self)
        self.predictionLabelDescription.setGeometry(int(30+3/2*video_width), description_label_vertical, label_width, label_height)
        self.predictionLabelDescription.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.predictionLabelDescription.setStyleSheet("font-size: 12pt")

        self.predictionLabelLabal = QLabel(self)
        self.predictionLabelLabal.setGeometry(int(30+3/2*video_width), label_vertical, label_width, label_height)
        self.predictionLabelLabal.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.predictionLabelLabal.setStyleSheet("font-size: 12pt")
        
        self.videoInfoLabel = QLabel("Select a folder of surgical video frames to start", self)
        self.videoInfoLabel.setGeometry(10, last3_line_vertical, 1000, 100)
        self.videoInfoLabel.setStyleSheet("font-size: 12pt")

        self.playButton = QPushButton('Play', self)
        self.playButton.setGeometry(10+(button_width+10)*0, last_line_vertical, button_width, button_height)
        self.playButton.clicked.connect(self.play)

        self.pauseButton = QPushButton('Pause', self)
        self.pauseButton.setGeometry(10+(button_width+10)*1, last_line_vertical, button_width, button_height)
        self.pauseButton.clicked.connect(self.pause)

        self.nextButton = QPushButton('Next', self)
        self.nextButton.setGeometry(10+(button_width+10)*2, last_line_vertical, button_width, button_height)
        self.nextButton.clicked.connect(self.showNextImage)
        
        self.previousButton = QPushButton('Previous', self)
        self.previousButton.setGeometry(10+(button_width+10)*3, last_line_vertical, button_width, button_height)
        self.previousButton.clicked.connect(self.showPreviousImage)

        self.selectFolderButton = QPushButton('Select Folder', self)
        self.selectFolderButton.setGeometry(10+(button_width+10)*4, last_line_vertical, button_width+20, button_height)
        self.selectFolderButton.clicked.connect(self.selectFolder)
        
        self.fpsSlider = QSlider(self)
        self.fpsSlider.setGeometry(10+(button_width+10)*5+20, last_line_vertical, button_width, button_height)
        self.fpsSlider.setOrientation(Qt.Horizontal)
        self.fpsSlider.setMinimum(1)
        self.fpsSlider.setMaximum(60)
        self.fpsSlider.setValue(30)

        self.fpsInfoLabel = QLabel("Pause and adjust FPS then click play", self)
        self.fpsInfoLabel.setGeometry(10+(button_width+10)*6, last_line_vertical, 500, 30)

        self.frameSlider = QSlider(self)
        self.frameSlider.setGeometry(last_column_horizontal-frameSlider_width, last_line_vertical, frameSlider_width, 30)
        self.frameSlider.setOrientation(Qt.Horizontal)
        self.frameSlider.valueChanged.connect(self.frameChanged)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.showNextImage)
        self.imageList = []
        self.currentIndex = 0

    def selectFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.imageList = sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.png')])
            tripletLabelFile = os.path.join(folder, 'triplet.txt')
            tripletLabelList_withoutColor = data.read_txt_to_string_list(tripletLabelFile, mapping_file, 'triplet')
            self.tripletLabelList = data.add_color_to_string_list(tripletLabelList_withoutColor)
            predictionResultFile = os.path.join(folder, 'prediction.txt')
            predictionLabelList_withoutColor = data.read_txt_to_string_list(predictionResultFile, mapping_file, 'triplet')
            self.predictionLabelList = data.add_color_to_string_list(predictionLabelList_withoutColor)
            self.currentIndex = 0
            self.frameSlider.setMinimum(0)
            self.frameSlider.setMaximum(len(self.imageList) - 1)
            self.frameSlider.setValue(0)
            if self.imageList:
                self.showImage()

    def play(self):
        if self.imageList:
            fps = self.fpsSlider.value()
            self.timer.start(1000 // fps)

    def pause(self):
        self.timer.stop()

    def showNextImage(self):
        '''
        Change to show next image
        '''
        if self.currentIndex < len(self.imageList) - 1:
            self.currentIndex += 1
        else:
            self.currentIndex = 0
        self.frameSlider.setValue(self.currentIndex)
        self.showImage()
    
    def showPreviousImage(self):
        if self.currentIndex > 0:
            self.currentIndex -= 1
        else:
            self.currentIndex = len(self.imageList) - 1
        self.frameSlider.setValue(self.currentIndex)
        self.showImage()
    
    def showImage(self):
        '''
        Showing images for every frame
        '''
        d_print("showImage", f"current index is {self.currentIndex}")
        currentImagePath = self.imageList[self.currentIndex]
        currentLabel = "<br>".join(self.tripletLabelList[self.currentIndex])
        self.currentLabelLabel.setText(currentLabel)
        if self.currentIndex + 5 < len(self.imageList) - 1:
            d_print("showImage", "current index + 5 is less than the the length of whole video")
            futureImagePath = self.imageList[self.currentIndex + 5]
            futureLabel = "<br>".join(self.tripletLabelList[self.currentIndex + 5])
            self.futureLabelLabel.setText(futureLabel)
            predictionLabel = "<br>".join(self.predictionLabelList[self.currentIndex])
            self.predictionLabelLabal.setText(predictionLabel)
        else:
            d_print("showImage", "current index + 5 is more than the the length of whole video")
            futureImagePath = self.imageList[-1]
            futureLabel = "<br>".join(self.tripletLabelList[-1])
            self.futureLabelLabel.setText(futureLabel)
            predictionLabel = "<br>".join(self.predictionLabelList[-1])
            self.predictionLabelLabal.setText(predictionLabel)
        currentPixmap = QPixmap(currentImagePath)
        futurePixmap = QPixmap(futureImagePath)
        self.currentImageLabel.setPixmap(currentPixmap.scaled(self.currentImageLabel.width(), self.currentImageLabel.height(), aspectRatioMode=0))
        self.futureImageLabel.setPixmap(futurePixmap.scaled(self.futureImageLabel.width(), self.futureImageLabel.height(), aspectRatioMode=0))
        self.videoInfoLabel.setText(f"Displaying surgical video: Left is the current frame, Right is the future frame.")

    def frameChanged(self, index):
        '''
        For frame slider
        '''
        if self.imageList and 0 <= index < len(self.imageList):
            self.currentIndex = index
            self.showImage()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageViewer()
    ex.show()
    sys.exit(app.exec_())
