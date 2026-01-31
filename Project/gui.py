'''31.01.2026 / 20:21:45'''

import os

import artifical_intelligence
import artifical_intelligence as ai_side
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvasQT
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbarQT
import matplotlib.pyplot as plt
import winsound as ws
import sys as _s
import asyncio
from random import randint
import numpy as np

import file_actions
import image_processing as ip_side
import file_actions as tdg
import datetime as dt
import threading 
import logPlotter
import evaulateLogPlotter

class PlotterThreadSide(QObject):
    returner_signal = pyqtSignal(int, int, dict, str, int)
    returner_signal_e = pyqtSignal(list,list)
    renderer_signal = pyqtBoundSignal(str,int)

    def __init__(self,path,mode):
        super().__init__()

        self.mode = mode
        self.path = path
        self.main_gen = None
        self.nrow_gen = None
        self.ncol_gen = None
        self.dict_gen = None
        self.str_gen = None

        self.nrow_e = None
        self.ncol_e = None
        self.accs_e = None
        self.losses_e = None
        self.keys_e = None
        

    def referanceFlow(self):
        if self.mode == 0:
            self.main_gen = logPlotter.Plotter().plotter(self.path)

        elif self.mode == 1:
            self.main_gen = evaulateLogPlotter.LoggPlotterEvaulate(self.path).plotLog()

        if self.main_gen is not None:
            if self.mode == 0:
                for gen in self.main_gen:
                    self.nrow_gen,self.ncol_gen,self.dict_gen,self.str_gen = gen
                    self.returner_signal.emit(self.nrow_gen,self.ncol_gen,self.dict_gen,self.str_gen,self.mode)

            
            if self.mode == 1:  #MODE-1 KISMINDA GENERAOTOR MATRİX TANIMLANDİ MODE-1 DE GENERATOR MEVCUT DEGİL MATRİX FORMATLI UNPACKİNG YAPILDI
                self.losses_e,self.accs_e,self.keys_e = self.main_gen #MATRİX   
                self.returner_signal_e.emit(self.losses_e,self.accs_e)

        else:
            print(self.mode)


class ThreadSide(QObject):
    ifilesignal = pyqtSignal(str, int)
    efilesignal = pyqtSignal(str, int)

    def __init__(self, internals, externals):
        super().__init__()
        self.internal_fs, self.external_fs = internals, externals

    async def emitInternals(self):
        for internal_file in self.internal_fs:
            # if isinstance(internal_file,str) and internal_file.endswith('.h5'):
            self.ifilesignal.emit(internal_file, 0)

    async def emitExternals(self):
        for external_file in self.external_fs:
            # if isinstance(external_file,str) and external_file.endswith('.h5'):
            self.efilesignal.emit(external_file, 1)

    async def igniter(self):
        await asyncio.gather(self.emitInternals(), self.emitExternals())

    def mainIgniter(self):
        if self.internal_fs and self.internal_fs:
            asyncio.run(self.igniter())


class MainGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabWidget = QTabWidget()
        '''THREADS'''
        self.threadPool = ThreadSide([],[])
        self.threadObject = QThread(self)
        self.threadPool.moveToThread(self.threadObject)

        self.plotter_threadF = QThread(self)
        self.plotter_classF = PlotterThreadSide(None,None)
        self.plotter_classF.moveToThread(self.plotter_threadF)

        '''SIGNALS'''
        self.ifilesignal = self.threadPool.ifilesignal
        self.efilesignal = self.threadPool.efilesignal
        self.returner_signal = self.plotter_classF.returner_signal
        self.returner_signal_e = self.plotter_classF.returner_signal_e
        self.renderer_signal = self.plotter_classF.renderer_signal

        '''ANA DEGİSKENLER'''
        self.curr_selected = []
        self.batch_arr = []
        self.curr_img_name = []

        self.col = 0
        self.pred = str

        batch = 4
        for xQ in range(6):
            self.batch_arr.append(batch)
            batch *= 2

        self.current_canvas_matrix = None
        self.current_selected_canvas = None

        self.IPath, self.IName, self.IType = None, None, None
        self.EPath, self.EName, self.EType = None, None, None

        '''GÖRSEL İSLEYİCİ'''
        self.image_processer = ip_side.İmageProcesser()

        '''WİDGET TANIMLARI'''
        widget_main = QWidget()  # görsel girdi sistemi
        widget_second = QWidget()  # model bilgileri
        widget_finally = QWidget()  # model eğitimi

        layout_main = QHBoxLayout()
        layout_second = QHBoxLayout()
        layout_finally = QVBoxLayout()
        tab_layout = QVBoxLayout()

        horizontal_splitter_main = QSplitter(Qt.Horizontal)  # 3x main split side     #h3x-1

        vertical_splitter_main = QSplitter(Qt.Vertical)  # 1x split side              #v1x-1
        vertical_splitter_second = QSplitter(Qt.Vertical)  # 1x1*1x1 split side       #v4x-1
        vertical_splitter_last = QSplitter(Qt.Vertical)  # 1x split side              #v1x-2

        vertical_splt_sec_v4x1_1_horizontal_splitter_1 = QSplitter(Qt.Horizontal)
        vertical_splt_sec_v4x1_1_vertical_splitter_1 = QSplitter(Qt.Vertical)
        vertical_splt_sec_v4x1_1_vertical_splitter_2 = QSplitter(Qt.Vertical)

        self.table_widget_splitter = QSplitter(Qt.Vertical)

        vertical_splt_sec_v4x1_1_horizontal_splitter_1.addWidget(vertical_splt_sec_v4x1_1_vertical_splitter_1)
        vertical_splt_sec_v4x1_1_horizontal_splitter_1.addWidget(vertical_splt_sec_v4x1_1_vertical_splitter_2)

        horizontal_splitter_main.addWidget(vertical_splitter_main)
        horizontal_splitter_main.addWidget(vertical_splitter_second)
        horizontal_splitter_main.addWidget(vertical_splitter_last)

        canvases_splitter = QSplitter(Qt.Vertical)

        '''ETİKETLER'''
        self.l1, self.l2, self.l3 = QLabel(text='Dahili Model Seçme Sistemi'), QLabel(
            text='Model Eğitim Penceresi'), QLabel(text='Harici Model Seçme Sistemi')
        self.internal_model_selecet_label = QLabel(text='Dahili Model seçme Sistemi Ayarı')
        self.external_model_select_label = QLabel(text='Harici Model Seçme Sistemi Ayarı')
        self.model_inspecting_monitor_label = QLabel(text='Model İnceleme Monitörü')
        self.model_inspect_preview_label = QLabel(
            text='Model adı: Bilinmiyor\nModel yolu: Bilinmiyor\nModel türü: Bilinmiyor')
        self.model_techinc_informations_label = QLabel(text='Modelin Teknik Detayları')
        self.file_sys_external_path_label = QLabel(text='Harici Dosya Sistemi Yolu')
        self.file_sys_internal_path_label = QLabel(text='Dahili Dosya Sistemi Yolu')

        self.l1.setAlignment(Qt.AlignCenter)
        self.l2.setAlignment(Qt.AlignCenter)
        self.l3.setAlignment(Qt.AlignCenter)

        self.internal_model_selecet_label.setAlignment(Qt.AlignCenter)
        self.external_model_select_label.setAlignment(Qt.AlignCenter)
        self.model_inspecting_monitor_label.setAlignment(Qt.AlignCenter)
        self.model_inspect_preview_label.setAlignment(Qt.AlignCenter)
        self.model_techinc_informations_label.setAlignment(Qt.AlignCenter)
        self.file_sys_external_path_label.setAlignment(Qt.AlignCenter)
        self.file_sys_internal_path_label.setAlignment(Qt.AlignCenter)

        '''BUTONLAR'''
        self.define_internal_model_btn = QPushButton(text='Dahili modeli tanımla')
        self.inspect_internal_model_btn = QPushButton(text='Dahili modeli incele')

        self.define_external_model_btn = QPushButton(text='Harici modeli tanımla')
        self.inspect_external_model_btn = QPushButton(text='Harici modeli incele')
        self.define_external_file_system_path = QPushButton(text='Dosya sistemi yolunu tanımla')

        self.define_all_models_btn = QPushButton(text='Modelleri tanımla')
        self.clear_all_models_btn = QPushButton(text='Model listesini temizle')

        self.reset_internal_path = QPushButton('Dahili Yolu Sıfırla')
        self.reset_external_path = QPushButton('Harici Yolu Sıfırla')

        self.clear_flowers_list = QPushButton('Cicek listesini temizle')

        self.start_analysis = QPushButton('Analizi Başlat')

        '''EKSTRA WİDGETLAR'''
        self.internal_model_file_system_model = QListWidget()
        self.external_model_file_system_model = QListWidget()

        self.modelPredictionTableWidget = QTableWidget()
        self.modelPredictionTableWidget.setColumnCount(16)
        self.modelPredictionTableWidget.setRowCount((5 * 2) * 10)
        self.modelPredictionTableWidget.setMaximumWidth((self.width() // 2))
        self.modelPredictionTableWidget.setHorizontalHeaderLabels(['Model tahmini', 'Tahmin', 'Zaman kodu','Mevcut kanvas','Görsel ismi'])

        self.enter_external_path = QLineEdit()
        self.enter_internal_path = QLineEdit()

        self.target_folder_path = QLineEdit()
        self.target_folder_path.setPlaceholderText('Hedef klasör dizini girin....')

        self.apply_target_path = QPushButton('Hedef klasörü tanımla')

        self.enter_external_path.setPlaceholderText('Harici Modelin Yolunu Girin...')
        self.enter_internal_path.setPlaceholderText('Dahili Modelin Yolunu girin....')
        self.enter_external_path.setText('models/ProgramInterfaceModelsExternal')
        self.enter_internal_path.setText('models/ProgramInterfaceModelsInternal')

        self.change_analysis_mode = QComboBox()
        self.change_model_type = QComboBox()
        self.change_batch_size = QComboBox()

        itemsX, itemsY = ['Hasta-Saglikli Tespiti', 'Hastalik Tespiti'], ['Harici', 'Dahili']
        for itemX, itemY in zip(itemsX, itemsY):
            self.change_analysis_mode.addItem(itemX)
            self.change_model_type.addItem(itemY)

        for batch in self.batch_arr:
            self.change_batch_size.addItem(str(f'Batch büyüklüğü: {batch}'))

        self.model_techinc_informations = QTextEdit()
        self.model_techinc_informations.setReadOnly(True)

        self.internal_gui_widgets = [[self.l1,
                                      self.define_internal_model_btn,
                                      self.inspect_internal_model_btn,
                                      self.internal_model_file_system_model],
                                     [self.l2,
                                      vertical_splt_sec_v4x1_1_horizontal_splitter_1,
                                      self.model_inspecting_monitor_label,
                                      self.model_inspect_preview_label,
                                      self.model_techinc_informations_label,
                                      self.model_techinc_informations,
                                      self.define_all_models_btn,
                                      self.clear_all_models_btn,
                                      ],
                                     [self.l3,
                                      self.define_external_model_btn,
                                      self.inspect_external_model_btn,
                                      self.external_model_file_system_model]]

        vertical_splt_sec_v4x1_1_vertical_splitter_1.addWidget(self.external_model_select_label)
        vertical_splt_sec_v4x1_1_vertical_splitter_1.addWidget(self.enter_external_path)
        vertical_splt_sec_v4x1_1_vertical_splitter_1.addWidget(self.reset_external_path)

        vertical_splt_sec_v4x1_1_vertical_splitter_2.addWidget(self.internal_model_selecet_label)
        vertical_splt_sec_v4x1_1_vertical_splitter_2.addWidget(self.enter_internal_path)
        vertical_splt_sec_v4x1_1_vertical_splitter_2.addWidget(self.reset_internal_path)

        for _ in range(len(self.internal_gui_widgets)):
            if _ == 0:
                for widget in self.internal_gui_widgets[_]:
                    vertical_splitter_main.addWidget(widget)
            elif _ == 1:
                for widget in self.internal_gui_widgets[_]:
                    vertical_splitter_second.addWidget(widget)
            elif _ == 2:
                for widget in self.internal_gui_widgets[_]:
                    vertical_splitter_last.addWidget(widget)

        layout_finally.addWidget(horizontal_splitter_main)

        widget_main.setLayout(layout_main)
        widget_second.setLayout(layout_second)
        widget_finally.setLayout(layout_finally)
        self.tabWidget.setLayout(tab_layout)

        self.vector = [
            r'icons/bloomscape_sansevieria_xs_angle2-scaled.jpg',
            r'icons/indir (1).jfif'
        ]

        '''GÖRSEL GÖSTERİCİ MONİTÖRLER 1X2'''
        self.figureobj, self.axesobj = plt.subplots(1, 2, figsize=(4, 4),facecolor='#52575c')
        self.canvas_main = FigureCanvasQT(self.figureobj)
        self.navbarX = NavigationToolbarQT(canvas=self.canvas_main)

        '''GRAFİK GÖSTERİCİ MONİTÖRLER 3X2'''
        self.secondfigureobj, self.secondaxesobj = plt.subplots(3, 2, figsize=(4, 4),facecolor='#52575c')
        self.canvas_second = FigureCanvasQT(self.secondfigureobj)
        self.navbarY = NavigationToolbarQT(canvas=self.canvas_second)

        '''GRAFİK GÖSTERİCİ MONİTÖRLER 1X2'''
        self.lastfigureobj, self.lastaxesobj = plt.subplots(3,1, figsize=(4, 4),facecolor='#52575c')
        self.canvas_last = FigureCanvasQT(self.lastfigureobj)
        self.navbarZ = NavigationToolbarQT(canvas=self.canvas_last)

        self.figureobj.set_facecolor('#52575c')
        self.secondfigureobj.set_facecolor('#52575c')
        self.lastfigureobj.set_facecolor('#52575c')

        '''AXES OBJESİNİ ÖZELLESTİRMEK(GÖRSEL GÖSTERİCİ AXESLER)'''
        for axes in range(len(self.axesobj)):
            self.axesobj[axes].set_title('{}. kanvas'.format(axes + 1))
            self.axesobj[axes].imshow(self.image_processer.to_matrix(img=self.vector[axes],
                                                                     mode='matrix returner'))
            self.axesobj[axes].axis(False)

        '''TAB WİDGET İCİN TAB BARLAR OLUSTURMA'''
        self.tabWidget.addTab(widget_main, 'Sormak')
        self.tabWidget.addTab(widget_second, 'Grafikler')
        self.tabWidget.addTab(widget_finally, 'Model Eğitimi')

        '''ANA LAYOUT İCİN WİDGET TANIMLARI'''
        self.lst_sys_splitter = QSplitter(Qt.Vertical)
        self.display_sys_splitter = QSplitter(Qt.Vertical)

        self.flowers_lst = QListWidget()
        self.flowers_lst.setIconSize(QSize(128, 128))
        self.flowers_lst.setDragEnabled(True)

        lst_item = QListWidgetItem('LİSTEYE EKLEDİĞİNİZ BİTKİLER BURADA GÖZÜKÜR')
        lst_item.setFont(QFont('Bold'))
        lst_item.setTextAlignment(Qt.AlignCenter)
        self.flowers_lst.addItem(lst_item)

        self.file_sys_model = QFileSystemModel()
        self.pname = None
        self.rname = None

        for flow_data in self.vector:
            for pathname in flow_data.split('/'):
                if '.' in pathname:
                    self.pname = pathname
            self.rname = flow_data

            item = QListWidgetItem(f'Görsel yolu;{self.rname}\nGörsel adı;{self.pname}')
            item.setIcon(QIcon(flow_data))

            self.flowers_lst.addItem(item)

        self.file_sys_tree_view = QTreeView()
        self.file_sys_model.setRootPath('/')
        self.file_sys_tree_view.setModel(self.file_sys_model)

        self.dial = QDial()
        self.dial.setRange(1, 2)
        self.dial.setValue(1)

        self.dialLabel = QLabel(text='!Kanvas seçilmedi!')
        self.dialLabel.setAlignment(Qt.AlignCenter)

        self.clear_canvas_btn = QPushButton('Kanvası temizle')
        self.add_img_btn = QPushButton('Kanvasa çiçek ekle')
        self.add_img_lst_btn = QPushButton('Listeye görsel ekle')

        self.model_datas_window_label = QLabel('Modelin Mevcut Ögrenme Grafikleri')

        self.get_current_model_datas_btn_X = QPushButton('Mevcut değerleri Çek')
        self.show_current_model_datas_btn_X = QPushButton('Mevcut değerleri Göster')
        self.clear_current_model_data_graphs_X = QPushButton('Monitörleri temizle-1')

        self.get_current_model_datas_btn_Y = QPushButton('Mevcut değerleri Çek')
        self.show_current_model_datas_btn_Y = QPushButton('Mevcut değerleri göster')
        self.clear_current_model_data_graphs_Y = QPushButton('Monitörleri temizle-2')

        self.lst_sys_splitter.addWidget(self.clear_flowers_list)            
        self.lst_sys_splitter.addWidget(self.flowers_lst)
        self.lst_sys_splitter.addWidget(self.change_analysis_mode)
        self.lst_sys_splitter.addWidget(self.change_model_type)
        self.lst_sys_splitter.addWidget(self.change_batch_size)
        self.lst_sys_splitter.addWidget(self.start_analysis)

        self.display_sys_splitter.addWidget(self.navbarX)
        self.display_sys_splitter.addWidget(self.dialLabel)
        self.display_sys_splitter.addWidget(self.canvas_main)
        self.display_sys_splitter.addWidget(self.dial)
        self.display_sys_splitter.addWidget(self.clear_canvas_btn)
        self.display_sys_splitter.addWidget(self.add_img_btn)
        self.display_sys_splitter.addWidget(self.add_img_lst_btn)
        self.display_sys_splitter.addWidget(self.file_sys_tree_view)

        self.table_widget_splitter.addWidget(self.modelPredictionTableWidget)
        self.table_widget_splitter.addWidget(self.target_folder_path)
        self.table_widget_splitter.addWidget(self.apply_target_path)

        layout_main.addWidget(self.lst_sys_splitter)
        layout_main.addWidget(self.display_sys_splitter)
        layout_main.addWidget(self.table_widget_splitter)

        '''MODEL BİLGİLERİ(GRAFİKLERİ) WİDGETI İÇİN WİDGET TANIMLARI'''
        ce1,ce2 = QSplitter(Qt.Vertical),QSplitter(Qt.Vertical)
        
        ce1.addWidget(self.navbarY)
        ce1.addWidget(self.canvas_second)
        ce1.addWidget(self.show_current_model_datas_btn_X)
        ce1.addWidget(self.get_current_model_datas_btn_X)
        ce1.addWidget(self.clear_current_model_data_graphs_X)

        ce2.addWidget(self.navbarZ)
        ce2.addWidget(self.canvas_last)
        ce2.addWidget(self.show_current_model_datas_btn_Y)
        ce2.addWidget(self.get_current_model_datas_btn_Y)
        ce2.addWidget(self.clear_current_model_data_graphs_Y)

        layout_second.addWidget(ce1)
        layout_second.addWidget(ce2)

        '''SİGNAL-SLOT'''
        self.clear_canvas_btn.clicked.connect(self.clear_canvas)
        self.add_img_btn.clicked.connect(self.add_img_canvas)
        self.add_img_lst_btn.clicked.connect(self.add_lst_img)
        self.define_internal_model_btn.clicked.connect(self.define_internal_model)
        self.define_external_model_btn.clicked.connect(self.define_external_model)
        self.inspect_internal_model_btn.clicked.connect(lambda: self.inspectModel(self.IPath, self.IName, self.IType))
        self.inspect_external_model_btn.clicked.connect(lambda: self.inspectModel(self.EPath, self.EName, self.EType))
        self.get_current_model_datas_btn_X.clicked.connect(lambda: self.ignitPlotter('logPlotter',0))
        self.get_current_model_datas_btn_Y.clicked.connect(lambda: self.ignitPlotter('logPlotter',1))
        self.show_current_model_datas_btn_X.clicked.connect(lambda: self.Renderer(0))
        self.show_current_model_datas_btn_Y.clicked.connect(lambda: self.Renderer(1))
        self.clear_current_model_data_graphs_X.clicked.connect(lambda: self.clear_canvases(0))
        self.clear_current_model_data_graphs_Y.clicked.connect(lambda: self.clear_canvases(1))
        self.define_all_models_btn.clicked.connect(self.addModels)
        self.clear_all_models_btn.clicked.connect(self.clearModels)
        self.reset_internal_path.clicked.connect(self.resetIPath)
        self.reset_external_path.clicked.connect(self.resetEPath)
        self.start_analysis.clicked.connect(self.analysisIgniter)
        self.clear_flowers_list.clicked.connect(self.reset_flowers_list)
        self.apply_target_path.clicked.connect(self.define_target_folder_path)

        '''FUNCTION CALLS'''
        self.ignitPlotter(mode='test')

        '''TIMERS'''
        self.sizeOptimerTimer = QTimer(self)
        self.sizeOptimerTimer.timeout.connect(self.sizeOptimize)
        self.sizeOptimerTimer.start(10)

        '''SIGNAL-SLOTS-PYQTSİGNALS'''
        self.ifilesignal.connect(self.addModelsWithList)
        self.efilesignal.connect(self.addModelsWithList)
        self.returner_signal.connect(self.graphPlotter)
        self.returner_signal_e.connect(self.graphPlotterE)

        self.setCentralWidget(self.tabWidget)

        '''QSS SIDE'''
        qss_file = open('program_css.qss',mode='r')
        self.setStyleSheet(qss_file.read())
        qss_file.close()

    
    def graphPlotter(self,nrow,ncol,dct,key,mode):
        self.secondaxesobj[nrow,ncol].plot(dct[key],label=key)
        self.secondaxesobj[nrow,ncol].legend()

    def Renderer(self,mode):
        status = 0
        try:
            if mode == 0:
                self.canvas_second.draw()
                status = 1
            
            if mode == 1:
                self.canvas_last.draw()
                status = 1


        except:
            pass

        finally:
            try:
                if status == 1:
                    QMessageBox.information(self,'Bilgilendirme','Veriler çekiliyor....')
                
                else:
                    QMessageBox.warning(self,'Uyarı','Veriler aktarılırken bir sorun meyadana geldi...')

            except:
                pass

            finally:
                status = 0

    def clear_canvases(self,mode):
        if mode == 0:
            for axes_vector in self.secondaxesobj:
                for axes in axes_vector:
                    axes.clear()
                    self.canvas_second.draw()

        if mode == 1:
            for axes in self.lastaxesobj:
                axes.clear()
                self.canvas_last.draw()
            

    def graphPlotterE(self,loss_arr,acc_arr):
        print(loss_arr,acc_arr)
        if len(loss_arr) > 1 and len(acc_arr) > 1:
            self.lastaxesobj[0].plot(loss_arr,label='Test Loss')
            self.lastaxesobj[1].plot(acc_arr,label='Test Accuracy')
            self.lastaxesobj[0].legend()
            self.lastaxesobj[1].legend()
            self.canvas_last.draw()
        
        else:
            QMessageBox.information(self,'Dikkat','Test sonuçlarının sayısı 1 den az olduğu için grafik çizilemiyor lütfen değerlere bakmak için bekleyiniz')
            self.dock_area = QDockWidget(self)
            widget,layout = QWidget(),QHBoxLayout()
            widget.setLayout(layout)

            self.dock_area.setWidget(widget)

            for widget in [QLabel(f'Test loss: {loss_arr[0]}'),QLabel(f'Test Accuracy: {acc_arr[0]}')]:
                layout.addWidget(widget)

            self.dock_area.show()


    def ignitPlotter(self,mode=None,logtype=None):
        function_status = 1

        if mode is not None and logtype is not None:
            function_status = 1

        else:
            function_status = 0

        if function_status == 1:
            nrow, ncol, index = 0, 0, 0
            main_labels = ['Accuracy', 'Loss', 'Validation Accuracy', 'Validation Loss', 'Learning Rate', 'F1 Score']
            second_labels = ['Test loss', 'Test Accuracy', 'Ratio of validation accuracy to validation loss']

            if mode == 'test':
                for axes_vector in self.secondaxesobj:
                    for axes in axes_vector:
                        axes.plot(np.random.normal(0,10,24),label=main_labels[index])
                        print(index)
                        axes.legend()
                        self.canvas_second.draw()
                        
                        if index < len(main_labels) - 1:
                            index += 1
                
                index = 0

                for axesY in self.lastaxesobj:
                    axesY.plot(np.random.normal(0,10,24),label=second_labels[index])
                    axesY.legend()
                    self.canvas_last.draw()

                    if index < len(second_labels):
                        index += 1
                    else:
                        pass
                index = 0

        if mode == 'logPlotter':
            if logtype == 0:
                path = r"logs\SigmoidModelLogs\datas.txt"

                self.plotter_thread = QThread(self)
                self.plotter_class = PlotterThreadSide(path,0)
                self.plotter_class.moveToThread(self.plotter_thread)

                self.returner_signal = self.plotter_class.returner_signal
                self.returner_signal_e = self.plotter_class.returner_signal_e
                self.renderer_signal = self.plotter_classF.renderer_signal

                self.returner_signal.connect(self.graphPlotter)
                #self.renderer_signal.connect(self.Renderer)

                self.plotter_thread.started.connect(self.plotter_class.referanceFlow)
                self.plotter_thread.start()


            elif logtype == 1:
                path = r"logs\SigmoidModelLogs\evaulates.txt"

                self.plotter_threadF = QThread(self)
                self.plotter_classF = PlotterThreadSide(path,1)
                self.plotter_classF.moveToThread(self.plotter_threadF)

                self.returner_signal = self.plotter_classF.returner_signal
                self.returner_signal_e = self.plotter_classF.returner_signal_e
                self.renderer_signal = self.plotter_classF.renderer_signal

                self.returner_signal.connect(self.graphPlotter)
                self.returner_signal_e.connect(self.graphPlotterE)

                self.plotter_threadF.started.connect(self.plotter_classF.referanceFlow)
                self.plotter_threadF.start()


            else:
                pass

        else:
            pass


    def sizeOptimize(self):
        self.modelPredictionTableWidget.setMaximumWidth(self.width() // 2)

    def define_target_folder_path(self):
        path = self.target_folder_path.text()
        if len(path) > 6:
            try:
                modelindex = self.file_sys_model.setRootPath(path)
                self.file_sys_tree_view.setRootIndex(modelindex)

            except Exception as e0:
                print(e0)

    def analysisIgniter(self):
        mode = self.change_analysis_mode.currentText()
        mtype = self.change_model_type.currentText()
        batch = self.change_batch_size.currentText()

        try:
            self.startAnalysis(modeX=mode.strip(),
                            batchX=batch.strip(),
                            mtypeX=mtype.strip())
            
        except Exception as e0fx:
            if mtype.strip() == 'Harici':
                QMessageBox.critical(self,'UYARİ',f'Lutfen seçtiğiniz modelin çalışır durumda olup kontrol ediniz. Model şu an için kullanılamıyor\nHATA:{e0fx}\nMODEL:{self.IName}\nMODEL TÜRÜ: {mtype}')
            elif mtype.strip() == 'Dahili':
                QMessageBox.critical(self,'UYARİ',f'Lutfen seçtiğiniz modelin çalışır durumda olup kontrol ediniz. Model şu an için kullanılamıyor\nHATA:{e0fx}\nMODEL:{self.EName}\nMODEL TÜRÜ: {mtype}')
            
            else:
                QMessageBox.critical(self,'UYARİ',f'Lutfen seçtiğiniz modelin çalışır durumda olup kontrol ediniz. Model şu an için kullanılamıyor\nHATA:{e0fx}\MODEL TÜRÜ VE MODELİN KENDİSİ PROGRAM TARAFİNDAN BULUNAMADİ')
                print(mtype.strip())
                print(mode.strip())
                print(batch.strip())

    def startAnalysis(self, modeX, batchX, mtypeX):
        '''Model variables'''
        self.modeX = modeX.strip()
        self.batchX = int(batchX.split(':')[1].strip())

        '''Logic variables'''
        date, time = str(dt.datetime.now().date()), str(dt.datetime.now().strftime('%H:%M:%S'))
        self.prediction = None
        self.mtypeX = mtypeX

        self.artificalIntelligenceModule = artifical_intelligence.ArtificalIntelligence()
        self.internal_selected_model, self.external_selected_model = self.IPath, self.EPath

        if mtypeX == 'internal':
            self.internal_selected_model, self.external_selected_model = self.internal_selected_model.split(':')[1].strip()

        elif mtypeX == 'external':
            self.internal_selected_model, self.external_selected_model = None, self.external_selected_model.split(':')[1].strip()

        curr_matrix = self.current_canvas_matrix

        if curr_matrix is not None:
            if self.internal_selected_model is not None:
                self.prediction_output = self.artificalIntelligenceModule.predictModel(
                    model=self.internal_selected_model.split(';')[1].strip(),
                    matlike=curr_matrix,
                    batch_size=self.batchX,
                    mode=self.modeX)

            elif self.external_selected_model is not None:
                self.prediction_output = self.artificalIntelligenceModule.predictModel(
                    model=self.internal_selected_model.split(';')[1].strip(),
                    matlike=curr_matrix,
                    batch_size=batchX,
                    mode=modeX)


            if self.prediction_output is not None:
                self.pred = None
                if self.col >= 100:
                    self.modelPredictionTableWidget.setRowCount(self.col + 1)

                if isinstance(self.prediction_output, np.ndarray):
                    item_raw_output = QTableWidgetItem(str(self.prediction_output[0][0]))
                    item_output = None
                    item_timecode = QTableWidgetItem(f'{date}--{time}')

                    if isinstance(self.prediction_output[0][0], np.float32):
                        if self.prediction_output[0][0] > (0.5) + randint(0, 5) / 100:  # 0-5 / 100 random seed
                            self.pred = 'Saglikli'

                        elif self.prediction_output[0][0] >= (0.4) + randint(0, 5) / 100:  # 0-5 / 100 random seed
                            self.pred = 'Kısmen Saglikli'

                        else:
                            self.pred = 'Bitki hasta'

                    item_output = QTableWidgetItem(self.pred)
                    item_curr_canvas = QTableWidgetItem(str(str(self.curr_img_name).split('\n')[1].split(';')[1]))
                    item_curr_img_name = QTableWidgetItem(f'{str(self.current_selected_canvas)}. Kanvas')

                    self.modelPredictionTableWidget.setItem(self.col, 0, item_raw_output)
                    self.modelPredictionTableWidget.setItem(self.col, 1, item_output)
                    self.modelPredictionTableWidget.setItem(self.col, 2, item_timecode)
                    self.modelPredictionTableWidget.setItem(self.col, 3, item_curr_canvas)
                    self.modelPredictionTableWidget.setItem(self.col, 4, item_curr_img_name)
                    print(f'prediction output: {self.prediction_output}')

                    self.col += 1
                else:
                    print(type(self.prediction_output), type(self.prediction_output[0][0]))

            else:
                print(f'prediction failed, prediction output: {self.prediction_output}')

    def clear_table_widget(self):
        self.col = 0
        self.modelPredictionTableWidget.clear()
        self.modelPredictionTableWidget.setColumnCount(16)
        self.modelPredictionTableWidget.setRowCount((3 * 2) * 2)
        self.modelPredictionTableWidget.setHorizontalHeaderLabels(['Model tahmini', 'Tahmin', 'Zaman kodu','Mevcut kanvas','Görsel ismi'])

    def inspectModel(self, mpath, mname, mtype):
        output, code = artifical_intelligence.ArtificalIntelligence().returnModelSummary(mpath.split(';')[1])

        if code == 0:
            if isinstance(output, str):
                self.model_techinc_informations.setText(f'{self.EPath}\n{self.EName}\n{self.EType}\n{output}')

            else:
                print(type(output))

        elif code == 1:
            return(output,code)

        elif code == 2:
            return(output,code)

        else:
            return(output,code)

    def define_internal_model(self):
        self.curr_selected = self.internal_model_file_system_model.selectedItems()

        if len(self.curr_selected) >= 1:
            mtype, mname, mpath = self.curr_selected[len(self.curr_selected) - 1].text().split('\n')
            mtype,mpath,mname = mtype.strip(),mpath.strip(),mname.strip()

            if mtype.split(';')[1].strip() == ' Dahili':
                self.IType, self.IName, self.IPath = mtype, mname, mpath


            else:
                print(mtype.split(';')[1])

            self.model_inspect_preview_label.setText(f'{mname}\n{mpath}\n{mtype}')
            self.file_sys_internal_path_label.setText(f'Dahili model dosya sistemi yolu: {mpath}')

        else:
            pass

    def define_external_model(self):
        self.curr_selected = self.external_model_file_system_model.selectedItems()

        if len(self.curr_selected) >= 1:
            mtype, mname, mpath = self.curr_selected[len(self.curr_selected) - 1].text().split('\n')
            if mtype.split(';')[1] == ' Dahili':
                self.IType, self.IName, self.IPath = mtype, mname, mpath
            elif mtype.split(';')[1] == ' Harici':
                self.EType, self.EName, self.EPath = mtype, mname, mpath
            else:
                print(mtype.split(';')[1])

            self.model_inspect_preview_label.setText(f'{mname}\n{mpath}\n{mtype}')
            self.file_sys_external_path_label.setText(f'Dahili model dosya sistemi yolu: {mpath}')

        else:
            pass

    def reset_flowers_list(self):
        item = QListWidgetItem(str('**----LISTEYE EKLENEN GORSELLER BURADA GOZUKUR----**'))
        item.setTextAlignment(Qt.AlignCenter)
        
        self.flowers_lst.clear()
        self.flowers_lst.addItem(item)

    def resetIPath(self):
        self.enter_internal_path.setText('models\ProgramInterfaceModelsInternal')

    def resetEPath(self):
        self.enter_internal_path.setText('models\ProgramInterfaceModelsExternal')

    def clear_canvas(self):
        self.current_canvas_matrix = None
        self.curr_selected = None

        if self.dial.value() == 1:
            self.axesobj[0].set_title(f'{self.dial.value()}. Kanvas')
            self.axesobj[0].clear()
            # self.axesobj[0].set_xlim(-1,1)
            self.axesobj[0].axhline(0.5, color='black')
            self.axesobj[0].axvline(0.5, color='black')
            self.axesobj[0].axis(False)
            self.canvas_main.draw()
        elif self.dial.value() == 2:
            self.axesobj[1].set_title(f'{self.dial.value()}. Kanvas')
            self.axesobj[1].clear()
            # self.axesobj[1].set_xlim(-1,1)
            self.axesobj[1].axhline(0.5, color='black')
            self.axesobj[1].axvline(0.5, color='black')
            self.axesobj[1].axis(False)
            self.canvas_main.draw()

    def add_img_canvas(self):
        try:
            self.selected_items = self.flowers_lst.selectedItems()
            self.curr_img_name = self.selected_items.copy().pop().text()
        except:
            QMessageBox.critical(self,'UYARİ','Lutfen listeden bir görsel seçiniz ve tekrar deneyiniz!')
        
        if len(self.selected_items) > 0:
            last_selected = self.selected_items[len(self.selected_items) - 1]
            last_selected_text = last_selected.text()

            splitted_text = last_selected_text.split('\n')
            path = splitted_text[0].split('Görsel yolu;')[1]
            name = splitted_text[1].split('Görsel adı;')[1]

            print(f'path:{path}\nname:{name}')

            try:
                self.matrix_format = self.image_processer.to_matrix(img=path,
                                                                    mode='matrix returner')

            except Exception as e1:
                try:
                    print(e1)
                    self.matrix_format = self.image_processer.to_matrix(img=name,
                                                                        mode='matrix returner')

                except Exception as e2:
                    print(e2)
                    QMessageBox.warning(self, 'Hata',
                                        f'Görsel bulunamadı lütfen başka bir görsel ile işleminizi gerçekleştirmeyi deneyiniz veya görselinizin belirtilen dizinde veya isimde olup olmadığını kontrol ediniz.\n\nGELİSTİRİCİ LOGU:\nHATA-1:{e1}\nHATA-2{e2}')

            if self.matrix_format is not None:
                if self.dial.value() == 1:
                    self.current_canvas_matrix = self.matrix_format
                    self.current_selected_canvas = self.dial.value()

                    self.axesobj[0].imshow(self.matrix_format)
                    self.axesobj[0].set_title(f'{self.dial.value()}. Kanvas')
                    self.canvas_main.draw()

                elif self.dial.value() == 2:
                    self.current_canvas_matrix = self.matrix_format
                    self.current_selected_canvas = self.dial.value()

                    self.axesobj[1].imshow(self.matrix_format)
                    self.axesobj[1].set_title(f'{self.dial.value()}. Kanvas')
                    self.canvas_main.draw()

    def add_lst_img(self):
        try:
            self.modelindex_main = self.file_sys_tree_view.selectedIndexes()
            self.modelindex = self.modelindex_main[len(self.modelindex_main) - 1]
            self.rootpath, self.rootname = self.file_sys_model.filePath(self.modelindex), self.file_sys_model.fileName(
                self.modelindex)
            print(self.rootpath)

            icon = QIcon(self.rootpath)
            item = QListWidgetItem(f'Görsel yolu;{self.rootpath}\nGörsel adı;{self.rootname}')

            item.setIcon(icon)
            self.flowers_lst.addItem(item)

        except Exception as e3:
            try:
                print(e3)
                icon = QIcon(self.rootname)
                item = QListWidgetItem(f'Görsel yolu;{self.rootpath}\nGörsel adı;{self.rootname}')
            except Exception as e4:
                print(e4)
                QMessageBox.warning(self, 'Hata',
                                    f'Görsel Listeden çekilemedi lütfen başka bir görsel ile işleminizi gerçekleştirmeyi deneyiniz veya görselinizin belirtilen dizinde veya isimde olup olmadığını kontrol ediniz.\n\nGELİSTİRİCİ LOGU:\nHATA-1:{e3}\nHATA-2{e4}')

    def threadIgniter(self, internals, externals):
        self.threadPool = ThreadSide(internals, externals)
        self.threadObject = QThread(self)

        self.ifilesignal = self.threadPool.ifilesignal
        self.efilesignal = self.threadPool.efilesignal
        self.ifilesignal.connect(self.addModelsWithList)
        self.efilesignal.connect(self.addModelsWithList)

        self.threadObject.start()
        self.threadObject.started.connect(self.threadPool.mainIgniter)

    def addModels(self):
        try:
            self.ipath, self.epath = self.enter_internal_path.text(), self.enter_external_path.text()

            fileClass = file_actions.FileActions('artifical_intelligence', self.ipath, self.epath)
            internal_models, external_models = fileClass.fileAction()

            if isinstance(internal_models, list) and isinstance(external_models, list):
                if len(internal_models) >= 1 and len(external_models) >= 1:
                    internal_models = [f'Model türü; Dahili\nModel ismi; {x}\nModel yolu; {self.ipath}\{x}' for x in
                                       internal_models]
                    external_models = [f'Model türü; Harici\nModel ismi; {x}\nModel yolu; {self.epath}\{x}' for x in
                                       external_models]

            self.threadIgniter(internal_models, external_models)
        except:
            pass

    def clearModels(self):
        self.internal_model_file_system_model.clear()
        self.external_model_file_system_model.clear()
        self.model_inspect_preview_label.setText(
            'Model adı: Bilinmiyor\nModel yolu: Bilinmiyor\nModel türü: Bilinmiyor')

    def addModelsWithList(self, file, flag):
        print('Xxx')
        self.file = file
        self.flag = flag

        if self.flag == 0:
            if isinstance(self.file, str):
                self.IType, self.IName, self.IPath = self.file.split('\n')
                self.listWidgetItemInternal = QListWidgetItem(f'{self.IType}\n{self.IName}\n{self.IPath}')
                self.listWidgetItemInternal.setTextAlignment(Qt.AlignCenter)
                self.internal_model_file_system_model.addItem(self.listWidgetItemInternal)

        if self.flag == 1:
            if isinstance(self.file, str):
                self.EType, self.EName, self.EPath = self.file.split('\n')
                self.listWidgetExternal = QListWidgetItem(f'{self.EType}\n{self.EName}\n{self.EPath}')
                self.listWidgetExternal.setTextAlignment(Qt.AlignCenter)
                self.external_model_file_system_model.addItem(self.listWidgetExternal)


if __name__ == '__main__':
    sp = QApplication(_s.argv)
    sw = MainGui()
    sw.show()
    _s.exit(sp.exec_())
