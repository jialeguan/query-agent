import logging
import os
import subprocess

from kubernetes import config
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class CommandResponse(BaseModel):
    command: str = Field(description="The generated kubectl command.")


class SafeResponse(BaseModel):
    safe: bool = Field(description="Whether the command is safe to execute.")
    reason: str = Field(description="Reason for the safety evaluation.")


class KubernetesAgent:
    def __init__(self):
        self._init_k8s()
        self.llm = ChatOpenAI(temperature=0.1, model="gpt-4o")

        command_parser = JsonOutputParser(pydantic_object=CommandResponse)

        translate_prompt = PromptTemplate(
            input_variables=["instruction"],
            partial_variables={
                "format_instructions": command_parser.get_format_instructions()},
            template="""
            Translate the following instruction into an executable `kubectl` command:

            {format_instructions}

            Instruction: {instruction}
            Command: 
            """
        )

        safety_parser = JsonOutputParser(pydantic_object=SafeResponse)

        safety_prompt = PromptTemplate(
            input_variables=["command"],
            partial_variables={
                "format_instructions": safety_parser.get_format_instructions()},

            template="""
            Evaluate the safety of the following kubectl command:

            {format_instructions}

            Command: {command}
            Response:
            """
        )

        self.translate_chain = translate_prompt | self.llm | command_parser
        self.safety_chain = safety_prompt | self.llm | safety_parser

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

    def translate_instruction(self, instruction: str) -> str:
        '''
        translate the human input to a kubectl command
        '''
        response = self.translate_chain.invoke(
            {"instruction": instruction})
        logging.info(response)
        # print(response)
        command = response["command"]
        return command

    def evaluate_safety(self, command: str) -> bool:
        '''
        evaluate the safety of the kubectl command
        '''
        response = self.safety_chain.invoke({"command": command})
        logging.info(response)
        # print(response)
        return response["safe"]

    def execute_command(self, command: str):
        '''
        execute the kubectl command
        '''
        logging.info(f"Executing: {command}")
        try:
            result = subprocess.run(command, shell=True,
                                    capture_output=True, text=True)
            stdout, stderr = result.stdout, result.stderr
            logging.info("Execution Output:")
            logging.info(stdout)
            if stderr:
                logging.error(stderr)
            return stdout.strip()
        except subprocess.CalledProcessError as e:
            logging.error("Error during execution:")
            logging.error(e.stderr)
            return e.stderr

    def handle_query(self, instruction: str) -> str:
        '''
        handle the user query
        '''
        command = self.translate_instruction(instruction)
        # print(f"Command: {command}")
        if not self.evaluate_safety(command):
            return "Command not executed due to safety concerns."
        return self.execute_command(command)
