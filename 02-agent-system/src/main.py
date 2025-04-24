import asyncio
import logging
import os
import sys

sys.path.insert(1, '../../shared')  # add the shared directory to the Python path
import utils

from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import (
    Agent,
    AgentThread,
    AsyncFunctionTool,
    AsyncToolSet,
    BingGroundingTool,
    CodeInterpreterTool,
    FileSearchTool,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from enza_data import EnzaData
from stream_event_handler import StreamEventHandler
from terminal_colors import TerminalColors as tc
from utilities import Utilities

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

load_dotenv()

AGENT_NAME = "Enza Zaden Plant Analysis Agent"
API_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")
PROJECT_CONNECTION_STRING = os.environ.get("PROJECT_CONNECTION_STRING")
BING_CONNECTION_NAME = os.getenv("BING_CONNECTION_NAME")
MAX_COMPLETION_TOKENS = 10240
MAX_PROMPT_TOKENS = 20480
# The LLM is used to generate the SQL queries.
# Set the temperature and top_p low to get more deterministic results.
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
TOP_P = float(os.getenv("TOP_P", "0.1"))
INSTRUCTIONS_FILE = "instructions/function_calling.txt"

# Create utilities and enza_data instances
toolset = AsyncToolSet()
utilities = Utilities()
enza_data = EnzaData(utilities)

# Validate required environment variables
if not PROJECT_CONNECTION_STRING:
    logger.error("PROJECT_CONNECTION_STRING environment variable not set. Please set this in your .env file.")
    exit(1)

# Initialize the AI Project Client
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=PROJECT_CONNECTION_STRING,
)

# Define the functions tool with our API functions
functions = AsyncFunctionTool(
    {
        enza_data.async_fetch_plant_data_using_sql_query,
        enza_data.async_run_algorithm,
        enza_data.async_get_weather,
    }
)


async def add_agent_tools() -> None:
    """Add tools for the agent."""
    # Add the functions tool for API access
    toolset.add(functions)
    
    # Participants can uncomment and configure these additional tools during the hackathon
    
    # Add Bing grounding (if configured)
    # if BING_CONNECTION_NAME:
    #     try:
    #         bing_connection = await project_client.connections.get(connection_name=BING_CONNECTION_NAME)
    #         bing_grounding = BingGroundingTool(connection_id=bing_connection.id)
    #         toolset.add(bing_grounding)
    #         print(f"{tc.GREEN}✓{tc.RESET} Added Bing grounding tool")
    #     except Exception as e:
    #         print(f"{tc.RED}✗{tc.RESET} Failed to add Bing grounding tool: {str(e)}")
    
    # Add code interpreter
    # code_interpreter = CodeInterpreterTool()
    # toolset.add(code_interpreter)
    # print(f"{tc.GREEN}✓{tc.RESET} Added code interpreter tool")


async def initialize() -> tuple[Agent, AgentThread]:
    """Initialize the agent with database schema and instructions."""
    # Create instructions directory if it doesn't exist
    os.makedirs("instructions", exist_ok=True)
    
    # Create default instructions if they don't exist
    if not os.path.exists(INSTRUCTIONS_FILE):
        with open(INSTRUCTIONS_FILE, "w") as f:
            f.write("""You are a helpful plant analysis assistant for Enza Zaden, a vegetable breeding company.
            
You help users analyze plant data and make predictions about plant growth and yields.

You can access the following database schema:
{database_schema_string}

When the user asks for data, always use SQL queries through the async_fetch_plant_data_using_sql_query function.
When the user asks to run the growth algorithm, use the async_run_algorithm function.
When the user asks about weather, use the async_get_weather function.

Always be helpful, professional, and clear in your responses.
""")
    
    await add_agent_tools()
    await enza_data.connect()
    database_schema_string = await enza_data.get_database_info()

    try:
        # Load instructions from file
        with open(INSTRUCTIONS_FILE, "r") as f:
            instructions = f.read()
        
        # Replace the placeholder with the database schema string
        instructions = instructions.replace(
            "{database_schema_string}", database_schema_string)

        print(f"{tc.BOLD}Creating agent...{tc.RESET}")
        agent = await project_client.agents.create_agent(
            model=API_DEPLOYMENT_NAME,
            name=AGENT_NAME,
            instructions=instructions,
            toolset=toolset,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
            max_prompt_tokens=MAX_PROMPT_TOKENS,
            headers={"x-ms-enable-preview": "true"},
        )
        print(f"{tc.GREEN}✓{tc.RESET} Created agent, ID: {agent.id}")

        print(f"{tc.BOLD}Creating thread...{tc.RESET}")
        thread = await project_client.agents.create_thread()
        print(f"{tc.GREEN}✓{tc.RESET} Created thread, ID: {thread.id}")

        return agent, thread

    except Exception as e:
        logger.error("An error occurred initializing the agent: %s", str(e))
        return None, None


async def cleanup(agent: Agent, thread: AgentThread) -> None:
    """Cleanup the resources."""
    if thread and agent:
        await project_client.agents.delete_thread(thread.id)
        await project_client.agents.delete_agent(agent.id)
    await enza_data.close()


async def post_message(content: str, agent: Agent, thread: AgentThread) -> None:
    """Post a message to the Azure AI Agent Service."""
    try:
        handler = StreamEventHandler()
        response = await project_client.agents.post_message(
            agent_id=agent.id,
            thread_id=thread.id,
            message=content,
            event_handler=handler,
            headers={"x-ms-enable-preview": "true"},
        )
    except Exception as e:
        logger.error("An error occurred posting a message: %s", str(e))


async def main() -> None:
    """Run the main application."""
    try:
        # Initialize the agent and thread
        agent, thread = await initialize()
        
        if not agent or not thread:
            print(f"{tc.RED}Failed to initialize agent or thread. Please check your environment variables and try again.{tc.RESET}")
            return
        
        print(f"\n{tc.BLUE}===================================={tc.RESET}")
        print(f"{tc.BOLD}Enza Zaden Plant Analysis Agent{tc.RESET}")
        print(f"{tc.BLUE}===================================={tc.RESET}")
        print(f"{tc.GREEN}Ready! Type 'exit' to quit.{tc.RESET}\n")
        
        while True:
            # Get user input
            user_input = input(f"{tc.BOLD}User: {tc.RESET}")
            
            if user_input.lower() in ["exit", "quit"]:
                break
            
            # Post the message and process the response
            await post_message(user_input, agent, thread)
            print()  # Add a newline for readability
    
    except KeyboardInterrupt:
        print("\nExiting...")
    
    except Exception as e:
        logger.error("An error occurred in the main loop: %s", str(e))
    
    finally:
        # Clean up resources
        if 'agent' in locals() and 'thread' in locals():
            await cleanup(agent, thread)


if __name__ == "__main__":
    asyncio.run(main())
