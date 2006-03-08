# Copyright (c) 2004-2006 Nanorex, Inc.  All rights reserved.
"""
whatsthis.py

$Id$
"""

from qt import *

#bruce 051227-29 code for putting hyperlinks into most WhatsThis texts
# (now finished enough for release, though needs testing and perhaps cleanup and documentation)

enable_whatsthis_links = True

debug_whatsthis_links = False # do not commit with True

class MyWhatsThis(QWhatsThis): #bruce 060120 revised this as part of fixing bug 1295, and added docstring
    """QWhatsThis subclass for handling links. Due to quirks in Qt, this is used in two distinct ways:
     1. For most widgets, mainly toolbuttons, they have their own whatsthis text, but that's ignored when they have this
    object attached to them for handling whatsthis; Qt queries it for the text and also calls its clicked method.
    So in this case, this object does two jobs: know the text (with embedded links), and know how to handle link clicks.
     2. For menu items in QPopupMenu, the menu item itself is not a widget, and neither is the QAction it was probably
    made from; neither of those (menu item or QAction) can have a QWhatsThis object of their own. The QPopupMenu can
    have one, but it doesn't know which item to return text for, which doesn't matter anyway because Qt, for some
    reason, never bothers to ask it for the text in the first place. But Qt will let it handle links. So this object
    does only the click handling, and we separately modify the menu item whatsthis text (via their QActions) to contain
    the links.
     1+2. These ways interact as follows: separate code must modify QAction whatsthis text to contain links (so case (2)
    can work), but that same text gets seen on toolbuttons made from those QActions, and modified again (re case (1)).
    So the code to modify the text has to not cause trouble when run twice. See that code (end of this file) for details.
    """
    ## note: doesn't work on QActions (at least for an earlier version of the class with no __init__ method):
    ## MyWhatsThis(self.editCopyAction) ## TypeError: argument 1 of QWhatsThis() has an invalid type
    def __init__(self, widget, text = None):
        QWhatsThis.__init__(self, widget) # this has a side effect of registering self as the whatsthis handler for widget
        self.__text = text # notes: using QString(text) here is ok but not required. text might be None.
        self.__widget = widget # perhaps only used for debug prints
    def text(self, pos):
        # this runs when Qt puts up a WhatsThis help window for widget --
        # but not for QPopupMenu widgets (at least not those in the main menu bar; context menu popups untested).
        if debug_whatsthis_links:
            print "text at pos %r in %r for %r queried by Qt" % (pos, self, self.__widget) # note: pos repr not useful, doesn't show x,y
        text = self.__text
        if not text and debug_whatsthis_links:
            print " no text" # never happens in current calling code [051227] (still true 060120, in theory)
        return text
    def clicked(self, link):
        # this runs when user clicks on a hyperlink in the help text, with 'link' being the link text (href attribute)
        link = str(link) # QString to string (don't know if this is needed, guess yes)
        # note: link is not a real URL, but either false or "Feature:<featurename>"
        # (whether or not wiki_help_url() still hardcodes "Feature:" or some other prefix).
        if link:
            if debug_whatsthis_links:
                print "clicked hyperlink in %r for %r, href text is %r" % (self, self.__widget, link)
            # change link text to URL, and open browser to help page (see wiki_help.py)
            if link.startswith("Feature:"):
                from wiki_help import wiki_help_url, open_wiki_help_URL
                featurename = link[len("Feature:"):]
                    # not exactly the featurename, since we already turned ' ' into '_', but close enough (doing it twice won't hurt)
                url = wiki_help_url( featurename) # presently this just redundantly turns ' ' into '_' and re-prepends "Feature:"
                worked = open_wiki_help_URL(url, whosdoingthis = "What's This link")
                ## close_dialog = worked # let it stay open if it fails (not sure why since it'll go away soon anyway)
                close_dialog = True # close it even on failure so user knows something happened and looks at history
            else:
                print "bug: invalid What's This pseudo-url %r" % link # even if not debug_whatsthis_links
                ## close_dialog = False
                close_dialog = True
        else:
            # happens for clicking any empty part or other text in that popup dialog
            if debug_whatsthis_links:
                print "clicked non-link in %r for %r, text starts %r" % (self, self.__widget, (self.__text or "")[:27])
            close_dialog = True
        return close_dialog # return True to make help text widget go away, or False to keep it around (with no change in contents)
        # hint for debugging 1359: see if returning False helps prevent hangs on Linux. [bruce guess 060120]
    pass # end of class MyWhatsThis

# ===

def createWhatsThis(self):
        
        ##############################################
        # File Toolbar
        ##############################################
        
        #### Open File ####
        
        fileOpenText = "<u><b>Open File</b></u>    (Ctrl + O)</b></p><br> "\
                        "<p><img source=\"fileopen\"><br> "\
                       "Opens a new file."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "fileopen",
                                                       self.fileOpenAction.iconSet().pixmap() )

        self.fileOpenAction.setWhatsThis( fileOpenText )
        
        #### Save File ####
        
        fileSaveText = "<u><b>Save File</b></u>     (Ctrl + S)</b></p><br> "\
                       "<p><img source=\"filesave\"><br> "\
                       "Saves the current file."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "filesave",
                                                       self.fileSaveAction.iconSet().pixmap() )

        self.fileSaveAction.setWhatsThis( fileSaveText )
        
        ##############################################
        # Edit Toolbar
        ##############################################
        
        #### Undo ####
        
        editUndoText =  "<u><b>Undo</b></u>     (Ctrl + Z)</b></p><br> "\
                       "<p><img source=\"editUndo\"><br> "\
                       "Reverses the last edit or command to the active part. "\
                       "<b>Currently not implemented</b>."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "editUndo",
                                                       self.editUndoAction.iconSet().pixmap() )

        self.editUndoAction.setWhatsThis( editUndoText )
        
        #### Redo ####
        
        editRedoText =  "<u><b>Redo</b></u>     (Ctrl + Y)</b></p><br> "\
                       "<p><img source=\"editRedo\"> <br>"\
                       "Re-applies the actions or commands on which you have used "\
                       "the Undo command. <b>Currently not implemented</b>."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "editRedo",
                                                       self.editRedoAction.iconSet().pixmap() )

        self.editRedoAction.setWhatsThis( editRedoText )
        
        #### Cut ####
        
        editCutText =  "<u><b>Cut</b></u>     (Ctrl + X)</b></p><br> "\
                       "<p><img source=\"editCut\"><br> "\
                       "Removes the selected object(s) and stores the cut data on the"\
                       "clipboard."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "editCut",
                                                       self.editCutAction.iconSet().pixmap() )

        self.editCutAction.setWhatsThis( editCutText )
        
        #### Copy ####
        
        editCopyText =  "<u><b>Copy</b></u>     (Ctrl + C)</b></p><br> "\
                       "<p><img source=\"editCopy\"><br> "\
                      "Places a copy of the selected chunk(s) on the clipboard "\
                      "while leaving the original chunk(s) unaffected."\
                      "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "editCopy",
                                                       self.editCopyAction.iconSet().pixmap() )

        self.editCopyAction.setWhatsThis( editCopyText )
        
        #### Paste ####
        
        editPasteText = "<u><b>Paste</b></u>     (Ctrl + V)</b></p><br> "\
                       "<p><img source=\"editPaste\"><br> "\
                       "When selecting this feature, you are placed in "\
                       "<b>Build Atom</b> mode where you may paste copies "\
                       "of clipboard objects into the model where ever you click."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "editPaste",
                                                       self.editPasteAction.iconSet().pixmap() )

        self.editPasteAction.setWhatsThis( editPasteText )
   
        #### Delete ####
                                 
        editDeleteText =  "<u><b>Delete</b></u>     (DEL)</b></p><br> "\
                       "<p><img source=\"editDelete\"><br> "\
                       "Deletes the selected object(s).  "\
                       "For this Alpha release, deleted objects may be permanently lost, or they might be recoverable using Undo.</p>"
            #bruce 060212 revised above text (and fixed spelling error); should be revised again before A7 release
        
        QMimeSourceFactory.defaultFactory().setPixmap( "editDelete",
                                                       self.editDeleteAction.iconSet().pixmap() )

        self.editDeleteAction.setWhatsThis( editDeleteText )
        
        ##############################################
        # View Toolbar
        ##############################################
        
        #### Home View ####
        
        setViewHomeActionText = "<u><b>Home</b></u>     (Home)<br>"\
                       "<p><img source=\"setViewHome\"><br> "\
                       "When you create a new model, it appears in a default view orientation (FRONT view). When you open an existing model, it appears in the orientation it was last saved.  You can change the default orientation by selecting <b>Set Home View to Current View</b> from the <b>View</b> menu.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewHome",
                                                       self.setViewHomeAction.iconSet().pixmap() )

        self.setViewHomeAction.setWhatsThis( setViewHomeActionText )

        #### Fit to Window ####
        
        setViewFitToWindowActionText = "<u><b>Fit To Window</b></u><br>"\
                       "<p><img source=\"setViewFitToWindow\"><br> "\
                       "Refits the model to the screen so you can view the entire model."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewFitToWindow",
                                                       self.setViewFitToWindowAction.iconSet().pixmap() )

        self.setViewFitToWindowAction.setWhatsThis( setViewFitToWindowActionText )   

        #### Recenter ####
        
        setViewRecenterActionText = "<u><b>Recenter</b></u><br>"\
                       "<p><img source=\"setViewRecenter\"><br> "\
                       "Changes the view center and zoom factor so that the origin is in the "\
                       "center of the view and you can view the entire model."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewRecenter",
                                                       self.setViewRecenterAction.iconSet().pixmap() )

        self.setViewRecenterAction.setWhatsThis( setViewRecenterActionText )       
        
        #### Zoom Tool ####
        
        setzoomToolActionText = "<u><b>Zoom Tool</b></u><br>"\
                       "<p><img source=\"setzoomTool\"><br> "\
                       "Allows the user to zoom into a specific area of the model by specifying a rectangular area. "\
                       "This is done by holding down the left button and dragging the mouse.</p>"\
                       "<p>A mouse with a mouse wheel can also be used to zoom in and out "\
                       "at any time, without using the Zoom Tool.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setzoomTool",
                                                       self.zoomToolAction.iconSet().pixmap() )

        self.zoomToolAction.setWhatsThis( setzoomToolActionText )      

        
        #### Pan Tool ####
        
        setpanToolActionText = "<u><b>Pan Tool</b></u><br>"\
                       "<p><img source=\"setpanTool\"><br> "\
                       "Allows X-Y panning using the left mouse button.</p>"\
                       "<p>Users with a 3-button mouse can pan the model at any time by pressing "\
                       "the middle mouse button while holding down the Shift key.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setpanTool",
                                                       self.panToolAction.iconSet().pixmap() )

        self.panToolAction.setWhatsThis( setpanToolActionText )

        
        #### Rotate Tool ####
        
        setrotateToolActionText = "<u><b>Rotate Tool</b></u><br>"\
                       "<p><img source=\"setrotateTool\"><br> "\
                       "Allows free rotation using the left mouse button.</p>"\
                       "<p>Users with a 3-button mouse can rotate the model at any time by pressing "\
                       "the middle mouse button and dragging the mouse.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setrotateTool",
                                                       self.rotateToolAction.iconSet().pixmap() )

        self.rotateToolAction.setWhatsThis( setrotateToolActionText )
        
        #### Orthographic Projection ####
        
        setViewOrthoActionText = "<u><b>Orthographic Projection</b></u><br>"\
                       "<p>Sets nonperspective (or parallel) projection, with no foreshortening."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewOrtho",
                                                       self.setViewOrthoAction.iconSet().pixmap() )

        self.setViewOrthoAction.setWhatsThis( setViewOrthoActionText )

        #### Perspective Projection ####
        
        setViewPerspecActionText = "<u><b>Perspective Projection</b></u><br>"\
                       "<p>Set perspective projection, drawing objects slightly larger "\
                       "that are closer to the viewer."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewPerspec",
                                                       self.setViewPerspecAction.iconSet().pixmap() )

        self.setViewPerspecAction.setWhatsThis( setViewPerspecActionText )        

        #### Normal To ####
        
        setViewNormalToActionText = "<u><b>Set View Normal To</b></u><br>"\
                       "<p><img source=\"setViewNormalTo\"><br> "\
                       "Orients view to the normal vector of the plane defined by "\
                       "3 or more selected atoms, or a jig's axis."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewNormalTo",
                                                       self.setViewNormalToAction.iconSet().pixmap() )

        self.setViewNormalToAction.setWhatsThis( setViewNormalToActionText )
        
        #### Parallel To ####
        
        setViewParallelToActionText = "<u><b>Set View Parallel To</b></u><br>"\
                       "<p><img source=\"setViewParallelTo\"><br> "\
                       "Orients view parallel to the vector defined by 2 selected atoms."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewParallelTo",
                                                       self.setViewParallelToAction.iconSet().pixmap() )

        self.setViewParallelToAction.setWhatsThis( setViewParallelToActionText ) 
        
        #### Save Named View ####
        
        saveNamedViewActionText = "<u><b>Save Named View</b></u><br>"\
                       "<p><img source=\"saveNamedView\"><br> "\
                       "Saves the current view as a custom <b>named view</b> and places it in the Model Tree.</p>" \
                       "<p>The view can be restored by selecting <b>Change View</b> from its context menu in the Model Tree."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "saveNamedView",
                                                       self.saveNamedViewAction.iconSet().pixmap() )

        self.saveNamedViewAction.setWhatsThis( saveNamedViewActionText ) 
        
        
        #### Front View ####
        
        setViewFrontActionText = "<u><b>Front View</b></u><br>"\
                       "<p><img source=\"setViewFront\"><br> "\
                       "Orients the view to the Front View."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewFront",
                                                       self.setViewFrontAction.iconSet().pixmap() )

        self.setViewFrontAction.setWhatsThis( setViewFrontActionText )  

        #### Back View ####
        
        setViewBackActionText = "<u><b>Back View</b></u><br>"\
                       "<p><img source=\"setViewBack\"><br> "\
                       "Orients the view to the Back View."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewBack",
                                                       self.setViewBackAction.iconSet().pixmap() )

        self.setViewBackAction.setWhatsThis( setViewBackActionText )     
        
        #### Top View ####
        
        setViewTopActionText = "<u><b>Top View</b></u><br>"\
                       "<p><img source=\"setViewTop\"><br> "\
                       "Orients the view to the Top View."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewTop",
                                                       self.setViewTopAction.iconSet().pixmap() )

        self.setViewTopAction.setWhatsThis( setViewTopActionText )      
        
        #### Bottom View ####
        
        setViewBottomActionText = "<u><b>Bottom View</b></u><br>"\
                       "<p><img source=\"setViewBottom\"><br> "\
                       "Orients the view to the Bottom View."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewBottom",
                                                       self.setViewBottomAction.iconSet().pixmap() )

        self.setViewBottomAction.setWhatsThis( setViewBottomActionText )  
        
        #### Left View ####
        
        setViewLeftActionText = "<u><b>Left View</b></u><br>"\
                       "<p><img source=\"setViewLeft\"><br> "\
                       "Orients the view to the Left View."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewLeft",
                                                       self.setViewLeftAction.iconSet().pixmap() )

        self.setViewLeftAction.setWhatsThis( setViewLeftActionText )
        
        #### Right View ####
        
        setViewRightActionText = "<u><b>Right View</b></u><br>"\
                       "<p><img source=\"setViewRight\"><br> "\
                       "Orients the view to the Right View."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewRight",
                                                       self.setViewRightAction.iconSet().pixmap() )

        self.setViewRightAction.setWhatsThis( setViewRightActionText )
        
        #### Rotate View 180 ####
        
        setViewOppositeActionText = "<u><b>Rotate View 180</b></u><br>"\
                       "<p><img source=\"setViewOpposite\"><br> "\
                       "Rotates the view 180 degrees."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewOpposite",
                                                       self.setViewOppositeAction.iconSet().pixmap() )

        self.setViewOppositeAction.setWhatsThis( setViewOppositeActionText )
        
        #### Rotate View +90 ####
        
        setViewPlus90ActionText = "<u><b>Rotate View +90</b></u><br>"\
                       "<p><img source=\"setViewPlus90\"><br> "\
                       "Increment the current view by 90 degrees around the vertical axis."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewPlus90",
                                                       self.setViewPlus90Action.iconSet().pixmap() )

        self.setViewPlus90Action.setWhatsThis( setViewPlus90ActionText )
        
        #### Rotate View -90 ####
        
        setViewMinus90ActionText = "<u><b>Rotate View -90</b></u><br>"\
                       "<p><img source=\"setViewMinus90\"><br> "\
                       "Decrement the current view by 90 degrees around the vertical axis."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "setViewMinus90",
                                                       self.setViewMinus90Action.iconSet().pixmap() )

        self.setViewMinus90Action.setWhatsThis( setViewMinus90ActionText )
        
        ##############################################
        # Grids Toolbar
        ##############################################
        
        #### Surface 100 ####
        
        orient100ActionText = "<u><b>Surface 100</b></u><br>"\
                       "<p><img source=\"orient100Action\"><br> "\
                       "Reorients the view to the nearest angle that would "\
                       "look straight into a (1,0,0) surface of a diamond lattice."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "orient100Action",
                                                       self.orient100Action.iconSet().pixmap() )

        self.orient100Action.setWhatsThis(orient100ActionText )
        
        #### Surface 110 ####
        
        orient110ActionText = "<u><b>Surface 110</b></u><br>"\
                       "<p><img source=\"orient110Action\"><br> "\
                       "Reorients the view to the nearest angle that would "\
                       "look straight into a (1,1,0) surface of a diamond lattice."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "orient110Action",
                                                       self.orient110Action.iconSet().pixmap() )

        self.orient110Action.setWhatsThis(orient110ActionText )
        
        #### Surface 111 ####

        orient111ActionText = "<u><b>Surface 111</b></u><br>"\
                       "<p><img source=\"orient111Action\"><br> "\
                       "Reorients the view to the nearest angle that would "\
                       "look straight into a (1,1,1) surface of a diamond lattice."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "orient111Action",
                                                       self.orient111Action.iconSet().pixmap() )

        self.orient111Action.setWhatsThis(orient111ActionText )
        
        ##############################################
        # Molecular Display toolbar
        ##############################################
        
        #### Display Default  ####

        dispDefaultActionText = "<u><b>Display Default</b></u><br>"\
                       "<p><img source=\"dispDefaultAction\"><br> "\
                       "Changes the <i>display setting</i> of selected atoms or chunks to "\
                       "<b>Default</b> , rendering them in the <b>Current Display Mode</b>."\
                       "</p>"\
                       "<p>If no atoms or chunks are selected, then this action will change the "\
                       "<b>Current Display Mode</b> of the 3D workspace to the <b>Default Display Mode</b>. " \
                       "All chunks with their display setting set to <b>Default</b> will be rendered in the "\
                       "<b>Default Display Mode</b>."\
                       "</p>"\
                       "<p>The <b>Default Display Mode</b> can be changed via the "\
                       "<b>Edit > Preferences</b> menu and selecting the <b>General</b> tab."\
                       "</p>"\
                       "<p>The <b>Current or Default Display Mode</b> is displayed in the status bar in the "\
                       "lower right corner of the main window."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "dispDefaultAction",
                                                       self.dispDefaultAction.iconSet().pixmap() )

        self.dispDefaultAction.setWhatsThis(dispDefaultActionText )
 
        #### Display Invisible ####

        dispInvisActionText = "<u><b>Display Invisible</b></u><br>"\
                       "<p><img source=\"dispInvisAction\"><br> "\
                       "Changes the <i>display setting</i> of selected atoms or chunks to "\
                       "<b>Invisible</b>, making them invisible."\
                       "</p>"\
                       "<p>If no atoms or chunks are selected, then this action will change the "\
                       "<b>Current Display Mode</b> of the 3D workspace to <b>Invisible</b>. " \
                       "All chunks with their display setting set to <b>Default</b> will inherit "\
                       "this display property."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "dispInvisAction",
                                                       self.dispInvisAction.iconSet().pixmap() )

        self.dispInvisAction.setWhatsThis(dispInvisActionText )       

        #### Display Lines ####

        dispLinesActionText = "<u><b>Display Lines</b></u><br>"\
                       "<p><img source=\"dispLinesAction\"><br> "\
                       "Changes the <i>display setting</i> of selected atoms or chunks to "\
                       " <b>Lines</b>.  Only bonds are rendered as colored lines."\
                       "</p>"\
                       "<p>If no atoms or chunks are selected, then this action will change the "\
                       "<b>Current Display Mode</b> of the 3D workspace to <b>Lines</b>. " \
                       "All chunks with their display setting set to <b>Default</b> will inherit "\
                       "this display property."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "dispLinesAction",
                                                       self.dispLinesAction.iconSet().pixmap() )

        self.dispLinesAction.setWhatsThis(dispLinesActionText )  
        
        #### Display Tubes ####

        dispTubesActionText = "<u><b>Display Tubes</b></u><br>"\
                       "<p><img source=\"dispTubesAction\"><br> "\
                       "Changes the <i>display setting</i> of selected atoms or chunks to "\
                       "<b>Tubes</b>.  Atoms and bonds are rendered as colored tubes."\
                       "</p>"\
                       "<p>If no atoms or chunks are selected, then this action will change the "\
                       "<b>Current Display Mode</b> of the 3D workspace to <b>Tubes</b>. " \
                       "All chunks with their display setting set to <b>Default</b> will inherit "\
                       "this display property."\
                       "</p>"


        QMimeSourceFactory.defaultFactory().setPixmap( "dispTubesAction",
                                                       self.dispTubesAction.iconSet().pixmap() )

        self.dispTubesAction.setWhatsThis(dispTubesActionText )  
        
        #### Display Ball and Stick (was CPK) ####

        dispCPKActionText = "<u><b>Display Ball and Stick</b></u><br>"\
                       "<p><img source=\"dispCPKAction\"><br> "\
                       "Changes the <i>display setting</i> of selected atoms or chunks to "\
                       "<b>Ball and Stick</b> mode.  Atoms are rendered "\
                       "as spheres and bonds are rendered as narrow cylinders."\
                       "</p>"\
                       "<p>If no atoms or chunks are selected, then this action will change the "\
                       "<b>Current Display Mode</b> of the 3D workspace to <b>Ball and Stick</b>. " \
                       "All chunks with their display setting set to <b>Default</b> will inherit "\
                       "this display property."\
                       "</p>"\
                       "<p>The scale of the spheres and cylinders can be changed from the "\
                       "<b>Atoms</b> and <b>Bonds</b> pages of the <b>Preferences</b> dialog."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "dispCPKAction",
                                                       self.dispCPKAction.iconSet().pixmap() )

        self.dispCPKAction.setWhatsThis(dispCPKActionText ) 
        
        #### Display CPK (was VdW) ####

        dispVdWActionText = "<u><b>Display CPK</b></u><br>"\
                       "<p><img source=\"dispVdWAction\"><br> "\
                       "Changes the <i>display setting</i> of selected atoms or chunks to "\
                       "<b>CPK</b> mode.  Atoms are rendered as spheres with "\
                       "a size equal to the VdW radius.  Bonds are not rendered."\
                       "</p>"\
                       "<p>If no atoms or chunks are selected, then this action will change the "\
                       "<b>Current Display Mode</b> of the 3D workspace to <b>CPK</b>. " \
                       "All chunks with their display setting set to <b>Default</b> will inherit "\
                       "this display property."\
                       "</p>"
                      
        QMimeSourceFactory.defaultFactory().setPixmap( "dispVdWAction",
                                                       self.dispVdWAction.iconSet().pixmap() )

        self.dispVdWAction.setWhatsThis(dispVdWActionText )         
        
        ##############################################
        # Select toolbar
        ##############################################
        
        #### Select All ####

        selectAllActionText = "<u><b>Select All</b></u>     (Ctrl + A)</b></p><br>"\
                       "<p><img source=\"selectAllAction\"><br> "\
                       "During <b>Select Atoms</b> mode, this will select all the atoms in "\
                       "the model.  Otherwise, this will select all the chunks in the model."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "selectAllAction",
                                                       self.selectAllAction.iconSet().pixmap() )

        self.selectAllAction.setWhatsThis(selectAllActionText )
        
        #### Select None ####

        selectNoneActionText = "<u><b>Select None</b></u></p><br>"\
                       "<p><img source=\"selectNoneAction\"><br> "\
                       "Unselects everything currently selected.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "selectNoneAction",
                                                       self.selectNoneAction.iconSet().pixmap() )

        self.selectNoneAction.setWhatsThis(selectNoneActionText )
 
        #### Invert Selection ####

        selectInvertActionText = "<u><b>Invert Selection</b></u> <br>    (Ctrl + Shift + I)</b></p><br>"\
                       "<p><img source=\"selectInvertAction\"><br> "\
                       "Inverts the current selection.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "selectInvertAction",
                                                       self.selectInvertAction.iconSet().pixmap() )

        self.selectInvertAction.setWhatsThis(selectInvertActionText )
        
        #### Select Connected ####

        selectConnectedActionText = "<u><b>Select Connected</b></u>     (Ctrl + Shift + C)</b></p><br>"\
            "<p><img source=\"selectConnectedAction\"><br> "\
            "Selects all the atoms that can be reached by the currently selected atom "\
            "via an unbroken chain of bonds. </p>"\
            "<p>To use this feature, you must first be in "\
            "<b>Select Atoms</b> mode and select at least one atom.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "selectConnectedAction",
                                                       self.selectConnectedAction.iconSet().pixmap() )

        self.selectConnectedAction.setWhatsThis(selectConnectedActionText )
        
        #### Select Doubly ####

        selectDoublyActionText = "<u><b>Select Doubly</b></u></b></p><br>"\
                       "<p><img source=\"selectDoublyAction\"><br> "\
                       "Selects all the atoms that can be reached from a currently selected "\
                       "atom through two disjoint unbroken chains of bonds.  Atoms singly "\
                       "connected to this group and unconnected to anything else are also "\
                       "included in the selection.</p>"\
                       "<p>To use this feature, you must first be in "\
                       "<b>Select Atoms</b> mode and select at least one atom.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "selectDoublyAction",
                                                       self.selectDoublyAction.iconSet().pixmap() )

        self.selectDoublyAction.setWhatsThis(selectDoublyActionText )
        
        #### Expand Selection ####

        selectExpandActionText = "<u><b>Expand Selection</b></u>    (Ctrl + D)</b></p><br>"\
                       "<p><img source=\"selectExpandAction\"><br> "\
                       "Selects any atom that is a neighbor of a currently selected atom."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "selectExpandAction",
                                                       self.selectExpandAction.iconSet().pixmap() )

        self.selectExpandAction.setWhatsThis(selectExpandActionText )
        
        #### Contract Selection ####

        selectContractActionText = "<u><b>Contract Selection</b></u>    (Ctrl + Shift + D)</b></p><br>"\
                       "<p><img source=\"selectContractAction\"><br> "\
                       "Deselects any atom that is a neighbor of a non-picked atom or has a bondpoint."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "selectContractAction",
                                                       self.selectContractAction.iconSet().pixmap() )

        self.selectContractAction.setWhatsThis(selectContractActionText )
        
        ##############################################
        # Modify Toolbar
        ##############################################
        
        #### Minimize Selection ####

        modifyMinimizeSelActionText = "<u><b>Minimize Selection</b></u>    (Ctrl + M)</b></p><br>"\
                       "<p><img source=\"modifyMinimizeSelAction\"><br> "\
                       "Arranges the atoms (<i>of the current selection</i>) to their chemically stable point of "\
                       "equilibrium in reference to the other atoms in the structure."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "modifyMinimizeSelAction",
                                                       self.modifyMinimizeSelAction.iconSet().pixmap() )

        self.modifyMinimizeSelAction.setWhatsThis(modifyMinimizeSelActionText )
        
        #### Minimize All ####

        modifyMinimizeAllActionText = "<u><b>Minimize All</b></u></p><br>"\
                       "<p><img source=\"modifyMinimizeAllAction\"><br> "\
                       "Arranges the atoms (<i>of the entire part</i>) to their chemically stable point of "\
                       "equilibrium in reference to the other atoms in the structure."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "modifyMinimizeAllAction",
                                                       self.modifyMinimizeAllAction.iconSet().pixmap() )

        self.modifyMinimizeAllAction.setWhatsThis(modifyMinimizeAllActionText )
        
        #### Hydrogenate ####

        modifyHydrogenateActionText = "<u><b>Hydrogenate</b></u> </b></p><br>"\
                       "<p><img source=\"modifyHydrogenateAction\"><br> "\
                       "Adds hydrogen atoms to all the bondpoints in the selection.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "modifyHydrogenateAction",
                                                       self.modifyHydrogenateAction.iconSet().pixmap() )

        self.modifyHydrogenateAction.setWhatsThis(modifyHydrogenateActionText )

        #### Dehydrogenate ####

        modifyDehydrogenateActionText = "<u><b>Dehydrogenate</b></u><br>"\
                       "<p><img source=\"modifyDehydrogenateAction\"><br> "\
                       "Removes all hydrogen atoms from the selection.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "modifyDehydrogenateAction",
                                                       self.modifyDehydrogenateAction.iconSet().pixmap() )

        self.modifyDehydrogenateAction.setWhatsThis(modifyDehydrogenateActionText )     
        
        #### Passivate ####

        modifyPassivateActionText = "<u><b>Passivate</b></u>    (Ctrl + P)</b></p><br>"\
                       "<p><img source=\"modifyPassivateAction\"><br> "\
                       "Changes the types of incompletely bonded atoms to atoms with the "\
                       "right number of bonds, using atoms with the best atomic radius."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "modifyPassivateAction",
                                                       self.modifyPassivateAction.iconSet().pixmap() )

        self.modifyPassivateAction.setWhatsThis(modifyPassivateActionText )
        
        #### Stretch ####

        modifyStretchActionText = "<u><b>Stretch</b></u><br>"\
                       "<p><img source=\"modifyStretchAction\"><br> "\
                       "Stretches the bonds of the selected chunk(s).</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "modifyStretchAction",
                                                       self.modifyStretchAction.iconSet().pixmap() )

        self.modifyStretchAction.setWhatsThis(modifyStretchActionText )

        #### Delete Bonds ####

        modifyDeleteBondsActionText = "<u><b>Delete Bonds</b></u><br>"\
                       "<p><img source=\"modifyDeleteBondsAction\"><br> "\
                       "Delete all bonds between selected and unselected atoms or chunks.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "modifyDeleteBondsAction",
                                                       self.modifyDeleteBondsAction.iconSet().pixmap() )

        self.modifyDeleteBondsAction.setWhatsThis(modifyDeleteBondsActionText )  
        
        #### Separate ####

        modifySeparateActionText = "<u><b>Separate</b></u><br>"\
                       "<p><img source=\"modifySeparateAction\"><br> "\
                       "Creates a new chunk from the currently selected atoms.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "modifySeparateAction",
                                                       self.modifySeparateAction.iconSet().pixmap() )

        self.modifySeparateAction.setWhatsThis(modifySeparateActionText )  
        
        #### Merge Chunks ####

        modifyMergeActionText = "<u><b>Merge Chunks</b></u><br>"\
                       "<p><img source=\"modifyMergeAction\"><br> "\
                       "Merges two or more chunks into a single chunk.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "modifyMergeAction",
                                                       self.modifyMergeAction.iconSet().pixmap() )
       
        self.modifyMergeAction.setWhatsThis(modifyMergeActionText )  
                
        #### Invert Chunks ####

        modifyInvertActionText = "<u><b>Invert</b></u><br>"\
                       "<p><img source=\"modifyInvertAction\"><br> "\
                       "Inverts the atoms of the selected chunks.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "modifyInvertAction",
                                                       self.modifyInvertAction.iconSet().pixmap() )
       
        self.modifyInvertAction.setWhatsThis(modifyInvertActionText )  

        #### Align to Common Axis ####

        modifyAlignCommonAxisActionText = "<u><b>Align To Common Axis</b></u><br>"\
                       "<p><img source=\"modifyAlignCommonAxis\"><br> "\
                       "Aligns one or more chunks to the axis of the first selected chunk."\
                       "You must select two or more chunks before using this feature."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "modifyAlignCommonAxis",
                                                       self. modifyAlignCommonAxisAction.iconSet().pixmap() )
       
        self. modifyAlignCommonAxisAction.setWhatsThis( modifyAlignCommonAxisActionText )
                
        ##############################################
        # Tools Toolbar
        ##############################################
        
        #### Select Chunks ####

        toolsSelectMoleculesActionText = "<u><b>Select Chunks</b></u><!-- [[Feature:Select Chunks Mode]] --><br>"\
                       "<p><img source=\" toolsSelectMoleculesAction\"><br> "\
                       "<b>Select Chunks</b> allows you to select/unselect chunks with the mouse.</p>"\
                       "<p><b><u>Mouse/Key Combinations</u></b></p>"\
                       "<p><b>Left Click/Drag</b> - selects a chunk(s).</p>"\
                       "<p><b>Ctrl+Left Click/Drag</b> - removes chunk(s) from selection.</p>"\
                       "<p><b>Shift+Left Click/Drag</b> - adds chunk(s) to selection."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " toolsSelectMoleculesAction",
                                                       self. toolsSelectMoleculesAction.iconSet().pixmap() )
       
        self. toolsSelectMoleculesAction.setWhatsThis( toolsSelectMoleculesActionText )  

        #### Select Atoms ####

        toolsSelectAtomsActionText = "<u><b>Select Atoms</b></u><!-- [[Feature:Select Atoms Mode]] --><br>"\
                       "<p><img source=\" toolsSelectAtomsAction\"><br> "\
                       "<b>Select Atoms</b> allows you to select/unselect atoms with the mouse.</p>"\
                       "<p><b><u>Mouse/Key Combinations</u></b></p>"\
                       "<p><b>Left Click/Drag</b> - selects an atom(s).</p>"\
                       "<p><b>Ctrl+Left Click/Drag</b> - removes atom(s) from selection.</p>"\
                       "<p><b>Shift+Left Click/Drag</b> - adds atom(s) to selection."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " toolsSelectAtomsAction",
                                                       self. toolsSelectAtomsAction.iconSet().pixmap() )
       
        self. toolsSelectAtomsAction.setWhatsThis( toolsSelectAtomsActionText ) 
        
        #### Move Chunks ####

        toolsMoveMoleculeActionText = "<u><b>Move Chunks</b></u><!-- [[Feature:Move Chunks Mode]] --><br>"\
                       "<p><img source=\" toolsMoveMoleculeAction\"><br> "\
                       "Activates <b>Move Chunks</b> mode, allowing you to select, "\
                       "move and rotate one of more chunks with the mouse.</p>"\
                       "<p><b><u>Mouse/Key Combinations</u></b></p>"\
                       "<p><b>Left Drag</b> - moves the selected chunk(s).</p>"\
                       "<p><b>Ctrl+Left Drag</b> - freely rotates selected chunk(s).</p>"\
                       "<p><b>Shift+Left Drag</b> - constrained movement and rotation of a chunk about its own axis."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " toolsMoveMoleculeAction",
                                                       self. toolsMoveMoleculeAction.iconSet().pixmap() )
       
        self. toolsMoveMoleculeAction.setWhatsThis( toolsMoveMoleculeActionText ) 
        
        #### Build Atoms Tool ####

        toolsDepositAtomActionText = "<u><b>Build Tool</b></u><!-- [[Feature:Build Mode]] --><br>"\
                       "<p><img source=\" toolsDepositAtomAction\"><br> "\
                       "<b>Build Mode</b> allows you to build structures by depositing objects "\
                       "from the Molecular Modeling Kit, including atoms, clipboard objects and parts "\
                       "from the nanoENGINEER-1 Library.</p>"\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " toolsDepositAtomAction",
                                                       self. toolsDepositAtomAction.iconSet().pixmap() )
       
        self. toolsDepositAtomAction.setWhatsThis( toolsDepositAtomActionText ) 
        
        #### Cookie Cutter ####
                                        
        toolsCookieCutActionText = "<u><b>Cookie Cutter Tool</b></u><!-- [[Feature:Cookie Cutter Mode]] --><br>"\
                       "<p><><img source=\" toolsCookieCutAction\"><br> "\
                       "Activates <b>Cookie Cutter</b> mode, allowing you to cut out 3-D shapes from a "\
                       "slab of diamond or lonsdaleite lattice.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " toolsCookieCutAction",
                                                       self. toolsCookieCutAction.iconSet().pixmap() )
       
        self. toolsCookieCutAction.setWhatsThis( toolsCookieCutActionText )
       
        #### Extrude Tool ####

        toolsExtrudeActionText = "<u><b>Extrude Tool</b></u><!-- [[Feature:Extrude Mode]] --><br>"\
                       "<p><img source=\" toolsExtrudeAction\"><br> "\
                       "Activates <b>Extrude</b> mode, allowing you to create a rod or ring using a chunk as "\
                       "a repeating unit.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " toolsExtrudeAction",
                                                       self. toolsExtrudeAction.iconSet().pixmap() )
       
        self. toolsExtrudeAction.setWhatsThis( toolsExtrudeActionText )  
        
        #### Fuse Chunks Tool ####

        toolsFuseChunksActionText = "<u><b>Fuse Chunks Tool</b></u><!-- [[Feature:Fuse Chunks Mode]] --><br>"\
                       "<p><img source=\" toolsFuseChunksAction\"><br> "\
                       "<b>Fuse Chunks</b> can be used to interactively join two or more "\
                       "chunks by dragging chunks around and fusing them together.  "\
                       "Two types of fusing are supported:<br><br>"\
                       "<b>Make Bonds</b> creates bonds between the existing bondpoints) "\
                       "of two or more chunks.  Bonds are drawn (and undrawn) as chunks "\
                       "are moved together (and apart).<br><br>"\
                       "<b>Fuse Atoms</b> fuses overlapping atoms between chunks. Overlapping "\
                       "pairs of atoms are highlighted in green and blue to indicate which atoms "\
                       "will be fused.<br>"\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " toolsFuseChunksAction",
                                                       self. toolsFuseChunksAction.iconSet().pixmap() )
       
        self.toolsFuseChunksAction.setWhatsThis( toolsFuseChunksActionText )
        
        #### Fuse Atoms Tool ####

        toolsFuseAtomsActionText = "<u><b>Fuse Atoms Tool</b></u><!-- [[Feature:Fuse Atoms Mode]] (nim?) --><br>"\
                       "<p><img source=\" toolsFuseAtomsAction\"><br> "\
                       "<b>Fuse Atoms</b> fuses the overlapping atoms between two or more chunks.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " toolsFuseAtomsAction",
                                                       self. toolsFuseAtomsAction.iconSet().pixmap() )
       
        self.toolsFuseAtomsAction.setWhatsThis( toolsFuseAtomsActionText )  

        #### Movie Player ####

        simMoviePlayerActionText = "<u><b>Movie Player</b></u><br>"\
                       "<p><img source=\" simMoviePlayerAction\"><br> "\
                       "Plays the most recent trajectory (movie) file created by the <b>Simulator</b>.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " simMoviePlayerAction",
                                                       self. simMoviePlayerAction.iconSet().pixmap() )
       
        self. simMoviePlayerAction.setWhatsThis( simMoviePlayerActionText )  
        
        #### Simulator ####

        simSetupActionText = "<u><b>Simulator</b></u><br>"\
                       "<p><img source=\" simSetupAction\"><br> "\
                       "Creates a trajectory (movie) file by calculating the inter-atomic potentials and bonding "\
                       "of the entire model.  The user determines the number of frames in the movie, the time step, "\
                       "and the temperature for the simulation.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " simSetupAction",
                                                       self. simSetupAction.iconSet().pixmap() )
       
        self. simSetupAction.setWhatsThis( simSetupActionText )

        #### Plot Tool ####

        simPlotToolActionText = "<u><b>Plot Tool</b></u><br>"\
                       "<p><img source=\" simPlotToolAction\"><br> "\
                       "Plots a simulator trace file using GNUplot.  A simulation must be run to create "\
                       "the trace file, and the part must have a jig that writes output to the trace file. <br><br>"\
                       "The following list of jigs write data to the trace file:<br>"\
                       "<b>Rotary Motors:</b> speed (GHz) and torque (nn-nm)<br>"\
                       "<b>Linear Motors:</b> displacement (pm)<br>"\
                       "<b>Anchors:</b> torque (nn-nm)<br>"\
                       "<b>Thermostats:</b> energy added (zJ)<br>"\
                       "<b>Thermometer:</b> temperature (K)<br>"\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " simPlotToolAction",
                                                       self. simPlotToolAction.iconSet().pixmap() )
       
        self. simPlotToolAction.setWhatsThis( simPlotToolActionText )
                
        ##############################################
        # Dashboard Buttons
        ##############################################
        
        #### Done ####

        toolsDoneActionText = "<u><b>Done</b></u><br>"\
                       "<p><img source=\" toolsDoneAction\"><br> "\
                       "Completes the current operation and enters Select Chunks mode."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " toolsDoneAction",
                                                       self. toolsDoneAction.iconSet().pixmap() )
       
        self. toolsDoneAction.setWhatsThis( toolsDoneActionText )  

        #### Cancel ####

        toolsCancelActionText = "<u><b>Cancel</b></u><br>"\
                       "<p><img source=\" toolsCancelAction\"><br> "\
                       "Cancels the current operation and enters Select Chunks mode."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " toolsCancelAction",
                                                       self.toolsCancelAction.iconSet().pixmap() )
       
        self. toolsCancelAction.setWhatsThis( toolsCancelActionText ) 
        
        #### Back up ####

        toolsBackUpActionText = "<u><b>Back Up</b></u><br>"\
                       "<p><img source=\" toolsBackUpAction\"><br> "\
                       "Undoes the previous operation."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( " toolsBackUpAction",
                                                       self.toolsBackUpAction.iconSet().pixmap() )
       
        self. toolsBackUpAction.setWhatsThis( toolsBackUpActionText ) 
   
        #### Start Over ####
                        
        toolsStartOverActionText = "<u><b>Start Over</b></u><br>"\
                       "<p><img source=\"toolsStartOverAction\"><br> "\
                       "Cancels the current operation, leaving the user in the current mode."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "toolsStartOverAction",
                                                       self.toolsStartOverAction.iconSet().pixmap() )
       
        self.toolsStartOverAction.setWhatsThis(toolsStartOverActionText ) 
        
        #### Add Layers ####
                        
        ccAddLayerActionText = "<u><b>Add Layer</b></u><br>"\
                       "<p><img source=\"ccAddLayerAction\"><br> "\
                       "Adds a new layer of diamond lattice to the existing layer."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "ccAddLayerAction",
                                                       self.ccAddLayerAction.iconSet().pixmap() )
       
        self.ccAddLayerAction.setWhatsThis(ccAddLayerActionText ) 
        
        ##############################################
        # Jigs
        ##############################################
        
        #### Anchor ####

        jigsAnchorActionText = "<u><b>Anchor</b></u><br>"\
                       "<p><img source=\"jigsAnchorAction\"><br> "\
                       "Attaches a <b>Anchor</b> to the selected atom(s), which "\
                       "constrains its motion during a minimization or simulation."\
                       "</p>"\
                       "<p>To create an Anchor, enter <b>Select Atoms</b> mode, "\
                       "select the atom(s) you want to anchor and then select this action. "\
                       "Anchors are drawn as a black wireframe box around each selected atom."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "jigsAnchorAction",
                                                       self.jigsAnchorAction.iconSet().pixmap() )
       
        self.jigsAnchorAction.setWhatsThis(jigsAnchorActionText )  
        
        #### Rotary Motor ####

        jigsMotorActionText = "<u><b>Rotary Motor</b></u><br>"\
                       "<p><img source=\"jigsMotorAction\"><br> "\
                       "Attaches a <b>Rotary Motor</b> to the selected atoms.  The Rotary Motor is used by "\
                       "the simulator to apply rotary motion to a set of atoms during a simulation run.  You may "\
                       "specify the <b>torque (in nN*nm)</b> and <b>speed (in Ghz)</b> of the motor."\
                       "</p>"\
                       "<p>To create a Rotary Motor, enter <b>Select Atoms</b> mode, "\
                       "select the atoms you want to attach the motor to and then select this action."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "jigsMotorAction",
                                                       self.jigsMotorAction.iconSet().pixmap() )
       
        self.jigsMotorAction.setWhatsThis(jigsMotorActionText )  
        
        #### Linear Motor ####

        jigsLinearMotorActionText = "<u><b>Linear Motor</b></u><br>"\
                       "<p><img source=\"jigsLinearMotorAction\"><br> "\
                       "Attaches a <b>Linear Motor</b> to the selected atoms.  The Linear Motor is used by "\
                       "the simulator to apply linear motion to a set of atoms during a simulation run.  You may "\
                       "specify the <b>force (in nN*nm)</b> and <b>stiffness (in N/m)</b> of the motor."\
                       "</p>"\
                       "<p>To create a Linear Motor, enter <b>Select Atoms</b> mode, "\
                       "select the atoms you want to attach the motor to and then select this action."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "jigsLinearMotorAction",
                                                       self.jigsLinearMotorAction.iconSet().pixmap() )
       
        self.jigsLinearMotorAction.setWhatsThis(jigsLinearMotorActionText )  
        
        #### Thermostat ####

        jigsStatActionText = "<u><b>Thermostat</b></u><br>"\
                       "<p><img source=\"jigsStatAction\"><br> "\
                       "Attaches a <b>Langevin Thermostat</b> to a single selected atom, thereby associating "\
                       "the themostat to the entire molecule of which the selected atom is a member. The user "\
                       "specifies the temperature (in Kelvin)."\
                       "</p>"\
                       "<p>The Langevin Thermostat is used to set and hold the temperature "\
                       "of a molecule during a simulation run."\
                       "</p>"\
                       "<p>To create a Langevin Thermostat, enter <b>Select Atoms</b> mode, "\
                       "select a single atom and then select this action. The thermostat is drawn as a "\
                       "blue wireframe box around the selected atom."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "jigsStatAction",
                                                       self.jigsStatAction.iconSet().pixmap() )
       
        self.jigsStatAction.setWhatsThis(jigsStatActionText ) 

        #### Thermometer ####

        jigsThermoActionText = "<u><b>Thermometer</b></u><br>"\
                       "<p><img source=\"jigsThermoAction\"><br> "\
                        "Attaches a <b>Thermometer</b> to a single selected atom, thereby associating "\
                       "the themometer to the entire molecule of which the selected atom is a member. "\
                       "<p>The temperature of the molecule will be recorded and written to a trace file "\
                       "during a simulation run."\
                       "</p>"\
                       "<p>To create a Thermometer, enter <b>Select Atoms</b> mode, "\
                       "select a single atom and then select this action. The thermometer is drawn as a "\
                       "dark red wireframe box around the selected atom."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "jigsThermoAction",
                                                       self.jigsThermoAction.iconSet().pixmap() )
       
        self.jigsThermoAction.setWhatsThis(jigsThermoActionText )
        
        #### ESP Image ####
        
        jigsESPImageActionText = "<u><b>ESP Image</b></u></b></p><br>"\
                       "<p><img source=\"jigsESPImageAction\"><br> "\
                        "An <b>ESP Image</b> allows the user to visualize the electrostatic potential "\
                        "of points on the face of a square 2D surface. Nano-Hive's MPQC ESP Plane plug-in "\
                        "is used to calculate the electrostatic potential."\
                       "</p>"\
                       "<p>To create an ESP Image, enter <b>Select Atoms</b> mode, "\
                       "select three or more atoms and then select this jig. The ESP Image is drawn as a "\
                       "plane with a bounding volume."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "jigsESPImageAction",
                                                       self.jigsESPImageAction.iconSet().pixmap() )
       
        self.jigsESPImageAction.setWhatsThis(jigsESPImageActionText )
        
        #### Atom Set ####
        
        jigsAtomSetActionText = "<u><b>Atom Set</b></u></b></p><br>"\
                       "<p><img source=\"jigsAtomSetAction\"><br> "\
                        "An <b>Atom Set</b> jig provides a convienient way to save an atom "\
                        "selection which can be reselected later."\
                       "</p>"\
                       "<p>To create an Atom Set, enter <b>Select Atoms</b> mode, "\
                       "select any number of atoms and then select this jig. The Atom Set is "\
                       "drawn as a set of wireframe boxes around each atom in the selection."\
                       "</p>"\
                       "<p>To reselect the atoms in an Atom Set, select it's context "\
                       "menu in the Model Tree and click the menu item that states "\
                       "<b>Select this jig's atoms</b>."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "jigsAtomSetAction",
                                                       self.jigsAtomSetAction.iconSet().pixmap() )
       
        self.jigsAtomSetAction.setWhatsThis(jigsAtomSetActionText )
        
        #### Measure Distance ####
        
        jigsDistanceActionText = "<u><b>Measure Distance Jig</b></u></b></p><br>"\
                       "<p><img source=\"jigsDistanceAction\"><br> "\
                        "A <b>Measure Distance Jig</b> functions as a dimension to display the "\
                        "distance between two atoms."\
                       "</p>"\
                       "<p>To create the Measure Distance Jig, enter <b>Select Atoms</b> mode, "\
                       "select two atoms and then select this jig. The Measure Distance Jig is "\
                       "drawn as a pair of wireframe boxes around each atom connected by "\
                       "a line and a pair of numbers.  The first number is the distance between the "\
                       "VdW radii (this can be a negative number for atoms that are close together). "\
                       "The second number is the distance between the nuclei."\
                       "</p>"\
                       "<p>The Measure Distance Jig will write the two distance values to the trace file "\
                       "for each frame of a simulation run and can be plotted using the Plot Tool."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "jigsDistanceAction",
                                                       self.jigsDistanceAction.iconSet().pixmap() )
       
        self.jigsDistanceAction.setWhatsThis(jigsDistanceActionText )
        
        #### Measure Angle ####
        
        jigsAngleActionText = "<u><b>Measure Angle Jig</b></u></b></p><br>"\
                       "<p><img source=\"jigsAngleAction\"><br> "\
                        "A <b>Measure Angle Jig</b> functions as a dimension to display the "\
                        "angle between three atoms.</p>"\
                       "<p>To create the Measure Angle Jig, enter <b>Select Atoms</b> mode, "\
                       "select three atoms and then select this jig. The Measure Angle Jig is "\
                       "drawn as a set of wireframe boxes around each atom and a number "\
                       "which is the angle between the three atoms."\
                       "</p>"\
                       "<p>The Measure Angle Jig will write the angle value to the trace file "\
                       "for each frame of a simulation run and can be plotted using the Plot Tool."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "jigsAngleAction",
                                                       self.jigsAngleAction.iconSet().pixmap() )
       
        self.jigsAngleAction.setWhatsThis(jigsAngleActionText )
        
        #### Measure Dihedral ####
        
        jigsDihedralActionText = "<u><b>Measure Dihedral Jig</b></u></b></p><br>"\
                       "<p><img source=\"jigsDihedralAction\"><br> "\
                        "A <b>Measure Dihedral Jig</b> functions as a dimension to display the "\
                        "dihedral angle of a four atom sequence.</p>"\
                       "<p>To create the Measure Dihedral Jig, enter <b>Select Atoms</b> mode, "\
                       "select four atoms and then select this jig. The Measure Dihedral Jig is "\
                       "drawn as a set of wireframe boxes around each atom and a number "\
                       "which is the dihedral angle value."\
                       "</p>"\
                       "<p>The Measure Dihedral Jig will write the dihedral angle value to the trace file "\
                       "for each frame of a simulation run and can be plotted using the Plot Tool."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "jigsDihedralAction",
                                                       self.jigsDihedralAction.iconSet().pixmap() )
       
        self.jigsDihedralAction.setWhatsThis(jigsDihedralActionText )
        
        #### GAMESS Jig ####
        
        jigsGamessActionText = "<u><b>GAMESS Jig</b></u></b></p><br>"\
                       "<p><img source=\"jigsGamessAction\"><br> "\
                        "A <b>GAMESS Jig</b> is used to tag a set of atoms for running a GAMESS "\
                        "calculation. <b>Energy</b> and <b>Geometry Optimization</b> calculations are supported."\
                        "</p>"\
                        "<p>To create the GAMESS Jig, enter <b>Select Atoms</b> mode, "\
                        "select the atoms to tag and then select this jig. The GAMESS Jig is drawn as a "\
                        "set of magenta wireframe boxes around each atom."\
                        "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "jigsGamessAction",
                                                       self.jigsGamessAction.iconSet().pixmap() )
       
        self.jigsGamessAction.setWhatsThis(jigsGamessActionText )
        
        #### Grid Plane Jig ####
        
        jigsGridPlaneActionText = "<u><b>Grid Plane</b></u></b></p><br>"\
                       "<p><img source=\"jigsGridPlaneAction\"><br> "\
                        "A <b>Grid Plane</b> jig is a rectanglar plane that can display a square or SiC grid "\
                        "within its boundary. It is often used as an aid in constructing large lattice "\
                        "structures made of silicon carbide (SiC).  It is also used as a visual aid in estimating "\
                        "distances between atoms and/or other structures."\
                        "</p>"\
                        "<p>To create the Grid Plane jig, enter <b>Select Atoms</b> mode, "\
                        "select three or more atoms and then select this jig. "\
                        "</p>"\
                        "<p>The Grid Plane jig is drawn as a rectanglar plane with a grid."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "jigsGridPlaneAction",
                                                       self.jigsGridPlaneAction.iconSet().pixmap() )
       
        self.jigsGridPlaneAction.setWhatsThis(jigsGridPlaneActionText )
        
        ##############################################
        # Display
        ##############################################
        
        #### Display Object Color ####

        dispObjectColorActionText = "<u><b>Object Color</b></u><br>"\
                       "<p><img source=\"dispObjectColorAction\"><br> "\
                       "Allows you to change the color of the selected object(s).</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "dispObjectColorAction",
                                                       self.dispObjectColorAction.iconSet().pixmap() )
       
        self.dispObjectColorAction.setWhatsThis(dispObjectColorActionText ) 
        
        #### Display Background Color ####

        dispBGColorActionText = "<u><b>Background Color</b></u><br>"\
                       "<p><img source=\"dispBGColorAction\"><br> "\
                       "Allows you to change the background color of the main window.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "dispBGColorAction",
                                                       self.dispBGColorAction.iconSet().pixmap() )
       
        self.dispBGColorAction.setWhatsThis(dispBGColorActionText ) 
       
        ##############################################
        # Help Toolbar
        ##############################################
        
        #### What's This ####
        
        helpWhatsThisText = "<u><b>What's This</b></u><br>"\
                        "<p><img source=\"helpWhatsThis\"><br> "\
                       "Click this option to invoke a small question mark that is attached to the mouse pointer. "\
                       "Click on a feature which you would like more information about. "\
                       "A popup box appears with information about the feature.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "helpWhatsThis",
                                                       self.helpWhatsThisAction.iconSet().pixmap() )

        self.helpWhatsThisAction.setWhatsThis( helpWhatsThisText )
        

        ##############################################
        # Datum Display Toolbar
        ##############################################
        
        #### Display Trihedron ####

        dispTrihedronText = "<u><b>Display Trihedron</b></u><br>"\
                       "<p><img source=\"dispTrihedron\"><br> "\
                       "Toggles the trihedron on and off.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "dispTrihedron",
                                                       self.dispTrihedronAction.iconSet().pixmap() )
       
        self.dispTrihedronAction.setWhatsThis(dispTrihedronText ) 

        #### Display Csys ####

        dispCsysText = "<u><b>Display Csys Axis</b></u><br>"\
                       "<p><img source=\"dispCsys\"><br> "\
                       "Toggles the coordinate system axis on and off."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "dispCsys",
                                                       self.dispCsysAction.iconSet().pixmap() )
       
        self.dispCsysAction.setWhatsThis(dispCsysText ) 
        
        #### Display Datum Lines ####

        dispDatumLinesText = "<u><b>Display Datum Lines</b></u><br>"\
                       "<p><img source=\"dispDatumLines\"><br> "\
                       "Toggles Datum Lines on and off.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "dispDatumLines",
                                                       self.dispDatumLinesAction.iconSet().pixmap() )
       
        self.dispDatumLinesAction.setWhatsThis(dispDatumLinesText )    

        #### Display Datum Planes ####

        dispDatumPlanesText = "<u><b>Display Datum Planes</b></u><br>"\
                       "<p><img source=\"dispDatumPlanes\"><br> "\
                       "Toggles Datum Planes on and off.</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "dispDatumPlanes",
                                                       self.dispDatumPlanesAction.iconSet().pixmap() )
       
        self.dispDatumPlanesAction.setWhatsThis(dispDatumPlanesText )    
        
        #### Display Grid ####

        dispGridText = "<u><b>Display 3-D Grid</b></u><br>"\
                       "<p><img source=\"dispGrid\"><br> "\
                       "Toggles the 3-D grid on and off."\
                       "</p>"

        QMimeSourceFactory.defaultFactory().setPixmap( "dispGrid",
                                                       self.dispGridAction.iconSet().pixmap() )
       
        self.dispGridAction.setWhatsThis(dispGridText )           

def create_whats_this_descriptions_for_selectAtomsMode(w):
    "Create What's This descriptions for the Select Atoms mode dashboard widgets."
    
    #### Element Selector ####

    eSelectorText = "<u><b>Element Selector</b></u><br>"\
                       "<p><img source=\"eselectoricon\"><br> "\
                       "Opens the <b>Element Selector</b>, which aids in atom selection when the "\
                       "<b>Selection Filter</b> is activated."\
                       "</p>"\
                       "<p>It also contains a <b>Transmute</b> button, which allows the user to change the "\
                       "selected atoms to the current atom type (in the Element Selector)."\
                       "</p>"

    QMimeSourceFactory.defaultFactory().setPixmap( "eselectoricon",
                                                       w.modifySetElementAction.iconSet().pixmap() )
       
    w.modifySetElementAction.setWhatsThis(eSelectorText )
    
    # Filter Checkbox #
    
    filterText = "<u><b>Selection Filter</b></u><br> "\
                        "When turned on, only atoms of the current atom type are selected."\
                        "</p>"

    #QWhatsThis.add ( w.filterCheckBox, filterText )
    
    # Atom Type Combobox #
    
    elemFilterText = "<u><b>Atom Type</b></u><br> "\
                        "Decides the type of atoms that will be selected while performing select atoms operation in the 3D workspace. \
Example: if this combobox is showing 'Carbon' as the element type, only carbon atoms will be selected when 'select atoms' operation is performed the next time \
in the 3 D workspace."\
"</p>"
                        
    QWhatsThis.add ( w.elemFilterComboBox, elemFilterText)
    
def create_whats_this_descriptions_for_depositMode(w):
    "Create What's This descriptions for the deposit (Build) mode dashboard widgets."
    
    #### Modeling Kit ####

    mmkitText = "<u><b>Modeling Kit</b></u><br>"\
                       "<p><img source=\"mmkiticon\"><br> "\
                       "Opens the Modeling Kit, which aids in atom and clipboard selection."\
                       "</p>"

    QMimeSourceFactory.defaultFactory().setPixmap( "mmkiticon",
                                                       w.modifyMMKitAction.iconSet().pixmap() )
       
    w.modifyMMKitAction.setWhatsThis(mmkitText )
        
    # Deposit (Atom) button
    
    depositText = "<u><b>Deposit Atom</b></u><br> "\
                        "<p><img source=\"eyedroppericon\"><br> "\
                        "Sets <i>Deposit Atom</i> mode."\
                        "</p>"

    QMimeSourceFactory.defaultFactory().setPixmap( "eyedroppericon",
                        w.depositAtomDashboard.depositBtn.iconSet().pixmap() )

    QWhatsThis.add ( w.depositAtomDashboard.depositBtn, depositText )
    
    # Paste button
    
    pasteText = "<u><b>Paste from Clipboard</b></u><br> "\
                        "<p><img source=\"clipboardicon\"><br> "\
                        "Sets <i>Paste</i> mode."\
                        "</p>"

    QMimeSourceFactory.defaultFactory().setPixmap( "clipboardicon",
                        w.depositAtomDashboard.pasteBtn.iconSet().pixmap() )

    QWhatsThis.add ( w.depositAtomDashboard.pasteBtn, pasteText )
    
    # Build Atoms button
    
    buildAtomsText = "<u><b>Build Mode</b></u><br> "\
                        "<p><img source=\"buildatomsicon\"><br> "\
                        "Sets <i>Build</i> mode.  Double clicking on empty space deposits an object from the MMKit. "\
                        "Clicking on a bondpoint will deposit an atom or other MMKit object on the bondpoint if the object has a hotspot."\
                        "</p>"

    QMimeSourceFactory.defaultFactory().setPixmap( "buildatomsicon",
                        w.depositAtomDashboard.buildBtn.iconSet().pixmap() )

    QWhatsThis.add ( w.depositAtomDashboard.buildBtn, buildAtomsText )
    
    # Single Bond button
    
    singleBondText = "<u><b>Single Bond Mode</b></u><br> "\
                        "<p><img source=\"singlebondicon\"><br> "\
                        "Sets <i>Single Bond</i> mode.  Clicking on a highlighted bond "\
                        "will change the bond to a single bond, if permitted."\
                        "</p>"

    QMimeSourceFactory.defaultFactory().setPixmap( "singlebondicon",
                        w.depositAtomDashboard.bond1Btn.iconSet().pixmap() )

    QWhatsThis.add ( w.depositAtomDashboard.bond1Btn, singleBondText )
    
    # Double Bond button
    
    doubleBondText = "<u><b>Double Bond Mode</b></u><br> "\
                        "<p><img source=\"doublebondicon\"><br> "\
                        "Sets <i>Double Bond</i> mode.  Clicking on a highlighted bond "\
                        "will change the bond to a double bond, if permitted."\
                        "</p>"

    QMimeSourceFactory.defaultFactory().setPixmap( "doublebondicon",
                        w.depositAtomDashboard.bond2Btn.iconSet().pixmap() )

    QWhatsThis.add ( w.depositAtomDashboard.bond2Btn, doubleBondText )
    
    # Triple Bond button
    
    tripleBondText = "<u><b>Triple Bond Mode</b></u><br> "\
                        "<p><img source=\"triplebondicon\"><br> "\
                        "Sets <i>Triple Bond</i> mode.  Clicking on a highlighted bond "\
                        "will change the bond to a triple bond, if permitted."\
                        "</p>"

    QMimeSourceFactory.defaultFactory().setPixmap( "triplebondicon",
                        w.depositAtomDashboard.bond3Btn.iconSet().pixmap() )

    QWhatsThis.add ( w.depositAtomDashboard.bond3Btn, tripleBondText )
    
    # Aromatic Bond button
    
    aromaticBondText = "<u><b>Aromatic Bond Mode</b></u><br> "\
                        "<p><img source=\"aromaticbondicon\"><br> "\
                        "Sets <i>Aromatic Bond</i> mode.  Clicking on a highlighted bond "\
                        "will change the bond to an aromatic bond, if permitted."\
                        "</p>"

    QMimeSourceFactory.defaultFactory().setPixmap( "aromaticbondicon",
                        w.depositAtomDashboard.bondaBtn.iconSet().pixmap() )

    QWhatsThis.add ( w.depositAtomDashboard.bondaBtn, aromaticBondText )
    
    # Graphitic Bond button
    
    graphiticBondText = "<u><b>Graphitic Bond Mode</b></u><br> "\
                        "<p><img source=\"graphiticbondicon\"><br> "\
                        "Sets <i>Graphitic Bond</i> mode.  Clicking on a highlighted bond "\
                        "will change the bond to a graphitic bond, if permitted."\
                        "</p>"

    QMimeSourceFactory.defaultFactory().setPixmap( "graphiticbondicon",
                        w.depositAtomDashboard.bondgBtn.iconSet().pixmap() )

    QWhatsThis.add ( w.depositAtomDashboard.bondgBtn, graphiticBondText )
    
    # Autobond checkbox
    
    autoBondText = "<u><b>Autobond</b></u><br> "\
                        "Enables/disables <b>Autobonding</b><br> "\
                        "<br> When <b>enabled</b>, additional bonds are formed "\
                        "<b>automatically</b> with the deposited atom  if any "\
                        "bondpoints of neighboring atoms fall within the VdW radius, "\
                        "and the deposited atom has extra bonds available.<br>"\
                        "<br>When <b>disabled</b>, the deposited atom will form only one "\
                        "bond <b>manually</b> with the bondpoint selected by the user."\
                        "</p>"

    QWhatsThis.add ( w.depositAtomDashboard.autobondCB, autoBondText )
    
    autoBondTipText = "Enables/disables 'Autobonding'"

    QToolTip.add(w.depositAtomDashboard.autobondCB, autoBondTipText)
    
    # Water checkbox
    
    waterText = "<u><b>Water</b></u><br> "\
                        "Enables/disables the <b>Water Surface</b> selection filter<br> "\
                        "<br>When <b>enabled</b>, a semi-transparent water surface is displayed."\
                        "The water surface serves as a selection filter.  Only atoms and bonds above "\
                        "the surface are highlighted and pickable.<br>"\
                        "<br>The depth of the water surface can be changed by holding down the Shift+Control/Command "\
                        "keys and then pressing the middle mouse button and dragging the mouse up "\
                        "and down."\
                        "</p>"

    QWhatsThis.add ( w.depositAtomDashboard.waterCB, waterText )
    
    waterTipText = "Enables/disables the 'Water Surface' selection filter"

    QToolTip.add(w.depositAtomDashboard.waterCB, waterTipText)
    
    # Highlighting checkbox
    
    highlightingText = "<u><b>Highlighting</b></u><br> "\
                        "Enables/disables <b>Hover Highlighting</b><br> "\
                        "<br>When <b>enabled</b>, atoms and bonds under the cursor "\
                        "are highlighted to indicate what would be selected if the user clicks "\
                        "the left mouse button.<br>"\
                        "<br>The highlighting color for atoms and bonds can be changed "\
                        "by selecting <b>Edit > Preferences</b> and clicking on the <b>Atoms</b> "\
                        "or <b>Bonds</b> tab."\
                        "</p>"

    QWhatsThis.add ( w.depositAtomDashboard.highlightingCB, highlightingText )
    
    highlightingTipText = "Enables/disables 'Hover Highlighting'"

    QToolTip.add(w.depositAtomDashboard.highlightingCB, highlightingTipText)
    

def create_whats_this_descriptions_for_UserPrefs_dialog(w):
    "Create What's This descriptions for the User Prefs dialog widgets."

    #### Bond Line Thickness ####

    bondThicknessText = "<u><b>Bond Thickness</b></u><br>"\
                       "Sets the <i>Bond Thickness</i> (in pixels) for Lines Display Mode."\
                       "This will also affect the thickness of bonds where atoms or chunks "\
                       "have been set to <b>Lines</b> display."\
                       "</p>"
       
    QWhatsThis.add ( w.bond_line_thickness_spinbox, bondThicknessText )

def create_whats_this_descriptions_for_NanoHive_dialog(w):
    "Create What's This descriptions for the Nano-Hive dialog widgets."
    
    #### MPQC Electrostatics Potential Plane ####

    MPQCESPText = "<u><b>MPQC Electrostatics Potential Plane</b></u><br>"\
                       "Enables the <i>MPQC Electrostatics Potential Plane</i> plugin. "\
                       "</p>"
       
    QWhatsThis.add ( w.MPQC_ESP_checkbox, MPQCESPText )
    
    MPQCESPTipText = "Enables/disables MPQC Electrostatics Potential Plane Plugin"

    QToolTip.add(w.MPQC_ESP_checkbox, MPQCESPTipText)

# ===

_actions = {} # map from QActions to the featurenames in their whatsthis text [bruce 060121 to help with Undo]

def fix_whatsthis_text_for_mac(parent):
    #bruce 051227-29 revised this; now it's misnamed and needs renaming ###@@@
    #bruce 060120 revised this as part of fixing bug 1295
    """MISNAMED: does things for all OSes, not just macs. This should be 
    called after all widgets (and their whatsthis text) in the UI have been created.
    It does two things:
    1. If the system is a Mac, this replaces all occurrences of 'Ctrl' with 'Cmd' in all the 
    whatsthis text for all QAction or QWidget objects that are children of parent.  
    2. For all systems, it replaces certain whatsthis text patterns with hyperlinks,
    and adds MyWhatsThis objects to widgets with text modified that way (or that might contain hyperlinks)
    or that are QPopupMenus.
    """
    from platform import is_macintosh
    mac = is_macintosh()
    if mac or enable_whatsthis_links:
        # fix text in 1 or 2 ways for all QAction objects (which are not widgets)
        objList = parent.queryList("QAction")
        for obj in objList:
            text = str(obj.whatsThis())
            if mac:
                text = replace_ctrl_with_cmd(text)
            if enable_whatsthis_links:
                text = turn_featurenames_into_links(text, savekey = id(obj), saveplace = _actions )
            obj.setWhatsThis(text)
    if enable_whatsthis_links:
        # add MyWhatsThis objects to all widgets that might need them
        # (and also fix their text if it's not fixed already --
        #  needed in case it didn't come from a QAction; maybe that never happens as of 060120)
        objList = parent.queryList("QWidget")
            # this includes QMenuBar, QPopupMenu for each main menu and cmenu (I guess),
            # but not menuitems themselves. (No hope of including dynamic cmenu items, but since
            # we make those, we could set their whatsthis text and process it the same way
            # using separate code (nim ###@@@).) [bruce 060120]
            # In fact there is no menu item class in Qt that I can find! You add items as Actions or as sets of attrs.
            # Actions also don't show up in this list...
        for obj in objList:
            text = whatsthis_text_for_widget(obj) # could be either "" or None
            if text:
                # in case text doesn't come from a QAction, modify it in the same ways as above,
                # and store it again or pass it to the MyWhatsThis object;
                # both our mods are ok if they happen twice -- if some hyperlink contains 'ctrl',
                # so did the text before it got command names converted to links.
                if mac:
                    text = replace_ctrl_with_cmd(text)
                text = turn_featurenames_into_links(text)
                assert text # we'll just feed it to a MyWhatsThis object so we don't have to store it here
            else:
                text = None # turn "" into None
            if text or isinstance(obj, QPopupMenu):
                # assume any text (even if not changed here) might contain hyperlinks,
                # so any widget with text might need a MyWhatsThis object;
                # the above code (which doesn't bother storing mac-modified text) also assumes we're doing this
                give_widget_MyWhatsThis_and_text( obj, text)
            continue
    return # from (misnamed) fix_whatsthis_text_for_mac
    
def replace_ctrl_with_cmd(text): # by mark; might be wrong for text which uses Ctrl in unexpected ways
    "Replace all occurrences of Ctrl with Cmd in the given string."
    text = text.replace('Ctrl', 'Cmd')
    text = text.replace('ctrl', 'cmd')
    return text

_KEEPERS = [] # keep permanent refs to certain objects we create

def whatsthis_text_for_widget(widget): #bruce 060120 split this out of other code
    "Return a Python string containing the WhatsThis text for widget (perhaps ""), or None if we can't find that."
    try:
        ## original_text = widget.whatsThis() # never works for widgets (though it would work for QActions)
        text = QWhatsThis.textFor( widget) # often a null string, often an exception; don't know if it can be a QString
    except:
        # this happens for a lot of QObjects (don't know what they are), e.g. for <constants.qt.QObject object at 0xb96b750>
        return None
    else:
        return str( text or "" )
            # note: the 'or ""' above is in case we got None (probably never needed, but might as well be safe)
            # note: the str() (in case of QString) might not be needed; during debug it seemed this was already a Python string
    pass

def give_widget_MyWhatsThis_and_text(widget, text): #bruce 051229; renamed 060120
    obj1 = MyWhatsThis( widget, text)
    ## widget._KEEP_WHATSTHIS = obj1 # this was not sufficient to prevent a bus error
    _KEEPERS.append(obj1) # this is needed to prevent a bus error
    return

def debracket(text, left, right): #bruce 051229 ##e refile this?
    """If text contains (literal substrings) left followed eventually by right (without another occurrence of left),
    return the triple (before, between, after)
    where before + left + between + right + after == text. Otherwise return None.
    """
    splitleft = text.split(left, 1)
    if len(splitleft) < 2: return None # len should never be more than 2
    before, t2 = splitleft
    splitright = t2.split(right, 1)
    if len(splitright) < 2: return None
    between, after = splitright
    assert before + left + between + right + after == text
    if left in between: return None # not sure we found the correct 'right' in this case
    return (before, between, after)
    
def turn_featurenames_into_links(text, savekey = None, saveplace = None): #bruce 051229; revised and renamed 060120; save args 060121
    """Given some nonempty whatsthis text, return identical or modified text (e.g. containing a web help URL).
    If savekey and saveplace are passed, and if the text contains a featurename, set saveplace[savekey] to that featurename.
    """
    # look for words between <u><b> and </b></u> to replace with a web help link
    if text.startswith("<u><b>"): # require this at start, not just somewhere like debracket would
        split1 = debracket(text, "<u><b>", "</b></u>")
        if split1:
            junk, name, rest = split1
            featurename = name # might be changed below
            if "[[Feature:" in rest: # it's an optim to test this first, since usually false
                # Extract feature name to use in the link, when this differs from name shown in WhatsThis text;
                # this name is usually given in an HTML comment but we use it w/o modifying the text whether or not it's in one.
                # We use it in the link but not in the displayed WhatsThis text.
                split2 = debracket(rest, "[[Feature:", "]]")
                if not split2:
                    print "syntax error in Feature: link for WhatsThis text for %r" % name
                    return text
                junk, featurename, junk2 = split2
            #e should verify featurename is one or more capitalized words sep by ' '; could use split, isalpha (or so) ###@@@
            if debug_whatsthis_links:
                if featurename != name:
                    print "web help name for %r: %r" % (name, featurename,)
                else:
                    print "web help name: %r" % (featurename,)
            if saveplace is not None:
                saveplace[savekey] = featurename
            link = "Feature:" + featurename.replace(' ','_')
                # maybe we can't let ' ' remain in it, otherwise replacement not needed since will be done later anyway
            return "<a href=\"%s\">%s</a>" % (link, name) + rest # featurename will be made into URL later (url prefix varies at runtime)
    return text

# end