from memento.sql.synchronous.src.basememory import SQLMemory
from litellm import completion, ModelResponse
from openai.types.chat import ChatCompletion
from openai import AzureOpenAI
from typing import Generator
import pytest

@pytest.fixture
def mem():
    return SQLMemory("sqlite:///test.db")

@pytest.fixture
def ai():
    return AzureOpenAI()

def test_nosqlmemory(mem: SQLMemory):
    assert isinstance(mem, SQLMemory)

def testc_azure_client(ai: AzureOpenAI):
    assert isinstance(ai, AzureOpenAI)

def test_response(ai: AzureOpenAI):
    memento = SQLMemory("sqlite:///test.db")

    gen = memento(ai.chat.completions.create)
    response = gen(message="Hello", model="gpt4-2")

    assert isinstance(response, ChatCompletion)

def test_response_decorator(ai: AzureOpenAI):
    memento = SQLMemory("sqlite:///test.db")

    @memento
    def gen(*args, **kwargs):
        return ai.chat.completions.create(*args, **kwargs)

    response = gen(message="Hi", model="gpt4-2")

    assert isinstance(response, ChatCompletion)

def test_stream_response(ai: AzureOpenAI):
    memento = SQLMemory("sqlite:///test.db")

    gen = memento(ai.chat.completions.create, stream=True)
    response = gen(message="Hello", model="gpt4-2", stream=True)

    assert isinstance(response, Generator)

def test_stream_response_decorator(ai: AzureOpenAI):
    memento = SQLMemory("sqlite:///test.db")

    @memento(stream=True)
    async def gen(*args, stream=True, **kwargs):
        return ai.chat.completions.create(*args, **kwargs, stream=stream)

    response = gen(message="Hi", model="gpt4-2")

    assert isinstance(response, Generator)

### LiteLLM

def test_response_func():
    memento = SQLMemory("sqlite:///test.db")

    gen = memento(completion)
    response = gen(message="Hello", model="azure/gpt4-2")

    assert isinstance(response, ModelResponse)

def test_response_decorator_func():
    memento = SQLMemory("sqlite:///test.db")

    @memento
    def gen(*args, **kwargs):
        return completion(*args, **kwargs)

    response = gen(message="Hi", model="azure/gpt4-2")

    assert isinstance(response, ModelResponse)

def test_stream_response_func():
    memento = SQLMemory("sqlite:///test.db")

    gen = memento(completion, stream=True)
    response = gen(message="Hello", model="azure/gpt4-2", stream=True)

    assert isinstance(response, Generator)

def test_stream_response_decorator_func():
    memento = SQLMemory("sqlite:///test.db")

    @memento(stream=True)
    async def gen(*args, stream=True, **kwargs):
        return completion(*args, **kwargs, stream=stream)

    response = gen(message="Hi", model="azure/gpt4-2")

    assert isinstance(response, Generator)
