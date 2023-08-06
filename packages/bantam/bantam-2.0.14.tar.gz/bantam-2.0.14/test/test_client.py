import json
from typing import AsyncIterator, Dict
from unittest.mock import patch

import pytest
from abc import abstractmethod

from bantam.api import RestMethod
from bantam.client import WebInterface
from bantam.decorators import web_api
from bantam.http import WebApplication


class MockWebClientInterface(WebInterface):

    def jsonrepr(self):
        return {'self_id': id(self)}

    @web_api(method=RestMethod.GET, is_constructor=True, content_type='application/json')
    @classmethod
    @abstractmethod
    async def constructor(data: str) -> "MockWebClientInterface":
        """
        constructor mock
        :param data:
        :return:
        """
        raise NotImplementedError()


    @web_api(method=RestMethod.GET, content_type='application/json')
    @classmethod
    @abstractmethod
    async def class_method(cls, value: float) -> Dict[str, str]:
        raise NotImplementedError()

    @web_api(method=RestMethod.GET, content_type='json')
    @staticmethod
    @abstractmethod
    async def static_method_streamed(val1: int, val2: float) -> AsyncIterator[str]:
        raise NotImplementedError()

    @web_api(method=RestMethod.POST, content_type='application/json')
    @abstractmethod
    async def instance_method(self, val: str) -> str:
        raise NotImplementedError()

Client = MockWebClientInterface.Client()
MyClient: MockWebClientInterface = Client['http://someendpoint/']
MyClient2: MockWebClientInterface = Client['http://someendpoint2/']


class TestWebClient:

    class MockContent:

        @property
        def content(self):
            return self

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        async def iter_chunks(self):
            for text in ['I', "am", 'the', 'very', 'model']:
                yield text.encode('utf-8'), text == 'model'

        async def read(self, *args, **kwargs):
            class MockWebClient(MockWebClientInterface):

                async def constructor(data: str) -> "MockWebClient":
                    return MyClient()

            if TestWebClient._get_count == 1:
                return json.dumps(MockWebClientInterface.jsonrepr(MyClient2(self_id=1234))).encode('utf-8')
            elif TestWebClient._get_count == 2:
                return json.dumps({'a': "1"}).encode('utf-8')
            elif TestWebClient._get_count == 4:
                return b'PONG'

        def raise_for_status(self, *args, **kwargs):
            pass

    _get_count = 0
    _suffix = ""

    @staticmethod
    def mock_get(url: str, **kwargs):
        urls = [
            f"http://someendpoint{TestWebClient._suffix}/MockWebClient/constructor?data=data",
            f"http://someendpoint{TestWebClient._suffix}/MockWebClient/class_method?value=1.2",
            f"http://someendpoint{TestWebClient._suffix}/MockWebClient/static_method_streamed?val1=1&val2=2.34",
            (f"http://someendpoint{TestWebClient._suffix}/MockWebClient/instance_method?self","val=PING"),
        ]
        if TestWebClient._get_count < 3:
            assert url == urls[TestWebClient._get_count]
        else:
            assert url.startswith(urls[TestWebClient._get_count][0])
            assert kwargs['data'] == json.dumps({'val': 'PING'})
        TestWebClient._get_count += 1
        return TestWebClient.MockContent()


    @pytest.mark.asyncio
    @patch(target='aiohttp.ClientSession.get', new=mock_get)
    @patch(target='aiohttp.ClientSession.post', new=mock_get)
    async def test_client(self):
        assert MyClient2 != MyClient
        instance = await MyClient.constructor(data='data')
        assert await MyClient.class_method(value=1.2) == {'a': "1"}
        data_values = []
        async for data in MyClient.static_method_streamed(val1=1, val2=2.34):
            data_values.append(data)
        assert data_values == ['I', 'am', 'the', 'very', 'model']
        assert await instance.instance_method(val="PING") == 'PONG'

        TestWebClient._get_count = 0
        TestWebClient._suffix = "2"
        instance = await MyClient2.constructor(data='data')
        assert await MyClient2.class_method(value=1.2) == {'a': "1"}
        data_values = []
        async for data in MyClient2.static_method_streamed(val1=1, val2=2.34):
            data_values.append(data)
        assert data_values == ['I', 'am', 'the', 'very', 'model']
        assert await instance.instance_method(val="PING") == 'PONG'