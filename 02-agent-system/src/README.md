# Architecture Overview

```
User Request → AI Agent Service → APIM → Function App(s) → Backend Services
                     ↑                         ↓
                     └─────────────────────────┘
                            Response Flow
```

# Step-by-Step Setup Guide

## 1. Create Environment Variables File

Create a `.env` file in the `02-agent-system/workshop` directory by copying the sample file:

```sh
cp .env.sample .env
```

## 2. Update Environment Variables

Edit the `.env` file to add the values you obtained in the previous lab:

```sh
# Azure OpenAI settings
MODEL_DEPLOYMENT_NAME=gpt-4o-mini
TEMPERATURE=0.1
TOP_P=0.1

# These values are from the 00-setup lab deployment outputs
APIM_GATEWAY_URL=https://{your_apim_instance_name}.azure-api.net
APIM_SUBSCRIPTION_KEY={your_apim_subscription_key}

# Azure AI project settings - you'll create these during this lab
PROJECT_CONNECTION_STRING={your_project_connection_string}
BING_CONNECTION_NAME={optional_bing_connection_name}
```

Where to find these values:

1. **APIM_GATEWAY_URL and APIM_SUBSCRIPTION_KEY**:
   - These values were output at the end of the 00-setup/setup.ipynb notebook
   - You can also find them in the Azure Portal under your APIM instance
2. **PROJECT_CONNECTION_STRING**:
   - You'll create an Azure AI Project in the Azure Portal
   - Go to Azure AI Services → Create a Project → Get the connection string
3. **MODEL_DEPLOYMENT_NAME**:
   - This is the name of your Azure OpenAI model deployment
   - It was set during the 00-setup lab (default is "gpt-4o-mini")

### 4. Create the Azure AI Project (if not already created)

1. Go to the [Azure Portal](https://portal.azure.com/)
2. Search for "Azure AI Studio" and select it
3. Create a new project or use an existing one
4. Go to the project settings to get the connection string
5. Add this connection string to your `.env` file as `PROJECT_CONNECTION_STRING`

### 5. Create the Instructions Directory

```sh
mkdir instructions
```

### 6. Run the Agent System

Run the agent with:

```sh
python main.py
```

## How It Works

### Agent Initialization

1. The main script loads environment variables from your `.env` file
2. It connects to the Azure AI Project service using your connection string
3. It creates tools for the agent, including your API functions
4. It constructs instructions with your database schema and capabilities
5. It starts a conversation thread for the agent

### API Functions

The agent can call three main functions through APIM:

1. **`async_fetch_plant_data_using_sql_query`**: Executes SQL queries against Enza Zaden's database
2. **`async_run_algorithm`**: Runs Enza Zaden's custom algorithms for plant analysis
3. **`async_get_weather`**: Gets weather data for specific locations

### Agent Interaction Flow

1. User inputs a question or request
2. The LLM processes the request and determines which function(s) to call
3. The agent calls the appropriate function(s) via APIM
4. The function calls the Azure Function App, which connects to the backend systems
5. Results are returned to the agent
6. The agent formats and presents the results to the user

## Customizing the Agent

During the hackathon, you can customize the agent in several ways:

### 1. Modify Instructions

Edit the file at `instructions/function_calling.txt` to change how the agent behaves and what it knows about the data.

### 2. Add New Functions

To add a new function:

1. Add the function definition to `enza_data.py`
2. Register the function in the `functions` variable in `main_enza.py`
3. Update the agent instructions to tell it about the new capability

### 3. Change Agent Parameters

Adjust parameters like temperature and top_p in your `.env` file to control how deterministic vs. creative the agent is.

### 4. Add Additional Tools

The agent can use other tools besides function calling:

- Code Interpreter for data analysis and visualization
- Bing Grounding for real-time web information
- File Search for information from uploaded documents

## Example Queries to Try

Once your agent is running, try these example queries:

- "Show me the growth data for plant ID XYZ123"
- "What's the predicted yield for tomato plants in greenhouse A?"
- "Run a growth analysis on plant ID ABC456"
- "What's the weather like in Amsterdam where our main greenhouse is located?"
- "Compare the health scores of different plant varieties"

## Troubleshooting

### Common Issues:

1. **Connection Errors**:

   - Verify your APIM_GATEWAY_URL and APIM_SUBSCRIPTION_KEY in the .env file
   - Check that your Azure Function App is running

2. **Authentication Errors**:

   - Ensure your PROJECT_CONNECTION_STRING is correct
   - Check that you're logged in with `az login`

3. **Function Errors**:

   - Check the API response formats in `enza_data.py`
   - Verify that your function parameters match what the API expects

4. **Invalid SQL Queries**:
   - The agent might generate invalid SQL; you can improve this by providing better schema information and examples in the instructions

## Next Steps

After completing this lab, you can explore more advanced scenarios in the next section, including:

- Multi-agent systems
- Memory and context management
- Custom visualizations and reporting
- Security and authentication patterns
