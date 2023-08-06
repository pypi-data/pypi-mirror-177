import math
import time
import traceback
from datetime import datetime
from redis import Redis, exceptions
from typing import Generator, Optional, Tuple, Union

SECONDS_PER_DAY = 24 * 3600
DATE_FORMAT = '%y%m%d'   # keys in the db


class Tag:
    """ Mapping of tags to database record prefixes.
    """
    DEBUG = 'D'
    INFO = 'I'
    WARNING = 'W'
    ERROR = 'E'
    CRITICAL = 'C'

    SUCCESS = 'S'


class Thread:
    """ A chain of messages in a log.
        Used to push new messages to the database.
    """
    @staticmethod
    def _get_key(timestamp: float) -> Tuple[str, int]:
        """ Computes the DB key and time offset from midnight used to indentify a log message.
        """
        key = datetime.utcfromtimestamp(timestamp).strftime(DATE_FORMAT)
        delta = int((timestamp % SECONDS_PER_DAY) * 1000)    # milliseconds since midnight
        return key, delta

    def _push(self, key: str, value: bytes) -> int:
        """ Pushes a value containing the message info to a list corresponding to a specific day.
            Returns zero-based index of the inserted message in the list.
        """
        idx = self.log.db.rpush(key, value) - 1
        if idx == 0:
            # first entry for the key, set the expire time
            self.log.db.expire(key, self.log.retention_time)
        return idx

    def __init__(self, log, tag: Tag, message: str):
        """ Pushes a new message in a log.
            The pushed message starts a new thread.
        """
        self.log = log
        self.upd_ctr = 0
        self.key, delta = Thread._get_key(time.time())

        # form the value to store in the DB:
        #   | zeros[31] | has next[1] | ms since midnight[4*8] | tag[8] | message[...]
        self.value = bytearray(b'\0\0\0\0' + delta.to_bytes(4, 'big') + tag[0].encode() + message.encode('utf-8'))

        self.idx = self._push(self.key, bytes(self.value))

    def update(self, tag: Tag, message: str):
        """ Adds a new message in the thread.
            The new message is linked to the preceding one.
        """
        # change the predecessor record: set 'has next' bit
        self.value[3] += 1
        try:
            self.log.db.lset(self.key, self.idx, bytes(self.value))
        except exceptions.ResponseError:
            # 'no such key' if flushed the logs in the meantime
            self.__init__(self.log, tag, message)
            return

        # increase conter, get new key
        self.upd_ctr += 1
        newkey, delta = Thread._get_key(time.time())

        # form the value to store in the DB:
        #   | num updates > 0[31] | has next[1] | ms since midnight[4*8] | prev msg key[48] | prev msg idx[32] | tag[8] | message[...]
        self.value = bytearray((self.upd_ctr * 2).to_bytes(4, 'big')            # num updates and 'has next' bit (=0)
                                + delta.to_bytes(4, 'big')                      # ms since bidnight
                                + self.key.encode()                             # predecessor key
                                + self.idx.to_bytes(4, 'big')                   # predecessor index
                                + tag[0].encode() + message.encode('utf-8'))    # tag + message content

        # push to a list
        self.idx = self._push(newkey, bytes(self.value))
        self.key = newkey

    def debug(self, message: str):
        self.update(Tag.DEBUG, message)

    def info(self, message: str):
        self.update(Tag.INFO, message)

    def warning(self, message: str):
        self.update(Tag.WARNING, message)

    def error(self, message: str):
        self.update(Tag.ERROR, message)

    def critical(self, message: str):
        self.update(Tag.CRITICAL, message)

    def success(self, message: str):
        self.update(Tag.SUCCESS, message)

    def report_exception(self, message: str, exception: Exception, level=None):
        self.update(
            level or Tag.CRITICAL,
            f'{message}: {exception}\n' + '\n'.join(traceback.format_tb(exception.__traceback__))
        )

    def __len__(self):
        """ Returns number of messages in the thread.
        """
        return self.upd_ctr + 1


class Message:
    """ A message record in a log.
        Stores a timestamp, number of times the thread was updated before this message, tag, content, link to
        the preceding message in the thread (if any) and a boolean flag whether it is last in the thread or not.
    """
    COUNTER = 0

    def __init__(self,
                 raw: bytes,
                 midnight_ts: int):
        """ Constructs a message from a raw database record.
                raw: the database record
                midnight_ts: midnight timestamp corresponding to the message date
        """
        # parse raw message header
        upd_ctr = int.from_bytes(raw[:4], 'big')
        delta = int.from_bytes(raw[4:8], 'big')
        self.is_last = (upd_ctr & 1) == 0
        self.update_number = upd_ctr >> 1
        self.timestamp = midnight_ts + 0.001 * delta
        self.id = Message.COUNTER
        Message.COUNTER += 1

        # if has a preceding message in the same thread (predecessor)
        if self.update_number > 0:
            pred_date = raw[8:14].decode()
            pred_idx = int.from_bytes(raw[14:18], 'big')
            self.tag = chr(raw[18])
            self.content = raw[19:].decode('utf-8')
            self.pred = (pred_date, pred_idx)

        # if does not have predecessor
        else:
            self.tag = chr(raw[8])
            self.content = raw[9:].decode('utf-8')
            self.pred = None

    def __str__(self):
        return str(self.content)


class Log:
    """ Logging to a redis database.
        Keys are date in plain text ('20081231'), values are lists of messages per day.
        Messages form threads: every message contain an update counter and can be linked to another message in past.
    """
    DEFAULT_RETENTION_TIME_SEC = 100 * SECONDS_PER_DAY     # 100 days

    def __init__(self,
                 host: str = "localhost",
                 port: int = 6379,
                 db: int = 15,
                 retention_time: int = DEFAULT_RETENTION_TIME_SEC):
        """ Creates a new Log instance.
            Log maintains a DB connection and is used to read and write log messages.
        """
        self.db = Redis(host=host, port=port, db=db)
        self.retention_time = retention_time

    def __call__(self, tag: Tag, message: str) -> Thread:
        """ Pushes a new message.
            Returns a thread beginning with the new message.
        """
        return Thread(self, tag, message)

    def debug(self, message: str) -> Thread:
        return self.__call__(Tag.DEBUG, message)

    def info(self, message: str) -> Thread:
        return self.__call__(Tag.INFO, message)

    def warning(self, message: str) -> Thread:
        return self.__call__(Tag.WARNING, message)

    def error(self, message: str) -> Thread:
        return self.__call__(Tag.ERROR, message)

    def critical(self, message: str) -> Thread:
        return self.__call__(Tag.CRITICAL, message)

    def success(self, message: str) -> Thread:
        return self.__call__(Tag.SUCCESS, message)

    def report_exception(self, message: str, exception: Exception, tag: Tag=None) -> Thread:
        return self.__call__(
            tag or Tag.CRITICAL,
            f'{message}: {exception}\n' + '\n'.join(traceback.format_tb(exception.__traceback__))
        )

    def read_day(self, date: Union[str, int] = 0, time_range: Optional[Tuple[float, float]] = None) -> Generator[Message, None, None]:
        """ Retrieves all messages at a single given day. Optionally filters by a given time range.
                date: date in `DATE_FORMAT` format, or integer (0=today, 1=yesterday, etc.)
                time_range: absolute timestamp range (two-tuple) to pick messages in; can be none
        """
        # get key in string format
        if isinstance(date, int):
            ts = time.time() - date * SECONDS_PER_DAY
            date = datetime.utcfromtimestamp(ts).strftime(DATE_FORMAT)
        midnight = datetime.strptime(date, DATE_FORMAT).timestamp()

        # loop raw messages
        daily_cache = {}   # index => message for messages having predecessors
        raw_messages = self.db.lrange(date, 0, -1)
        for idx, raw in enumerate(raw_messages):
            # parse message
            message = Message(raw, midnight)

            # check if within the time_range
            if time_range:
                if message.timestamp < time_range[0]:
                    continue
                if time_range[1] <= message.timestamp:
                    break

            # resolve the thread
            thread = message
            while thread is not None and thread.pred is not None:
                pred_date, pred_idx = thread.pred

                # check for the preceding message in the cache
                if pred_date == date and pred_idx in daily_cache:
                    thread.pred = daily_cache.pop(pred_idx)
                    break
                else:
                    # not found in the cache; get from the DB
                    pred_db_record = self.db.lrange(pred_date, pred_idx, pred_idx)

                    # create the preceding message if `pred_db_record` exists (may disappear due to its TTL)
                    thread.pred = Message(
                        pred_db_record[0],
                        datetime.strptime(pred_date, DATE_FORMAT).timestamp(),
                    ) if pred_db_record else None

                    # check if within the time_range
                    if time_range and thread.pred.timestamp < time_range[0]:
                        # if out of bounds, mark the predecessor as existing one but do not keep
                        thread.pred = True
                        break

                # loop
                thread = thread.pred

            # put to cache if the current message preceeds another one
            if not message.is_last:
                daily_cache[idx] = message

            yield message

    def read(self, from_ts: float, to_ts: float) -> Generator[Message, None, None]:
        """ Retrieves messages between two given timestamps.
        """
        marks = range(math.floor(from_ts), math.floor(to_ts) + 1, SECONDS_PER_DAY)
        dates = map(lambda t: datetime.utcfromtimestamp(t).strftime(DATE_FORMAT), marks)
        for day in dates:
            for message in self.read_day(day, (from_ts, to_ts)):
                yield message
