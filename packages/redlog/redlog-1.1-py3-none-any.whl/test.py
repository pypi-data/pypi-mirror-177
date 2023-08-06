from redlog import Log, Tag, Thread

import time
import unittest
from redis import Redis


DB_HOST = "localhost"
DB_PORT = 6379
DB_INDEX = 15


class LogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = Redis(DB_HOST, DB_PORT, db=DB_INDEX)

    def test_basic(self):
        """ Basic logging test """
        self.db.flushdb()
        log = Log(DB_HOST, DB_PORT, db=DB_INDEX, retention_time=1)
        # push
        test_messages = ["Yeah!", "", "qwerty"]
        for msg in test_messages:
            log.info(msg)
        # pop and compare
        msg = None
        for msg in log.read_day():
            now = time.time()
            self.assertTrue(now - 1 < msg.timestamp <= now)
            self.assertEqual(msg.tag, Tag.INFO)
            self.assertEqual(msg.content, test_messages.pop(0))
            self.assertTrue(msg.is_last)
            self.assertIsNone(msg.pred)
        self.assertIsNotNone(msg)   # to make sure we ever enter the loop
        # expiration
        time.sleep(1.1)
        for _ in log.read_day():
            self.fail("Some messages are not expired in the log")

    def test_chaining(self):
        """ Log message updating """
        self.db.flushdb()
        log = Log(DB_HOST, DB_PORT, db=DB_INDEX)
        # push
        msg = log.info("info")
        msg.warning("warn")
        log.info("another info!")
        msg.error("error")
        # check
        messages = list(log.read_day())
        self.assertEqual(len(messages), 4)
        # - content
        self.assertEqual(messages[0].content, "info")
        self.assertEqual(messages[1].content, "warn")
        self.assertEqual(messages[2].content, "another info!")
        self.assertEqual(messages[3].content, "error")
        # - tag
        self.assertEqual(messages[0].tag, Tag.INFO)
        self.assertEqual(messages[1].tag, Tag.WARNING)
        self.assertEqual(messages[2].tag, Tag.INFO)
        self.assertEqual(messages[3].tag, Tag.ERROR)
        # - update number
        self.assertEqual(messages[0].update_number, 0)
        self.assertEqual(messages[1].update_number, 1)
        self.assertEqual(messages[2].update_number, 0)
        self.assertEqual(messages[3].update_number, 2)
        # - is last
        self.assertFalse(messages[0].is_last)
        self.assertFalse(messages[1].is_last)
        self.assertTrue(messages[2].is_last)
        self.assertTrue(messages[3].is_last)
        # - predecessors
        self.assertIsNone(messages[0].pred)
        self.assertEqual(messages[1].pred, messages[0])
        self.assertIsNone(messages[2].pred)
        self.assertIsNotNone(messages[3].pred, messages[2])

    def test_chaining_past_date(self):
        """ Log message updating across dates """
        self.db.flushdb()
        log = Log(DB_HOST, DB_PORT, db=DB_INDEX)
        # push
        msg = log.info("info")
        # cheat: change the date to past
        self.assertTrue(hasattr(msg, 'key'))
        newkey, _ = Thread._get_key(time.time() - 1234567)
        self.db.rename(msg.key, newkey)
        msg.key = newkey
        # push more
        msg.info("another info!")
        log.warning("warn")
        msg.error("error")
        # check
        messages = list(log.read_day())
        self.assertEqual(len(messages), 3)
        # - predecessors
        self.assertIsNone(messages[0].pred.pred)
        self.assertIsNotNone(messages[0].pred)
        self.assertIsNone(messages[1].pred)
        self.assertEqual(messages[2].pred, messages[0])
        # - content
        self.assertEqual(messages[0].pred.content, "info")
        self.assertEqual(messages[0].content, "another info!")
        self.assertEqual(messages[1].content, "warn")
        self.assertEqual(messages[2].content, "error")
        # - tag
        self.assertEqual(messages[0].pred.tag, Tag.INFO)
        self.assertEqual(messages[0].tag, Tag.INFO)
        self.assertEqual(messages[1].tag, Tag.WARNING)
        self.assertEqual(messages[2].tag, Tag.ERROR)
        # - update number
        self.assertEqual(messages[0].pred.update_number, 0)
        self.assertEqual(messages[0].update_number, 1)
        self.assertEqual(messages[1].update_number, 0)
        self.assertEqual(messages[2].update_number, 2)
        # - is last
        self.assertFalse(messages[0].pred.is_last)
        self.assertFalse(messages[0].is_last)
        self.assertTrue(messages[1].is_last)
        self.assertTrue(messages[2].is_last)

    def test_flushed_logs_before_update(self):
        """ Flushing logs before updating a message """
        # push
        self.db.flushdb()
        log = Log(DB_HOST, DB_PORT, db=DB_INDEX)
        msg = log.info("info")
        self.db.flushdb()
        msg.info("new info")
        # check
        for n, msg in enumerate(log.read_day()):
            self.assertEqual(n, 0)
            self.assertIsNone(msg.pred)
            self.assertEqual(msg.content, "new info")
            self.assertEqual(msg.tag, Tag.INFO)
            self.assertEqual(msg.update_number, 0)
            self.assertTrue(msg.is_last)

    def test_long_thread(self):
        """ Making a long thread of messages """
        self.db.flushdb()
        log = Log(DB_HOST, DB_PORT, db=DB_INDEX)
        thread = log.info("start")
        for i in range(12345):
            thread.info(f"message #{i}")
        messages = list(log.read(0, time.time()))
        self.assertEqual(len(messages), 12345 + 1)

    def test_range_filter(self):
        """ Picking messages in a given time range """
        self.db.flushdb()
        log = Log(DB_HOST, DB_PORT, db=DB_INDEX)
        # push
        log.error("First message").debug("Thread to the first message")
        start_time = time.time()
        time.sleep(0.01)
        log.warning("Second message")
        # check
        rng = (start_time, time.time())
        messages = list(log.read_day(0, rng))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content, "Second message")
        self.assertEqual(messages[0].tag, Tag.WARNING)
        self.assertIsNone(messages[0].pred)
