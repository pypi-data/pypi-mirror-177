#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com

import os
import requests
from pprint import pprint


class Bamboo(object):
    def __init__(self, host, token):
        self.__session = requests.session()
        self.__base_url = host
        self.__headers = {
            "Authorization": "Bearer %s" % token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def rest_api_list_deployment_project(self):
        """
        Bamboo REST API - GET /rest/api/latest/deploy/project/all
        :return:
        """
        url = self.__base_url + "/rest/api/latest/deploy/project/all"
        rsp = self.__session.get(url=url, headers=self.__headers)
        assert rsp.status_code == 200, "Status Code: %s \n%s" % (rsp.status_code, rsp.json())
        return rsp.json()

    def rest_api_create_deployment_version(self, project_id, version_name, plan_result_key):
        """
        Bamboo REST API - POST /rest/api/latest/deploy/project/projectId/version
        :param project_id:
        :param version_name:
        :param plan_result_key:
        :return:
        """
        url = self.__base_url + "/rest/api/latest/deploy/project/%s/version" % project_id
        body = {
            "name": version_name,
            "nextVersionName": version_name,
            "planResultKey": plan_result_key
        }
        rsp = self.__session.post(url=url, headers=self.__headers, json=body)
        assert rsp.status_code in (200, 400), "Status Code: %s \n%s" % (rsp.status_code, rsp.json())
        if rsp.status_code == 400:
            error_str = "This release version is already in use, select another."
            assert rsp.json()["fieldErrors"]["versionName"][0] == error_str, \
                "Status Code: %s \n%s" % (rsp.status_code, rsp.json())
        return rsp.json()

    def rest_api_list_deployment_version(self, project_id):
        """
        Bamboo REST API - GET /rest/api/latest/deploy/project/projectId/versions
        :param project_id:
        :return:
        """
        url = self.__base_url + "/rest/api/latest/deploy/project/%s/versions" % project_id
        rsp = self.__session.get(url=url, headers=self.__headers)
        assert rsp.status_code == 200, "Status Code: %s \n%s" % (rsp.status_code, rsp.json())
        return rsp.json()

    def rest_api_update_deployment_environment_variable(self, environment_id, variable_name, variable_value):
        """
        Bamboo REST API - PUT /rest/api/latest/deploy/environment/environmentId/variable/variableName
        :return:
        """
        url = self.__base_url + "/rest/api/latest/deploy/environment/%s/variable/%s" % (environment_id, variable_name)
        body = {
            "name": variable_name,
            "value": variable_value
        }
        rsp = self.__session.put(url=url, headers=self.__headers, json=body)
        assert rsp.status_code == 200, "Status Code: %s \n%s" % (rsp.status_code, rsp.json())
        return rsp.json()

    def rest_api_trigger_deployment_environment_setup(self, version_id, environment_id):
        """
        Bamboo REST API - POST /rest/api/latest/queue/deployment?versionId=&environmentId=
        :return:
        """
        url = self.__base_url + "/rest/api/latest/queue/deployment"
        params = {
            "versionId": version_id,
            "environmentId": environment_id
        }
        rsp = self.__session.post(url=url, headers=self.__headers, params=params)
        assert rsp.status_code == 200
        return rsp.json()

    def rest_api_list_plan_result(self, plan_key, max_results=1):
        """
        Bamboo REST API - GET /rest/api/latest/result/planKey?max-results=
        :return:
        """
        url = self.__base_url + "/rest/api/latest/result/" + plan_key
        params = {
            "max-results": max_results
        }
        rsp = self.__session.get(url=url, headers=self.__headers, params=params)
        assert rsp.status_code == 200, "Status Code: %s \n%s" % (rsp.status_code, rsp.json())
        return rsp.json()

    def get_deployment_project_id_and_env_id(self, project_name, environment_name):
        projects = self.rest_api_list_deployment_project()
        for project_item in projects:
            if project_item.get("name") == project_name:
                for env_item in project_item.get("environments"):
                    if env_item.get("name") == environment_name:
                        return {
                            "project_id": project_item.get("id"),
                            "environment_id": env_item.get("id")
                        }
        assert False, "Not found project [%s] and environment [%s]" % (project_name, environment_name)

    def update_deployment_environment_variable(self, environment_id, variables):
        for key, value in variables.items():
            if not self.rest_api_update_deployment_environment_variable(
                    environment_id,
                    variable_name=key,
                    variable_value=value
            ):
                return False
        return True

    def get_deployment_version(self, project_id):
        return self.rest_api_list_deployment_version(project_id)["versions"][0].get("id")

    def get_latest_plan_result_key(self, plan_key):
        plan_result = self.rest_api_list_plan_result(plan_key)
        return plan_result["results"]["result"][0]["planResultKey"]["key"]

    def trigger_deployment_environment_setup(self, deploy_project, deploy_environment, trigger_param):
        deploy_project_env = self.get_deployment_project_id_and_env_id(deploy_project, deploy_environment)
        deploy_project_id = deploy_project_env["project_id"]
        deploy_environment_id = deploy_project_env["environment_id"]
        deploy_version_id = self.get_deployment_version(deploy_project_id)
        self.update_deployment_environment_variable(deploy_environment_id, trigger_param)
        return self.rest_api_trigger_deployment_environment_setup(deploy_version_id, deploy_environment_id)


if __name__ == "__main__":
    print("This is Bamboo Client script")
