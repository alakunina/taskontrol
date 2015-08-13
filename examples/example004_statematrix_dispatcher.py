#!/usr/bin/env python

'''
This example shows a simple paradigm organized by trials (using dispatcher)
and how to use the statematrix module to assemble the matrix easily.
'''

__author__ = 'Santiago Jaramillo <sjara@uoregon.edu>'
__created__ = '2013-03-18'

import sys
from PySide import QtCore 
from PySide import QtGui 
from taskontrol.settings import rigsettings
from taskontrol.core import dispatcher
from taskontrol.core import statematrix
import signal

class Paradigm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Paradigm, self).__init__(parent)

        # -- Read settings --
        smServerType = rigsettings.STATE_MACHINE_TYPE

        # -- Create dispatcher --
        self.dispatcherModel = dispatcher.Dispatcher(serverType=smServerType,interval=0.3)
        self.dispatcherView = dispatcher.DispatcherGUI(model=self.dispatcherModel)

        # -- Add graphical widgets to main window --
        centralWidget = QtGui.QWidget()
        layoutMain = QtGui.QVBoxLayout()
        layoutMain.addWidget(self.dispatcherView)
        centralWidget.setLayout(layoutMain)
        self.setCentralWidget(centralWidget)
        self.center_in_screen()

        # --- Create state matrix ---
        self.set_state_matrix()

        # -- Connect signals from dispatcher --
        self.dispatcherModel.prepareNextTrial.connect(self.prepare_next_trial)
        self.dispatcherModel.timerTic.connect(self.timer_tic)

    def center_in_screen(self):
        '''Position window in center of screen'''
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_state_matrix(self):
        self.sm = statematrix.StateMatrix(inputs=rigsettings.INPUTS,
                                          outputs=rigsettings.OUTPUTS,
                                          readystate='ready_next_trial')

        # -- Set state matrix --
        self.sm.add_state(name='first_state', statetimer=0.9,
                    transitions={'Cin':'second_state','Tup':'second_state'},
                    outputsOn={'CenterWater'})
        self.sm.add_state(name='second_state', statetimer=2.1,
                    transitions={'Lin':'first_state','Tup':'ready_next_trial'},
                    outputsOff={'CenterWater'})
        print self.sm

        self.dispatcherModel.set_state_matrix(self.sm)

    def prepare_next_trial(self, nextTrial):
        print '\nPrepare trial %d'%nextTrial
        lastTenEvents = self.dispatcherModel.eventsMat[-10:-1]
        print 'Last 10 events:'
        for oneEvent in lastTenEvents:
            print '%0.3f\t %d\t %d'%(oneEvent[0],oneEvent[1],oneEvent[2])
            #print np.array(lastTenEvents)
        self.dispatcherModel.ready_to_start_trial()

    '''
    def start_new_trial(self, currentTrial):
        print '\n======== Started trial %d ======== '%currentTrial
    '''


    def timer_tic(self,etime,lastEvents):
        print '.',
        sys.stdout.flush() # Force printing on the screen at this point


    def closeEvent(self, event):
        '''
        Executed when closing the main window.
        This method is inherited from QtGui.QMainWindow, which explains
        its camelCase naming.
        '''
        self.dispatcherModel.die()
        event.accept()


if __name__ == "__main__":
    #QtCore.pyqtRemoveInputHook() # To stop looping if error occurs (for PyQt not PySide)
    signal.signal(signal.SIGINT, signal.SIG_DFL) # Enable Ctrl-C
    app = QtGui.QApplication(sys.argv)
    paradigm = Paradigm()
    paradigm.show()
    app.exec_()
