import unittest
import time
import datetime

from QueueScheduler import Task, TaskQueue


class TestTaskScheduler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sanity(self):
        self.assertTrue(True)

    def test_task_queue(self):
        queue = TaskQueue()

        time_12am = datetime.time(12, 50, 0)
        time_6am = datetime.time(6, 0, 10)
        time_12pm = datetime.time(12, 0, 20)
        time_5pm = datetime.time(17, 0, 30)
        time_6pm = datetime.time(18, 0, 40)

        task_12am = Task(time_12am, True, print, time_12am.strftime("%I:%M:%S %p"))
        task_6am = Task(time_6am, True, print, time_6am.strftime("%I:%M:%S %p"))
        task_12pm = Task(time_12pm, True, print, time_12pm.strftime("%I:%M:%S %p"))
        task_5pm = Task(time_5pm, False, print, time_5pm.strftime("%I:%M:%S %p"))  # do once
        task_6pm = Task(time_6pm, True, print, time_6pm.strftime("%I:%M:%S %p"))

        queue.add_task(task_12am)
        queue.add_task(task_6am)
        queue.add_task(task_12pm)
        queue.add_task(task_5pm)
        queue.add_task(task_6pm)

        while True:
            queue.run()
            time.sleep(1)


if __name__ == '__main__':
    unittest.main()



