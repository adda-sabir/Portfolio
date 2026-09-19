# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pyDbModuleGen.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenuBar, QPlainTextEdit, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.SqQLiteDataType=['INTEGER', 'REAL','TEXT','BLOB','DATE','DATETIME']
        self.SqQLiteStrDataType=['TEXT','BLOB','DATE','DATETIME']
        
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1100, 670)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        font16B = QFont()
        font16B.setPointSize(16)
        font16B.setBold(True)
        font14 = QFont()
        font14.setPointSize(14)
        font12 = QFont()
        font12.setPointSize(12)
        font11 = QFont()
        font11.setPointSize(11)
        self.tabDbStructure = QTabWidget(self.centralwidget)
        self.tabDbStructure.setObjectName(u"tabDbStructure")
        self.tabDbStructure.setGeometry(QRect(0, 0, 1090, 650))
        self.tabDbStructure.setFont(font12)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setFont(font12)
        self.LbDriver = QLabel(self.tab)
        self.LbDriver.setObjectName(u"LbDriver")
        self.LbDriver.setGeometry(QRect(20, 20, 70, 30))
        self.LbDriver.setFont(font11)
        self.LbDBName = QLabel(self.tab)
        self.LbDBName.setObjectName(u"LbDBName")
        self.LbDBName.setGeometry(QRect(240, 20, 70, 30))
        self.LbDBName.setFont(font11)
        self.BtOpenJson=QPushButton(self.tab)
        self.BtOpenJson.setObjectName('BtOpenJson')
        self.BtOpenJson.setGeometry(450,20,111,30)
        self.BtOpenJson.setFont(font11)
        self.EdDbDriver = QLineEdit(self.tab)
        self.EdDbDriver.setObjectName(u"EdDbDriver")
        self.EdDbDriver.setGeometry(QRect(100, 20, 113, 30))
        self.EdDbDriver.setFont(font11)
        self.EdDatabaseName = QLineEdit(self.tab)
        self.EdDatabaseName.setObjectName(u"EdDatabaseName")
        self.EdDatabaseName.setGeometry(QRect(320, 20, 120, 30))
        self.EdDatabaseName.setFont(font11)
        self.lbAuto = QLabel(self.tab)
        self.lbAuto.setObjectName(u"lbAuto")
        self.lbAuto.setGeometry(QRect(245, 80, 35, 18))
        self.lbPK = QLabel(self.tab)
        self.lbPK.setObjectName(u"label")
        self.lbPK.setGeometry(QRect(290, 80, 21, 18))
        self.lbFieldName = QLabel(self.tab)
        self.lbFieldName.setObjectName(u"label_2")
        self.lbFieldName.setGeometry(QRect(320, 80, 91, 18))
        self.lbFieldType = QLabel(self.tab)
        self.lbFieldType.setObjectName(u"label_3")
        self.lbFieldType.setGeometry(QRect(470, 80, 91, 18))
        self.lbFieldLength = QLabel(self.tab)
        self.lbFieldLength.setObjectName(u"label_4")
        self.lbFieldLength.setGeometry(QRect(570, 80, 91, 18))
        self.lbUnique = QLabel(self.tab)
        self.lbUnique.setObjectName(u"label_5")
        self.lbUnique.setGeometry(QRect(670, 80, 75, 18))
        self.lbNotNull = QLabel(self.tab)
        self.lbNotNull.setObjectName(u"label_6")
        self.lbNotNull.setGeometry(QRect(740, 80, 80, 18))
        self.lbFKTableName = QLabel(self.tab)
        self.lbFKTableName.setObjectName(u"label_8")
        self.lbFKTableName.setGeometry(QRect(820, 80, 110, 18))
        self.lbFKFieldName = QLabel(self.tab)
        self.lbFKFieldName.setObjectName(u"label_9")
        self.lbFKFieldName.setGeometry(QRect(960, 80, 100, 18))
        self.listTable = QListWidget(self.tab)
        self.listTable.setObjectName(u"listTable")
        self.listTable.setGeometry(QRect(20, 110, 210, 280))
        self.EdTableName = QLineEdit(self.tab)
        self.EdTableName.setObjectName(u"EdTableName")
        self.EdTableName.setGeometry(QRect(20, 70, 151, 31))
        self.lbTables = QLabel(self.tab)
        self.lbTables.setObjectName(u"label_7")
        self.lbTables.setGeometry(QRect(20, 50, 49, 16))
        self.BtDeleteTable = QPushButton(self.tab)
        self.BtDeleteTable.setObjectName(u"BtDeleteTable")
        self.BtDeleteTable.setGeometry(QRect(50, 480, 171, 31))
        font11 = QFont()
        font11.setPointSize(11)
        font12 = QFont()
        font12.setPointSize(12)
        self.BtDeleteTable.setFont(font12)
        self.BtAddTable = QPushButton(self.tab)
        self.BtAddTable.setObjectName(u"BtAddTable")
        self.BtAddTable.setGeometry(QRect(170, 70, 31, 31))
        self.BtAddTable.setFont(font16B)
        self.BtGenerate = QPushButton(self.tab)
        self.BtGenerate.setObjectName(u"BtGenerate")
        self.BtGenerate.setGeometry(QRect(20, 540, 280, 50))
        self.BtGenerate.setFont(font14)
        self.BtSaveJson = QPushButton(self.tab)
        self.BtSaveJson.setObjectName(u"BtSaveJson")
        self.BtSaveJson.setGeometry(QRect(320, 440, 300, 41))
        self.BtSaveJson.setFont(font12)
        self.compo=[]
        for icompo in range(10):
            self.compo.append({})
            if icompo>0:
                self.compo[icompo]['BtUp'] = QPushButton(self.tab)
                self.compo[icompo]['BtUp'].setObjectName(u"BtUp_"+str(icompo))
                self.compo[icompo]['BtUp'].setGeometry(QRect(440, 110+icompo*30, 20, 20))


            self.compo[icompo]['Auto'] = QCheckBox(self.tab)
            self.compo[icompo]['Auto'].setObjectName(u"CbAuto_"+str(icompo))
            self.compo[icompo]['Auto'].setGeometry(QRect(255, 110+icompo*30, 15, 20))

            self.compo[icompo]['PK'] = QCheckBox(self.tab)
            self.compo[icompo]['PK'].setObjectName(u"CbPK_"+str(icompo))
            self.compo[icompo]['PK'].setGeometry(QRect(290, 110+icompo*30, 115, 20))

            self.compo[icompo]['FieldName'] = QLineEdit(self.tab)
            self.compo[icompo]['FieldName'].setObjectName(u"EdFieldName_"+str(icompo))
            self.compo[icompo]['FieldName'].setGeometry(QRect(320, 110+icompo*30, 113, 22))
            self.compo[icompo]['FieldName'].setFont(font11)

            self.compo[icompo]['FieldType'] = QComboBox(self.tab)
            self.compo[icompo]['FieldType'].setObjectName(u"CbxFieldType_"+str(icompo))
            self.compo[icompo]['FieldType'].setGeometry(QRect(470, 110+icompo*30, 90, 22))
            self.compo[icompo]['FieldType'].setFont(font11)

            self.compo[icompo]['FieldLength'] = QLineEdit(self.tab)
            self.compo[icompo]['FieldLength'].setObjectName(u"EdFieldLength_"+str(icompo))
            self.compo[icompo]['FieldLength'].setGeometry(QRect(570, 110+icompo*30, 61, 22))

            self.compo[icompo]['Unique'] = QCheckBox(self.tab)
            self.compo[icompo]['Unique'].setObjectName(u"CbUnique_1"+str(icompo))
            self.compo[icompo]['Unique'].setGeometry(QRect(690, 110+icompo*30, 15, 20))

            self.compo[icompo]['NotNull'] = QCheckBox(self.tab)
            self.compo[icompo]['NotNull'].setObjectName(u"CbNotNull_"+str(icompo))
            self.compo[icompo]['NotNull'].setGeometry(QRect(760, 110+icompo*30, 15, 20))

            self.compo[icompo]['FKTable'] = QComboBox(self.tab)
            self.compo[icompo]['FKTable'].setObjectName(u"CbxFKTable_"+str(icompo))
            self.compo[icompo]['FKTable'].setGeometry(QRect(820, 110+icompo*30, 121, 22))

            self.compo[icompo]['FKField'] = QComboBox(self.tab)
            self.compo[icompo]['FKField'].setObjectName(u"CbxFKField_"+str(icompo))
            self.compo[icompo]['FKField'].setGeometry(QRect(960, 110+icompo*30, 111, 22))

        self.tabDbStructure.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.EdResults = QPlainTextEdit(self.tab_2)
        self.EdResults.setObjectName(u"EdResults")
        self.EdResults.setGeometry(QRect(30, 30, 1231, 681))
        self.tabDbStructure.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1293, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabDbStructure.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.LbDriver.setText(QCoreApplication.translate("MainWindow", u"DB Driver : ", None))
        self.LbDBName.setText(QCoreApplication.translate("MainWindow", u"DB Name : ", None))
        self.EdDbDriver.setText(QCoreApplication.translate("MainWindow", u"QSQLITE", None))
        self.EdDatabaseName.setText(QCoreApplication.translate("MainWindow", u"myDbName", None))
        self.BtOpenJson.setText(QCoreApplication.translate("MainWindow", u"Open Json File",None))
        self.lbTables.setText(QCoreApplication.translate("MainWindow", u"Tables", None))
        self.BtDeleteTable.setText(QCoreApplication.translate("MainWindow", u"Remove Table", None))
        self.BtAddTable.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.BtGenerate.setText(QCoreApplication.translate("MainWindow", u"Generate myDbName.py", None))
        self.BtSaveJson.setText(QCoreApplication.translate("MainWindow", "Save this config as myDbName.json", None))
        self.lbAuto.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.lbPK.setText(QCoreApplication.translate("MainWindow", u"PK", None))
        self.lbFieldName.setText(QCoreApplication.translate("MainWindow", u"Field name", None))
        self.lbFieldType.setText(QCoreApplication.translate("MainWindow", u"Field type", None))
        self.lbFieldLength.setText(QCoreApplication.translate("MainWindow", u"Field Length", None))
        self.lbUnique.setText(QCoreApplication.translate("MainWindow", u"Unique ?", None))
        self.lbNotNull.setText(QCoreApplication.translate("MainWindow", u"Not Null ?", None))
        self.lbFKTableName.setText(QCoreApplication.translate("MainWindow", u"FK Table Name", None))
        self.lbFKFieldName.setText(QCoreApplication.translate("MainWindow", u"FK Field Name", None))
        
        self.lbAuto.setVisible(False)

        for icompo in range(10):
            if icompo>0:
                self.compo[icompo]['BtUp'].setText(QCoreApplication.translate("MainWindow", chr(8593),None))
            self.compo[icompo]['Auto'].setText("")
            self.compo[icompo]['Auto'].setVisible(False)
            self.compo[icompo]['PK'].setText("")
            self.compo[icompo]['FieldLength'].setVisible(False)
            self.compo[icompo]['Unique'].setText("")
            self.compo[icompo]['NotNull'].setText("")
            self.compo[icompo]['FKField'].setVisible(False)
            self.compo[icompo]['FieldType'].addItems(self.SqQLiteDataType)


        self.tabDbStructure.setTabText(self.tabDbStructure.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Database Structure", None))
        self.tabDbStructure.setTabText(self.tabDbStructure.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Results", None))
    # retranslateUi

