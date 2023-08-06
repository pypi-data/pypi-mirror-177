import sys
import time
import random
import numpy as np
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
# noinspection PyUnresolvedReferences
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class Animator_View(QtWidgets.QWidget):

    def __init__(self, debug=True):
        super(Animator_View, self).__init__()

        self.weight = 0.5
        self.ibas = random.random()

        self.I = 10
        self.V = 6
        self.R = 0

        self.I_set = []
        self.V_set = []
        self.R_set = []

        self.setWindowTitle("Live Data Plot V0.0.1")
        layout = QtWidgets.QGridLayout(self)

        # define widget
        self.Real_Time_Info = QtWidgets.QLabel("I = Unknown\n"
                                          "U = Unknown\n"
                                          "R = Unknown\n"
                                          )
        self.Real_Time_Info.setFont(QFont("Consolas", 16, QFont.Bold))
        # self.Real_Time_Info.setMargin(80)
        self.Real_Time_Info.setFixedSize(300,80)
        Current_Canvas = FigureCanvas(Figure(figsize=(5, 3)).set_tight_layout(True))
        Voltage_Canvas = FigureCanvas(Figure(figsize=(5, 3)).set_tight_layout(True))
        Resistance_Canvas = FigureCanvas(Figure(figsize=(5, 3)))

        layout.addWidget(self.Real_Time_Info, 1, 1)
        layout.addWidget(Current_Canvas, 1, 2)
        layout.addWidget(Voltage_Canvas, 1, 3)
        layout.addWidget(Resistance_Canvas, 2, 1, 1, -1)
        layout.addWidget(NavigationToolbar(Resistance_Canvas, self), 3, 1, 1, -1)

        self.Current_Canvas_Fig = Current_Canvas.figure.subplots()
        self.Current_Canvas_Fig.set_ylim(5, 15)
        self.Current_Canvas_Fig.set_title("Current-Time")
        self.Current_Canvas_Fig.set_xlabel("Time(s)")
        self.Current_Canvas_Fig.set_ylabel("I(A)")
        # self.Current_Canvas_Fig.set_tight_layout(tight)[source]

        self.Voltage_Canvas_Fig = Voltage_Canvas.figure.subplots()
        self.Voltage_Canvas_Fig.set_ylim(0, 10)
        self.Voltage_Canvas_Fig.set_title("Voltage-Time")
        self.Voltage_Canvas_Fig.set_xlabel("Time(s)")
        self.Voltage_Canvas_Fig.set_ylabel("U(V)")

        self.Resistance_Canvas_Fig = Resistance_Canvas.figure.subplots()
        self.Resistance_Canvas_Fig.set_ylim(0.2, 0.8)
        self.Resistance_Canvas_Fig.set_title("Resistance-Time")
        self.Resistance_Canvas_Fig.set_xlabel("Time(s)")
        self.Resistance_Canvas_Fig.set_ylabel("R(Ω)")

        # debug ON
        if debug:
            # display Debug Mode ON
            Debug_State = QtWidgets.QLabel("Debug Mode ON", self)
            Debug_State.setGeometry(0, 0, 1000, 80)
            Debug_State.setFont(QFont("Consolas", 30, QFont.Bold))
            Debug_State.setStyleSheet("color:red")

            self.setWindowTitle("[Debug Mode]Live Data Plot V0.0.1")

            # self.debug()
        else:
            pass

        t = np.linspace(0, 10, 101)
        for k in range(101):
            self.I = self.I + random.random()
            self.V = self.V + random.random()
            self.I_set.append(self.I)
            self.V_set.append(self.V)
            self.R = self.V / self.I
            self.R_set.append(self.R)

        self._line, = self.Current_Canvas_Fig.plot(t, self.I_set)
        self._timer = Current_Canvas.new_timer(50)
        self._timer.add_callback(self._update_canvas)
        self._timer.start()

        # self._Current_Canvas_Fig, = self.Current_Canvas_Fig.plot(t, self.I_set)
        # self._Ctimer = Current_Canvas.new_timer(50)
        self._Voltage_Canvas_Fig, = self.Voltage_Canvas_Fig.plot(t, self.V_set)
        self._Vtimer = Voltage_Canvas.new_timer(50)
        self._Vtimer.start()
        self._Resistance_Canvas_Fig, = self.Resistance_Canvas_Fig.plot(t, self.R_set)
        self._Rtimer = Resistance_Canvas.new_timer(50)

        # self._Ctimer.add_callback(self._update_canvas)
        # self._Ctimer.start()
        # self._Vtimer.add_callback(self._update_canvas)
        # self._Vtimer.start()
        # self._Rtimer.add_callback(self._update_canvas)
        # self._Rtimer.start()

    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        self.I_set = []
        self.V_set = []
        self.R_set = []
        for k in range(101):
            self.I = 10
            self.V = 6
            self.R = 0
            self.I = self.I + random.random()
            self.V = self.V + random.random()
            self.I_set.append(self.I)
            self.V_set.append(self.V)
            self.R = self.V / self.I
            self.R_set.append(self.R)
            self.Real_Time_Info.setText(f"I(A) = {round(self.I,5)}\n"
                                          f"U(V) = {round(self.V,5)}\n"
                                          f"R(Ω) = {round(self.R,5)}\n")
        self._line.set_data(t, self.I_set)
        self._line.figure.canvas.draw()
        # self._Current_Canvas_Fig.set_data(t, self.I_set)
        self._Voltage_Canvas_Fig.set_data(t, self.V_set)
        self._Resistance_Canvas_Fig.set_data(t, self.R_set)
        # self._Current_Canvas_Fig.figure.canvas.draw()
        self._Voltage_Canvas_Fig.figure.canvas.draw()
        self._Resistance_Canvas_Fig.figure.canvas.draw()

    def debug(self, I=10):
        weight = 0.5
        ibas = random.random()
        self.I = self.I + random.random()
        self.V = weight * self.I + ibas
        self.R = self.V / self.I


if __name__ == "__main__":
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = Animator_View()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()
