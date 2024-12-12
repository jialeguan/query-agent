from agent.tools import *

tool_definitions = [
    (get_pod_count,
        "Get the number of pods in the specified namespace. Parameters: namespace."),
    (get_pod_status,
        "Get the status of a specified pod in the namespace. Parameters: pod_name, namespace."),
    (get_pod_logs,
        "Get the logs of a specified pod in the namespace. Parameters: pod_name, namespace."),
    (get_pods_by_deployment,
        "Get the number of pods spawned by a deployment in the namespace. Parameters: deployment_name, namespace."),
    (get_pods_with_label,
        "Get the number of pods with a specified label in the namespace. Parameters: label_key=app, label_value, namespace."),
    (get_service_count,
        "Get the number of services in the specified namespace. Parameters: namespace."),
    (get_service_count_all,
        "Get the number of services in the cluster. Parameters: None"),
    (get_deployment_count,
        "Get the number of deployments in the specified namespace. Parameters: namespace."),
    (get_node_count,
        "Get the number of nodes in the cluster. Parameters: None"),
    (get_namespace_count,
        "Get the number of namespaces in the cluster. Parameters: None"),
]
