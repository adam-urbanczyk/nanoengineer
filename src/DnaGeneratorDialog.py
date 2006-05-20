# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DnaGeneratorDialog.ui'
#
# Created: Fri May 19 13:26:17 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


from qt import *


class DnaGeneratorDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("DnaGeneratorDialog")



        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setGeometry(QRect(10,20,90,30))

        self.strandAchkbox = QCheckBox(self,"strandAchkbox")
        self.strandAchkbox.setGeometry(QRect(10,50,80,22))
        self.strandAchkbox.setChecked(1)

        self.seq_linedit = QLineEdit(self,"seq_linedit")
        self.seq_linedit.setGeometry(QRect(100,20,240,24))

        self.strandBchkbox = QCheckBox(self,"strandBchkbox")
        self.strandBchkbox.setGeometry(QRect(260,50,80,22))
        self.strandBchkbox.setChecked(1)

        LayoutWidget = QWidget(self,"layout30")
        LayoutWidget.setGeometry(QRect(10,80,240,50))
        layout30 = QHBoxLayout(LayoutWidget,11,6,"layout30")
        spacer1 = QSpacerItem(92,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout30.addItem(spacer1)

        self.ok_btn = QPushButton(LayoutWidget,"ok_btn")
        self.ok_btn.setMinimumSize(QSize(0,30))
        self.ok_btn.setDefault(1)
        layout30.addWidget(self.ok_btn)

        self.cancel_btn = QPushButton(LayoutWidget,"cancel_btn")
        self.cancel_btn.setMinimumSize(QSize(0,30))
        layout30.addWidget(self.cancel_btn)

        self.languageChange()

        self.resize(QSize(358,161).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.ok_btn,SIGNAL("clicked()"),self.accept)
        self.connect(self.cancel_btn,SIGNAL("clicked()"),self.reject)

        self.setTabOrder(self.ok_btn,self.cancel_btn)


    def languageChange(self):
        self.setCaption(self.__tr("Dna Generator"))
        self.textLabel1.setText(self.__tr("Sequence :"))
        self.strandAchkbox.setText(self.__tr("Strand A"))
        self.seq_linedit.setText(self.__tr("GATTACA"))
        self.strandBchkbox.setText(self.__tr("Strand B"))
        self.ok_btn.setText(self.__tr("&OK"))
        self.ok_btn.setAccel(self.__tr("Alt+O"))
        self.cancel_btn.setText(self.__tr("&Cancel"))
        self.cancel_btn.setAccel(self.__tr("Alt+C"))


    def __tr(self,s,c = None):
        return qApp.translate("DnaGeneratorDialog",s,c)
