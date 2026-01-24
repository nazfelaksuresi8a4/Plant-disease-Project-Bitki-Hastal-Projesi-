import artifical_intelligence as ai_side
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvasQT
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbarQT
import matplotlib.pyplot as plt
import winsound as ws
import sys as _s

import file_actions
import image_processing as ip_side
import file_actions as tdg


class ThreadSide(QObject):
    filesignal = pyqtSignal(str, str)

    def __init__(self, internals, externals):
        super().__init__()
        self.internal_fs, self.external_fs = internals, externals

    def emitFiles(self):
        print('emitted')
        if len(self.internal_fs) == len(self.external_fs):
            for ifile, efile in zip(self.internal_fs, self.external_fs):
                self.filesignal.emit(ifile, efile)

        else:
            if len(self.internal_fs) >= 1:
                for ifile in self.internal_fs:
                    self.filesignal.emit(ifile, 'x')

            if len(self.external_fs) >= 1:
                for efile in self.external_fs:
                    self.filesignal.emit('x', efile)


class MainGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabWidget = QTabWidget()
        '''THREADS'''
        self.threadPool = ThreadSide([], [])
        self.threadObject = QThread(self)
        self.threadPool.moveToThread(self.threadObject)

        '''SIGNALS'''
        self.filesignal = self.threadPool.filesignal

        '''ANA DEGİSKENLER'''
        self.current_canvas_matrix = None
        self.current_selected_canvas = None

        '''GÖRSEL İSLEYİCİ'''
        self.image_processer = ip_side.İmageProcesser()

        '''WİDGET TANIMLARI'''
        widget_main = QWidget()  # görsel girdi sistemi
        widget_second = QWidget()  # model bilgileri
        widget_finally = QWidget()  # model eğitimi

        layout_main = QHBoxLayout()
        layout_second = QVBoxLayout()
        layout_finally = QVBoxLayout()
        tab_layout = QVBoxLayout()

        horizontal_splitter_main = QSplitter(Qt.Horizontal)  # 3x main split side     #h3x-1

        vertical_splitter_main = QSplitter(Qt.Vertical)  # 1x split side              #v1x-1
        vertical_splitter_second = QSplitter(Qt.Vertical)  # 1x1*1x1 split side       #v4x-1
        vertical_splitter_last = QSplitter(Qt.Vertical)  # 1x split side              #v1x-2

        vertical_splt_sec_v4x1_1_horizontal_splitter_1 = QSplitter(Qt.Horizontal)
        vertical_splt_sec_v4x1_1_vertical_splitter_1 = QSplitter(Qt.Vertical)
        vertical_splt_sec_v4x1_1_vertical_splitter_2 = QSplitter(Qt.Vertical)

        vertical_splt_sec_v4x1_1_horizontal_splitter_1.addWidget(vertical_splt_sec_v4x1_1_vertical_splitter_1)
        vertical_splt_sec_v4x1_1_horizontal_splitter_1.addWidget(vertical_splt_sec_v4x1_1_vertical_splitter_2)

        horizontal_splitter_main.addWidget(vertical_splitter_main)
        horizontal_splitter_main.addWidget(vertical_splitter_second)
        horizontal_splitter_main.addWidget(vertical_splitter_last)

        '''ETİKETLER'''
        self.l1, self.l2, self.l3 = QLabel(text='Dahili Model Seçme Sistemi'), QLabel(
            text='Model Eğitim Penceresi'), QLabel(text='Harici Model Seçme Sistemi')
        self.internal_model_selecet_label = QLabel(text='Dahili Model seçme Sistemi Ayarı')
        self.external_model_select_label = QLabel(text='Harici Model Seçme Sistemi Ayarı')
        self.model_inspecting_monitor_label = QLabel(text='Model İnceleme Monitörü')
        self.model_inspect_preview_label = QLabel(
            text='Model adı: Bilinmiyor\nModelin bellekte kapsadığı yer: Bilinmiyor')
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

        self.define_file_system_internal_path = QPushButton(text='Dahili Dosya Sistemi Yolunu Tanımla')
        self.define_file_system_external_path = QPushButton(text='Harici Dosya Sistemi Yolunu Tanımla')

        self.define_external_model_btn = QPushButton(text='Harici modeli tanımla')
        self.inspect_external_model_btn = QPushButton(text='Harici modeli incele')
        self.define_external_file_system_path = QPushButton(text='Dosya sistemi yolunu tanımla')

        self.define_all_models_btn = QPushButton(text='Modelleri tanımla')

        self.reset_external_path = QPushButton('Yolu Sıfırla')
        self.reset_internal_path = QPushButton('Yolu Sıfırla')

        '''EKSTRA WİDGETLAR'''
        self.internal_model_file_system_model = QListWidget()
        self.external_model_file_system_model = QListWidget()
        self.enter_external_path = QLineEdit()
        self.enter_internal_path = QLineEdit()
        self.enter_external_path.setPlaceholderText('Harici Modelin Yolunu Girin...')
        self.enter_internal_path.setPlaceholderText('Dahili Modelin Yolunu girin....')

        self.model_techinc_informations = QListWidget()

        self.internal_gui_widgets = [[self.l1,
                                      self.define_internal_model_btn,
                                      self.inspect_internal_model_btn,
                                      self.define_file_system_internal_path,
                                      self.internal_model_file_system_model],
                                     [self.l2,
                                      vertical_splt_sec_v4x1_1_horizontal_splitter_1,
                                      self.model_inspecting_monitor_label,
                                      self.model_inspect_preview_label,
                                      self.model_techinc_informations_label,
                                      self.model_techinc_informations,
                                      self.define_all_models_btn
                                      ],
                                     [self.l3,
                                      self.define_external_model_btn,
                                      self.inspect_external_model_btn,
                                      self.define_external_file_system_path,
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
        self.figureobj, self.axesobj = plt.subplots(1, 2, figsize=(8, 8))
        self.canvas_main = FigureCanvasQT(self.figureobj)
        self.navbar = NavigationToolbarQT(canvas=self.canvas_main)

        '''GRAFİK GÖSTERİCİ MONİTÖRLER 2X2'''
        self.secondfigureobj, self.secondaxesobj = plt.subplots(2, 2, figsize=(8, 8))
        self.canvas_second = FigureCanvasQT(self.secondfigureobj)
        self.navbar = NavigationToolbarQT(canvas=self.canvas_main)

        '''AXES OBJESİNİ ÖZELLESTİRMEK(GÖRSEL GÖSTERİCİ AXESLER)'''
        for axes in range(len(self.axesobj)):
            self.axesobj[axes].set_title('{}. kanvas'.format(axes + 1))
            self.axesobj[axes].imshow(self.image_processer.to_matrix(self.vector[axes]))
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

            item = QListWidgetItem(f'Görsel yolu:{self.rname}\nGörsel adı:{self.pname}')
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
        self.show_current_model_datas_btn = QPushButton('Mevcut değerleri göster')
        self.clear_current_model_data_graphs = QPushButton('Monitörleri temizle')

        self.lst_sys_splitter.addWidget(self.flowers_lst)

        self.display_sys_splitter.addWidget(self.navbar)
        self.display_sys_splitter.addWidget(self.dialLabel)
        self.display_sys_splitter.addWidget(self.canvas_main)
        self.display_sys_splitter.addWidget(self.dial)
        self.display_sys_splitter.addWidget(self.clear_canvas_btn)
        self.display_sys_splitter.addWidget(self.add_img_btn)
        self.display_sys_splitter.addWidget(self.add_img_lst_btn)
        self.display_sys_splitter.addWidget(self.file_sys_tree_view)

        layout_main.addWidget(self.lst_sys_splitter)
        layout_main.addWidget(self.display_sys_splitter)

        '''MODEL BİLGİLERİ(GRAFİKLERİ) WİDGETI İÇİN WİDGET TANIMLARI'''
        layout_second.addWidget(self.model_datas_window_label)
        layout_second.addWidget(self.canvas_second)
        layout_second.addWidget(self.show_current_model_datas_btn)
        layout_second.addWidget(self.clear_current_model_data_graphs)

        '''SİGNAL-SLOT'''
        self.clear_canvas_btn.clicked.connect(self.clear_canvas)
        self.add_img_btn.clicked.connect(self.add_img_canvas)
        self.add_img_lst_btn.clicked.connect(self.add_lst_img)
        self.define_all_models_btn.clicked.connect(self.addModels)

        '''SIGNAL-SLOTS-PYQTSİGNALS'''
        self.filesignal.connect(self.addModelsWithList)

        self.setCentralWidget(self.tabWidget)

    def clear_canvas(self):
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
        self.selected_items = self.flowers_lst.selectedItems()
        if len(self.selected_items) > 0:
            last_selected = self.selected_items[len(self.selected_items) - 1]
            last_selected_text = last_selected.text()

            splitted_text = last_selected_text.split('\n')
            path = splitted_text[0].split('Görsel yolu:')[1]
            name = splitted_text[1].split('Görsel adı:')[1]

            print(f'path:{path}\nname:{name}')

            try:
                self.matrix_format = self.image_processer.to_matrix(path)

            except Exception as e1:
                try:
                    print(e1)
                    self.matrix_format = self.image_processer.to_matrix(name)

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
            item = QListWidgetItem(f'Görsel yolu:{self.rootpath}\nGörsel adı:{self.rootname}')

            item.setIcon(icon)
            self.flowers_lst.addItem(item)

        except Exception as e3:
            try:
                print(e3)
                icon = QIcon(self.rootname)
                item = QListWidgetItem(f'Görsel yolu:{self.rootpath}\nGörsel adı:{self.rootname}')
            except Exception as e4:
                print(e4)
                QMessageBox.warning(self, 'Hata',
                                    f'Görsel Listeden çekilemedi lütfen başka bir görsel ile işleminizi gerçekleştirmeyi deneyiniz veya görselinizin belirtilen dizinde veya isimde olup olmadığını kontrol ediniz.\n\nGELİSTİRİCİ LOGU:\nHATA-1:{e3}\nHATA-2{e4}')

    def threadIgniter(self, internals, externals):
        self.threadPool = ThreadSide(internals, externals)
        self.threadObject = QThread(self)

        self.filesignal = self.threadPool.filesignal
        self.filesignal.connect(self.addModelsWithList)

        self.threadObject.start()
        self.threadObject.started.connect(self.threadPool.emitFiles)

    def addModels(self):
        self.ipath, self.epath = self.enter_internal_path.text(), self.enter_external_path.text()

        fileClass = file_actions.FileActions('artifical_intelligence', self.ipath, self.epath)
        internal_models, external_models = fileClass.fileAction()

        if isinstance(internal_models, list) and isinstance(external_models, list):
            if len(internal_models) >= 1 and len(external_models) >= 1:
                internal_models = [f'Model türü: Dahili\nModel ismi: {x}\nModel yolu:{self.ipath}\\{x}' for x in
                                   internal_models]
                external_models = [f'Model türü: Harici\nModel ismi: {x}\nModel yolu:{self.epath}\\{x}' for x in
                                   external_models]

        self.threadIgniter(internal_models, external_models)

    def addModelsWithList(self, internal_model, external_model):
        '''listeye ekleme şeylerini kodla adamı hasta etme'''
        print('Xxx')
        if isinstance(internal_model, str) and isinstance(external_model, str):
            if len(internal_model) > 6 and len(external_model) > 6:
                self.Imodel_type, self.Imodel_name, self.Imodel_path = internal_model.split('\n')
                self.Emodel_type, self.Emodel_name, self.Emodel_path = external_model.split('\n')

                self.ilist_widget_item = QListWidgetItem(f'{self.Imodel_name}\n{self.Imodel_path}\n{self.Imodel_type}')
                self.elist_widget_item = QListWidgetItem(f'{self.Emodel_name}\n{self.Emodel_path}\n{self.Emodel_type}')

                self.ilist_widget_item.setTextAlignment(Qt.AlignCenter)
                self.elist_widget_item.setTextAlignment(Qt.AlignCenter)

                self.internal_model_file_system_model.addItem(self.ilist_widget_item)
                self.external_model_file_system_model.addItem(self.elist_widget_item)

            elif len(internal_model) > 6 and len(external_model) < 6:
                self.Imodel_type, self.Imodel_name, self.Imodel_path = internal_model.split('\n')

                self.ilist_widget_item = QListWidgetItem(f'{self.Imodel_name}\n{self.Imodel_path}\n{self.Imodel_type}')

                self.ilist_widget_item.setTextAlignment(Qt.AlignCenter)

                self.internal_model_file_system_model.addItem(self.ilist_widget_item)

            elif len(internal_model) < 6 and len(external_model) > 6:
                self.Emodel_type, self.Emodel_name, self.Emodel_path = external_model.split('\n')

                self.elist_widget_item = QListWidgetItem(f'{self.Emodel_name}\n{self.Emodel_path}\n{self.Emodel_type}')

                self.elist_widget_item.setTextAlignment(Qt.AlignCenter)

                self.external_model_file_system_model.addItem(self.elist_widget_item)


if __name__ == '__main__':
    sp = QApplication(_s.argv)
    sw = MainGui()
    sw.show()
    _s.exit(sp.exec_())