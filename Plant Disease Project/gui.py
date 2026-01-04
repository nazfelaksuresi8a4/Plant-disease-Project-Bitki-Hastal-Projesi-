import artifical_intelligence as ai_side
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvasQT
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbarQT
import matplotlib.pyplot as plt
import winsound as ws
import sys as _s
import  image_processing as ip_side

class ThreadSide(QObject):
    def __init__(self):
        super().__init__()
        self.run_main()

    def run_main(self):
        for _ in range(12):
            print(_)


class MainGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabWidget = QTabWidget()
        '''ANA DEGİSKENLER'''
        self.current_canvas_matrix = None
        self.current_selected_canvas = None

        '''GÖRSEL İSLEYİCİ'''
        self.image_processer = ip_side.İmageProcesser()

        '''WİDGET TANIMLARI'''
        widget_main = QWidget()         #görsel girdi sistemi
        widget_second = QWidget()       #model bilgileri
        widget_finally = QWidget()      #model eğitimi

        layout_main = QHBoxLayout()
        layout_second = QVBoxLayout()
        layout_finally = QVBoxLayout()
        tab_layout = QVBoxLayout()

        widget_main.setLayout(layout_main)
        widget_second.setLayout(layout_second)
        widget_finally.setLayout(layout_finally)
        self.tabWidget.setLayout(tab_layout)

        self.vector = [
            r'icons/bloomscape_sansevieria_xs_angle2-scaled.jpg',
            r'icons/indir (1).jfif'
        ]

        self.figureobj,self.axesobj = plt.subplots(1,2)
        self.canvas_main = FigureCanvasQT(self.figureobj)
        self.navbar = NavigationToolbarQT(canvas=self.canvas_main)

        '''AXES OBJESİNİ ÖZELLESTİRMEK'''
        for axes in range(len(self.axesobj)):
            self.axesobj[axes].set_title('{}. kanvas'.format(axes + 1))
            self.axesobj[axes].imshow(self.image_processer.to_matrix(self.vector[axes]))
            self.axesobj[axes].axis(False)

        '''TAB WİDGET İCİN TAB BARLAR OLUSTURMA'''
        self.tabWidget.addTab(widget_main,'Sormak')
        self.tabWidget.addTab(widget_second, 'Grafikler')
        self.tabWidget.addTab(widget_finally, 'Model Eğitimi')

        '''ANA LAYOUT İCİN WİDGET TANIMLARI'''
        self.lst_sys_splitter = QSplitter(Qt.Vertical)
        self.display_sys_splitter = QSplitter(Qt.Vertical)

        self.flowers_lst = QListWidget()
        self.flowers_lst.setIconSize(QSize(128,128))
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
        self.dial.setRange(1,2)
        self.dial.setValue(1)

        self.dialLabel = QLabel(text='!Kanvas seçilmedi!')
        self.dialLabel.setAlignment(Qt.AlignCenter)

        self.clear_canvas_btn = QPushButton('Kanvası temizle')
        self.add_img_btn = QPushButton('Kanvasa çiçek ekle')
        self.add_img_lst_btn = QPushButton('Listeye görsel ekle')

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

        '''SİGNAL-SLOT'''
        self.clear_canvas_btn.clicked.connect(self.clear_canvas)
        self.add_img_btn.clicked.connect(self.add_img_canvas)
        self.add_img_lst_btn.clicked.connect(self.add_lst_img)

        self.setCentralWidget(self.tabWidget)

    def clear_canvas(self):
        if self.dial.value() == 1:
            self.axesobj[0].set_title(f'{self.dial.value()}. Kanvas')
            self.axesobj[0].clear()
            self.axesobj[0].set_xlim(-1,1)
            self.axesobj[0].axhline(0.5,color='black')
            self.axesobj[0].axvline(0,color='black')
            self.axesobj[0].axis(False)
            self.canvas_main.draw()
        elif self.dial.value() == 2:
            self.axesobj[1].set_title(f'{self.dial.value()}. Kanvas')
            self.axesobj[1].clear()
            self.axesobj[1].set_xlim(-1,1)
            self.axesobj[1].axhline(0.5,color='black')
            self.axesobj[1].axvline(0,color='black')
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
                    QMessageBox.warning(self,'Hata',f'Görsel bulunamadı lütfen başka bir görsel ile işleminizi gerçekleştirmeyi deneyiniz veya görselinizin belirtilen dizinde veya isimde olup olmadığını kontrol ediniz.\n\nGELİSTİRİCİ LOGU:\nHATA-1:{e1}\nHATA-2{e2}')

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
        self.modelindex_main = self.file_sys_tree_view.selectedIndexes()
        self.modelindex = self.modelindex_main[len(self.modelindex_main) - 1]
        self.rootpath,self.rootname = self.file_sys_model.filePath(self.modelindex),self.file_sys_model.fileName(self.modelindex)
        print(self.rootpath)

        try:
            icon = QIcon(self.rootpath)
            item = QListWidgetItem(f'Görsel yolu:{self.rootpath}\nGörsel adı:{self.rootname}')
        except Exception as e3:
            try:
                print(e3)
                icon = QIcon(self.rootname)
                item = QListWidgetItem(f'Görsel yolu:{self.rootpath}\nGörsel adı:{self.rootname}')
            except Exception as e4:
                print(e4)
                QMessageBox.warning(self,'Hata',f'Görsel Listeden çekilemedi lütfen başka bir görsel ile işleminizi gerçekleştirmeyi deneyiniz veya görselinizin belirtilen dizinde veya isimde olup olmadığını kontrol ediniz.\n\nGELİSTİRİCİ LOGU:\nHATA-1:{e3}\nHATA-2{e4}')

        item.setIcon(icon)
        self.flowers_lst.addItem(item)


if __name__ == '__main__':
    sp = QApplication(_s.argv)
    sw = MainGui()
    sw.show()
    _s.exit(sp.exec_())