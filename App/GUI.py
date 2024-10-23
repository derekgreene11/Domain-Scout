from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
import requests
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Domain Scout")
        self.setMinimumSize(QSize(1050,600))
        
        layout_main = QVBoxLayout()
        layout_search = QHBoxLayout()
        layout_search.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_buttons = QVBoxLayout()
        layout_buttons.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout_table = QHBoxLayout()
        layout_title = QHBoxLayout()
        
        self.data_table = QTableWidget()
        self.data_table.setRowCount(50)
        self.data_table.setColumnCount(9)
        self.data_table.setHorizontalHeaderLabels(["Domain", "Admin Email", "Registrar", "Tech Email", "Registrant Email", "Creation Date", "Expiration Date", "Updated Date", "emails"  ])
        
        appTitle = QLabel("Domain Scout")
        font = QFont("Cooper Black", 24, QFont.Weight.Bold)
        appTitle.setFont(font)
        appTitle.setFixedWidth(240)
        appTitle.setStyleSheet("color: #00b2c3;")
        
        appVersion = QLabel("V1.0")
        font2 = QFont("Cooper Black", 10)
        appVersion.setFont(font2)
        appVersion.setStyleSheet("color: #00b2c3;")
        
        layout_title.addWidget(appTitle)
        layout_title.addWidget(appVersion)
        layout_title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

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
        
        layout_table.addWidget(self.data_table)
        layout_table.addLayout(layout_buttons)
        
        layout_main.addLayout(layout_title)
        layout_main.addLayout(layout_search) 
        layout_main.addLayout(layout_table)
           
        widget_search = QWidget()
        widget_search.setLayout(layout_main)
        self.setCentralWidget(widget_search)
        self.inputTbData()
    
    def fetchData(self):
        response = requests.get('https://derekrgreene.com/ct-data/api')
        if response.status_code == 200:
            records = response.json()
            return records
        else:
            print("Error: Failed to connect to API")
        return []
    
    def inputTbData(self):
        records = self.fetchData()
        self.data_table.setRowCount(len(records))
        
        tableOrder = ["domain", "admin_email", "registrar", "tech_email", 
                    "registrant_email", "creation_date", 
                    "expiration_date", "updated_date", "emails"]

        for rowX, record in enumerate(records):
            for colY, column in enumerate(tableOrder):
                item = QTableWidgetItem(str(record.get(column, "")))
                self.data_table.setItem(rowX, colY, item)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
