import os

from langchain.agents import AgentType, Tool, initialize_agent
from langchain.llms import OpenAI

# Initialize the OpenAI model (or use Puter.js model)
llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Define a tool for generating questions
tool = Tool(
    name="QuestionGenerator",
    func=lambda query: f"Generated question for {query}",
    description="Generates a question based on a given product name."
)

# Initialize agent with the tool
agent = initialize_agent(
    tools=[tool],
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    llm=llm,
    verbose=True
)

# Function to generate content using the agent
def generate_agent_response(query):
    return agent.run(query)

# Example usage
query = "Tell me about the benefits of GlowBoost Vitamin C Serum"
response = generate_agent_response(query)
print(response)
