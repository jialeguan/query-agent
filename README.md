# KubernetesAgent: Automating and Securing `kubectl` Command Generation

## Overview

This project provides a Python-based agent, `KubernetesAgent`, that automates the generation, safety evaluation, and execution of Kubernetes `kubectl` commands. By leveraging OpenAI's language model through LangChain, the agent translates natural language instructions into executable `kubectl` commands, ensures their safety, and executes them in a Kubernetes cluster.

The agent is designed with modularity, safety, and usability in mind. It ensures the generated commands are syntactically correct, evaluates their safety before execution, and seamlessly integrates with Kubernetes environments

---

## How It Works

1. **Translate Instruction**:
   - Takes a natural language input (e.g., "List all pods in the default namespace").
   - Converts it into a structured JSON response with the `kubectl` command.

2. **Evaluate Safety**:

   - Checks the command's safety using LangChain and returns a boolean indicating whether the command is safe to execute.

3. **Execute Command**:

    - If the command is safe, it is executed using `subprocess.run`.
    - The execution output or error is logged and returned.

---

## Features

1. **Natural Language to `kubectl` Command Translation**:
   - Converts plain-language instructions into valid `kubectl` commands using OpenAI's LLM.
   - Ensures commands are returned in a structured JSON format.

2. **Safety Evaluation**:
   - Evaluates the safety of `kubectl` commands to prevent accidental or harmful operations.
   - Provides a clear safety decision (`safe` or `unsafe`) and the reasoning behind it.

3. **Command Execution**:
   - Executes the generated and validated `kubectl` commands in the configured Kubernetes environment.
   - Logs detailed execution results, including output and errors.

4. **Kubernetes Environment Initialization**:
   - Automatically detects in-cluster or out-of-cluster configurations for Kubernetes clients.

---

## Approach

### 1. **Prompt Templates with Structured Output**

The agent uses LangChain's `PromptTemplate` to define prompts for both translation and safety evaluation. Each prompt enforces structured JSON output, parsed using `JsonOutputParser`.

- **Command Translation**:
  - Input: Natural language instruction.
  - Output: JSON object containing the `kubectl` command.
  - Example:

    ```json
    {
      "command": "kubectl get pods -n default"
    }
    ```

- **Safety Evaluation**:
  - Input: `kubectl` command.
  - Output: JSON object indicating safety and reasoning.
  - Example:

    ```json
    {
      "safe": true,
      "reason": "The command only lists resources and does not make changes."
    }
    ```

### 2. **Chains for Workflow Automation**

LangChain's chaining mechanism is used to seamlessly integrate:

- Prompt generation.
- LLM interaction.
- Structured JSON parsing.

```python
self.translate_chain = translate_prompt | self.llm | command_parser
self.safety_chain = safety_prompt | self.llm | safety_parser
```

### 3. **Kubernetes Client Initialization**

Handles both in-cluster and out-of-cluster Kubernetes client configurations:

- Tries to load in-cluster config.
- Falls back to ~/.kube/config if not running in a cluster.

---

## Usage

1. **Create kubernetes cluster**:

    ```bash
    kubectl create -f k8s/deployment.yaml
    ```

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

1. **Run the Agent**:

   ```bash
   python main.py
   ```

1. **Use Test**:

    ```bath
    python test/test_api.py
    ```

---

## Future Work

1. **Interactive Feedback**:

    - Allow users to refine instructions if the generated command is incorrect.

1. **Extended Safety Evaluation**:

    - Integrate more sophisticated checks for potential command risks.

1. **Support for More Instructions**:

    - Fine-tune the language model and feed with more examples and documents to support a broader range of instructions.

1. **Batch Processing**:

    - Handle multiple instructions in a single execution pipeline.

1. **Enhanced Logging**:

    - Include detailed execution metrics and timing information.
