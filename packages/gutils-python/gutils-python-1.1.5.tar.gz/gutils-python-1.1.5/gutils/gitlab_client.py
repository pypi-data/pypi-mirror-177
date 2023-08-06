import os
import requests


class GitlabClient(object):
    def __init__(self, token, local_path=None):
        self._base_url = 'https://gitlab.myteksi.net/api/v4'
        self._token = token
        self._artifacts_file_name = 'artifacts.zip'
        self._local_path = local_path if local_path else '/tmp'

    def download_artifacts(self, project_id, job_id, file_path=None):
        """
        Download artifacts(archive file or specific file)
        :param project_id:
        :param job_id:
        :param file_path: (optional) the relative path of target file, e.g. test/build/grab.ipa;
        None by default, will download archive file of artifacts
        :return: absolute local path for downloaded file, e.g. /tmp/artifacts.zip
        """
        url = '{}/projects/{}/jobs/{}/artifacts'.format(self._base_url, project_id, job_id)
        if file_path:
            url += '/{}'.format(file_path)
            filename = file_path.split('/')[-1]
        else:
            filename = self._artifacts_file_name
        download_path = '{}/{}'.format(self._local_path, filename)
        resp = requests.get(url, headers={'PRIVATE-TOKEN': self._token})
        if resp.status_code != 200:
            raise Exception('Error found in downloading artifacts')
        if os.path.exists(download_path):
            os.remove(download_path)
        with open(download_path, "wb") as build_file:
            build_file.write(resp.content)
        return download_path

    def get_job_id_by_pipeline_id_and_job_name(self, project_id, pipeline_id, job_name):
        """
        Get job id by job name
        :param project_id: The ID or URL-encoded path(e.g. mobile%2Fpax-ios) of the project
        :param pipeline_id:
        :param job_name: e.g. qa build
        :return: job id or None
        """
        url = '{}/projects/{}/pipelines/{}/jobs?per_page=100'.format(self._base_url, project_id, pipeline_id, job_name)

        resp = requests.get(url, headers={'PRIVATE-TOKEN': self._token})
        if resp.status_code != 200:
            raise Exception('Error to get jobs from pipeline {}'.format(pipeline_id))
        for job in resp.json():
            if job['name'] == job_name:
                return job['id']
        return None

    def get_job_id_by_commit_sha_and_job_name(self, project_id, commit_sha, job_name):
        """
        Get job id by commit sha and job name
        :param project_id: The ID or URL-encoded path(e.g. mobile%2Fpax-android) of the project
        :param commit_sha:
        :param job_name: e.g. qa_build
        :return: job id or None
        """
        url = '{}/projects/{}/repository/commits/{}/statuses?name={}'.format(self._base_url, project_id, commit_sha, job_name)

        resp = requests.get(url, headers={'PRIVATE-TOKEN': self._token})
        if resp.status_code != 200:
            raise Exception('Error to get jobs from commit_sha[{}] and job_name {}'.format(commit_sha, job_name))
        if resp.json():
            return [job['id'] for job in resp.json()]
        else:
            return None
