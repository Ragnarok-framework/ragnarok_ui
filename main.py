import sys
import os
import json
from PySide2 import *
from PyQt5 import QtCore, QtGui, QtWidgets

# IMPORT GUI FILE
sys.path.insert(0, './ui_src')
sys.path.insert(1, '../ragnarok_probes/ragnarok_probes/')
sys.path.insert(2, '../ragnarok_server/ragnarok_server/modules/')

# IMPORT SCANNER RESOURCES
from ui_interface import *
from netscan import Netscan
from port_finder import PortFinder


class MainWindow(QtWidgets.QMainWindow):
    """ MAIN WINDOW CLASS """
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Remove window tittle bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Set main background to transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Shadow effect style
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 92, 157, 550))

        # Apply shadow to central widget
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        # Set window Icon
        # This icon and title will not appear on our app main window because we removed the title bar
        self.setWindowIcon(QtGui.QIcon(":/icons/icons/github.svg"))
        # Set window tittle
        self.setWindowTitle("RAGNAROK")

        # Window Size grip to resize window
        QtWidgets.QSizeGrip(self.ui.size_grip)



        #Minimize window
        self.ui.minimize_window_button.clicked.connect(lambda: self.showMinimized())


        #Close window
        self.ui.close_window_button.clicked.connect(lambda: self.close())
        self.ui.exit_button.clicked.connect(lambda: self.close())


        #Restore/Maximize window
        self.ui.restore_window_button.clicked.connect(lambda: self.restore_or_maximize_window())

        # Adding Hyperlink
        self.ui.pushButton_10.clicked.connect(lambda: self.link("https://github.com/Ragnarok-framework/ragnarok_ui"))
        self.ui.pushButton_11.clicked.connect(lambda: self.link("https://github.com/Ragnarok-framework/ragnarok_probes"))
        self.ui.pushButton_12.clicked.connect(lambda: self.link("https://github.com/Ragnarok-framework"))
        self.ui.pushButton_13.clicked.connect(lambda: self.link("https://wiki.python.org/moin/PyQt"))
        self.ui.pushButton_14.clicked.connect(lambda: self.link("https://pypi.org/project/PlugyPy/"))
        self.ui.report_gen_button.clicked.connect(lambda: self.link("http://localhost:8000/report.html"))

        # Initiate Report Generator
        self.ui.generator.clicked.connect(lambda: self.generateReport())

        def moveWindow(e):
            """ Function to Move window on mouse drag event on the tittle bar """

            # Detect if the window is  normal size
            if self.isMaximized() == False: #Not maximized
                # Move window only when window is normal size
                # if left mouse button is clicked (Only accept left mouse button clicks)
                if e.buttons() == QtCore.Qt.LeftButton:
                    #Move window
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()

        # Add click event/Mouse move event/drag event to the top header to move the window
        self.ui.header_frame.mouseMoveEvent = moveWindow

        #Left Menu toggle button
        self.ui.open_close_side_bar_btn.clicked.connect(lambda: self.slideLeftMenu())


        self.show()

    def link(self, linkStr):
        """ Hyperlink adding function """

        # Open an url
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(linkStr))


    def slideLeftMenu(self):
        """ Slide left menu function """

        # Get current left menu width
        width = self.ui.slide_menu_container.width()

        # If minimized
        if width == 0:
            # Expand menu
            newWidth = 200
            self.ui.open_close_side_bar_btn.setIcon(QtGui.QIcon(u":/icons/icons/chevron-left.svg"))
        # If maximized
        else:
            # Restore menu
            newWidth = 0
            self.ui.open_close_side_bar_btn.setIcon(QtGui.QIcon(u":/icons/icons/align-left.svg"))

        # Animate the transition
        self.animation = QtCore.QPropertyAnimation(self.ui.slide_menu_container, b"maximumWidth")#Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)#Start value is the current menu width
        self.animation.setEndValue(newWidth)#end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()


    def mousePressEvent(self, event):
        """ Add mouse events to the window """

        # Get the current position of the mouse
        self.clickPosition = event.globalPos()

    def generateReport(self):
        """ Generate a report """

        IP = str(self.ui.textEdit.toPlainText())
        ports = [ p for p in range(21, 81)]
        process = str(self.ui.textEdit.toPlainText())
        value = {
        "IP":IP,
        "Open_Ports": PortFinder().main(IP,ports),
        "Mac_Address": Netscan().scan(IP),
        "Vendor":Netscan().mac_vendor(),
        "Background_Process": ProcessChecker(process)
        }
        jsonString = json.dumps(value)
        sys.path.insert(3, './web_results/json')
        jsonFile = open("results.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()

    def restore_or_maximize_window(self):
        """ Update restore button icon on maximizing or minimizing window """

        # If window is maxmized
        if self.isMaximized():
            self.showNormal()
            # Change Icon
            self.ui.restore_window_button.setIcon(QtGui.QIcon(u":/icons/icons/maximize-2.svg"))
        else:
            self.showMaximized()
            # Change Icon
            self.ui.restore_window_button.setIcon(QtGui.QIcon(u":/icons/icons/minimize-2.svg"))

## START APP
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
