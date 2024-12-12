import json
import logging

from kubernetes import client


def evaluate(action_input: str) -> dict:
    """
    Evaluate the action input from str to dict
    """
    try:
        input_data = json.loads(action_input)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON input.")
    return input_data


'''
pod query
'''


def get_pod_count(action_input: str) -> int:
    """
    Get the number of pods in the specified namespace.
    Input: {"namespace": "default"}
    """
    return len(get_pod_list(action_input))


def get_pod_list(action_input: str) -> str:
    """
    Get the list of pods in the specified namespace.
    Input: {"namespace": "default"}
    """
    logging.info(f"Input data: {action_input}")

    action_input = evaluate(action_input)
    namespace = action_input.get("namespace", "default")
    k8s_client = client.CoreV1Api()
    pods = k8s_client.list_namespaced_pod(namespace)
    pod_list = [pod.metadata.name for pod in pods.items]
    return pod_list


def get_pod_status(action_input: str) -> str:
    """
    Get the status of a pod in the specified namespace.
    Input: {"pod_name": "example-pod", "namespace": "default"}
    """
    logging.info(f"Input data: {action_input}")
    action_input = evaluate(action_input)
    pod_name = action_input.get("pod_name")  #
    if not pod_name:
        raise ValueError("The 'pod_name' field is required.")
    namespace = action_input.get("namespace", "default")

    k8s_client = client.CoreV1Api()
    pod = k8s_client.read_namespaced_pod(pod_name, namespace)
    return pod.status.phase


def get_pod_logs(action_input: str) -> str:
    """
    Get the logs of a pod in the specified namespace.
    Input: {"pod_name": "example-pod", "namespace": "default"}
    """
    logging.info(f"Input data: {action_input}")
    action_input = evaluate(action_input)
    pod_name = action_input.get("pod_name")
    if not pod_name:
        raise ValueError("The 'pod_name' field is required.")
    namespace = action_input.get("namespace", "default")

    k8s_client = client.CoreV1Api()
    try:
        logs = k8s_client.read_namespaced_pod_log(pod_name, namespace)
        return logs
    except client.exceptions.ApiException as e:
        return f"Error retrieving logs: {str(e)}"


def get_pods_by_deployment(action_input: str) -> int:
    """
    Get the number of pods spawned by a deployment in the specified namespace.
    Input: {"deployment_name": "example-deployment", "namespace": "default"}
    """
    logging.info(f"Input data: {action_input}")
    action_input = evaluate(action_input)
    deployment_name = action_input.get("deployment_name")
    if not deployment_name:
        raise ValueError("The 'deployment_name' field is required.")
    namespace = action_input.get("namespace", "default")

    k8s_client = client.CoreV1Api()
    k8s_apps_client = client.AppsV1Api()
    try:
        deployment = k8s_apps_client.read_namespaced_deployment(
            deployment_name, namespace)
        match_labels = deployment.spec.selector.match_labels
        label_selector = ",".join(
            f"{key}={value}" for key, value in match_labels.items())

        pods = k8s_client.list_namespaced_pod(
            namespace, label_selector=label_selector)

        return len(pods.items)

    except client.exceptions.ApiException as e:
        return f"Error retrieving pods by deployment: {str(e)}"


def get_pods_with_label(action_input: str) -> int:
    """
    Get the number of pods with a specific label in the specified namespace.
    Input: {"label_key": "app", label_value: "nginx", "namespace": "default"}
    """
    logging.info(f"Input data: {action_input}")
    action_input = evaluate(action_input)
    label_key = action_input.get("label_key", "app")
    label_value = action_input.get("label_value")
    if not label_value:
        raise ValueError("The 'label_value' field is required.")
    namespace = action_input.get("namespace", "default")

    k8s_client = client.CoreV1Api()
    pods = k8s_client.list_namespaced_pod(
        namespace, label_selector=f"{label_key}={label_value}")
    return len(pods.items)


'''
service query
'''


def get_service_count(action_input: str) -> int:
    """
    Get the number of services in the specified namespace.
    Input: {"namespace": "default"}
    """
    logging.info(f"Input data: {action_input}")
    action_input = evaluate(action_input)
    namespace = action_input.get("namespace", "default")

    k8s_client = client.CoreV1Api()
    services = k8s_client.list_namespaced_service(namespace)
    return len(services.items)


def get_service_list(action_input: str) -> str:
    """
    Get the list of services in the specified namespace.
    Input: {"namespace": "default"}
    """
    logging.info(f"Input data: {action_input}")
    action_input = evaluate(action_input)
    namespace = action_input.get("namespace", "default")

    k8s_client = client.CoreV1Api()
    services = k8s_client.list_namespaced_service(namespace)
    service_list = [service.metadata.name for service in services.items]
    return service_list


def get_service_count_all(action_input: str) -> int:
    """
    Get the number of services in all namespaces.
    Input: {}
    """
    logging.info(f"Input data: {action_input}")

    k8s_client = client.CoreV1Api()
    services = k8s_client.list_service_for_all_namespaces()
    return len(services.items)


def get_deployment_count(action_input: str) -> int:
    """
    Get the number of deployments in the specified namespace.
    Input: {"namespace": "default"}
    """
    return len(get_deployment_list(action_input))


def get_deployment_list(action_input: str):
    """
    Get the list of deployments in the specified namespace.
    Input: {"namespace": "default"}
    """
    logging.info(f"Input data: {action_input}")
    action_input = evaluate(action_input)
    namespace = action_input.get("namespace", "default")

    k8s_client = client.AppsV1Api()
    deployments = k8s_client.list_namespaced_deployment(namespace)
    deployment_list = [
        deployment.metadata.name for deployment in deployments.items]
    return deployment_list


def get_node_count(action_input: str) -> int:
    return len(get_node_list(action_input))


def get_node_list(action_input: str) -> str:
    """
    Get the list of nodes in the cluster.
    Input: {}
    """
    logging.info(f"Input data: {action_input}")

    k8s_client = client.CoreV1Api()
    nodes = k8s_client.list_node()
    node_list = [node.metadata.name for node in nodes.items]
    return node_list


def get_namespace_count(action_input: str) -> int:
    """
    Get the number of namespaces in the cluster.
    Input: {}
    """
    logging.info(f"Input data: {action_input}")

    k8s_client = client.CoreV1Api()
    namespaces = k8s_client.list_namespace()
    return len(namespaces.items)
