import pytest
import requests

# Define the target URL for the API
BASE_URL = "http://localhost:8000/query"

# Dynamically generate test cases from the Kubernetes cluster state
test_cases = [
    {
        # kubectl get pods -n default --no-headers | wc -l
        "query": "How many pods are in the default namespace?",
        "expected": "3"
    },
    {
        # kubectl get services -n default --no-headers | wc -l
        "query": "How many services are in the default namespace?",
        "expected": "2"
    },
    {
        # kubectl get pods --selector=app=nginx
        "query": "What is the status of the pod named nginx-deployment-7cdd46f898-4nvkv",
        "expected": "1"
    },
    {
        # kubectl get nodes --no-headers | wc -l
        "query": "How many nodes are in the cluster?",
        "expected": "1"
    },
    {
        # kubectl get namespaces --no-headers | wc -l
        "query": "How many namespaces are in the cluster?",
        "expected": "5"
    }
]

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

    # Extract the answer from the response
    answer = response.json()["answer"]

    # Validate the response content
    assert answer == test_case["expected"], f"Failed for query: {test_case['query']}"


if __name__ == "__main__":
    pytest.main()
