#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import QWidget, QFileDialog

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import matplotlib.colors as mcolors

import random


# Given header line, parse headers
def get_headers(line):
    headers = {}
    tokens = line.strip().split('\t')
    for i in range(1, len(tokens)):
        headers.update({i: tokens[i]})
    return headers


# Given a file of Collateral Sensitivity scores matrix, return drugs, resistant strains, and edge scores
def get_edges(matrix_file):
    headers = {}
    strain_list = []
    edge_list = []


    ab4heat = []
    reader = open(matrix_file, 'r')
    for line in reader:
        if line.find('*\t') == 0:
            headers = get_headers(line)
            continue

        tokens = line.strip().split('\t')
        strain_res = tokens[0]
        ab = [ int(tokens[i]) for i in range(1,len(tokens)) ]
        ab4heat.append(ab)
        strain_list.append(strain_res)
        for i in range(1, len(tokens)):
            drug = headers[i]
            value = int(tokens[i])
            edge_list.append((strain_res, drug, value))

    return headers.values(), strain_list, edge_list, ab4heat


class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.file = 'matrix_data.txt'

        # Just some button connected to `plot` method
        self.button = QtGui.QPushButton('Plot')
        self.fileOpen = QtGui.QPushButton('file')

        self.combobox = QtGui.QComboBox(self)

        self.create_combo()

        self.button.clicked.connect(self.plot)
        self.fileOpen.clicked.connect(self.getfile)

        # set the layout

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.combobox)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addWidget(self.fileOpen)

        self.setLayout(layout)

    def getfile(self):
        self.file = QFileDialog.getOpenFileName(QWidget(), 'Open File', '/')
        self.create_combo()

    def plot(self):


        os.system("python HealthHack.py %s %s" % (self.file, str(self.combobox.currentText())))

    def create_combo(self):
        # string_list = QtCore.QStringList(self.s_list)
        d_list, s_list, e_list, ab4heat = get_edges(self.file)
        self.combobox.clear()
        self.figure.clear()
        self.combobox.addItems(s_list)

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph


        ax.set_xticks(range(len(s_list)), minor=False)
        ax.set_yticks(range(len(d_list)), minor= False)
        ax.set_xticklabels(d_list, minor=False, rotation='vertical')
        ax.set_yticklabels(s_list, minor=False)
        ax.set_xlabel("Drug")
        ax.set_ylabel("Strain Resistance")


        # plot data
        #pos_colors = plt.cm.binary([0.1,2,4,8,16,32])
        #neg_colors = plt.cm.binary([-8,-4,-2,0])
        #all_colors = np.vstack((neg_colors,pos_colors))
        #map = mcolors.LinearSegmentedColorMap.from_list('my_colormap',all_colors)
        cax = ax.imshow(ab4heat,cmap='RdBu_r',vmax=16.1,vmin=-16.1)
        self.figure.colorbar(cax,ticks=[-8,-4,-2,0,2,4,8,16,32]) #boundaries=[-8,-4,-2,0,2,4,8,16,32]
        ax.set_title(self.file)


        # refresh canvas
        self.canvas.draw()


        return


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
