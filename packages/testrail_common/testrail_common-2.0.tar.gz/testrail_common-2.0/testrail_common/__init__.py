from testrail_common import testrail
import configparser

config = configparser.ConfigParser()


class TestRailApi:
    def __init__(self, url, project, suite):
        self.config = config.read('system.config')
        self.client = APIClient(url)
        self.client.user = config.get('Testrail', 'username')
        self.client.password = config.get('Testrail', 'password')
        self.projectId = config.get('Testrail', project)
        self.test_suite = config.get('Testrail', suite)

    def testrail_get_all_cases_from_suite(self):
        """ Fetch all appropriate test cases from TestRail """
        valid_list = []
        try:
            test_cases = self.client.send_get(f'get_cases/{self.projectId}&suite_id={self.test_suite}')
        except Exception as e:
            print(e)

        for cases in test_cases['cases']:
            valid_case = dict(
                title=cases['title'],
                id=cases['id']
            )
            valid_list.append(valid_case)

        return valid_list

    def testrail_get_case(self, case_id):
        """ Fetch specific test cases from TestRail using test case ID """
        try:
            get_case = self.client.send_get(f'get_case/{case_id}')
        except Exception as e:
            print(e)

        return get_case

    def testrail_get_active_run(self):
        """ Get active test run in TestRail """
        active = []
        get_run = self.client.send_get(f'get_runs/{self.projectId}')
        for runs in get_run['runs']:
            if not runs['is_completed']:
                print(f"Active test run found... RunID = {runs['id']}")
                active.append({'id': runs['id'], 'name': runs['name']})
        return active

    def testrail_create_run(self, run_name, description, milestone):
        """ Create test run in Testrail """
        test_id_list = []
        tests = self.testrail_get_all_cases_from_suite()
        for cases in tests:
            test_id_list.append(cases['id'])
        data = {
            "suite_id": self.test_suite,
            "name": run_name,
            "description": description,
            "milestone_id": milestone,
            "include_all": False,
            "case_ids": test_id_list
        }
        print("Adding a test run...")
        try:
            self.client.send_post(f'add_run/{self.projectId}', data)
        except Exception as e:
            print(e)

    def testrail_add_bulk_results(self, run_id, results):
        """ Send test results to active test run in Testrail """
        try:
            self.client.send_post(f'add_results_for_cases/{run_id}', {"results": results})
        except Exception as e:
            print(e)

    def testrail_close_active_run(self, run_id):
        """ Close an active test run in TestRail """
        try:
            self.client.send_post(f"close_run/{run_id}", "")
        except Exception as e:
            print(e)
