# Copyright (c) 2004-2005 Nanorex, Inc.  All rights reserved.
"""
ops_atoms.py -- operations on the atoms and/or bonds inside a Part.
These operations generally create or destroy atoms, open bonds, or real bonds.
Operations specific to single modes (Build, Cookie, Extrude) are not included here.

$Id$

History:

bruce 050507 made this by collecting appropriate methods (by various authors)
from existing modules, from class Part and class basicMode.
"""

from HistoryWidget import greenmsg, redmsg
from assembly import SELWHAT_CHUNKS, SELWHAT_ATOMS
from platform import fix_plurals
from elements import Singlet

class ops_atoms_Mixin:
    "Mixin class for providing these methods to class Part"
    
    ###e should modifyTransmute also be brought in here?
    
    def modifyDeleteBonds(self):
        """Delete all bonds between selected and unselected atoms or chunks
        """
        if not self.selatoms and not self.selmols: # optimization, and different status msg
            msg = redmsg("Delete Bonds: Nothing selected")
            self.w.history.message(msg)
            return
        
        self.w.history.message(greenmsg("Delete Bonds:"))
        
        cutbonds = 0
        
        # Delete bonds between selected atoms and their neighboring atoms that are not selected.
        for a in self.selatoms.values():
            for b in a.bonds[:]:
                neighbor = b.other(a)
                if neighbor.element != Singlet:
                    if not neighbor.picked:
                        b.bust()
                        a.pick() # Probably not needed, but just in case...
                        cutbonds += 1

        # Delete bonds between selected chunks and chunks that are not selected.
        for mol in self.selmols[:]:
            # "externs" contains a list of bonds between this chunk and a different chunk
            for b in mol.externs[:]:
                # atom1 and atom2 are the connect atoms in the bond
                if int(b.atom1.molecule.picked) + int(b.atom2.molecule.picked) == 1: 
                    b.bust()
                    cutbonds += 1
                    
        msg = fix_plurals("%d bond(s) deleted" % cutbonds)
        self.w.history.message(msg)
        
        if self.selatoms and cutbonds:
            self.modifySeparate() # Separate the selected atoms into a new chunk
        else:
            self.w.win_update() #e do this in callers instead?
        return

    # change surface atom types to eliminate dangling bonds
    # a kludgey hack
    # bruce 041215 added some comments.
    def modifyPassivate(self):
        if self.selwhat == SELWHAT_CHUNKS:
            for m in self.selmols:
                m.Passivate(True) # arg True makes it work on all atoms in m
        else:
            assert self.selwhat == SELWHAT_ATOMS
            for m in self.molecules:
                m.Passivate() # lack of arg makes it work on only selected atoms
                # (maybe it could just iterate over selatoms... #e)
                
        self.changed() # could be much smarter
        self.o.gl_update()

    # add hydrogen atoms to each dangling bond
    # Changed this method to mirror what modifyDehydrogenate does.
    # It is more informative about the number of chunks modified, etc.
    # Mark 050124
    def modifyHydrogenate(self):
        """Add hydrogen atoms to open bonds on selected chunks/atoms.
        """
        fixmols = {} # helps count modified mols for statusbar
        if self.selmols:
            counta = countm = 0
            for m in self.selmols:
                changed = m.Hydrogenate()
                if changed:
                    counta += changed
                    countm += 1
                    fixmols[id(m)] = m
            if counta:
                didwhat = "Added %d atom(s) to %d chunk(s)" \
                          % (counta, countm)
                if len(self.selmols) > countm:
                    didwhat += \
                        " (%d selected chunk(s) had no open bonds)" \
                        % (len(self.selmols) - countm)
                didwhat = fix_plurals(didwhat)
            else:
                didwhat = "Selected chunks contain no open bonds"    

        elif self.selatoms:
            count = 0
            for a in self.selatoms.values():
                ma = a.molecule
                for atm in a.neighbors():
                    matm = atm.molecule
                    changed = atm.Hydrogenate()
                    if changed:
                        count += 1
                        fixmols[id(ma)] = ma
                        fixmols[id(matm)] = matm
            if fixmols:
                didwhat = \
                    "Added %d atom(s) to %d chunk(s)" \
                    % (count, len(fixmols))
                didwhat = fix_plurals(didwhat)
                # Technically, we *should* say ", affected" instead of "from"
                # since the count includes mols of neighbors of
                # atoms we removed, not always only mols of atoms we removed.
                # Since that's rare, we word this assuming it didn't happen.
                # [#e needs low-pri fix to be accurate in that rare case;
                #  might as well deliver that as a warning, since that case is
                #  also "dangerous" in some sense.]
            else:
                didwhat = "No open bonds on selected atoms"
        else:
            didwhat = "Nothing selected"

        if fixmols:
            self.changed()
            self.w.win_update()
        self.w.history.message(didwhat)
        return

    # Remove hydrogen atoms from each selected atom/chunk
    # (coded by Mark ~10/18/04; bugfixed/optimized/msgd by Bruce same day,
    #  and cleaned up (and perhaps further bugfixed) after shakedown changes
    #  on 041118.)
    def modifyDehydrogenate(self):
        """Remove hydrogen atoms from selected chunks/atoms.
        """
        fixmols = {} # helps count modified mols for statusbar
        if self.selmols:
            counta = countm = 0
            for m in self.selmols:
                changed = m.Dehydrogenate()
                if changed:
                    counta += changed
                    countm += 1
                    fixmols[id(m)] = m
            if counta:
                didwhat = "Removed %d atom(s) from %d chunk(s)" \
                          % (counta, countm)
                if len(self.selmols) > countm:
                    didwhat += \
                        " (%d selected chunk(s) had no hydrogens)" \
                        % (len(self.selmols) - countm)
                didwhat = fix_plurals(didwhat)
            else:
                didwhat = "Selected chunks contain no hydrogens"
        elif self.selatoms:
            count = 0
            for a in self.selatoms.values():
                ma = a.molecule
                for atm in list(a.neighbors()) + [a]:
                    #bruce 041018 semantic change: added [a] as well
                    matm = atm.molecule
                    changed = atm.Dehydrogenate()
                    if changed:
                        count += 1
                        fixmols[id(ma)] = ma
                        fixmols[id(matm)] = matm
            if fixmols:
                didwhat = \
                    "Removed %d atom(s) from %d chunk(s)" \
                    % (count, len(fixmols))
                didwhat = fix_plurals(didwhat)
                # Technically, we *should* say ", affected" instead of "from"
                # since the count includes mols of neighbors of
                # atoms we removed, not always only mols of atoms we removed.
                # Since that's rare, we word this assuming it didn't happen.
                # [#e needs low-pri fix to be accurate in that rare case;
                #  might as well deliver that as a warning, since that case is
                #  also "dangerous" in some sense.]
            else:
                didwhat = "No hydrogens bonded to selected atoms"
        else:
            didwhat = "Nothing selected"
        if fixmols:
            self.changed() #e shouldn't we do this in lower-level methods?
            self.w.win_update()
        self.w.history.message(didwhat)
        return

    pass # end of class ops_atoms_Mixin

# end


