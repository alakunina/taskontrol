Defining state transitions
==========================

Let's look at how we can detect events and produce outputs. To do this, we need to define the concept of *state transitions*. At the center of TASKontrol paradigms there is a `finite-state machine (FSM)`_ which controls how outputs (stimuli) change given internal or external events. Here is a summary of what this means:

* The system is in only one state at a time.
* When an event occurs, the system transitions from one state to another.
* Events can be triggered externally (*e.g.*, by a button press) or internally (*e.g.*, by a timer).
* Changes in outputs occur when the system enters a state.

.. _finite-state machine (FSM): https://en.wikipedia.org/wiki/Finite-state_machine


.. We also need to define the concept of trials and DISPATCHER!!!


Adding state transitions and outputs to the paradigm
----------------------------------------------------

The following code shows how we can add states, transitions and outputs to our paradigm. To do this, we override the method ``prepare_next_trial()`` inherited from our template class. Inside this method, which will be called at the each of each trial, we define states (with corresponding outputs) and transitions for each event.

.. code-block:: python
    :linenos:

    from taskontrol.plugins import templates

    class Paradigm(templates.ParadigmMinimal):
        def __init__(self,parent=None):
            super(Paradigm, self).__init__(parent)
            # The parent class defines self.sm and self.dispatcherModel used below.
        
        def prepare_next_trial(self, nextTrial):
            # -- Set state matrix --
            self.sm.add_state(name='wait_for_event', statetimer=100,
                              transitions={'Cin':'light_on'})
            self.sm.add_state(name='light_on', statetimer=2.0,
                              transitions={'Cin':'light_off','Tup':'light_off'},
                              outputsOn=['centerLED'])
            self.sm.add_state(name='light_off', statetimer=0,
                              transitions={'Tup':'ready_next_trial'},
                              outputsOff=['centerLED'])
            self.dispatcherModel.set_state_matrix(self.sm)
            # -- Tell the state machine that we are ready to start --
            self.dispatcherModel.ready_to_start_trial()

    if __name__ == "__main__":
        (app,paradigm) = templates.paramgui.create_app(Paradigm)

In this example, an empty state transition matrix ``self.sm`` is created by the parent class ``templates.ParadigmMinimal`` (line 5). One special state is created at this point (``ready_next_trial``), which should be the final state reached at the end of each trial.

.. note:: In our implementation of the state machine, outputs have *memory* across states. That is, if an output has been turned on in one state, it will remain on until the system reaches a state that sets this output off.

