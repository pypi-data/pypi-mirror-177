# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airflow_google_cloud_run_plugin',
 'airflow_google_cloud_run_plugin.cloud_run_v1',
 'airflow_google_cloud_run_plugin.cloud_run_v1.namespaces',
 'airflow_google_cloud_run_plugin.cloud_run_v1.types',
 'airflow_google_cloud_run_plugin.cloud_run_v1.utils',
 'airflow_google_cloud_run_plugin.hooks',
 'airflow_google_cloud_run_plugin.operators.cloud_run']

package_data = \
{'': ['*']}

install_requires = \
['google-auth>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'airflow-google-cloud-run-plugin',
    'version': '0.3.2',
    'description': 'Airflow plugin for Google Cloud Run Jobs',
    'long_description': '# airflow-google-cloud-run-plugin\n\n[![PyPI version](https://badge.fury.io/py/airflow-google-cloud-run-plugin.svg)](https://badge.fury.io/py/airflow-google-cloud-run-plugin)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/airflow-google-cloud-run-plugin)](https://pypi.org/project/airflow-google-cloud-run-plugin/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/airflow-google-cloud-run-plugin.svg)](https://pypi.org/project/airflow-google-cloud-run-plugin/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nAirflow plugin for\norchestrating [Google Cloud Run jobs](https://cloud.google.com/run/docs/overview/what-is-cloud-run#jobs).\n\n## Features\n\n1. Easier to use alternative\n   to [`KubernetesPodOperator`](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html)\n2. Securely use sensitive data stored in Google Cloud Secrets Manager\n3. Create tasks with isolated dependencies\n4. Enables polyglot workflows\n\n## Resources\n\n### Core Operators\n\n1. `CloudRunJobOperator`\n\n### CRUD-Based Operators\n\n1. `CloudRunCreateJobOperator`\n2. `CloudRunGetJobOperator` 🔜\n3. `CloudRunUpdateJobOperator` 🔜\n4. `CloudRunDeleteJobOperator`\n5. `CloudRunListJobsOperator` 🔜\n\n### Hooks\n\n1. `CloudRunJobHook`\n\n### Sensors\n\n2. `CloudRunJobExecutionSensor` 🔜\n\n## Usage\n\n### Simple Job Lifecycle\n\n```python\nfrom airflow import DAG\n\nfrom airflow_google_cloud_run_plugin.operators.cloud_run import CloudRunJobOperator\n\nwith DAG(dag_id="example_dag") as dag:\n  job = CloudRunJobOperator(\n    task_id="example-job",\n    name="example-job",\n    location="us-central1",\n    project_id="example-project",\n    image="gcr.io/gcp-runtimes/ubuntu_18_0_4",\n    command=["echo"],\n    cpu="1000m",\n    memory="512Mi",\n    create_if_not_exists=True,\n    delete_on_exit=True\n  )\n```\n\n### CRUD Job Lifecycle\n\n```python\nfrom airflow import DAG\n\nfrom airflow_google_cloud_run_plugin.operators.cloud_run import (\n  CloudRunJobOperator,\n  CloudRunCreateJobOperator,\n  CloudRunDeleteJobOperator,\n)\n\nwith DAG(dag_id="example_dag") as dag:\n  create_job = CloudRunCreateJobOperator(\n    task_id="create",\n    name="example-job",\n    location="us-central1",\n    project_id="example-project",\n    image="gcr.io/gcp-runtimes/ubuntu_18_0_4",\n    command=["echo"],\n    cpu="1000m",\n    memory="512Mi"\n  )\n\n  run_job = CloudRunJobOperator(\n    task_id="run",\n    name="example-job",\n    location="us-central1",\n    project_id="example-project"\n  )\n\n  delete_job = CloudRunDeleteJobOperator(\n    task_id="delete",\n    name="example-job",\n    location="us-central1",\n    project_id="example-project"\n  )\n\n  create_job >> run_job >> delete_job\n```\n\n### Using Environment Variables\n\n```python\nfrom airflow import DAG\n\nfrom airflow_google_cloud_run_plugin.operators.cloud_run import CloudRunJobOperator\n\n# Simple environment variable\nFOO = {\n  "name": "FOO",\n  "value": "not_so_secret_value_123"\n}\n\n# Environment variable from Secret Manager\nBAR = {\n  "name": "BAR",\n  "valueFrom": {\n    "secretKeyRef": {\n      "name": "super_secret_password",\n      "key": "1"  # or "latest" for latest secret version\n    }\n  }\n}\n\nwith DAG(dag_id="example_dag") as dag:\n  job = CloudRunJobOperator(\n    task_id="example-job",\n    name="example-job",\n    location="us-central1",\n    project_id="example-project",\n    image="gcr.io/gcp-runtimes/ubuntu_18_0_4",\n    command=["echo"],\n    args=["$FOO", "$BAR"],\n    env_vars=[FOO, BAR],\n    cpu="1000m",\n    memory="512Mi",\n    create_if_not_exists=True,\n    delete_on_exit=True\n  )\n```\n\n## Improvement Suggestions\n\n- Add support for Cloud Run services\n- Nicer user experience for defining args and commands\n- Use approach from other GCP operators once this issue is resolved https://github.com/googleapis/python-run/issues/64\n- Add operators for all CRUD operations\n- Add run sensor (see [link](https://github.com/apache/airflow/tree/main/airflow/providers/google/cloud/sensors))\n- Enable volume mounts (see [TaskSpec](https://cloud.google.com/run/docs/reference/rest/v1/TaskSpec))\n- Allow user to configure resource requirements `requests` (\n  see [ResourceRequirements](https://cloud.google.com/run/docs/reference/rest/v1/Container#resourcerequirements))\n- Add remaining container options (see [Container](https://cloud.google.com/run/docs/reference/rest/v1/Container))\n- Allow non-default credentials and for user to specify service account (\n  see [link](https://google-auth.readthedocs.io/en/latest/user-guide.html#service-account-private-key-files))\n- Allow failure threshold. If more than one task is specified, user should be allowed to specify number of failures\n  allowed\n- Add custom links for log URIs\n- Add wrapper class for easier environment variable definition. Similar to `Secret` from Kubernetes provider (\n  see [link](https://github.com/apache/airflow/blob/main/airflow/kubernetes/secret.py))\n- Add slight time padding between job create and run\n- Add ability to choose to replace the job with new config values if values have changed\n',
    'author': 'Michael Harris',
    'author_email': 'mharris@luabase.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mharrisb1/airflow-google-cloud-run-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
