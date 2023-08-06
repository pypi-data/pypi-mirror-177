"""
Test for mbsim-core.server module
"""
import builtins
from importlib import import_module, reload
from itertools import combinations

import pytest
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext

import mbsim.core.server as mbserver


@pytest.fixture(scope="class")
def mb():
    """
    Import lib for testing and reload
    """
    mb = import_module("mbsim.core.server")
    yield mb
    reload(mb)


def genDevData():
    """
    Genrates device identity test data
    """
    default = {
        "VendorName": "mbsim",
        "ProductCode": "MB",
        "VendorUrl": "https://gitlab.com/nee2c/mbsim",
        "ProductName": "mbsim",
        "ModelName": "mbsim",
        "MajorMinorRevision": "1.0.0",
    }
    alt = {
        "VendorName": "tests",
        "ProductCode": "AZ",
        "VendorUrl": "https://example.com",
        "ProductName": "sim",
        "ModelName": "mb",
        "MajorMinorRevision": "1.0.1",
    }
    paramname = {
        "VendorName": "name",
        "ProductCode": "code",
        "VendorUrl": "url",
        "ProductName": "product",
        "ModelName": "model",
        "MajorMinorRevision": "version",
    }
    data = [(None, default)]
    for num, _ in enumerate(default, 1):
        for keys in combinations(default.keys(), num):
            test = {paramname[key]: alt[key] for key in keys}
            res = {
                **{key: alt[key] for key in keys},
                **{key: default[key] for key in set(default.keys()).difference(keys)},
            }
            data.append((test, res))
    return data


def genContext():
    return mbserver.genContext()


class TestGenDevice(object):
    """
    This is group test for the function of genDevice
    """

    @pytest.mark.parametrize("test,res", genDevData())
    def test_genDevice(self, test, res, mb):
        """
        Test identity after it genrated
        """
        if test is None:
            test = {}
        dev = mb.genDevice(**test)
        for key, value in res.items():
            assert getattr(dev, key) == value


class TestGenContext(object):
    """
    This is a group of text for testing generating Context
    """

    _fx = {2: "d", 4: "i", **{i: "h" for i in (3, 6, 16, 22, 23)}, **{i: "c" for i in (1, 5, 15)}}

    def test_passingNone(self, mb):
        """
        test calling genContext with no arguments
        """
        test = mb.genContext()
        assert isinstance(test, ModbusServerContext)
        assert test.single
        assert test[0] is test[1]
        for fx in self._fx.keys():
            assert test[0].getValues(fx, 200, count=5)

    def test_passingContext(self, mb):
        """
        test passing the function exsisting Server Context
        """
        test = ModbusServerContext()
        assert mb.genContext(test) is test

    @pytest.mark.parametrize(
        "testdict",
        [
            (
                {
                    2: {
                        "co": {0: [1, 0, 0, 1], 101: [0, 1, 1, 0]},
                        "di": {0: [1, 0, 0, 1], 201: [0, 1, 1, 0]},
                        "hr": {60: [100, 580, 40, 1], 101: [0, 101, 1111, 0]},
                        "ir": {10: [1000, 0, 0, 541], 101: [870, 221, 1, 0]},
                    }
                }
            ),
            (
                {
                    2: {
                        "co": [1, 0, 0, 1],
                        "di": [1, 0, 0, 1],
                        "hr": [100, 580, 40, 1],
                        "ir": [1000, 0, 0, 5410, 221, 1, 0],
                    }
                }
            ),
            (
                {
                    2: {
                        "co": [1, 0, 0, 1],
                        "di": [1, 0, 0, 1],
                        "hr": {60: [100, 580, 40, 1], 101: [0, 101, 1111, 0]},
                        "ir": {10: [1000, 0, 0, 541], 101: [870, 221, 1, 0]},
                    }
                }
            ),
            (
                {
                    2: {
                        "co": [1, 0, 0, 1],
                        "di": [1, 0, 0, 1],
                        "hr": [100, 580, 40, 1],
                        "ir": [1000, 0, 0, 5410, 221, 1, 0],
                    },
                    20: {
                        "co": [1, 1, 1, 1],
                        "di": [0, 0, 0, 0],
                        "hr": [107, 587, 44, 6],
                        "ir": [1006, 4, 0, 5402, 221, 4, 0],
                    },
                }
            ),
        ],
    )
    def test_customContext(self, testdict, mb):
        """
        create and test custom setup context
        """
        _fx = {"co": 1, "di": 2, "hr": 3, "ir": 4}
        test = mb.genContext(testdict, single=False)
        assert isinstance(test, ModbusServerContext)
        for slave in test.slaves():
            assert slave in testdict
            assert isinstance(test[slave], ModbusSlaveContext)
            for store, vals in testdict[slave].items():
                if isinstance(vals, dict):
                    for offset, regs in vals.items():
                        assert test[slave].getValues(_fx[store], offset, len(regs)) == regs
                elif isinstance(vals, list):
                    assert test[slave].getValues(_fx[store], 0, len(vals)) == vals


class MockCall(object):
    """
    A simple Test function to count the number of calls and arguments used
    """

    def __init__(self):
        """
        Init the test function
        """
        self.count = 0
        self.args = []
        self.kwargs = []

    def __call__(self, *args, **kwargs):
        """
        Increment the count due to being called
        """
        self.count += 1
        self.args.append(args)
        self.kwargs.append(kwargs)


class MockLoopingCall(object):
    """
    Mock object to mock twisted LoopingCall object
    """

    def __init__(self, f, a=None, kw=None):
        """
        test object to test LoopingCall

        :param f: function
        :param a: args, defaults to None
        :type a: tuple, optional
        :param kw: kwargs, defaults to None
        :type kw: dict, optional
        """
        self.started = False
        self.stopped = False
        self.func = f
        self.args = a
        self.kwargs = kw
        self.inter = None
        self.now = None

    def start(self, inter, now=False):
        """
        mock loopingCall start function

        :param inter: time interval
        :type inter: float
        :param now: first call or wait interval, defaults to False
        :type now: bool, optional
        """
        if self.started:
            raise RuntimeError("Mock Task has already been started")
        self.started = True
        self.inter = inter
        self.now = now

    def stop(self):
        """
        mock loopingCall stop function

        :param inter: time interval
        :type inter: float
        :param now: first call or wait interval, defaults to False
        :type now: bool, optional
        """
        if self.stopped:
            raise RuntimeError("Mock Task has already been started")
        self.stopped = True


class Test_Tasks(object):
    """
    Group of test to test Tasks
    """

    @pytest.mark.parametrize(
        "index,inter,args,kwargs,now,func",
        [
            (0, 1, (), {}, False, print),
            (1, 2, ("Hello"), {}, False, dict),
            (2, 3, (), {"Hello": "World"}, False, set),
            (3, 4, (), {}, True, max),
        ],
    )
    def test_createDecorator(self, index, inter, args, kwargs, now, func, mb, monkeypatch):
        """
        test the creation of tasks
        """
        monkeypatch.setattr(mb, "LoopingCall", MockLoopingCall)
        mb.Task(inter, args=args, kwargs=kwargs, now=now)(func)
        assert func == mb.Task.tasks[index].func
        assert inter == mb.Task.tasks[index].inter
        assert args == mb.Task.tasks[index].args
        assert kwargs == mb.Task.tasks[index].kwargs
        assert now == mb.Task.tasks[index].now
        assert isinstance(mb.Task.tasks[index].task, MockLoopingCall)

    @pytest.mark.parametrize(
        "index,inter,args,kwargs,now,func",
        [
            (0, 1, (), {}, False, print),
            (1, 2, ("Hello"), {}, False, dict),
            (2, 3, (), {"Hello": "World"}, False, set),
            (3, 4, (), {}, True, max),
        ],
    )
    def test_createInstance(self, index, inter, args, kwargs, now, func, mb, monkeypatch):
        """
        test the creation of tasks
        """
        monkeypatch.setattr(mb, "LoopingCall", MockLoopingCall)
        mb.Task(inter, func=func, args=args, kwargs=kwargs, now=now)
        assert func == mb.Task.tasks[index].func
        assert inter == mb.Task.tasks[index].inter
        assert args == mb.Task.tasks[index].args
        assert kwargs == mb.Task.tasks[index].kwargs
        assert now == mb.Task.tasks[index].now
        assert isinstance(mb.Task.tasks[index].task, MockLoopingCall)

    def test_startTasks(self, mb):
        """
        Test class method and by proxy instace start method
        """
        mb.Task.startTasks()
        for task in mb.Task.tasks:
            assert task.task.started
            assert task.inter == task.task.inter
            assert task.now == task.task.now
            assert task.args == task.task.args
            assert task.kwargs == task.task.kwargs

    def test_stopTasks(self, mb):
        """
        Test class method and by proxy instace stop method
        """
        mb.Task.stopTasks()
        for task in mb.Task.tasks:
            assert task.task.stopped

    @pytest.mark.xfail(reason="Monkeypatch fails to patch print in py37 and py38, need to rework MockCall")
    def test_twistedwrap(self, mb, monkeypatch):
        """
        Test wrap function for twisted loopingCall passing args
        """
        task = mb.Task.tasks[0]
        monkeypatch.setattr(builtins, "print", MockCall())
        test = task.wrap(a=("Hello", "World"), kw={"foo": 1, "bar": 2})
        assert test.count == 1
        assert test.args[0] == ("Hello", "World")
        assert test.kwargs[0] == {"foo": 1, "bar": 2}


class Test_Start(object):
    """
    Group of test to test the start function
    """

    def test_notimplemented(self, mb):
        """
        Test if unexpected server raise NotImplementedError
        """
        with pytest.raises(NotImplementedError, match="This server type Hello is not Iplemented"):
            mb.start("Hello")

    @pytest.mark.parametrize("context", [None, genContext()])
    def test_Context(self, context, monkeypatch, mb):
        """
        Test to ckeck behavior whith diffrent types of context is used as prams
        """
        server, mock = "tcp", MockCall()
        monkeypatch.setattr(mb, "StartTcpServer", mock)
        if context is None:
            # Call with no context param
            mb.start(server)
        mb.start(server, context=context)
        if context is None:
            assert mock.count == 2
        else:
            assert mock.count
        for kwargs in mock.kwargs:
            assert isinstance(kwargs.get("context"), ModbusServerContext)

    @pytest.mark.parametrize("test", ["tcp", "udp", "rtu"])
    def test_servercalls(self, test, monkeypatch, mb):
        """
        Test the pymodbus module is called correctly
        """
        servers = {
            "tcp": ("StartTcpServer", MockCall()),
            "udp": ("StartUdpServer", MockCall()),
            "rtu": ("StartSerialServer", MockCall()),
        }
        for server, (attr, mock) in servers.items():
            monkeypatch.setattr(mb, attr, mock)
        mb.start(test)
        _, res = servers.pop(test)
        assert res.count == 1
        for _, mock in servers.values():
            assert not mock.count

    def test_startTasks(self, mb, monkeypatch):
        """
        Test to make sure Tasks are started
        """
        test = MockCall()
        monkeypatch.setattr(mb, "StartTcpServer", MockCall())
        monkeypatch.setattr(mb.Task, "startTasks", test)
        mb.start("tcp")
        assert test.count == 1


class TestStop(object):
    """
    Test Stop functions
    """

    def test_stop(self, monkeypatch, mb):
        """
        Test Stop functions
        """
        mock = MockCall()
        monkeypatch.setattr(mb, "StopServer", mock)
        mb.stop()
        assert mock.count == 1
        assert not mock.args[0]
        assert not mock.kwargs[0]

    def test_stopTasks(self, mb, monkeypatch):
        """
        Test to make sure Tasks are started
        """
        test = MockCall()
        monkeypatch.setattr(mb, "StopServer", MockCall())
        monkeypatch.setattr(mb.Task, "stopTasks", test)
        mb.stop()
        assert test.count == 1
