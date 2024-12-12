import subprocess

import pytest
import requests

# Define the target URL for the API
BASE_URL = "http://localhost:8000/query"

# Dynamically generate test cases by executing `kubectl` commands


def get_kubectl_expected_results():
    """
    Execute `kubectl` commands to retrieve the expected results from the Kubernetes cluster.
    Returns a list of test cases with queries and expected results.
    """
    test_cases = []

    pod_list = subprocess.check_output(
        "kubectl get pods -n test --no-headers", shell=True, text=True
    ).strip().split("\n")

    pod_name = pod_list[0].split()[0]

    # 1. Query: Number of pods in the default namespace
    try:
        pods_count = subprocess.check_output(
            "kubectl get pods -n default --no-headers | wc -l", shell=True, text=True
        ).strip()
        test_cases.append(
            {"query": "How many pods in the default namespace?", "expected": pods_count})
    except subprocess.CalledProcessError as e:
        print(f"Error executing kubectl command for pods: {e}")

    # 2. Query: Number of pods in the test namespace
    try:
        pods_count = subprocess.check_output(
            "kubectl get pods -n test --no-headers | wc -l", shell=True, text=True
        ).strip()
        test_cases.append(
            {"query": "How many pods in the test namespace?", "expected": pods_count})
    except subprocess.CalledProcessError as e:
        print(f"Error executing kubectl command for pods: {
            e}")

    # 3. Query: Get the status of a specific pod in the test namespace
        # select the first pod from the list
    try:
        pod_status = subprocess.check_output(
            f"kubectl get pod {pod_name} -n test -o jsonpath={{.status.phase}}", shell=True, text=True
        ).strip()
        test_cases.append(
            {"query": f"Get the status of the pod {pod_name} in the test namespace.", "expected": pod_status})
    except subprocess.CalledProcessError as e:
        print(f"Error executing kubectl command for pod status: {e}")

    # 4. Query: Get the log of
    try:
        nginx_pods_count = subprocess.check_output(
            "kubectl get pods -n default -l app=nginx --no-headers | wc -l", shell=True, text=True
        ).strip()
        test_cases.append(
            {"query": "Get the number of pods with a specific label nginx in the default namespace.", "expected": nginx_pods_count})
    except subprocess.CalledProcessError as e:
        print(f"Error executing kubectl command for nginx pods: {e}")

    return test_cases


# Dynamically generate test cases from the Kubernetes cluster state
test_cases = get_kubectl_expected_results()

# Use pytest to parameterize test cases


@pytest.mark.parametrize("test_case", test_cases)
def test_query_endpoint(test_case):
    """
    Test the /query endpoint with various queries and validate the responses against expected results.
    """
    # Construct the API request payload
    payload = {"query": test_case["query"]}
    headers = {"Content-Type": "application/json"}

    # Send the POST request to the API
    response = requests.post(BASE_URL, json=payload, headers=headers)

    # Ensure the response status code is 200
    assert response.status_code == 200, f"Failed for query: {test_case['query']}"

    # Validate the response content contains the expected result
    assert test_case["expected"] in response.text, f"Unexpected response: {response.text}"
    assert test_case["expected"] in response.text, f"Unexpected response: {response.text}"
