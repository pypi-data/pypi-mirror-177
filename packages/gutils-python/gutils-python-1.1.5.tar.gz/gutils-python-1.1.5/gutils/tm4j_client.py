import json
import requests
from adaptavist import Adaptavist
from requests.exceptions import HTTPError
from gutils.config.settings import JIRA_URL, JIRA_USER, JIRA_PASSWORD


class TM4JClient(Adaptavist):
    def __init__(self, jira_user=JIRA_USER, jira_pwd=JIRA_PASSWORD):
        super(TM4JClient, self).__init__(JIRA_URL, jira_user, jira_pwd)

    def get_test_case_keys_in_folder(self, project_key, folder_id, priority=None):
        """
        Get test cases keys with given priority in given folder by folder ID

        :param project_key: key of given project, e.g. GFDAX
        :param folder_id: ID of given folder, e.g. 131410
        :param priority: optional, list of case priority, e.g. ['Critical', 'High']; no filter of priority by default
        :return: List of keys of test cases
        """
        search_string = 'projectKey = "{}" AND folderId = "{}"'.format(project_key, folder_id)
        if priority:
            search_string += ' AND priority IN ({})'.format(','.join(priority))

        return [case['key'] for case in self.get_test_cases(search_mask=search_string)]

    def delete_test_run(self, test_run_id):
        """
        Delete given test run by test run id

        :param test_run_id: ID of test run to delete
        :return: Bool True if succeed, otherwise False
        """
        request_url = self.jira_server + "/rest/tests/1.0/testrun/bulk/delete"

        request_data = [test_run_id]

        try:
            request = requests.post(request_url,
                                    auth=self._authentication,
                                    headers=self._headers,
                                    data=json.dumps(request_data))
            request.raise_for_status()
        except HTTPError as ex:
            self._logger.debug("request failed. %s", ex)
            return False
        except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as ex:
            self._logger.error("request failed. %s", ex)
            return False

        return True

    def get_test_run_id_by_key(self, test_run_key):
        """
        Get test run id by given test run key

        :param test_run_key:
        :return: test run ID
        """
        self._logger.debug("get_test_run_by_name(\"%s\")", test_run_key)

        request_url = self.jira_server + "/rest/tests/1.0/testrun/{}?fields=id".format(test_run_key)

        try:
            request = requests.get(request_url,
                                   auth=self._authentication,
                                   headers=self._headers)
            request.raise_for_status()
        except HTTPError as ex:
            self._logger.debug("request failed. %s", ex)
            return {}
        except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as ex:
            self._logger.error("request failed. %s", ex)
            return {}

        response = {} if not request.text else request.json()

        return response['id']

    def get_test_case_results(self, test_case_id):
        """
        Get execution results about a test case.

        :param str test_case_id: test case id to look for
        :return: Execution result about test case
        """
        request_url = self.jira_server + "/rest/tests/1.0/testcase/{}/testresults?fields=testResultStatus(name,i18nKey,color),key".format(
            test_case_id)

        try:
            request = requests.get(request_url,
                                   auth=self._authentication,
                                   headers=self._headers)
            request.raise_for_status()
        except HTTPError as ex:
            self._logger.debug("request failed. %s", ex)
            return {}
        except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as ex:
            self._logger.error("request failed. %s", ex)
            return {}

        response = {} if not request.text else request.json()

        return response['data']

    def get_test_case_id(self, test_case_key):
        """
        Get ID for given test case by its key.

        :param str test_case_key: test case key to look for
        :return: ID of given test case
        """
        request_url = self.jira_server + "/rest/tests/1.0/testcase/{}?fields=id".format(test_case_key)

        try:
            request = requests.get(request_url,
                                   auth=self._authentication,
                                   headers=self._headers)
            request.raise_for_status()
        except HTTPError as ex:
            self._logger.debug("request failed. %s", ex)
            return {}
        except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as ex:
            self._logger.error("request failed. %s", ex)
            return {}

        response = {} if not request.text else request.json()

        return response['id']

    def get_test_execution_result(self, test_execution_key):
        """
        Get execution result by test execution key.

        :param str test_execution_key: test execution key
        :return: Dict of Execution result
        """
        request_url = self.jira_server + "/rest/tests/1.0/testresult/{}?fields=id,comment".format(test_execution_key)

        try:
            request = requests.get(request_url,
                                   auth=self._authentication,
                                   headers=self._headers)
            request.raise_for_status()
        except HTTPError as ex:
            self._logger.debug("request failed. %s", ex)
            return {}
        except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as ex:
            self._logger.error("request failed. %s", ex)
            return {}

        response = {} if not request.text else request.json()

        return response

    def get_test_cases_by_execution_status(self, test_run_key, status):
        """
        Get test results by specific status
        :param test_run_key: str, test cycle key, e.g. GFDAX-C546
        :param status: str, 'Pass', 'Fail' or 'Not Executed'
        :return: list, test cases key, e.g. ['GFDAX-T4188', 'GFDAX-T4190', 'GFDAX-T4195']
        """
        results = self.get_test_run(test_run_key)

        return [case['testCaseKey'] for case in results['items'] if case['status'] == status]
