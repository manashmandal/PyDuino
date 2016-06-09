from PyQt4 import uic
from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox
import sys
from PyQt4.QtGui import QApplication

# import pyserial library
import serial
from serial.tools import list_ports

PyDuinoDialog, PyDuinoClass = uic.loadUiType('ui_pyduino.ui')

class PyDuino(PyDuinoDialog, QtGui.QDialog):

    def __init__(self):
        PyDuinoDialog.__init__(self)
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        # baud rate list
        self.bauds = ['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200']

        # Initializing com ports
        for device in list_ports.comports():
            self.COMComboBox.addItem(device.device)

        # adding the bauds
        for baud in self.bauds:
            self.BaudComboBox.addItem(str(baud))

        self.BaudComboBox.currentIndexChanged.connect(self.set_baudrate)
        self.RefreshButton.clicked.connect(self.refresh_com_ports)

        # When COM Port is selected
        self.COMComboBox.currentIndexChanged.connect(self.set_com_port)

        # When connect button is clicked
        self.ConnectButton.clicked.connect(self.connect_arduino)

        self.DisconnectButton.setEnabled(False)
        self.DisconnectButton.clicked.connect(self.disconnect_arduino)

        # when description button is clicked show a dialog
        self.DescriptionButton.clicked.connect(self.show_description)

        # when clicked ON Button sends a string
        self.ONButton.clicked.connect(self.send_on_command)
        self.OFFButton.clicked.connect(self.send_off_command)
        self.SendButton.clicked.connect(self.send_command)

        self.ClearInputButton.clicked.connect(self.clear_input)

    # refreshes the port list
    def refresh_com_ports(self):
        self.COMComboBox.clear()
        for device in list_ports.comports():
            self.COMComboBox.addItem(device.device)

    def set_com_port(self):
        self.current_port = self.COMComboBox.currentText()

    # connects
    def connect_arduino(self):
        self.ConnectButton.setEnabled(False)
        self.DisconnectButton.setEnabled(True)
        self.set_com_port()
        self.arduino = serial.Serial(str(self.current_port))
        self.arduino.baudrate = int(self.baudrate)
        self.arduino.close()
        self.arduino.open()

    def disconnect_arduino(self):
        self.DisconnectButton.setEnabled(False)
        self.arduino.close()
        self.ConnectButton.setEnabled(True)

    def set_baudrate(self, index):
        self.baudrate = str(self.BaudComboBox.currentText())
        print self.baudrate

    def show_description(self):
        self.port_description = ''
        for device in list_ports.comports():
            if device.device == str(self.COMComboBox.currentText()):
                self.port_description = device.description
        self.message_box = QMessageBox()
        self.message_box.setWindowTitle('About Selected Port')
        self.message_box.setText(self.port_description)
        self.message_box.setIcon(QMessageBox.Information)
        self.message_box.show()

    def send_on_command(self):
        if (self.arduino.is_open):
            self.arduino.write('on\n')
            if (self.ReadEnableCheckBox.isChecked()):
                self.ReadTextEdit.append(self.arduino.readline())

    def send_off_command(self):
        if (self.arduino.is_open):
            self.arduino.write('off\n')
            if (self.ReadEnableCheckBox.isChecked()):
                self.ReadTextEdit.append(self.arduino.readline())

    def send_command(self):
        if (self.arduino.is_open):
            self.text = str(self.CommandLineEdit.text()) + '\n'
            self.arduino.write(self.text)
            if (self.ReadEnableCheckBox.isChecked()):
                self.ReadTextEdit.append(self.arduino.readline())
            self.CommandLineEdit.clear()

    def clear_input(self):
        self.ReadTextEdit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pyduino = PyDuino()
    pyduino.show()
    sys.exit(app.exec_())

