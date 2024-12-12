import os

from kubernetes import config
from langchain.agents import initialize_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

from .tool_config import tool_definitions
from .tools import *


class KubernetesAgent:
    def __init__(self):
        self._init_k8s()

        self.tools = self._generate_tools()

        self.system_prompt = """
        You are a Kubernetes management assistant.
        When you invoke a took, please provide the necessary parameters as a JSON object.
        **Notes**:
        - If not specified, do not check different namespaces, label, or deployment.
        - Only respond with the exact number or result, without any additional words or context.
        - Return only the answer, without identifiers (e.g., "mongodb" instead of "mongodb-56c598c8fc").

        """

        self.llm = ChatOpenAI(temperature=0.1,)
        self.agent = initialize_agent(
            self.tools, self.llm, agent="zero-shot-react-description", verbose=True
        )

    def _init_k8s(self):
        """
        Initialize the Kubernetes client based on the execution environment.
        """
        try:
            config.load_incluster_config()
            logging.info(
                "Successfully loaded in-cluster Kubernetes configuration.")
        except config.ConfigException:
            kube_config_path = os.environ.get(
                "KUBECONFIG", os.path.expanduser("~/.kube/config")
            )
            try:
                config.load_kube_config(config_file=kube_config_path)
                logging.info(
                    f"Successfully loaded kubeconfig from {kube_config_path}.")
            except config.ConfigException as e:
                logging.error(
                    "Failed to configure Kubernetes client using both in-cluster and out-of-cluster methods."
                )
                logging.error(f"Error details: {e}")
                raise RuntimeError(
                    "Failed to configure Kubernetes client. Please ensure a valid kubeconfig is available."
                )

    def _generate_tools(self):
        """
        Dynamically generate a list of tools with their descriptions
        including the function signature.
        """
        tools = []

        for function, description in tool_definitions:
            tools.append(
                Tool(name=function.__name__,
                     description=description,
                     func=function)
            )
        return tools

    def handle_query(self, user_input: str):
        combined_input = f"{self.system_prompt}\n\nUser Input: {user_input}"
        return self.agent.run(combined_input)
