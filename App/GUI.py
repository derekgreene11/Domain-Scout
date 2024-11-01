from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
import requests

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Domain Scout")
        self.setMinimumSize(QSize(1060,600))
        self.setWindowIcon(QIcon("C:/Users/Derek/Desktop/CS361/App/appicon.ico"))

        # Light Mode and Dark Mode Styles 
        self.lightModeStyle = """QMainWindow { background-color: #cccccc;color: black; } QPushButton { background-color: #00b2c3; color: black; } QCheckBox { color: black; } 
                                 QLineEdit { background-color: white; color: black; } QTableWidget { background-color: #f2f2f2; color: black; } QDialog { background-color: #cccccc; color: black; } 
                                 QTextEdit { background-color: #f2f2f2; color: black }"""
        self.darkModeStyle = """QMainWindow { background-color: #2c2c2c; color: white; } QPushButton { background-color: #00b2c3; color: white; } QCheckBox { color: white; }
                            QLineEdit { background-color: #3c3c3c; color: white; } QTableWidget { background-color: #3c3c3c; color: white; } QDialog { background-color: #2c2c2c; color: white; }
                                QTextEdit { background-colorL #3c3c3c; color: white; }"""
        self.setStyleSheet(self.lightModeStyle)
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
        self.data_table.horizontalHeader().setStretchLastSection(True)
        
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
        
        searchTitle = QLabel("Search Records:")
        font3 = QFont("Cooper Black", 12)
        searchTitle.setFont(font3)
        searchTitle.setFixedWidth(150)
        searchTitle.setStyleSheet("color: #00b2c3;")
        
        self.sb_search = QLineEdit()
        self.sb_search.setFixedWidth(300)
        self.sb_search.textChanged.connect(self.inputTbData)

        layout_search.addWidget(searchTitle)
        layout_search.addWidget(self.sb_search)
        layout_search.addStretch()
         
        bt_whois = QPushButton("WHOIS Query")
        bt_whois.setFixedSize(110, 30)
        bt_add = QPushButton("Add Record")
        bt_add.setFixedSize(110, 30)
        bt_save = QPushButton("Save Records")
        bt_save.setFixedSize(110,30)
        bt_delete = QPushButton("Delete Record")
        bt_delete.setFixedSize(110, 30)
        bt_import = QPushButton("Import CSV")
        bt_import.setFixedSize(110, 30)
        bt_export = QPushButton("Export CSV")
        bt_export.setFixedSize(110, 30)
        bt_help = QPushButton("Help")
        bt_help.setFixedSize(110, 30)
        bt_settings = QPushButton("Settings")
        bt_settings.setFixedSize(110, 30)
        bt_about = QPushButton("About")
        bt_about.setFixedSize(110, 30)
        
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_whois)
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_add)
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_save)
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_delete)
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
        
        bt_whois.clicked.connect(lambda: WHOISWindow(self).exec())
        bt_add.clicked.connect(lambda: self.data_table.insertRow(self.data_table.rowCount()))
        bt_delete.clicked.connect(lambda: self.deleteRow())
        bt_about.clicked.connect(lambda: AboutWindow(self).exec())
        bt_help.clicked.connect(lambda: HelpWindow(self).exec())
        bt_settings.clicked.connect(lambda: SettingsWindow(self).exec())
              
        layout_table.addWidget(self.data_table)
        layout_table.addLayout(layout_buttons)
        
        layout_main.addLayout(layout_title)
        layout_main.addLayout(layout_search) 
        layout_main.addLayout(layout_table)
           
        widget_search = QWidget()
        widget_search.setLayout(layout_main)
        self.setCentralWidget(widget_search)
        self.allRecords = self.fetchData()
        self.popTable(self.allRecords)



    def fetchData(self):
        response = requests.get('https://derekrgreene.com/ct-data/api')
        if response.status_code == 200:
            records = response.json()
            return records
        else:
            print("Error: Failed to connect to API")
        return []
    
    def inputTbData(self):
        term = self.sb_search.text().lower()
        filteredRecords = [record for record in self.allRecords if any(term in str(value).lower() for value in record.values())]
        self.popTable(filteredRecords)
        
    def popTable(self, records):
        self.data_table.setRowCount(len(records))
        
        tableOrder = ["domain", "admin_email", "registrar", "tech_email", 
                    "registrant_email", "creation_date", 
                    "expiration_date", "updated_date", "emails"]

        for rowX, record in enumerate(records):
            for colY, column in enumerate(tableOrder):
                item = QTableWidgetItem(str(record.get(column, "")))
                self.data_table.setItem(rowX, colY, item)

    def deleteRow(self):
        currRow = self.data_table.currentRow()
        delRecord = self.data_table.item(currRow, 0).text()
        
        apiUrl = f"https://derekrgreene.com/ct-data/api/delete?domain={delRecord}"
        response = requests.delete(apiUrl)
        
        if response.status_code == 200:
            self.data_table.removeRow(currRow)
            QMessageBox.information(self, "Success", "Record Deleted Successfully!")
        else:
            QMessageBox.warning(self, "ERROR", "Failed to delete record from server.")

class WHOISWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setStyleSheet(main_window.styleSheet())
        self.setWindowTitle("WHOIS Details")
        self.setWindowIcon(QIcon("C:/Users/Derek/Desktop/CS361/App/appicon.ico"))
        self.setMinimumSize(QSize(600,630))   
        self.setMaximumSize(QSize(600,630)) 
               
        layout_main = QVBoxLayout()
        layout_search = QHBoxLayout()
        layout_search.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_buttons = QVBoxLayout()
        layout_buttons.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout_table = QHBoxLayout()
        layout_title = QHBoxLayout()
        
        self.data_table = QTableWidget()
        self.data_table.setRowCount(18)
        self.data_table.setColumnCount(1)
        self.data_table.setColumnWidth(0, 500)
        self.data_table.setVerticalHeaderLabels(["Domain", "Registrar", "WHOIS Server", "Referral URL", "Updated Date", "Creation Date", "Expiration Date", "Nameservers", "Status", "Emails", "DNNSEC", "Name", "Org", "Address", "City", "State", "Postal Code", "Country"  ])
        self.data_table.setHorizontalHeaderLabels([""])
        
        
        lb_title2 = QLabel("WHOIS Details")
        font = QFont("Cooper Black", 24, QFont.Weight.Bold)
        lb_title2.setFont(font)
        lb_title2.setFixedWidth(250)
        lb_title2.setStyleSheet("color: #00b2c3;")
        
        layout_title.addWidget(lb_title2)
        layout_title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        bt_back = QPushButton("Back")
        bt_back.setFixedSize(100, 30)
        bt_export = QPushButton("Export CSV")
        bt_export.setFixedSize(100, 30)
        bt_help = QPushButton("Help")
        bt_help.setFixedSize(100, 30)
        bt_settings = QPushButton("Settings")
        bt_settings.setFixedSize(100, 30)
        bt_about = QPushButton("About")
        bt_about.setFixedSize(100, 30)
        
        bt_back.clicked.connect(self.close)
        bt_about.clicked.connect(lambda: AboutWindow(self.main_window).exec())
        bt_help.clicked.connect(lambda: HelpWindow(self.main_window).exec())
        bt_settings.clicked.connect(lambda: SettingsWindow(self.main_window).exec())
        
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_back)
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_export)
        layout_buttons.addSpacing(350)
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

        self.setLayout(layout_main)

class AboutWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        
        self.main_window = main_window
        self.setStyleSheet(main_window.styleSheet())
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon("C:/Users/Derek/Desktop/CS361/App/appicon.ico"))
        self.setMinimumSize(QSize(400,400)) 
        self.setMaximumSize(QSize(400,400))  
               
        layout_main = QVBoxLayout()
        layout_main.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
                
        lb_title2 = QLabel("About Domain Scout")
        font = QFont("Cooper Black", 24, QFont.Weight.Bold)
        lb_title2.setFont(font)
        lb_title2.setFixedWidth(350)
        lb_title2.setStyleSheet("color: #00b2c3;")
        lb_title2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        bt_back = QPushButton("Back")
        bt_back.setFixedSize(100, 30)   
        bt_back.clicked.connect(self.close)
        
        aboutSection = QTextEdit()
        aboutSection.setReadOnly(True)
        aboutSection.setHtml("""<p"><span style="color: #00b2c3; font-family: Cooper Black;">Domain Scout</span> is the primary GUI to view vulnerable domains found by CT Domain Data (see https://derekrgreene.com/ct-data).<br><br> 
                            CT Domain Data identifies disposable email addresses used as contact methods in WHOIS records. Domains are collected using Certstream
                            Server Go which streams Certificate Transparency logs continuously to a websocket connection. Domains are extracted from the data stream 
                            and WHOIS queries are subsequently made to identify contact email addresses which are compared against a list of 15k+ known disposable email 
                            domains. If a disposable email address is found, the domain and associated data is added to the database and displayed in <span style="color: #00b2c3; font-family: Cooper Black;">Domain Scout</span>.<br><br><br></p>
                            <p style="text-align: center";<strong>Made with &#128154; by <span style="color: #00b2c3;">Derek R. Greene</span></strong><br>
                            &copy; 2024 <span style="color: #00b2c3;">Derek R. Greene</span>. All rights reserved.</p>""")
        
        layout_main.addWidget(lb_title2)
        layout_main.addWidget(bt_back)
        layout_main.setAlignment(bt_back, Qt.AlignmentFlag.AlignHCenter)
        layout_main.addWidget(aboutSection)
        self.setLayout(layout_main)
        
class HelpWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setStyleSheet(main_window.styleSheet())
        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon("C:/Users/Derek/Desktop/CS361/App/appicon.ico"))
        self.setMinimumSize(QSize(600,600))  
        self.setMaximumSize(QSize(600,600)) 
               
        layout_main = QVBoxLayout()
        layout_main.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
                
        lb_title2 = QLabel("Help")
        font = QFont("Cooper Black", 36, QFont.Weight.Bold)
        lb_title2.setFont(font)
        lb_title2.setFixedWidth(350)
        lb_title2.setStyleSheet("color: #00b2c3;")
        lb_title2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        bt_back = QPushButton("Back")
        bt_back.setFixedSize(100, 30)   
        bt_back.clicked.connect(self.close)
        
        aboutSection = QTextEdit()
        aboutSection.setReadOnly(True)
        aboutSection.setHtml("""<h2 style="color: #00b2c3;"><strong>Add Records</strong></h2><ul><li style="font-size: 16px;">To add a new record, press the 'Add Record' button and enter
                            the details into the new row.<li style="font-size: 16px;">Press the 'Save Records' button to save changes.</li></ul><h2 style="color: #00b2c3;"><strong>Delete Recods</Strong></h2><ul>
                            <li style="font-size: 16px;">To delete a record, select the desired record and press the 'Delete Record' button.<p style="color: red;">***Deleting a record is permanent and cannot be undone***</p></li></ul>
                            <h2 style="color: #00b2c3;"><strong>Search & Sort Records</strong></h2><ul><li style="font-size: 16px;">Records can be searched by entering a search query in the search bar.</li>
                            <li style="font-size: 16px;">Records can be sorted in ascending or descending order by clicking on the column headings (e.g. 'Domain', 'Admin Email', etc.).</li></ul><h2 style="color:
                            #00b2c3;"><strong>Importing & Exporting Records</h2></strong><ul><li style="font-size: 16px;">In order to properly import CSV records into the database, they will need to match the 
                            <strong>EXACT</strong> format of the database.</li><li style="font-size: 16px;">To view the required format, first export the data to view the resultant CSV file.</li><li style="font-size:
                            16px;">To export all records, simply click on the 'Export CSV' button. <br><span style="color: #00b2c3;"><strong>NOTE:</strong></span> This will export all records.</li></ul><h2 style="color: #00b2c3;"><strong>Misc</strong>
                            </h2><ul><li style="font-size: 16px;">This application fetches data from an API at:<br>https://derekrgreene.com/ct-data/api<br><br><span style="color: #00b2c3;"><strong>NOTE:</strong></span> If you are unable to resolve 
                            this domain, the application will not load the data. Please ensure the API is reachable.</li></ul><br><p style="text-align: center";<strong>Made with &#128154; by <span style="color: #00b2c3;">Derek R. Greene</span></strong><br>
                            &copy; 2024 <span style="color: #00b2c3;">Derek R. Greene</span>. All rights reserved.</p>""")
        
        layout_main.addWidget(lb_title2)
        layout_main.addWidget(bt_back)
        layout_main.setAlignment(lb_title2, Qt.AlignmentFlag.AlignHCenter)
        layout_main.setAlignment(bt_back, Qt.AlignmentFlag.AlignHCenter)
        layout_main.addWidget(aboutSection)
        self.setLayout(layout_main)

class SettingsWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setStyleSheet(main_window.styleSheet())
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("C:/Users/Derek/Desktop/CS361/App/appicon.ico"))
        self.setMinimumSize(QSize(600,600))  
        self.setMaximumSize(QSize(600,600)) 
               
        layout_main = QVBoxLayout()
        layout_buttons = QHBoxLayout()
        layout_main.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout_darkMode = QHBoxLayout()
        layout_refresh = QHBoxLayout()
                
        lb_title2 = QLabel("Settings")
        font = QFont("Cooper Black", 36, QFont.Weight.Bold)
        lb_title2.setFont(font)
        lb_title2.setFixedWidth(350)
        lb_title2.setStyleSheet("color: #00b2c3;")
        lb_title2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        bt_defaults = QPushButton("Load Defaults")
        bt_defaults.setFixedSize(130, 30)
        bt_back = QPushButton("Back")
        bt_back.setFixedSize(100, 30)   
        bt_back.clicked.connect(self.close)
        self.cb_darkMode = QCheckBox()
        self.cb_darkMode.setChecked(self.main_window.styleSheet() == self.main_window.darkModeStyle)
        self.cb_darkMode.stateChanged.connect(self.toggleDarkMode)
        bt_defaults.clicked.connect(lambda: (self.cb_darkMode.setChecked(False), self.cbb_refresh.setCurrentIndex(0)))
        self.cb_darkMode.setStyleSheet("QCheckBox::indicator { width: 30px; height: 30px; }")
        lb_darkMode = QLabel("""<span style="color: #00b2c3; font-size: 24px; font-family: Cooper Black;">Dark Mode </span><span style="color: grey; font-size: 14px; 
                            font-family: Cooper Black;">-changes the application theme to a dark color scheme</span>""")
        self.cbb_refresh = QComboBox()
        self.cbb_refresh.addItems(["1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "11s", "12s", "13s", "14s", "15s", "16s", "17s", "18s", 
                             "19s", "20s", "21s", "22s", "23s", "24s", "25s", "26s", "27s", "28s", "29s", "30s", "31s", "32s", "33s", "34s", "35s",
                             "36s", "37s", "38s", "39s", "40s", "41s", "42s", "43s", "44s", "45s", "46s", "47s", "48s", "49s", "50s", "51s", "52s",
                             "53s", "54s", "55s", "56s", "57s", "58s", "59s", "60s"])
        self.cbb_refresh.setFixedSize(50, 30)              
        lb_refresh = QLabel("""<span style="color: #00b2c3; font-size: 24px; font-family: Cooper Black;">Refresh Rate </span><span style="color: grey; font-size: 14px; 
                            font-family: Cooper Black;">-changes how often the app refreshes the data</span>""")
                
        layout_darkMode.addWidget(lb_darkMode)
        layout_darkMode.addSpacing(10)
        layout_darkMode.addWidget(self.cb_darkMode)
        layout_refresh.addWidget(lb_refresh)
        layout_refresh.addWidget(self.cbb_refresh)
        layout_buttons.addWidget(bt_defaults)
        layout_buttons.addWidget(bt_back)
        layout_main.addWidget(lb_title2)
        layout_main.addLayout(layout_buttons)
        layout_main.addSpacing(30)
        layout_main.addLayout(layout_darkMode)
        layout_main.addSpacing(30)
        layout_main.addLayout(layout_refresh)
        layout_main.setAlignment(lb_title2, Qt.AlignmentFlag.AlignHCenter)
        layout_main.setAlignment(bt_back, Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout_main)
    
    
    def toggleDarkMode(self):
        if self.cb_darkMode.isChecked():
            self.main_window.setStyleSheet(self.main_window.darkModeStyle)
            self.setStyleSheet(self.main_window.darkModeStyle)
        else:
            self.main_window.setStyleSheet(self.main_window.lightModeStyle)
            self.setStyleSheet(self.main_window.lightModeStyle)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
