from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QPushButton)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        main = QWidget()
        grid = QGridLayout()

        widget_a = QWidget()
        widget_a.setStyleSheet("background-color: salmon")
        widget_b = QWidget()
        widget_b.setStyleSheet("background-color: lightblue")
        widget_c = QWidget()
        widget_c.setStyleSheet("background-color: gold")
        widget_d = QWidget()
        widget_d.setStyleSheet("background-color: gray")
        widget_e = QWidget()
        widget_e.setStyleSheet("background-color: #80c342")
        widget_f = QWidget()
        widget_f.setStyleSheet("background-color: #e0c31e")
        widget_g = QWidget()
        widget_g.setStyleSheet("background-color: #b40000")
        widget_h = QWidget()
        widget_h.setStyleSheet("background-color: #ae32a0")
        widget_i = QWidget()
        widget_i.setStyleSheet("background-color: #6400aa")


        # widget, row, col, height space, width space
        grid.addWidget(widget_a, 0, 0, 1, 1)
        grid.addWidget(widget_b, 0, 1, 1, 1)
        grid.addWidget(widget_c, 0, 2, 1, 1)

        grid.addWidget(widget_d, 1, 0, 1, 2)
        grid.addWidget(widget_e, 1, 2, 2, 1)
        grid.addWidget(widget_f, 2, 0, 1, 1)

        grid.addWidget(widget_g, 2, 1, 1, 1)
        grid.addWidget(widget_i, 3, 0, 1, 1)
        grid.addWidget(widget_h, 3, 1, 1, 2)


        main.setLayout(grid)




        self.setCentralWidget(main)





    
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
