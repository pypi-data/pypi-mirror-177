import json
import time
from enum import Enum
from time import sleep
from typing import Callable

import requests.packages
import requests.packages.urllib3
from requests import Session as RSession
from robot.utils import timestr_to_secs
from urllib3.exceptions import InsecureRequestWarning

from robotframework_practitest.services.data_queue import CacheItem, DataQueueService, DEFAULT_ITEM_WAIT
from robotframework_practitest.utils.logger import logger
from robotframework_practitest.utils.misc_utils import get_error_info

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

REQUEST_TIMEOUT = 60
REQUEST_COUNTER = 0
THROTTLING_TIMEOUT = time.perf_counter()


class SupportedMethods(Enum):
    PUT = 'put'
    POST = 'post'
    GET = 'get'


class SessionWithCaching:
    def __init__(self, user, token, **kwargs):
        super().__init__()
        self._session = RSession()
        self._user = user
        self._token = token
        self._throttle_activated = None
        self._throttle_timeout = 0
        global REQUEST_COUNTER
        REQUEST_COUNTER = 0

    @property
    def active_timeout(self):
        return self._throttle_timeout if self._throttle_activated else 0

    @property
    def auth(self):
        return tuple(getattr(self, f) for f in ('_user', '_token'))

    @property
    def headers(self):
        return {'Content-type': 'application/json'}

    def _get_method(self, request_method) -> Callable:
        if request_method == SupportedMethods.PUT:
            return self._session.put
        elif request_method == SupportedMethods.POST:
            return self._session.post
        elif request_method == SupportedMethods.GET:
            return self._session.get
        else:
            raise AttributeError(f"Unsupported method: {request_method}")

    def wait_throttle_timeout(self, timeout=60):
        timeout_in_seconds = timestr_to_secs(timeout)
        self._throttle_activated = True
        self._throttle_timeout = timeout
        logger.warning(f"Retention {timeout} started")
        sleep(timeout_in_seconds)
        logger.warning("Retention ended")
        self._throttle_activated = False
        self._throttle_timeout = 0

    def run(self, method: SupportedMethods, cache_item: CacheItem, url, payload=None,
            ignore_cache=False, enforce_result=False, timeout=DEFAULT_ITEM_WAIT):
        logger.debug(f"job start: {self}, {url}, {payload}")
        try:
            if ignore_cache:
                raise AssertionError()
            res = DataQueueService().wait(cache_item, timeout + self.active_timeout)
        except (ValueError, IndexError, KeyError):
            logger.debug(f"Cannot retrieve from cache {cache_item}; Access API")
        except AssertionError:
            logger.debug(f"Cache ignored enforce access API")
        else:
            logger.debug(f"Retrieving from cache {cache_item}: {res}")
            return res

        try:

            res = self.request_call(method, url, payload)
            DataQueueService()[cache_item] = res
            if enforce_result:
                return DataQueueService().wait(cache_item, timeout)

            return cache_item.Key
        except AssertionError:
            raise
        except Exception as e:
            f, li = get_error_info()
            logger.error(f"Error Session call: {e}; File: {f}:{li}")
            raise

    def request_call(self, method: SupportedMethods, url, payload=None):
        global REQUEST_COUNTER, REQUEST_TIMEOUT
        try:
            retry_count = 3
            if payload is None:
                payload = {}
            request_method = self._get_method(method)
            while self._throttle_activated:
                sleep(0.5)
            response = None

            while True:
                try:
                    REQUEST_COUNTER += 1
                    response = request_method(url, auth=self.auth, headers=self.headers, data=json.dumps(payload),
                                              timeout=REQUEST_TIMEOUT)
                    assert response.status_code == 200, response
                except AssertionError as e:
                    response = e.args[0]
                    if response.status_code == 429:
                        end_throttling_period = time.perf_counter()
                        event = json.loads(response.content)['errors'][0]
                        throttling_event = \
                            f"{REQUEST_COUNTER} calls on last {end_throttling_period - REQUEST_TIMEOUT}s."
                        REQUEST_COUNTER = 0
                        REQUEST_TIMEOUT = time.perf_counter()
                        logger.warning(f"{response.status_code} {event['title']} got on {method.name} {url} "
                                       f"[{throttling_event}]")
                        self.wait_throttle_timeout(event['Retry-After'])
                        logger.warning(f"Continue after throttling timeout")
                    elif response.status_code == 500:
                        assert retry_count > 0, f"Cannot perform API action during 3 times\nRequest: {url} {payload}"
                        logger.warning(f"Server error occurred on payload:\nRequest {url} {payload}\n"
                                       f"Response:\n{response.content}\nRetrying...")
                        retry_count -= 1
                        sleep(0.5)
                    else:
                        raise
                except TypeError as e:
                    f, li = get_error_info()
                    logger.error(f"Error API call: URL: {url} {response} "
                                 f"[{type(e).__name__}: {e}; File: {f}:{li}]"
                                 f"\n-----------------------\n{payload}\n-----------------------\n")
                    retry_count -= 1
                except Exception as e:
                    f, li = get_error_info()
                    logger.error(f"Error API call: URL: {url} {response} "
                                 f"[{type(e).__name__}: {e}; File: {f}:{li}]")
                    retry_count -= 1
                    sleep(0.5)
                else:
                    if retry_count < 3:
                        logger.warning(f"API call succeed after error: {url}")
                    break
            return json.loads(response.content)

        except Exception as e:
            f, li = get_error_info()
            logger.error(f"Error API call: {e}; File: {f}:{li}")
