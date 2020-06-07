import json
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.notes = []

    def initUI(self):
        layout = QHBoxLayout()
        rightLayout = QVBoxLayout()
        grid = QGridLayout()

        placeHolder1 = QLabel('PH1')
        placeHolder2 = QLabel('')

        makeAdofile = QPushButton('adofai 파일로 내보내기')
        makeAdofile.setStyleSheet('background-color: #eeeeee;')
        saveBtn = QPushButton('저장')
        saveBtn.setStyleSheet('background-color: #eaeaea;')
        saveBtn.setDisabled(True)
        loadBtn = QPushButton('불러오기')
        loadBtn.setStyleSheet('background-color: #eaeaea;')
        loadBtn.setDisabled(True)
        notesList = QTextEdit()
        notesList.setReadOnly(True)
        notesList.setText('''음계 목록:

1: 낮은 도
2: 낮은 도#
3: 낮은 레
4: 낮은 레#
5: 낮은 미
6: 낮은 파
7: 낮은 파#
8: 낮은 솔
9: 낮은 솔#
10: 낮은 라
11: 낮은 라#
12: 낮은 시
13: 도
14: 도#
15: 레
16: 레#
17: 미
18: 파
19: 파#
20: 솔
21: 솔#
22: 라
23: 라#
24: 시
25: 높은 도
+12: 한 옥타브 위

길이:
1: 4분음표
기준으로 정수/소수로 나타내주세요'''
        )
        notesList.setFixedSize(120, 578)
        notesList.setStyleSheet('background-color: #ffffff; border: 1px solid lightgray')

        noteLabel = QLabel('음')

        self.noteIn = QLineEdit()
        self.noteIn.setPlaceholderText('음')

        lenLabel = QLabel('길이')

        self.lenIn = QLineEdit()
        self.lenIn.setPlaceholderText('길이')

        inputNote = QPushButton('입력')

        self.inputedNotes = QTextEdit()
        self.inputedNotes.setStyleSheet('background-color: #ffffff; border: 1px solid lightgray')

        grid.addWidget(noteLabel, 0, 0)
        grid.addWidget(lenLabel, 0, 1)

        grid.addWidget(self.noteIn, 1, 0)
        grid.addWidget(self.lenIn, 1, 1)

        grid.setAlignment(Qt.AlignTop)

        rightLayout.addLayout(grid)
        rightLayout.addWidget(inputNote)
        rightLayout.addWidget(self.inputedNotes)
        rightLayout.addWidget(makeAdofile)
        rightLayout.addWidget(saveBtn)
        rightLayout.addWidget(loadBtn)
        rightLayout.setAlignment(Qt.AlignTop)

        layout.addWidget(notesList)
        layout.addLayout(rightLayout)
        layout.addWidget(placeHolder2)

        inputNote.clicked.connect(self.inputNoteLen)
        self.inputedNotes.textChanged.connect(self.changeNotes)
        makeAdofile.clicked.connect(self.makeAdofai)

        self.setLayout(layout)
        self.setWindowTitle(' ')
        self.setGeometry(300, 300, 450, 120)
        self.setFixedSize(300, 600)
        self.show()

    def inputNoteLen(self):
        self.notes.append((self.noteIn.text(), self.lenIn.text()))
        self.inputedNotes.insertPlainText(self.noteIn.text() + ', ' + self.lenIn.text() + '\n')

    def changeNotes(self):
        data = self.inputedNotes.toPlainText().split('\n')
        try:
            while data[-1] == '':
                data = data[0:-1]
        except IndexError:
            pass
        data2 = data[:]
        data = []
        for i in data2:
            data.append(i.split(','))
        tmp = []
        for i in data:
            tmp.append(tuple(i))
        self.notes = tmp

    def makeAdofai(self):
        try:
            inputs = self.notes
            mode = 'RH'

            firstNotes = [320, 330, 360, 365, 400, 410, 425, 480, 500, 540, 570, 582] 
            nextNotes = [640, 660, 720, 730, 810, 853, 905, 960, 995, 1080, 1130, 1215, 1280]
            flat = mode[0]

            inputNotes = []

            pathlength = 0

            for i in inputs:
                if int(i[0]) < 12:
                    thisnote = firstNotes[int(i[0])]
                else:
                    thisnote = nextNotes[int(i[0]) % 12] * (round(int(i[0]) / 12 - 0.5))
                length = round(8 * thisnote / 320 * float(i[1]))
                inputNotes.append((thisnote, length))

            pathdata = ''
            tmp = 0
            actions = [{ "floor": 1, "eventType": "Twirl" },]
            for i in inputNotes:
                tmp += 1
                pathdata += 'R'
                actions.append({ "floor": tmp, "eventType": "SetSpeed", "speedType": "Bpm", "beatsPerMinute": 640, "bpmMultiplier": 1 },)
                actions.append({ "floor": tmp+1, "eventType": "SetSpeed", "speedType": "Bpm", "beatsPerMinute": i[0], "bpmMultiplier": 1 },)
                for i in range(i[1]):
                    tmp += 2
                    pathdata += 'RH'
                    actions.append({ "floor": tmp-1, "eventType": "Twirl" },)
                    actions.append({ "floor": tmp, "eventType": "Twirl" },)

            settings = {
                "version": 2, 
                "artist": "아티스트", 
                "song": "제목", 
                "author": "만든이", 
                "separateCountdownTime": "Enabled",
                "songFilename": "", 
                "bpm": 320, 
                "volume": 100, 
                "offset": 0, 
                "pitch": 100, 
                "hitsound": "Kick", 
                "hitsoundVolume": 100,
                "trackColorType": "Single", 
                "trackColor": "debb7b", 
                "secondaryTrackColor": "ffffff", 
                "trackColorAnimDuration": 2, 
                "trackColorPulse": "None", 
                "trackPulseLength": 10, 
                "trackStyle": "Standard", 
                "trackAnimation": "None", 
                "beatsAhead": 3, 
                "trackDisappearAnimation": "None", 
                "beatsBehind": 4,
                "backgroundColor": "000000", 
                "bgImage": "", 
                "bgImageColor": "ffffff", 
                "parallax": [100, 100], 
                "bgDisplayMode": "FitToScreen", 
                "lockRot": "Disabled", 
                "loopBG": "Disabled", 
                "unscaledSize": 100,
                "relativeTo": "Player", 
                "position": [0, 0], 
                "rotation": 0, 
                "zoom": 100,
                "bgVideo": "", 
                "loopVideo": "Disabled", 
                "vidOffset": 0, 
                "floorIconOutlines": "Disabled", 
                "stickToFloors": "Enabled", 
                "planetEase": "Linear", 
                "planetEaseParts": 1,
                "madewith": "AHS Free by PAPER_PPT_"
            }

            filedata = {}
            filedata['pathData'] = pathdata
            filedata['settings'] = settings
            filedata['actions'] = actions

            jsonData = json.dumps(filedata, indent=4)
            filters = "ADOFAI Custom Files (*.adofai)"
            path = QFileDialog.getSaveFileName(self, 'Open file', './', filters)
            file = open(path[0], mode='w')
            file.write(jsonData)
        except Exception as e:
            print('오류: ' + str(e))

app = QApplication(sys.argv)
ex = MyApp()
sys.exit(app.exec_())


