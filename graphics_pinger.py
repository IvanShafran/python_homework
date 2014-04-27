import sys
from PySide import QtGui
import os
import queue
from threading import Thread

class ThreadNumberLayout(QtGui.QHBoxLayout):
    def __init__(self):
        super(ThreadNumberLayout, self).__init__()
        self.InitLayout()

    def GetNumberOfThreads(self):
        return int(self.label_number_of_threads.text())

    def Decrease(self):
        self.label_number_of_threads.setText(str(max(1, int(self.label_number_of_threads.text()) - 1)))

    def Increase(self):
        self.label_number_of_threads.setText(str(min(20, int(self.label_number_of_threads.text()) + 1)))

    def InitLayout(self):
        self.label_number_of_threads = QtGui.QLabel("3")
        self.less_button = QtGui.QPushButton("--")
        self.less_button.clicked.connect(self.Decrease)
        self.more_button = QtGui.QPushButton("++")
        self.more_button.clicked.connect(self.Increase)
        self.addWidget(self.less_button)
        self.addWidget(self.label_number_of_threads)
        self.addWidget(self.more_button)


class Pinger(QtGui.QWidget):
    def __init__(self):
        super(Pinger, self).__init__()
        self.PingerInit()

    def Ping(self, ipaddress):
        return 0 == os.system("ping " + ipaddress)

    def check_ipaddress(self, ipaddress_queue):
        while not ipaddress_queue.empty():
            ipaddress = ipaddress_queue.get_nowait()
            if self.Ping(ipaddress):
                self.text_edit_after.insertPlainText(ipaddress + '\n')
            ipaddress_queue.task_done()

    def PingButtonClick(self):
        number_of_threads = self.thread_layout.GetNumberOfThreads()
        ipaddress_queue = queue.Queue()
        for ipaddress in self.text_edit_before.toPlainText().split():
            ipaddress_queue.put_nowait(ipaddress)

        for x in range(number_of_threads):
            thread = Thread(target=self.check_ipaddress, args=(ipaddress_queue, ))
            thread.daemon = False
            thread.start()

    def PingerInit(self):
        self.label_before = QtGui.QLabel("Enter a list of addresses")
        self.text_edit_before = QtGui.QTextEdit()
        self.label_after = QtGui.QLabel("Result of ping")
        self.text_edit_after = QtGui.QTextEdit()
        self.ping_button = QtGui.QPushButton("Ping")
        self.ping_button.clicked.connect(self.PingButtonClick)
        self.label_enter_number_of_threads = QtGui.QLabel("Enter a number of threads")

        self.thread_layout = ThreadNumberLayout()

        main_box = QtGui.QVBoxLayout()
        main_box.addWidget(self.label_before)
        main_box.addWidget(self.text_edit_before)
        main_box.addWidget(self.label_enter_number_of_threads)
        main_box.addLayout(self.thread_layout)
        main_box.addWidget(self.ping_button)
        main_box.addWidget(self.label_after)
        main_box.addWidget(self.text_edit_after)
        self.setLayout(main_box)

        self.setGeometry(300, 300, 200, 300)
        self.setWindowTitle('Pinger v0.1')
        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Pinger()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
