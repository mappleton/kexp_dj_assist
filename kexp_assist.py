"""
GUI for kexp_assist_func.py.  Gets current playing song on KEXP and finds
KEXP events, KEXP YouTube videos, and local (WA & OR) events for the artist.
Also checks whether it is an anniversary for the album and calculates age.

Author: Michael Appleton
Date: September 26, 2021
"""

import sys
from PyQt5.QtWidgets import QLayout,QVBoxLayout,QMainWindow,QPushButton,QApplication,QLabel,QWidget,QScrollArea,QFrame, QSizePolicy
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtCore import Qt
import kexp_assist_func as k 


current_play = k.get_playlist()
if current_play['artist'] != 'airbreak':
    in_studios = k.get_instudios(current_play['artist'])
    shows = k.get_shows(current_play['artist'])
    videos = k.get_youtube(current_play['artist'])
    if current_play['release_date'] is not None:
        anni = k.get_anniversary(current_play['release_date'])
        current_play['anniversary'] = anni
elif current_play['artist'] == 'airbreak':
    in_studios = 'N/A'
    shows = 'N/A'
    videos = 'N/A'
    current_play['aniversary'] = 'N/A'
    

class Window(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("KEXP DJ Assistant")

        self.resize(370, 850) #(width, height)
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSizeConstraint(QLayout.SetMinimumSize)
        widget.setLayout(layout)

        #   Scroll Area Properties
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)

        #separator line
        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.HLine)
        h_line.setLineWidth(2)

        #   Scroll Area Layer add
        scroll_layout = QVBoxLayout()
        scroll_layout.addWidget(scroll)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(scroll_layout) 

        button = QPushButton('Update', self)        
        button.setFixedSize(120, 30)
        button.clicked.connect(self.on_click)
        layout.addWidget(button, alignment=(Qt.AlignHCenter | Qt.AlignTop))

        self.label_currentplaytitle = QLabel(self)
        self.label_currentplaytitle.setText('<span style="font-size:20px;">Current Play</span>')
        self.label_currentplaytitle.setStyleSheet("padding-left :5px")
        self.label_currentplaytitle.setWordWrap(True)
        layout.addWidget(self.label_currentplaytitle, alignment=(Qt.AlignTop))

        for key, value in current_play.items():
            label = 'self.'+key
            if value is None:
                value = 'None'
            exec(label+' = QLabel(self)')
            exec(label+'.setTextInteractionFlags(Qt.TextSelectableByMouse)')
            exec(label+'.setText(\'<span style="font-size:14px;">'+key.replace("_", " ")+': '+value.replace("'","\\'")+'</span>\')')
            exec(label+'.setStyleSheet("padding-left :10px")')
            exec(label+'.setWordWrap(True)')
            exec('layout.addWidget('+label+', alignment=(Qt.AlignTop))')  

        self.label_instudiotitle = QLabel(self)
        self.label_instudiotitle.setText('<span style="font-size:20px;">Upcoming In-Studios</span>')
        self.label_instudiotitle.setStyleSheet("padding-left :5px")
        layout.addWidget(self.label_instudiotitle, alignment=(Qt.AlignTop))

        self.label_instudio = QLabel(self)
        self.label_instudio.setText('<span style="font-size:14px;">'+in_studios+'</span>')
        self.label_instudio.setStyleSheet("padding-left :10px")
        self.label_instudio.setTextInteractionFlags(Qt.TextSelectableByMouse)     
        self.label_instudio.setWordWrap(True)
        layout.addWidget(self.label_instudio, alignment=(Qt.AlignTop))

        self.label_showstitle = QLabel(self)
        self.label_showstitle.setText('<span style="font-size:20px;">WA & OR Shows</span>')
        self.label_showstitle.setStyleSheet("padding-left :5px")
        layout.addWidget(self.label_showstitle, alignment=(Qt.AlignTop))

        self.label_shows = QLabel(self)
        self.label_shows.setText('<span style="font-size:14px;">'+shows+'</span>')
        self.label_shows.setStyleSheet("padding-left :10px")
        self.label_shows.setTextInteractionFlags(Qt.TextSelectableByMouse)     
        self.label_shows.setWordWrap(True)
        layout.addWidget(self.label_shows, alignment=(Qt.AlignTop))

        self.label_videotitle = QLabel(self)
        self.label_videotitle.setText('<span style="font-size:20px;">KEXP YouTube</span>')
        self.label_videotitle.setStyleSheet("padding-left :5px")
        layout.addWidget(self.label_videotitle, alignment=(Qt.AlignTop))

        self.label_video = QLabel(self)
        self.label_video.setText('<span style="font-size:14px;">'+videos+'</span>')
        self.label_video.setStyleSheet("padding-left :10px")
        self.label_video.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_video.setWordWrap(True)
        layout.addWidget(self.label_video, alignment=(Qt.AlignTop))

        # Set the layout on the application's window
        layout.addStretch()
        self.setLayout(layout)


    def on_click(self):
        current_play = k.get_playlist()
        if current_play['artist'] != 'airbreak':
            in_studios = k.get_instudios(current_play['artist'])
            shows = k.get_shows(current_play['artist'])
            videos = k.get_youtube(current_play['artist'])
            if current_play['release_date'] is not None:
                anni = k.get_anniversary(current_play['release_date'])
                current_play['anniversary'] = anni

            for key, value in current_play.items():
                if value == None:
                    value = 'None'
                label = 'self.'+key
                exec(label+'.setText(\'<span style="font-size:14px;">'+key.replace("_", " ")+': '+value.replace("'","\\'")+'</span>\')')
                exec(label+'.adjustSize()')

        elif current_play['artist'] == 'airbreak':
            in_studios = 'N/A'
            shows = 'N/A'
            videos = 'N/A'
            current_play['aniversary'] = 'N/A'
        
        self.label_instudio.setText('<span style="font-size:14px;">'+in_studios+'</span>')
        self.label_instudio.adjustSize()

        self.label_shows.setText('<span style="font-size:14px;">'+shows+'</span>')
        self.label_shows.adjustSize()

        self.label_video.setText('<span style="font-size:14px;">'+videos+'</span>')
        self.label_video.adjustSize()
           


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Window()

    window.show()

    sys.exit(app.exec_())