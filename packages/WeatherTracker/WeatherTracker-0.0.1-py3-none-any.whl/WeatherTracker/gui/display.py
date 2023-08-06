import os
import sys
import json
import numpy as np
import pandas as pd
import qdarktheme
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from pyqtgraph import PlotWidget, plot
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import QSize, QFile, QTextStream
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QMessageBox, QComboBox, QApplication, \
    QVBoxLayout, QPushButton, QCheckBox, QApplication
from WeatherTracker import ROOT_PATH
from WeatherTracker.functions.movmean import movmean


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.degree_sign = u'\N{DEGREE SIGN}'

        # Window
        width = 1000
        height = 1000
        pad = 100
        self.setMinimumSize(QSize(width, height))
        self.setWindowTitle("Weather Display")

        # Plot
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.graphWidget.resize(width-2*pad, height-2*pad)
        # self.graphWidget.move(pad, pad)
        self.read_data()
        self.graphWidget.plot(np.arange(len(self.df1['datetime'])),
                              movmean((self.df1['temperature (K)']-273.15)*9/5+32, N=5), color=(255, 0, 0))
        self.graphWidget.plot(np.arange(len(self.df2['datetime'])),
                              movmean((self.df2['temperature (K)']-273.15)*9/5+32, N=5), color=(0, 255, 0))
        self.graphWidget.setLabel('left', f'Temperature ({self.degree_sign}C)')
        self.graphWidget.setLabel('bottom', 'Time Point')

    def read_data(self):
        self.df1 = pd.read_csv(os.path.join(ROOT_PATH, 'data', 'Pekin.csv'))
        self.df2 = pd.read_csv(os.path.join(ROOT_PATH, 'data', 'Urbana.csv'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarktheme.load_stylesheet())
    w = MainWindow()
    w.show()
    app.exec_()
