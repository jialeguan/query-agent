from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 定义响应的结构
response_schemas = [
    ResponseSchema(
        name="command", description="The kubectl command generated.")
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 定义 Prompt
prompt = PromptTemplate(
    input_variables=["instruction"],
    template=(
        "Translate the following instruction into a kubectl command.\n\n"
        "Instruction: {instruction}\n\n"
        "Respond in JSON format with the following key:\n"
        "- command: The generated kubectl command."
    ),
    output_parser=output_parser,
)

llm = ChatOpenAI(temperature=0)

# 获取并解析输出
response = llm.generate(
    [prompt.format(instruction="List all pods in the default namespace")])
parsed_output = output_parser.parse(response.generations[0].text)

print(f"Extracted Command: {parsed_output['command']}")
