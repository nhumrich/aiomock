import asyncio
import unittest.mock
from unittest.mock import Mock, _try_iter


unittest.mock._allowed_names.add('async_side_effect')
unittest.mock._allowed_names.add('async_return_value')


class AIOMock(Mock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return_is_async = False

    @staticmethod
    async def _mock_awaitable(value):
        return value

    def __get_async_side_effect(self):
        return self._mock_delegate

    def __set_async_side_effect(self, value):
        super()._NonCallableMock__set_side_effect(value)
        self._return_is_async = True

    async_side_effect = property(
        __get_async_side_effect,
        __set_async_side_effect)

    def __get_async_return_value(self):
        return super()._NonCallableMock__get_return_value()

    def __set_async_return_value(self, value):
        super()._NonCallableMock__set_return_value(value)
        self._return_is_async = True

    async_return_value = property(
        __get_async_return_value,
        __set_async_return_value
    )


    def _mock_call(_mock_self, *args, **kwargs):
        self = _mock_self
        ret_val = super()._mock_call(*args, **kwargs)

        if self._return_is_async:
            return self._mock_awaitable(ret_val)
        else:
            return ret_val
