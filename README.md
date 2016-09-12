# aiomock
a version of pythons unittest.Mock with async methods

This mock works exactly like unitest.mock.Mock, except that it also includes the following:

* mock.async_return_value  - an awaitable version of return_value
* mock.async_side_effect   - an awaitable version of side_effect

# installing

```
pip install aiomock
```

# rational

imagine you have the following code

```python
queue = asyncio.Queue()

async def wait_for_it():
    item = await queue.get()
    # do something with item
    return item
```

in order to test this, you cant use unittest.Mock.return_value because it is
not awaitable. This means you have to write a function for every test

```python
async def test_wait_for_it(monkeypatch):
    my_queue = Mock()
    async def my_get():
        return 1
    mock.get = my_get

    monkeypatch.setattr(asyncio.Queue, my_queue)
```

Its annoying that Mock has two excellant features, `side_effect`, and `return`, but
you cant use them because we are async. This fixes that

# Using
```python
from aiomock import AIOMock

async def test_wait_for_it(monkeypatch):
    my_queue = AIOMock()
    mock.get.async_return_value = 1

    monkeypatch.setattr(asyncio.Queue, my_queue)
```

or for side_effect, use

```python
mock.func_name.async_side_effect = [1, 2]
```

You can even use it with lambdas, and it will convert it to an awaitable

```python
mock.func_name.async_side_effect = lambda x: x+4
```
