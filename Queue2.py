import datetime
import time


class TriggerList:

    def __init__(self):
        self._list = []

    def add_trigger(self, trigger):
        self._list.append(trigger)

    def _clean_list(self):
        new_list = [trigger for trigger in self._list if trigger.should_remain]
        self._list = new_list
        del new_list

    def run(self):
        for trigger in self._list:
            if trigger.satisfied:
                # latch to prevent multiple executions
                if trigger.latch is False:
                    # TODO try execute, handle exceptions
                    trigger.execute()
                trigger.latch = True
            else:
                # unlatch after trigger is over
                trigger.latch = False

        self._clean_list()


class Trigger:
    # trigger only monitors changes in state!  Must know all state changes!
    # default trigger is immediate execution
    def __init__(self, persistent=False):
        # self._item = item
        # self._target_state = target_state
        self._persistent = persistent  # False -> execute once only
        self._latch = False  # True -> skip trigger.  Must reset latch appropriately

    # property must be calculated every loop, otherwise conditions are static
    @property
    def conditions(self):
        return [True, ]

    @property
    def latch(self):
        return self._latch

    @latch.setter
    def latch(self, state):
        self._latch = state

    @property
    def should_remain(self):
        # if already triggered and should not remain
        if self._persistent is False and self._latch is True:
            return False
        else:
            return True

    @property
    def satisfied(self):
        # if all conditions satisfied, do action
        if self.conditions_met:
            return True
        else:
            return False

    # override in child
    @property
    def conditions_met(self):
        return True

    def execute(self):
        pass


class InstantTrigger(Trigger):

    def __init__(self, item, target_state):

        super().__init__(persistent=False)
        self._item = item
        self._target_state = target_state

    @property
    def conditions_met(self):
        return True

    def execute(self):
        self._item.state = self._target_state


class ClockTrigger(Trigger):

    def __init__(self, item, target_state, clock, start_time, end_time, repeat='none'):

        super().__init__(persistent=True)

        if repeat == 'none':
            self._persistent = False
        elif repeat == 'yearly':
            # alter times to yearly
            pass
        elif repeat == 'monthly':
            # alter times to monthly
            pass
        elif repeat == 'weekly':
            # alter times to weekly
            pass
        elif repeat == 'daily':
            # alter times to daily
            pass
        elif repeat == 'hourly':
            # alter times to hourly
            pass
        elif repeat == 'minutely':
            # alter times to every minute
            pass
        elif repeat == 'secondly':
            # alter times to every second
            pass

        self._item = item
        self._target_state = target_state
        self._clock = clock
        self._start_time = start_time
        self._end_time = end_time

    @property
    def conditions_met(self):
        # return True if trigger should be executed
        # now = self._clock.state
        now = datetime.datetime.now().time()

        if self._start_time <= now <= self._end_time:
            return True
        else:
            return False

    def execute(self):
        self._item.state = self._target_state


class OverflowTrigger(Trigger):

    _item_type = FloodZone

    def __init__(self, zone):

        super().__init__(persistent=True)

        if isinstance(zone, OverflowTrigger._item_type) is False:
            raise RuntimeError("This is a trigger for zones only")
        self._zone = zone

    @property
    def conditions_met(self):
        # return True if trigger should be executed
        if self._zone.WaterLevelSensor.state == 'HIGH':
            return True
        else:
            return False

    def execute(self):
        self._zone.state = "MAINTAIN"

if __name__ == '__main__':



    #### Config ####
    trigger_list = TriggerList()

    time1 = (datetime.datetime.now() + datetime.timedelta(seconds=10)).time()
    time2 = (datetime.datetime.now() + datetime.timedelta(seconds=20)).time()
    time3 = (datetime.datetime.now() + datetime.timedelta(seconds=30)).time()

    dummy_item = 4

    task1 = ClockTrigger(dummy_item, time1, time2, repeat='daily')
    task2 = ClockTrigger(dummy_item, time2, time3, repeat='daily')

    trigger_list.add_trigger(task1)
    trigger_list.add_trigger(task2)

    #### event loop ####
    temp = 0
    while True:
        trigger_list.run()
        time.sleep(1)
        print(temp)
        print("task1 latch: " + str(task1.latch))
        print("task1 is_invoked: " + str(task1.satisfied))
        temp += 1
