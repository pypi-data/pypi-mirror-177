"""
======
Server
======

This module manages loading the modbus server or Slave
"""
import logging

from pymodbus.compat import get_next, iteritems, iterkeys
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.datastore.store import BaseModbusDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.exceptions import ParameterException
from pymodbus.server.asynchronous import (
    StartSerialServer,
    StartTcpServer,
    StartUdpServer,
    StopServer,
)
from pymodbus.version import version
from twisted.internet.task import LoopingCall

DEFAULTCONF = {
    "tcp": {"context": None, "identity": None, "address": ("", 502), "ignore_missing_slaves": False},
    "udp": {"context": None, "identity": None, "address": ("", 502), "ignore_missing_slaves": False},
    "rtu": {
        "context": None,
        "identity": None,
        "port": "/dev/ttyS0",
        "buadrate": 19200,
        "bytesize": 8,
        "stopbits": 1,
        "parity": "N",
        "timeout": 0,
        "xonxoff": 0,
        "rtscts": 0,
    },
}

log = logging.getLogger(__name__)
log.debug("pymodbus version: %s", version.short())


class ModbusSparseDataBlock(BaseModbusDataBlock):
    """
    Cloned of ModbusSparseDataBlock from pymodbus 2.5.3 to backport for python vesions 3.5 and 3.6

    Creates a sparse modbus datastore
    E.g Usage.
    sparse = ModbusSparseDataBlock({10: [3, 5, 6, 8], 30: 1, 40: [0]*20})
    This would create a datablock with 3 blocks starting at
    offset 10 with length 4 , 30 with length 1 and 40 with length 20
    sparse = ModbusSparseDataBlock([10]*100)
    Creates a sparse datablock of length 100 starting at offset 0 and default value of 10
    sparse = ModbusSparseDataBlock() --> Create Empty datablock
    sparse.setValues(0, [10]*10)  --> Add block 1 at offset 0 with length 10 (default value 10)
    sparse.setValues(30, [20]*5)  --> Add block 2 at offset 30 with length 5 (default value 20)
    if mutable is set to True during initialization, the datablock can not be altered with
    setValues (new datablocks can not be added)
    """

    def __init__(self, values=None, mutable=True):
        """
        Initializes a sparse datastore. Will only answer to addresses
        registered, either initially here, or later via setValues()
        :param values: Either a list or a dictionary of values
        :param mutable: The data-block can be altered later with setValues(i.e add more blocks)
        If values are list , This is as good as sequential datablock.
        Values as dictionary should be in {offset: <values>} format, if values
        is a list, a sparse datablock is created starting at offset with the length of values.
        If values is a integer, then the value is set for the corresponding offset.
        """
        self.values = {}
        self._process_values(values)
        self.mutable = mutable
        self.default_value = self.values.copy()
        self.address = get_next(iterkeys(self.values), None)

    @classmethod
    def create(klass, values=None):
        """Factory method to create sparse datastore.
        Use setValues to initialize registers.
        :param values: Either a list or a dictionary of values
        :returns: An initialized datastore
        """
        return klass(values)

    def reset(self):
        """Reset the store to the initially provided defaults"""
        self.values = self.default_value.copy()

    def validate(self, address, count=1):
        """Checks to see if the request is in range
        :param address: The starting address
        :param count: The number of values to test for
        :returns: True if the request in within range, False otherwise
        """
        if count == 0:
            return False
        handle = set(range(address, address + count))
        return handle.issubset(set(iterkeys(self.values)))

    def getValues(self, address, count=1):
        """Returns the requested values of the datastore
        :param address: The starting address
        :param count: The number of values to retrieve
        :returns: The requested values from a:a+c
        """
        return [self.values[i] for i in range(address, address + count)]

    def _process_values(self, values):
        def _process_as_dict(values):
            for idx, val in iteritems(values):
                if isinstance(val, (list, tuple)):
                    for i, v in enumerate(val):
                        self.values[idx + i] = v
                else:
                    self.values[idx] = int(val)

        if isinstance(values, dict):
            _process_as_dict(values)
            return
        if hasattr(values, "__iter__"):
            values = dict(enumerate(values))
        elif values is None:
            values = {}  # Must make a new dict here per instance
        else:
            raise ParameterException("Values for datastore must " "be a list or dictionary")
        _process_as_dict(values)

    def setValues(self, address, values, use_as_default=False):
        """Sets the requested values of the datastore
        :param address: The starting address
        :param values: The new values to be set
        :param use_as_default: Use the values as default
        """
        if isinstance(values, dict):
            new_offsets = list(set(list(values.keys())) - set(list(self.values.keys())))
            if new_offsets and not self.mutable:
                raise ParameterException("Offsets {} not " "in range".format(new_offsets))
            self._process_values(values)
        else:
            if not isinstance(values, list):
                values = [values]
            for idx, val in enumerate(values):
                if address + idx not in self.values and not self.mutable:
                    raise ParameterException("Offset {} not " "in range".format(address + idx))
                self.values[address + idx] = val
        if not self.address:
            self.address = get_next(iterkeys(self.values), None)
        if use_as_default:
            for idx, val in iteritems(self.values):
                self.default_value[idx] = val


class Task(object):
    """
    A Class to manage all the task to run periodically alongside the server

    This Can be called as a decorators.  The following example will print "Hello\\nworld" every second.
    The decorator can be used multiple times to call more than once.

    ..
        @mbsim.core.server.Task(1, args=("Hello", "world"))
        def hw(*args):
            for arg in args:
                print(arg)

        or

        mbsim.core.server.Task(1, func=hw, args=("Hello", "world"))

    Both example are equivalent
    """

    tasks = []

    def __init__(self, inter, func=None, args=(), kwargs={}, now=False):
        """
        This will take the arguments for the task to be run

        :param inter: Interval of time to wait before calling the no blocking function
        :type inter: float
        :param func: Function to call
        :param args: arguments to be past to task
        :type args: tuple, optional
        :param kwargs: key word arguments to be passed to task, defaults to {}
        :type kwargs: dict, optional
        :param now: To run immediately or wait the interval, defaults to False
        :type now: bool, optional
        """
        self.inter = inter
        self.args = args
        self.kwargs = kwargs
        self.now = now
        self.tasks.append(self)
        if func:
            self(func)

    def __call__(self, func):
        """
        Init the task and return original function

        :param func: A Non blocking function
        :type func: function
        :return: Original function
        :rtype: function
        """
        self.func = func
        log.debug("Adding task: %s", (self.func.__name__, self.inter, self.args, self.kwargs))
        self.task = LoopingCall(f=self.wrap, a=self.args, kw=self.kwargs)
        return func

    def wrap(self, a, kw):
        """
        A wrap for twisted to pass a and kw as args.  This function will explode them into the function

        :param a: args
        :type a: tuple
        :param kw: kwargs
        :type kw: dict
        """
        return self.func(*a, **kw)

    def start(self):
        """
        To start the task
        """
        log.debug("Starting task: %s", (self.func.__name__, self.inter, self.args, self.kwargs))
        self.task.start(self.inter, now=self.now)

    @classmethod
    def startTasks(cls):
        """
        Class method to start all tasks
        """
        for task in cls.tasks:
            task.start()

    def stop(self):
        """
        To stop a task
        """
        log.debug("Stopping task: %s", (self.func.__name__, self.inter, self.args, self.kwargs))
        self.task.stop()

    @classmethod
    def stopTasks(cls):
        """
        Class method to stop all tasks
        """
        for task in cls.tasks:
            task.stop()


def genDevice(**kwargs):
    """
    A function to create a identity.  All parameters are key word arguments.

    :param name: Vendor Name. Defaults to `mbsim`
    :type name: str
    :param code: Product Code. Defaults to `MB`
    :type code: str
    :param url: Vendor URL. Defaults to `https://gitlab.com/nee2c/mbsim`
    :type url: str
    :param product: Product Name. Defaults to `mbsim`
    :type product: str
    :param model: Model Name. Defaults to `mbsim`
    :type model: str
    :param version: Version. Defaults to `1.0.0`
    :type version: str
    :return: Returns an identity for server
    """
    identity = ModbusDeviceIdentification()

    identity.VendorName = kwargs.get("name", "mbsim")
    identity.ProductCode = kwargs.get("code", "MB")
    identity.VendorUrl = kwargs.get("url", "https://gitlab.com/nee2c/mbsim")
    identity.ProductName = kwargs.get("product", "mbsim")
    identity.ModelName = kwargs.get("model", "mbsim")
    identity.MajorMinorRevision = kwargs.get("version", "1.0.0")

    log.debug("Genrated identity: %s", identity.summary())
    return identity


def genContext(context=None, single=True):
    """
    A Function to return Context for Server.

    The context can be None. This will genrate a context that all slavesid will use. All values set to 0

    If context is an instance of ModbusServerContext, funtion returns the context

    Else dict of slaves with dict of address space("di", "co", "hr", "ir") with list or dict {offset: [reg0, reg1, ...]}


    dict Context example

    ..

        {0: {"di": [0, 1, 0, 1, 0], "co": {0: [1, 0, 1], 100: [1]}, "hr": [123, 10], "ir": {123: [123, 0, 123]}}, ...}

    :param context: Server Context or dict of Slaves context or dict
    :param single:
    :type single: bool
    """
    if isinstance(context, ModbusServerContext):
        log.debug("Already a Server Context")
        return context
    if context is None:
        log.debug("Genirating Server context: single: %s", single)
        return ModbusServerContext(slaves=ModbusSlaveContext(zero_mode=True), single=single)
    slaves = {}
    log.debug("Genrating context from %s", context)
    for slaveid, slavecontext in context.items():
        slaves[slaveid] = ModbusSlaveContext(
            **{key: ModbusSparseDataBlock(values=vals) for key, vals in slavecontext.items()},
            zero_mode=True,
        )
    return ModbusServerContext(slaves=slaves, single=single)


def start(server, **kwargs):
    """
    This is the function to start modbus server.  Passes all kwargs though to server, if missing uses default.

    :param server: The protocal to run modbus server
    :type server: str
    """
    if server not in DEFAULTCONF.keys():
        raise NotImplementedError("This server type {} is not Iplemented".format(server))
    serverargs = {**kwargs, **{key: val for key, val in DEFAULTCONF[server].items() if key not in kwargs.keys()}}
    if not serverargs.get("context"):
        serverargs["context"] = genContext()
    log.info("Starting %s server", server)
    log.debug("Server args: %s", str(serverargs))

    log.debug("Starting Tasks")
    Task.startTasks()
    log.debug("Started Tasks")

    log.debug("Starting %s Server", server)
    if server == "tcp":
        StartTcpServer(**serverargs)
    elif server == "udp":
        StartUdpServer(**serverargs)
    elif server == "rtu":
        StartSerialServer(**serverargs)
    log.debug("Started Server")


def stop():
    """
    Function to stop modbus server
    """
    log.debug("Stopping Tasks")
    Task.stopTasks()
    log.debug("Stopped Tasks")
    log.debug("Stopping Server")
    StopServer()
    log.debug("Stopped Server")
