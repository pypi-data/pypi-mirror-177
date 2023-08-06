from __future__ import annotations

import os.path
import re
from typing import Callable

from robotframework_practitest import utils
from robotframework_practitest.utils.logger import logger
from robotframework_practitest.models import practi_test as pt, robot as rb
from robotframework_practitest.models.field_adapter import fields_factory
from robotframework_practitest.models.practi_test import data_formatters as df
from robotframework_practitest.models.robot.helpers import get_test_fields, get_test_set_fields
from robotframework_practitest.services import data_queue as data, configuration, statistics as st

MISSED_TEST_IDs = []


def convert_test_display_to_id(client, *tags):
    kwargs = {'enforce_result': True, 'timeout': 3}
    related_test_display_ids = rb.helpers.get_related_test_display_ids(*tags)
    result_test_ids = []
    for display_id in related_test_display_ids:
        try:
            kwargs.update(**{'formatter': df.filter_test_by_display_id(display_id), 'display-ids': display_id})
            test_d = client.query_test(**kwargs)
            assert test_d
            result_test_ids.append(test_d['id'])
        except Exception as e:
            global MISSED_TEST_IDs
            MISSED_TEST_IDs.append(display_id)
    return result_test_ids


class RobotToPractiTest_Adapter(st.DataStatistics):
    def __init__(self):
        super().__init__()
        self._client: pt.PtClient = None
        self.test_set_hash_tag = None
        self.test_info_fields = {}
        self.test_tag_mapping = {}
        self.test_set_info_fields = {}
        self._involved_tags = []
        self._current_suite_cache = {}
        self.enabled_reporting = False
        self._data_driver_flag = False
        self.test_set_level = None
        self.current_suite_path_list = []
        self.external_run_id = None

    def init_adapter(self, client: pt.PtClient):
        self._client = client
        self.test_info_fields = fields_factory(get_test_fields())
        self.test_set_info_fields = fields_factory(get_test_set_fields())
        logger.info(f"Robot to PractiTest Adapter ready")

    @property
    def project_id(self):
        return self._client.project_id

    def add_suite_tests(self, suite: rb.wrappers.PTestSuite):
        try:
            tests_info = [(test.name, test.parent) for test in suite.tests]
            for test, path in tests_info:
                self.set_tests(st.TestStates.Robot, test, path=path)
            logger.info("\nPractiTest reporter: Suite '{0}' tests added:\n\t:{1}".format(
                suite.name,
                '\n\t'.join([f"{t} ({p})" for t, p in tests_info])))
        except Exception as e:
            f, li = utils.get_error_info()
            logger.error(f"{type(e).__name__}: {e}; File: {f}:{li}")

    def get_active_test_set_id(self, timeout=None):
        timeout = timeout or data.DEFAULT_ITEM_WAIT
        timeout += self._client.active_timeout
        try:
            return data.DataQueueService().wait(data.CacheItem(self._client.test_set_tag, self.test_set_hash_tag),
                                                timeout)
        except Exception as e:
            self.enabled_reporting = False
            logger.error(f"Cannot occur active test set; reporting to PractiTEst not allowed")

    def start_test_set(self, name, version, post_process: Callable = None, tags: list = None, **test_set_info):
        try:
            test_set_formatter = lambda data_: dict(id=data_['data']['id'],
                                                    display_id=data_['data']['attributes']['display-id'],
                                                    set_name=data_['data']['attributes']['name'],
                                                    )
            self.test_set_hash_tag = self._client.create_test_set(name,
                                                                  version=version,
                                                                  formatter=test_set_formatter,
                                                                  ignore_cache=True,
                                                                  tags=tags,
                                                                  **test_set_info)
            if post_process:
                post_process()
            logger.info(f"TestSet#{self.get_active_test_set_id()['display_id']}: Created from suite '{name}'")
        except Exception as e:
            f, w = utils.get_error_info()
            logger.error(f"PractiTest start_test_set: Cannot create TestSet '{name}'; Error: {e}; File: {f}:{w}")
            self.enabled_reporting = False
            raise

    def create_test_instance(self, robot_name, pt_name, tags, pure_tags, path, description, version, *steps,
                             **custom_fields):
        test_data = self._get_or_create_test(robot_name, pt_name, tags, description, version, *steps,
                                             **custom_fields)

        self.set_tests(st.TestStates.PractiTest, robot_name, status=st.TestStatuses.Pending,
                       path=path, update=pt_name, id_=f"Test#{test_data['attributes']['display-id']}")
        test_id = test_data['id']
        related_tests_list = convert_test_display_to_id(self._client, *pure_tags)
        full_tests_list = set([test_id] + related_tests_list)
        instance_list = []

        test_set_id = self.get_active_test_set_id(self._client.active_timeout).get('id')

        for id_ in full_tests_list:
            try:
                hash_tag = f"{test_set_id}_{id_}"
                self._client.create_test_instance(test_set_id, id_, version, hash_tag=hash_tag,
                                                  formatter=lambda d: d['data']['id'])

                instance_list.append(hash_tag)
                logger.info(f"Test '{robot_name}': Run Instance created with name '{pt_name}' (Id: {test_id})")
            except Exception as e:
                f, w = utils.get_error_info()
                logger.error(
                    f"PractiTest create_test_instance: "
                    f"Cannot add '{robot_name}' (Test#{id_}) to TestSet ({self.test_set_hash_tag}) "
                    f"[Error: {e}; File: {f}:{w}]"
                )
        data.DataQueueService()[data.CacheItem('run_instances', pt_name)] = set(instance_list)

    def _get_or_create_test(self, robot_name, pt_name, tags, description, version, *steps, **custom_fields):
        attempts = 0
        while True:
            test_data = self._client.query_test(name_exact=pt_name, ignore_cache=True, enforce_result=True,
                                                formatter=df.filter_test_by_name(pt_name), timeout=5)
            if test_data:
                logger.debug(f"Test {pt_name} already existing")
                return test_data
            try:
                assert attempts <= rb.helpers.TEST_ALLOWED_CREATE_ATTEMPTS, \
                    f"Cannot get or create test '{robot_name}' during {attempts} attempts"
                test_data = self._client.create_test_case(pt_name, version=version, description=description, tags=tags,
                                                          steps=steps, ignore_cache=True,
                                                          formatter=df.filter_test_by_name(pt_name), **custom_fields)
                logger.warning(f"Test '{robot_name}' created as '{pt_name}' successfully")
                return test_data
            except AssertionError as e:
                logger.error(e)
                raise
            except Exception as e:
                logger.error(f"Error creating test '{robot_name}': {e}")
                raise
            finally:
                attempts += 1

    def set_test_results(self, test: rb.wrappers.PTestCase, results: rb.wrappers.PTestResult):
        try:
            test_name = rb.helpers.get_name(test.name, *test.parent)
            related_test_list = data.DataQueueService().wait(data.CacheItem('run_instances', test_name),
                                                             configuration.WAIT_FOR_TEST_CREATED)
            logger.info(f"Result: {results.name}; {results.status}; Duration: {results.duration}")
            for index, instance in enumerate(related_test_list):
                try:
                    set_id, test_id = instance.split('_', 1)
                    instance_id = data.DataQueueService().wait(data.CacheItem(self._client.instance_tag, instance))
                    files = []
                    if len(results.automated_execution_output) > 255:
                        file_path = utils.write_to_temp_file(results.automated_execution_output,
                                                             name=re.sub(r'\\|\/|\s+', '_', test.name),
                                                             suffix=f"{instance_id}.txt")
                        file_name = os.path.basename(file_path)
                        files.append(file_path)
                        automated_execution_output = f"Output redirected to file: {file_name}"
                    else:
                        automated_execution_output = results.automated_execution_output

                    self._client.create_run(instance_id, results.exit_code, results.duration,
                                            automated_execution_output, files=files)
                    logger.info(
                        f"PractiTest Reporter: {'Robot' if index == 0 else 'Referenced'} Test '{test_name}' "
                        f"completed: {results.status} (TestSet: {set_id}, Test: {test_id}, Instance {instance_id})")
                except Exception as e:
                    logger.error(f"PractiTest Reporter: Error report result for test '{test_name}': {e}")
                else:
                    self.set_tests(st.TestStates.Status, test.name, status=st.TestStatuses[results.status],
                                   path=test.parent)
        except Exception as e:
            f, w = utils.get_error_info()
            logger.error(f"PractiTest set_test_results {test.name} [Error: {e}; File: {f}:{w}]")
            raise
