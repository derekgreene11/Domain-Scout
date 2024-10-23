from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Domain Scout")
        self.setMinimumSize(QSize(800,600))
        
        layout_main = QVBoxLayout()
        layout_search = QHBoxLayout()
        layout_search.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_buttons = QVBoxLayout()
        layout_buttons.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        appTitle = QLabel("Domain Scout")
        font = appTitle.font()
        font.setPointSize(30)
        appTitle.setFont(font)
        appTitle.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        
        
        
        
        lb_domain = QLabel("Domain")
        cb_domain = QCheckBox()
        lb_creation = QLabel("Creation Date")
        cb_creation = QCheckBox()
        lb_expiration = QLabel("Expiration Date")
        cb_expiration = QCheckBox()
        lb_emails = QLabel("Emails")
        cb_emails = QCheckBox()
        sb_search = QLineEdit()
        sb_search.setFixedWidth(300)
        bt_search = QPushButton("Search")
        bt_search.setFixedSize(100,20)
        
        layout_search.addWidget(lb_domain)
        layout_search.addWidget(cb_domain)
        layout_search.addWidget(lb_creation)
        layout_search.addWidget(cb_creation)
        layout_search.addWidget(lb_expiration)
        layout_search.addWidget(cb_expiration)
        layout_search.addWidget(lb_emails)
        layout_search.addWidget(cb_emails)
        layout_search.addWidget(sb_search)
        layout_search.addWidget(bt_search)
        
        
        bt_details = QPushButton("View Details")
        bt_details.setFixedSize(100,20)
        bt_add = QPushButton("Add Record")
        bt_add.setFixedSize(100,20)
        bt_delete = QPushButton("Delete Record")
        bt_delete.setFixedSize(100,20)
        bt_save = QPushButton("Save")
        bt_save.setFixedSize(100,20)
        bt_import = QPushButton("Import CSV")
        bt_import.setFixedSize(100,20)
        bt_export = QPushButton("Export CSV")
        bt_export.setFixedSize(100,20)
        bt_help = QPushButton("Help")
        bt_help.setFixedSize(100,20)
        bt_settings = QPushButton("Settings")
        bt_settings.setFixedSize(100,20)
        bt_about = QPushButton("About")
        bt_about.setFixedSize(100,20)
        
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_details)
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_add)
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_delete)
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_save)
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_import)
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_export)
        layout_buttons.addSpacing(1000)
        layout_buttons.addWidget(bt_help)
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_settings)
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_about)        
        
        
        
        #layout_main.addWidget(appTitle)
        layout_main.addLayout(layout_search)
        layout_main.addLayout(layout_buttons)
        
        
        widget_search = QWidget()
        widget_search.setLayout(layout_main)
        self.setCentralWidget(widget_search)
        

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
