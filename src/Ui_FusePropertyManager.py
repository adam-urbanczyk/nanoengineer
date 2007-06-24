# Copyright 2004-2007 Nanorex, Inc.  See LICENSE file for details. 
"""
Ui_FusePropertyManager.py
@author: Ninad
@version: $Id$
@copyright:2004-2007 Nanorex, Inc.  All rights reserved.
"""

__author__ = "Ninad"

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.Qt import *
from Utility import geticon, getpixmap
from Ui_MovePropertyManager import Ui_MovePropertyManager
from PropertyManagerMixin import pmAddTopRowButtons, pmMessageGroupBox, pmAddBottomSpacer
from PropMgr_Constants import *

class Ui_FusePropertyManager(Ui_MovePropertyManager):
    def setupUi(self, FusePropertyManager):
        
        self.w = FusePropertyManager.w
        
        FusePropertyManager.setObjectName("FusePropertyManager")
        FusePropertyManager.resize(QtCore.QSize(QtCore.QRect(0,0,200,320).size()).expandedTo(
            FusePropertyManager.minimumSizeHint()))    
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(3),QtGui.QSizePolicy.Policy(3))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FusePropertyManager.sizePolicy().hasHeightForWidth())
        FusePropertyManager.setSizePolicy(sizePolicy)
        
        palette = FusePropertyManager.getPropertyManagerPalette()
        FusePropertyManager.setPalette(palette)
        
        self.pmVBoxLayout = QtGui.QVBoxLayout(FusePropertyManager)
        self.pmVBoxLayout.setMargin(0) # was 1. Mark 2007-05-24.
        self.pmVBoxLayout.setSpacing(0) # was 1. Mark 2007-05-24.
        self.pmVBoxLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.pmVBoxLayout.setObjectName("pmVBoxLayout")
        
        self.heading_frame = QtGui.QFrame(FusePropertyManager)
        self.heading_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.heading_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.heading_frame.setObjectName("heading_frame")
        
        palette2 = QtGui.QPalette()
        palette2.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(10),
                          QtGui.QColor(120,120,120)) #bgrole(10) is 'Windows'
        palette2.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(10),
                          QtGui.QColor(120,120,120)) #bgrole(10) is 'Windows'
        palette2.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(10),
                          QtGui.QColor(120,120,120)) #bgrole(10) is 'Windows'
        self.heading_frame.setAutoFillBackground(True)
        self.heading_frame.setPalette(palette2)

        self.hboxlayout_heading = QtGui.QHBoxLayout(self.heading_frame)
        self.hboxlayout_heading .setMargin(2)
        self.hboxlayout_heading .setSpacing(5)
        self.hboxlayout_heading .setObjectName("hboxlayout")


        self.heading_pixmap = QtGui.QLabel(self.heading_frame)
        self.heading_pixmap.setPixmap(getpixmap('ui/actions/Tools/Build Tools/Fuse_Chunks'))
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.heading_pixmap.sizePolicy().hasHeightForWidth())
        self.heading_pixmap.setSizePolicy(sizePolicy)
        #self.heading_pixmap.setScaledContents(True)
        self.heading_pixmap.setObjectName("heading_pixmap")
        
        self.hboxlayout_heading .addWidget(self.heading_pixmap)
        
        self.heading_label = QtGui.QLabel(self.heading_frame)
	self.heading_label.setFont(getHeaderFont())
	self.heading_label.setAlignment(pmLabelLeftAlignment)
        self.hboxlayout_heading.addWidget(self.heading_label)
        
        self.pmVBoxLayout.addWidget(self.heading_frame)

        self.sponsor_frame = QtGui.QFrame(FusePropertyManager)
        self.sponsor_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.sponsor_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.sponsor_frame.setObjectName("sponsor_frame")

        self.gridlayout_sponsor = QtGui.QGridLayout(self.sponsor_frame)
        self.gridlayout_sponsor.setMargin(0)
        self.gridlayout_sponsor.setSpacing(0)
        self.gridlayout_sponsor.setObjectName("gridlayout")

        self.sponsor_btn = QtGui.QPushButton(self.sponsor_frame)
        self.sponsor_btn.setAutoDefault(False)
        self.sponsor_btn.setFlat(True)
        self.sponsor_btn.setObjectName("sponsor_btn")
        self.gridlayout_sponsor.addWidget(self.sponsor_btn,0,0,1,1)
        
        self.pmVBoxLayout.addWidget(self.sponsor_frame)
        
        pmAddTopRowButtons(FusePropertyManager, 
			   showFlags = pmDoneButton | pmWhatsThisButton)
	
	self.MessageGroupBox = pmMessageGroupBox(self, title="Message")
	self.pmVBoxLayout.addWidget(self.MessageGroupBox)
	pmAddBottomSpacer(self.MessageGroupBox, self.pmVBoxLayout)
	
        self.ui_fuseOptions_groupBox(FusePropertyManager)
	pmAddBottomSpacer(self.fuseOptions_groupBox, self.pmVBoxLayout)
	
        self.ui_translate_groupBox(FusePropertyManager)
	pmAddBottomSpacer(self.translate_groupBox, self.pmVBoxLayout)
	
        self.ui_rotate_groupBox(FusePropertyManager)
	pmAddBottomSpacer(self.rotate_groupBox, self.pmVBoxLayout, last=True)
            
    def ui_fuseOptions_groupBox(self, FusePropertyManager):
        #Start Rotate Options        
        self.fuseOptions_groupBox = QtGui.QGroupBox(FusePropertyManager)
        self.fuseOptions_groupBox.setObjectName("fuseOptions_groupBox")    
        
        self.fuseOptions_groupBox.setAutoFillBackground(True)
        palette = FusePropertyManager.getGroupBoxPalette()
        self.fuseOptions_groupBox.setPalette(palette)
        
        styleSheet = FusePropertyManager.getGroupBoxStyleSheet()        
        self.fuseOptions_groupBox.setStyleSheet(styleSheet)
        
        vlo_fuseOptions_groupBox = QtGui.QVBoxLayout(self.fuseOptions_groupBox)
        vlo_fuseOptions_groupBox.setMargin(0)
        vlo_fuseOptions_groupBox.setSpacing(6)
              
        self.fuseOptions_groupBoxButton = FusePropertyManager.getGroupBoxTitleButton(
            "Fuse Options", self.fuseOptions_groupBox)        
        vlo_fuseOptions_groupBox.addWidget(self.fuseOptions_groupBoxButton)
        
        self.fuseOptions_widgetHolder = QtGui.QWidget(self.fuseOptions_groupBox)
                
        vlo_widgetHolder = QtGui.QVBoxLayout(self.fuseOptions_widgetHolder)
        vlo_widgetHolder.setMargin(2)
        vlo_widgetHolder.setSpacing(6)    
        
        self.fuse_mode_combox = QComboBox(self.fuseOptions_widgetHolder)
        self.fuse_mode_combox.insertItem(0,'Make Bonds Between Chunks') 
        self.fuse_mode_combox.insertItem(1,'Fuse Overlapping Atoms')
        vlo_widgetHolder.addWidget(self.fuse_mode_combox)
        
        self.goPB = QPushButton("Make Bonds",self.fuseOptions_widgetHolder)
	self.goPB.setAutoDefault(False)
        vlo_widgetHolder.addWidget(self.goPB)
        
        self.mergeCB = QCheckBox("Merge chunks", self.fuseOptions_widgetHolder)
        self.mergeCB.setChecked(True)
        vlo_widgetHolder.addWidget(self.mergeCB)
        
        self.tolLB = QLabel()
        self.tolLB.setText(" Tolerance:")
        vlo_widgetHolder.addWidget(self.tolLB)
    
        self.toleranceSL = QSlider(Qt.Horizontal)
        ##self.toleranceSL.setMaximumWidth(150)
        self.toleranceSL.setValue(100)
        self.toleranceSL.setRange(0, 300)
        vlo_widgetHolder.addWidget(self.toleranceSL)
        
        self.toleranceLB = QLabel()
        self.toleranceLB.setText("100% => 0 bondable pairs")
        vlo_widgetHolder.addWidget(self.toleranceLB)
        
        vlo_fuseOptions_groupBox.addWidget(self.fuseOptions_widgetHolder)
        self.pmVBoxLayout.addWidget(self.fuseOptions_groupBox)
        
        spacer_fuseops_grpbx = QtGui.QSpacerItem(
            10,10,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        
        self.pmVBoxLayout.addItem(spacer_fuseops_grpbx)
        
                  
            
    def retranslateUi(self, FusePropertyManager):
        FusePropertyManager.setWindowTitle(QtGui.QApplication.translate("FusePropertyManager", 
                                                                        "FusePropertyManager",
                                                                        None, QtGui.QApplication.UnicodeUTF8))
        self.heading_label.setText(QtGui.QApplication.translate("FusePropertyManager", 
                                                                "<font color=\"#FFFFFF\">Fuse</font>", 
                                                                None, QtGui.QApplication.UnicodeUTF8))
        