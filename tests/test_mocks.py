from aiomock import AIOMock
from unittest.mock import Mock
import asyncio

loop = asyncio.get_event_loop()


def test_standard():
    def my_func():
        return True
    async def my_a_func():
        return True
    m = AIOMock()
    m.some_func.side_effect = [1, 2, 3]
    m.normal_func.return_value = [1, 2, 3]
    m.other_func = my_func
    m.async_func = my_a_func

    assert m.some_func() == 1
    assert m.some_func() == 2
    assert m.some_func() == 3

    assert m.normal_func() == [1, 2, 3]

    assert m.other_func()
    co = m.async_func()
    assert asyncio.iscoroutinefunction(m.async_func)
    loop = asyncio.get_event_loop()
    assert loop.run_until_complete(co)


def test_mock_side_effect():
    a = AIOMock()
    a.some_func.async_side_effect = [1, 2, 3]

    async def test():
        assert await a.some_func() == 1
        assert await a.some_func() == 2
        assert await a.some_func() == 3

    loop.run_until_complete(test())


def test_mock_return_value():
    a = AIOMock()
    a.some_func.async_return_value = [1, 2, 3]

    async def test():
        assert await a.some_func() == [1, 2, 3]

    loop.run_until_complete(test())


def test_mock_side_effect_with_lambda():
    a = AIOMock()
    a.some_func.async_side_effect = lambda x: x+4

    async def test():
        assert await a.some_func(1) == 5
        assert await a.some_func(2) == 6
        assert await a.some_func(-4) == 0

    loop.run_until_complete(test())
