# Name: Derek Greene
# OSU Email: greenede@oregonstate.edu
# Course: CS361 - Software Engineering I
# Description: Domain Scout is the primary GUI to view vulnerable domains found by CT Domain Data. CT Domain Data identifies disposable email addresses used as contact methods in WHOIS records.
#              Domains are collected using Certstream Server Go which streams Certificate Transparency logs continuously to a websocket connection. Domains are extracted from the data stream and
#              WHOIS queries are subsequently made to identify contact email addresses which are compared against a list of 15k+ known disposable email domains. If a disposable email address is 
#              found, the domain and associated data is added to the database and displayed in Domain Scout. This application fetches data from an API at: https://derekrgreene.com/ct-data/api.
#              If you are unable to resolve this domain, the application will not load the data. Please ensure the API is reachable.

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from dotenv import load_dotenv
import sys
import os
import subprocess
import requests
import socket

# Main Window Class
class MainWindow(QMainWindow):
    def __init__(self):
        # Call the parent constructor to initialize QMainWindow
        super().__init__()
        self.setWindowTitle("Domain Scout")
        self.setMinimumSize(QSize(1060,600))
        self.setWindowIcon(QIcon("appicon.ico"))
        
        # Define absolute paths to microservices 
        self.microservicesDir = os.path.dirname(os.path.abspath(__file__))
        self.export_Dir = os.path.join(self.microservicesDir, 'export.py')
        self.import_Dir = os.path.join(self.microservicesDir, 'import.py')
        self.whois_Dir = os.path.join(self.microservicesDir, 'whoisQuery.py')

        # Start micro-services
        self.export_service = subprocess.Popen([sys.executable, self.export_Dir])
        self.import_service = subprocess.Popen([sys.executable, self.import_Dir])
        self.whois_service = subprocess.Popen([sys.executable, self.whois_Dir])

        # Light Mode and Dark Mode Styles 
        self.lightModeStyle = """QMainWindow { background-color: #cccccc;color: black; } QPushButton { background-color: #00b2c3; color: black; } QCheckBox { color: black; } 
                                 QLineEdit { background-color: white; color: black; } QTableWidget { background-color: #f2f2f2; color: black; } QDialog { background-color: #cccccc; color: black; } 
                                 QTextEdit { background-color: #f2f2f2; color: black } QMessageBox { background-color: #cccccc; color: black; }"""
        self.darkModeStyle = """QMainWindow { background-color: #2c2c2c; color: white; } QPushButton { background-color: #00b2c3; color: white; } QCheckBox { color: white; }
                                QLineEdit { background-color: #3c3c3c; color: white; } QTableWidget { background-color: #3c3c3c; color: white; } QDialog { background-color: #2c2c2c; color: white; }
                                QTextEdit { background-color: #3c3c3c; color: white; } QMessageBox { background-color: #3c3c3c; color: white; }"""
        # Default lightModeStyle
        self.setStyleSheet(self.lightModeStyle)
        self.showLogin()

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
        
        appVersion = QLabel("V1.1")
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
        bt_import = QPushButton("Import SQL")
        bt_import.setFixedSize(110, 30)
        bt_export = QPushButton("Export SQL")
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
        
        # Events for button presses
        bt_whois.clicked.connect(lambda: self.whoisQuery())
        bt_add.clicked.connect(lambda: self.data_table.insertRow(self.data_table.rowCount()))
        bt_delete.clicked.connect(lambda: self.checkDelete())
        bt_save.clicked.connect(lambda: self.saveRecord())
        bt_export.clicked.connect(lambda: self.exportRecords())
        bt_import.clicked.connect(lambda: self.importRecords())
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
  
    """
    Method to display user tutorial upon login. 
    Parameters: None
    Returns: None
    """
    def tutorial(self):
        tutorial = QMessageBox(self)
        tutorial.setWindowTitle("Welcome Tutorial")
        tutorial.setWindowIcon(QIcon("appicon.ico"))
        tutorial.setText("""<p><h1><span style="color: #00b2c3; font-family: Cooper Black; text-align: center;">Welcome Tutorial!</span></h1><br><ul><span style="color: #00b2c3; font-family: Cooper Black;">Searching:</span><li>
                         <span style="color: #3c3c3c; font-family: Cooper Black;">To search records, enter your search query into the search bar at top of window.</span></li></ul><br><ul><span style="color: 
                         #00b2c3; font-family: Cooper Black;">WHOIS Details:</span><li><span style="color: #3c3c3c; font-family: Cooper Black;">To view associated WHOIS details, select desired domain
                         from list and then select the 'view details' button on the right of the screen.</span></li></ul><br><ul><span style="color: #00b2c3; font-family: Cooper Black;">Importing & Exporting:
                         </span><li><span style="color: #3c3c3c; font-family: Cooper Black;">To import and export data into the database, make sure data is formatted exactly matching the SQL database. See Help page for details and more information.</span></li></ul></p>""")
        tutorial.exec()
    
    """
    Method to display LoginWindow and load main window upon DialogCode.Accepted
    Parameters: None
    Returns: None
    """
    def showLogin(self):
        login = LoginWindow(self)
        if login.exec() == QDialog.DialogCode.Accepted:
            self.show()
            self.tutorial()
        else:
            sys.exit(0)
    
    """
    Method to fetch ct-data from api endpoint @ derekrgreene.com/ct-data/api.
    Parameters: None
    Returns: []: list of dict
    """
    def fetchData(self):
        response = requests.get('https://derekrgreene.com/ct-data/api')
        if response.status_code == 200:
            records = response.json()
            return records
        else:
            print("Error: Failed to connect to API")
        return []
    
    """
    Method to filter records by query term entered in search bar.
    Parameters: None
    Returns: None
    """
    def inputTbData(self):
        term = self.sb_search.text().lower()
        filteredRecords = [record for record in self.allRecords if any(term in str(value).lower() for value in record.values())]
        self.popTable(filteredRecords)
    
    """
    Method to populate QTableWidget with data fetched from ct-data api. 
    Parameters: records: list of dict
    Returns: None
    """
    def popTable(self, records):
        self.data_table.setRowCount(len(records))
        
        tableOrder = ["domain", "admin_email", "registrar", "tech_email", 
                    "registrant_email", "creation_date", 
                    "expiration_date", "updated_date", "emails"]

        for rowX, record in enumerate(records):
            for colY, column in enumerate(tableOrder):
                item = QTableWidgetItem(str(record.get(column, "")))
                self.data_table.setItem(rowX, colY, item)
    
    """
    Method to display popup asking if user really wants to delete record. 
    Parameters: None
    Returns: None
    """
    def checkDelete(self):
        currentRow = self.data_table.currentRow()

        # ensure a row is selected to delete
        if currentRow != -1:
            checkDelMsg = QMessageBox()
            # ensure pop up msg matches current system UI (lightmode vs darkmode)
            if self.styleSheet() == self.lightModeStyle:
                checkDelMsg.setStyleSheet("QMessageBox { background-color: #cccccc; color: black; }")
            else:
                checkDelMsg.setStyleSheet("QMessageBox { background-color: #3c3c3c; color: white; }")
        
            checkDelMsg.setText("<font color='red'>Deleting a record is permanent and cannot be undone. Are you sure you want to proceed?</font>")
            checkDelMsg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            checkDelMsg.setDefaultButton(QMessageBox.StandardButton.No)

            response = checkDelMsg.exec()
        
            if response == QMessageBox.StandardButton.Yes:
                self.deleteRow()
        else:
            QMessageBox.warning(self, "No Record", "You must click on a record first!")
    
    """
    Method to delete selected record from database. Displays success or error message.
    Parameters: None
    Returns: None
    """
    def deleteRow(self):
        currRow = self.data_table.currentRow()
        delRecord = self.data_table.item(currRow, 0).text()
        
        # API call to delete record from database
        apiUrl = f"https://derekrgreene.com/ct-data/api/delete?domain={delRecord}"
        response = requests.delete(apiUrl)

        if response.status_code == 200:
            self.data_table.removeRow(currRow)
            QMessageBox.information(self, "Success", "<font color='green'>Record Deleted Successfully!</font>")
        else:
            QMessageBox.warning(self, "ERROR", "<font color='red'>Failed to delete record from server.</font>")

    """
    Method to save new records to database. Displays message upon success.
    Parameters: None
    Returns: None
    """
    def saveRecord(self):
        newRecords = []

        # Check for new records to save
        for row in range(self.data_table.rowCount()):
            domain = self.data_table.item(row, 0).text() if self.data_table.item(row, 0) else ""
            admin_email = self.data_table.item(row, 1).text() if self.data_table.item(row, 1) else ""
            registrar = self.data_table.item(row, 2).text() if self.data_table.item(row, 2) else ""
            tech_email = self.data_table.item(row, 3).text() if self.data_table.item(row, 3) else ""
            registrant_email = self.data_table.item(row, 4).text() if self.data_table.item(row, 4) else ""
            creation_date = self.data_table.item(row, 5).text() if self.data_table.item(row, 5) else ""
            expiration_date = self.data_table.item(row, 6).text() if self.data_table.item(row, 6) else ""
            updated_date = self.data_table.item(row, 7).text() if self.data_table.item(row, 7) else ""
            emails = self.data_table.item(row, 8).text() if self.data_table.item(row, 8) else ""

            if domain and (domain not in [record['domain'] for record in self.allRecords]):
                newRecord = {
                    "domain": domain,
                    "admin_email": admin_email,
                    "registrar": registrar,
                    "tech_email": tech_email,
                    "registrant_email": registrant_email,
                    "creation_date": creation_date,
                    "expiration_date": expiration_date,
                    "updated_date": updated_date,
                    "emails": emails
                }
                newRecords.append(newRecord)

        # Send record to save to API to save to CT-Data application database
        if newRecords:
            try:
                response = requests.post('https://derekrgreene.com/ct-data/api/save', json=newRecords)

                if response.status_code == 200:
                    QMessageBox.information(self, "Success", "New record(s) saved successfully!", QMessageBox.StandardButton.Ok)

                    # Update allRecords list with new records
                    self.allRecords.extend(newRecords)
                    newRecords.clear()
                    self.popTable(self.allRecords)

                else:
                    QMessageBox.warning(self, "Error", f"Failed to save records: {response.json().get('error')}", QMessageBox.StandardButton.Ok)

            except requests.exceptions.RequestException as e:
                QMessageBox.critical(self, "Error", f"An error occurred while saving the records: {e}", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, "No New Records", "There are no new records to save.", QMessageBox.StandardButton.Ok)
    
    """
    Method to call export microservice to fetch SQL drump from API and save to local machine. Microservice is called oveer TCP sockets.
    Parameters: None
    Returns: None
    """
    def exportRecords(self):
        server = "127.0.0.1"
        port = 1024

        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            serverSocket.connect((server, port))
            serverSocket.send("start".encode())
            response = serverSocket.recv(1024).decode()

            if response:
                QMessageBox.information(self, "Success", response)
        except ConnectionRefusedError:
            QMessageBox.warning(self, "Connection Failed", "Could not connect to the service.")
        finally:
            serverSocket.close()
    
    """
    Method to call import microservice to fetch SQL dump from local files and sent to API to import to database. Microservice is called over TCP sockets.
    Parameters: None
    Returns: None
    """
    def importRecords(self):
        server = "127.0.0.1"
        port = 1026

        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            serverSocket.connect((server, port))
            serverSocket.send("start".encode())
            response = serverSocket.recv(1024).decode()

            if response:
                QMessageBox.information(self, "Status", response)
        except ConnectionRefusedError:
            QMessageBox.warning(self, "Connection Failed", "Could not connect to the service.")
        finally:
            serverSocket.close()
    
    """
    Method to call whois microservice to fetch WHOIS data for selected domain and populate response in QTableWidget. Microservice is called over TCP sockets.
    Parameters: None
    Returns: None
    """
    def whoisQuery(self):
        selectedRow = self.data_table.currentRow()
        if selectedRow != -1:
            selectedRow = self.data_table.currentRow()
            domain = self.data_table.item(selectedRow, 0).text()
            WHOISWindow(self, domain).exec()
        else:
            QMessageBox.warning(self, "No Record", "You must click on a record first!")
        
    """
    Method to stop microservices upon main applicaton exit. 
    Parameters: None
    Returns: None
    """    
    def closeEvent(self, event):
        self.export_service.terminate()
        self.import_service.terminate()
        self.whois_service.terminate()
        event.accept()
        
# Record Details Window Class
class WHOISWindow(QDialog):
    def __init__(self, main_window, domain):
        super().__init__()
        self.main_window = main_window
        self.domain = domain

        # Set UI to match main window
        self.setStyleSheet(main_window.styleSheet())
        self.setWindowTitle("WHOIS Details")
        self.setWindowIcon(QIcon("appicon.ico"))
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
        self.data_table.setRowCount(17)
        self.data_table.setColumnCount(1)
        self.data_table.setColumnWidth(0, 500)
        self.data_table.setVerticalHeaderLabels(["Domain", "Registrar", "WHOIS Server", "Referral URL", "Updated Date", "Creation Date", "Expiration Date", "Nameservers", "Status", "DNNSEC", "Name", "Org", "Address", "City", "State", "Postal Code", "Country"  ])
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
        bt_help = QPushButton("Help")
        bt_help.setFixedSize(100, 30)
        bt_settings = QPushButton("Settings")
        bt_settings.setFixedSize(100, 30)
        bt_about = QPushButton("About")
        bt_about.setFixedSize(100, 30)
        
        # Events for button presses
        bt_back.clicked.connect(self.close)
        bt_about.clicked.connect(lambda: AboutWindow(self.main_window).exec())
        bt_help.clicked.connect(lambda: HelpWindow(self.main_window).exec())
        bt_settings.clicked.connect(lambda: SettingsWindow(self.main_window).exec())
        
        layout_buttons.addSpacing(10)
        layout_buttons.addWidget(bt_back)
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
        self.popTable(self.domain)
    
    """
    Method to fetch WHOIS data from microservice over TCP socket to display in QTableWidget.
    Parameters: domain: str
    Returns: None
    """
    def popTable(self, domain):
        server = "127.0.0.1"
        port = 1025
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            serverSocket.connect((server, port))
            serverSocket.send(domain.encode()) 
            response = serverSocket.recv(1024).decode()
            lines = response.split("\n")  
        
            whois_info = {field: "N/A" for field in [
            "Domain Name", "Registrar", "Whois Server", "Referral URL", "Updated Date", "Creation Date", 
            "Expiration Date", "Name Servers", "Status", "DNSSEC", "Name", "Org", "Address", 
            "City", "State", "Postal Code", "Country"
            ]}

            for line in lines:
                for field in whois_info.keys():
                    if line.startswith(field):
                        value = line[len(field):].strip(': ').strip()
                        whois_info[field] = value
                        break  

            self.data_table.setItem(0, 0, QTableWidgetItem(domain))  # Domain
            self.data_table.setItem(1, 0, QTableWidgetItem(whois_info["Domain Name"])) 
            self.data_table.setItem(2, 0, QTableWidgetItem(whois_info["Whois Server"])) 
            self.data_table.setItem(3, 0, QTableWidgetItem(whois_info["Referral URL"]))
            self.data_table.setItem(4, 0, QTableWidgetItem(whois_info["Updated Date"]))
            self.data_table.setItem(5, 0, QTableWidgetItem(whois_info["Creation Date"])) 
            self.data_table.setItem(6, 0, QTableWidgetItem(whois_info["Expiration Date"])) 
            nameservers = whois_info["Name Servers"]
            self.data_table.setItem(7, 0, QTableWidgetItem(nameservers))
            self.data_table.setItem(8, 0, QTableWidgetItem(whois_info["Status"])) 
            self.data_table.setItem(9, 0, QTableWidgetItem(whois_info["DNSSEC"]))
            self.data_table.setItem(10, 0, QTableWidgetItem(whois_info["Name"])) 
            self.data_table.setItem(11, 0, QTableWidgetItem(whois_info["Org"])) 
            self.data_table.setItem(12, 0, QTableWidgetItem(whois_info["Address"]))
            self.data_table.setItem(13, 0, QTableWidgetItem(whois_info["City"])) 
            self.data_table.setItem(14, 0, QTableWidgetItem(whois_info["State"])) 
            self.data_table.setItem(15, 0, QTableWidgetItem(whois_info["Postal Code"])) 
            self.data_table.setItem(16, 0, QTableWidgetItem(whois_info["Country"])) 

        except Exception as e:
            print(f"Error fetching or displaying WHOIS data: {e}")
        except ConnectionRefusedError:
            QMessageBox.warning(self, "Connection Failed", "Could not connect to the server.")
        finally:
            serverSocket.close()

# About Window Class
class AboutWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Set UI to match main window
        self.setStyleSheet(main_window.styleSheet())
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon("appicon.ico"))
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

        # Event for button press
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

# Help Window Class
class HelpWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Set UI to match main window
        self.setStyleSheet(main_window.styleSheet())
        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon("appicon.ico"))
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

        # Event for button press
        bt_back.clicked.connect(self.close)
        aboutSection = QTextEdit()
        aboutSection.setReadOnly(True)
        aboutSection.setHtml("""<h2 style="color: #00b2c3;"><strong>Add Records</strong></h2><ul><li style="font-size: 16px;">To add a new record, press the 'Add Record' button and enter
                            the details into the new row.<li style="font-size: 16px;">Press the 'Save Records' button to save changes.</li><li style="font-size: 16px;">Dates must be entered in the fomat YYYY-MM-DD hh:mm:ss.</li></ul><h2 style="color: #00b2c3;"><strong>Delete Recods</Strong></h2><ul>
                            <li style="font-size: 16px;">To delete a record, select the desired record and press the 'Delete Record' button.<p style="color: red;">***Deleting a record is permanent and cannot be undone***</p></li></ul>
                            <h2 style="color: #00b2c3;"><strong>Search & Sort Records</strong></h2><ul><li style="font-size: 16px;">Records can be searched by entering a search query in the search bar.</li>
                            <li style="font-size: 16px;">Records can be sorted in ascending or descending order by clicking on the column headings (e.g. 'Domain', 'Admin Email', etc.).</li></ul><h2 style="color:
                            #00b2c3;"><strong>Importing & Exporting Records</h2></strong><ul><li style="font-size: 16px;">In order to properly import SQL records into the database, they will need to match the 
                            <strong>EXACT</strong> format of the database.</li><li style="font-size: 16px;">To view the required format, first export the data to view the resultant SQL dump file.</li><li style="font-size:
                            16px;">To export all records, simply click on the 'Export SQL' button. <br><span style="color: #00b2c3;"><strong>NOTE:</strong></span> This will export all records.</li></ul><h2 style="color: #00b2c3;"><strong>Misc</strong>
                            </h2><ul><li style="font-size: 16px;">This application fetches data from an API at:<br>https://derekrgreene.com/ct-data/api<br><br><span style="color: #00b2c3;"><strong>NOTE:</strong></span> If you are unable to resolve 
                            this domain, the application will not load the data. Please ensure the API is reachable.</li></ul><br><p style="text-align: center";<strong>Made with &#128154; by <span style="color: #00b2c3;">Derek R. Greene</span></strong><br>
                            &copy; 2024 <span style="color: #00b2c3;">Derek R. Greene</span>. All rights reserved.</p>""")
        layout_main.addWidget(lb_title2)
        layout_main.addWidget(bt_back)
        layout_main.setAlignment(lb_title2, Qt.AlignmentFlag.AlignHCenter)
        layout_main.setAlignment(bt_back, Qt.AlignmentFlag.AlignHCenter)
        layout_main.addWidget(aboutSection)
        self.setLayout(layout_main)

# Settings Window Class
class SettingsWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Set UI to match main window
        self.setStyleSheet(main_window.styleSheet())
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("appicon.ico"))
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
        
        # Events for button presses
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
    
    """
    Method to set UI dark upon checkbox selection and revert to light UI upon deselection. 
    Parameters: None
    Returns: None
    """
    def toggleDarkMode(self):
        if self.cb_darkMode.isChecked():
            self.main_window.setStyleSheet(self.main_window.darkModeStyle)
            self.setStyleSheet(self.main_window.darkModeStyle)
        else:
            self.main_window.setStyleSheet(self.main_window.lightModeStyle)
            self.setStyleSheet(self.main_window.lightModeStyle)

# Login Window Class
class LoginWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Set UI to match main window
        self.setStyleSheet(main_window.styleSheet())
        self.setWindowTitle("Welcome to Domain Scout")
        self.setWindowIcon(QIcon('appicon.ico'))
        self.setMinimumSize(QSize(600,600))  
        self.setMaximumSize(QSize(600,600)) 
               
        layout_main = QVBoxLayout()
        layout_uname = QHBoxLayout()
        layout_pass = QHBoxLayout()
        layout_title = QHBoxLayout()
        
        appTitle = QLabel("Domain Scout")
        font = QFont("Cooper Black", 24, QFont.Weight.Bold)
        appTitle.setFont(font)
        appTitle.setFixedWidth(240)
        appTitle.setStyleSheet("color: #00b2c3;")
        
        appVersion = QLabel("V1.1")
        font2 = QFont("Cooper Black", 10)
        appVersion.setFont(font2)
        appVersion.setStyleSheet("color: #00b2c3;")
       
        layout_title.addWidget(appTitle)
        layout_title.addWidget(appVersion)
        layout_title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        layout_uname.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layout_pass.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        font3 = QFont("Cooper Black", 20)
        self.lb_userName = QLabel("Username:")
        self.lb_userName.setFont(font3)
        self.lb_userName.setStyleSheet("color: #3c3c3c;")
        self.lb_uInput = QLineEdit()
        self.lb_pass = QLabel("Password:")
        self.lb_pass.setFont(font3)
        self.lb_pass.setStyleSheet("color: #3c3c3c;")
        self.lb_pInput = QLineEdit()

        # set input to show as *** for password input
        self.lb_pInput.setEchoMode(QLineEdit.EchoMode.Password)
        self.bt_login = QPushButton("Login")
        self.bt_signup = QPushButton("Sign Up")

        # Event for button press
        self.bt_login.clicked.connect(self.login)
        self.bt_signup.clicked.connect(lambda: SignupWindow(self).exec())

        startInfo = QTextEdit()
        startInfo.setReadOnly(True)
        startInfo.setMaximumSize(QSize(600, 150))
        startInfo.setHtml("""<ul><li><h2 style="color: #00b2c3;"><strong>Discover domains using known disposable email accounts in associated WHOIS email contacts!</strong></h2></li><li><h2 style="color: #00b2c3;">
                          <strong>Perform WHOIS queries in seconds!</strong></h2></li></ul>""")

        layout_uname.addWidget(self.lb_userName)
        layout_uname.addWidget(self.lb_uInput)
        layout_pass.addWidget(self.lb_pass)
        layout_pass.addWidget(self.lb_pInput)
        layout_main.addLayout(layout_title)
        layout_main.addLayout(layout_uname)
        layout_main.addLayout(layout_pass)
        layout_main.addWidget(startInfo)
        layout_main.addWidget(self.bt_login)
        layout_main.addWidget(self.bt_signup)
        self.setLayout(layout_main)
    
    """
    Method to check for correct username and password. Displays sucess or fail message. Store username and password in .env in root app directory.
    Parameters: None
    Returns: None
    """
    def login(self):
        # Load .env file for username and password credentials
        load_dotenv()
        usernameInput = self.lb_uInput.text()
        passwordInput = self.lb_pInput.text()
        userName = os.getenv("USER1")
        passWord = os.getenv("PASS")

        if usernameInput == userName and passwordInput == passWord:
            QMessageBox.information(self, "Login", "<font color='black'>Login successful!</font>")
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "<font color='red'>Invalid username or password!<font>")

    """
    Method to stop microservices upon login window exit. 
    Parameters: None
    Returns: None
    """    
    def closeEvent(self, event):
        self.main_window.export_service.terminate()
        self.main_window.import_service.terminate()
        self.main_window.whois_service.terminate()
        event.accept()

# Signup Window Class
class SignupWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Set UI to match main window
        self.setStyleSheet(main_window.styleSheet())
        self.setWindowTitle("Sign up for Domain Scout")
        self.setWindowIcon(QIcon('appicon.ico'))
        self.setMinimumSize(QSize(600,600))  
        self.setMaximumSize(QSize(600,600)) 
               
        layout_main = QVBoxLayout()
        layout_uname = QHBoxLayout()
        layout_pass = QHBoxLayout()
        layout_title = QHBoxLayout()
        
        appTitle = QLabel("Domain Scout")
        font = QFont("Cooper Black", 24, QFont.Weight.Bold)
        appTitle.setFont(font)
        appTitle.setFixedWidth(240)
        appTitle.setStyleSheet("color: #00b2c3;")
        
        appVersion = QLabel("V1.1")
        font2 = QFont("Cooper Black", 10)
        appVersion.setFont(font2)
        appVersion.setStyleSheet("color: #00b2c3;")
       
        layout_title.addWidget(appTitle)
        layout_title.addWidget(appVersion)
        layout_title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        layout_uname.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layout_pass.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        font3 = QFont("Cooper Black", 20)
        self.lb_userName = QLabel("Username:")
        self.lb_userName.setFont(font3)
        self.lb_userName.setStyleSheet("color: #3c3c3c;")
        self.lb_uInput = QLineEdit()
        self.lb_pass = QLabel("Password:")
        self.lb_pass.setFont(font3)
        self.lb_pass.setStyleSheet("color: #3c3c3c;")
        self.lb_pInput = QLineEdit()

        # set input to show as *** for password input
        self.lb_pInput.setEchoMode(QLineEdit.EchoMode.Password)
        self.bt_signUp = QPushButton("Sign Up")

        # Event for button press
        self.bt_signUp.clicked.connect(lambda: self.createEnv())


        startInfo = QTextEdit()
        startInfo.setReadOnly(True)
        startInfo.setMaximumSize(QSize(600, 150))
        startInfo.setHtml("""<ul><li><h2 style="color: #00b2c3;"><strong>To ensure user privacy, your username and password are never sent back to the developer and instead are stored locally on your machine in a .env file.</strong></h2></li>
                          <li><h2 style="color: #00b2c3;"><strong>After signup, you will be re-directed back to the login window.</strong></h2></li></ul>""")

        layout_uname.addWidget(self.lb_userName)
        layout_uname.addWidget(self.lb_uInput)
        layout_pass.addWidget(self.lb_pass)
        layout_pass.addWidget(self.lb_pInput)
        layout_main.addLayout(layout_title)
        layout_main.addLayout(layout_uname)
        layout_main.addLayout(layout_pass)
        layout_main.addWidget(startInfo)
        layout_main.addWidget(self.bt_signUp)
        self.setLayout(layout_main)
    
    """
    Method to create .env file to store username and password.
    Parameters: None
    Returns: None
    """
    def createEnv(self):
        usernameInput = self.lb_uInput.text()
        passwordInput = self.lb_pInput.text()
        envFile = '.env'
        
        if not usernameInput or not passwordInput:
            QMessageBox.warning(self, "Error", "<font color='red'>Please enter a username and password!</font>")
        else:
            # write username and password to .env file
            with open(envFile, 'w') as f:
                f.write(f"USER1={usernameInput}\n")
                f.write(f"PASS={passwordInput}\n")
                QMessageBox.information(self, "Signup", "<font color='black'>Signup successful!</font>")
                self.accept()      

"""
Function to start program and create main window object
Parameters: None
Returns: None
"""
def main():
    # Create application object
    app = QApplication(sys.argv)
    # Create main window object
    window = MainWindow()
    # Start Qt event loop
    app.exec()

if __name__ == "__main__":
    main()
