from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
import sys as _s
import download_python as dp
import download_reqs as dr

class DownloadReqsThread(QObject):
    drt_signal = pyqtSignal(int,str)

    def __init__(self):
        super().__init__()
        self.x = 0
    
    def start_drt(self):
        flag = True
        unbound_flag = False
        called = False
        self.command_array = []

        if called == False:
            try:
                install_reqs_module_class = dr.installPythonPackages()
                install_reqs_module = install_reqs_module_class.installPKGS()
                print(install_reqs_module_class.proces_out)

            except Exception as e0fx0:
                print(12,e0fx0)
                try:
                    install_reqs_module_class.proces_out == None
                
                except UnboundLocalError as err:
                    unbound_flag = True
                    print('unbound',err)

            finally:
                if unbound_flag == False:
                    if install_reqs_module_class.proces_out is not None:
                        for command_output in install_reqs_module_class.proces_out.stdout:
                            self.command_array.append(command_output)
                            self.drt_signal.emit(1,f'\n'.join(self.command_array))
                    


class DownloadPythonThread(QObject):
    dpt_signal = pyqtSignal(int,str)

    def __init__(self,bcount):
        super().__init__()
        self.bitcount = bcount
        self.x32_path = r'setup_system\python-3.11.0.exe'
        self.x64_path = r'setup_system\python-3.11.0-amd64.exe'

    def start_dpt(self):
        self.python_installer_module = dp.mixinClass(self.bitcount,
                                                     self.x32_path,
                                                     self.x64_path)

        flag = True

        while flag:
            if self.python_installer_module is not None:
                flag = False
                print(self.python_installer_module)
                print('completed')
                
                try:
                    import subprocess as sbp
                    sbp.Popen(['python','gui.py'])
                
                except Exception as e0fxl:
                    print(e0fxl)

                self.dpt_signal.emit(1,'x')
            
            else:
                pass


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        
        '''STATES'''
        #*//

        '''THREADS'''
        self.python_installer_thread_class = DownloadPythonThread(0)
        self.python_installer_thread = QThread(self)
        self.python_installer_thread_class.moveToThread(self.python_installer_thread)
        self.dpt_signal = self.python_installer_thread_class.dpt_signal

        self.reqs_installer_thread_class = DownloadReqsThread()
        self.reqs_installer_thread = QThread(self)
        self.reqs_installer_thread_class.moveToThread(self.reqs_installer_thread)
        self.drt_signal = self.reqs_installer_thread_class.drt_signal

        '''WIDGETS'''
        self.main_label = QLabel(text='Plant Disease Project Kurulum Yardımcısı')
        self.main_label.setAlignment(Qt.AlignCenter)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setAlignment(Qt.AlignCenter)

        self.mainbtnx = QPushButton("Setup'ı başlat")

        '''PARENTS'''
        self.main_layout.addWidget(self.main_label)
        self.main_layout.addWidget(self.text_edit)
        self.main_layout.addWidget(self.mainbtnx)

        '''SIGNALS'''
        self.mainbtnx.clicked.connect(self.installPythonIgniter)

        '''MAIN-WIDGET'''
        self.setCentralWidget(self.main_widget)

    def installPythonIgniter(self):
        dockwidget = QDockWidget(self)
        docklayout = QVBoxLayout()
        dockwidget_mainw = QWidget()

        self.labelX_dynamic = QLabel('Bit sayınızı seçin')
        self.combobox = QComboBox()
        self.btn_dynamic = QPushButton('Başla')

        for bitcountfX in ['64','32']:
            self.combobox.addItem(bitcountfX)

        docklayout.addWidget(self.labelX_dynamic)
        docklayout.addWidget(self.combobox)
        docklayout.addWidget(self.btn_dynamic)

        dockwidget_mainw.setLayout(docklayout)
        dockwidget.setWidget(dockwidget_mainw)

        self.btn_dynamic.clicked.connect(lambda : self.ip1i_igniter(int(self.combobox.currentText())))
        self.reqs_installer_thread_class.drt_signal.connect(self.ip2i_igniter)

        dockwidget.show()

    def installPackagesIgniter(self):
        pass

    def ip1i_igniter(self,bitcount):
        self.python_installer_thread_class = DownloadPythonThread(bitcount)
        self.python_installer_thread = QThread(self)
        self.python_installer_thread_class.moveToThread(self.python_installer_thread)
        self.dpt_signal = self.python_installer_thread_class.dpt_signal
        self.dpt_signal.connect(self.ip2i_igniter)
        
        self.python_installer_thread.started.connect(self.python_installer_thread_class.start_dpt)
        self.python_installer_thread.start()

    def ip2i_igniter(self,state,command):
        if state == 1:
            self.reqs_installer_thread_class = DownloadReqsThread()
            self.reqs_installer_thread = QThread(self)
            self.reqs_installer_thread_class.moveToThread(self.python_installer_thread)
            self.drt_signal = self.reqs_installer_thread_class.drt_signal
            self.drt_signal.connect(self.ip2i_receiver)
            
            self.reqs_installer_thread.started.connect(self.reqs_installer_thread_class.start_drt)
            self.reqs_installer_thread.start()

            print(command)
    
    def ip2i_receiver(self,state,outs):
        if state == 1:
            self.text_edit.clear()
            self.text_edit.setText(outs)
            self.text_edit.moveCursor(QTextCursor().End)
        
        else:
            if state == 0:
                print(0,outs)

if __name__ == "__main__":
    sp = QApplication(_s.argv)
    sw = mainWindow()
    sw.show()
    _s.exit(sp.exec_())
