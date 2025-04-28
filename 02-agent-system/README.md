# Building an Agent System with Azure AI Agent Service

In this lab, you'll create an AI agent that can interact with APIs through Azure API Management (APIM) and execute functions from your Azure Functions app. This section builds on the function calling concepts introduced in the previous lab and shows how to combine multiple functions into a cohesive agent system.

## What is an Azure AI Agent?

An Azure AI agent is an AI application pattern that can understand user requests, determine the appropriate actions to take, and provide relevant responses. Agents combine large language models (LLMs) with custom functions to create a powerful system that can:

1. **Interpret user intent** through natural language
2. **Decide which functions to call** based on the request
3. **Execute appropriate functions** with the right parameters
4. **Process function results** and generate coherent responses
5. **Maintain context** across multiple interactions

## Lab Overview

In this lab, you will:

1. **Set up an Azure AI Agent** that connects to your existing resources
2. **Register functions** from your Function App with the agent
3. **Configure the agent** with appropriate system prompts and settings
4. **Test the agent** with various queries
5. **Extend the agent** by adding new functions

## Architecture

The solution architecture for this lab includes:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────────┐
│             │     │              │     │             │     │                 │
│  Azure AI   │────▶│  Azure API   │────▶│    Azure    │────▶│   │
│    Agent    │     │  Management  │     │  Functions  │     │   Systems and   │
│             │     │              │     │             │     │   SQL Database  │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────────┘
```

## Getting Started

To start working with your agent system, follow these steps:

1. Make sure you've completed the [setup](../00-setup/README.md) and [function calling](../01-function-calling/README.md) labs.
2. Explore the code in the `src` directory, which contains the foundation for your AI agent.
3. During the hackathon, you'll modify this code to work with the Azure resources you deployed previously.

## Workshop Code Structure

The `src` directory contains code for the Enza Zaden agent system:

- **`main.py`**: Core agent implementation using Azure AI Agent Service
- **`enza_data.py`**: Functions for accessing Enza's data and APIs
- **`sales_data.py`**: Functions for querying the SQL database with sales information
- **`utilities.py`**: Utility functions for the agent system
- **`stream_event_handler.py`**: Handles streaming events from the agent
- **`terminal_colors.py`**: Helper for terminal color output

## New SQL Functionality

This agent system now includes the ability to query a SQL database with sales data. The agent can:

1. **Execute general SQL queries** against the sales database
2. **Get sales by region** to analyze regional performance
3. **Analyze product sales** across different categories
4. **Review customer sales data** by customer type
5. **Analyze sales trends over time** by month or quarter

### Setting Up SQL Query Functionality

To use the SQL query functionality:

1. Copy the `.env.sample` file to `.env` in the `src` directory
2. Update the environment variables with the values from your deployment:
   - Set `APIM_GATEWAY_URL` to your API Management gateway URL
   - Set `APIM_SUBSCRIPTION_KEY` to your API Management subscription key

### Sample Queries for Testing

Once your agent is running, try these sample prompts:

- "Show me the total sales for each region"
- "Which product category has the highest sales?"
- "Compare distributor and direct grower customer sales"
- "Show me the sales trend by month for 2024"
- "What's the average order value by customer type?"
- "Run a query to find the top 5 customers by total sales"

The agent will use the appropriate SQL query functions to retrieve the data and present the results in a user-friendly format.

## Extending the Agent

A key part of this lab will be extending the agent with new functions. You'll learn how to:

- Define function schemas
- Register new functions with the agent
- Test and debug agent integrations

## Resources

- [Azure AI Agent Service Documentation](https://learn.microsoft.com/azure/ai-services/prompt-flow/concepts-features-ai-agent)
- [Azure API Management Documentation](https://learn.microsoft.com/azure/api-management/)
- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)
