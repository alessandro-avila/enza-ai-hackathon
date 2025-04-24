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

The `src` directory contains code for a "NextGB Agent" that we'll adapt for our use cases:

- **`main.py`**: Core agent implementation using Azure AI Agent Service
- **`data.py`**: Connects to a database and provides query functions
- **`utilities.py`**: Helper functions for the agent
- **`stream_event_handler.py`**: Handles streaming responses
- **`terminal_colors.py`**: Formatting for terminal output

## Hackathon Tasks

During this lab, you'll modify the workshop code to:

1. **Connect to your Azure resources**: Update the code to use the APIM endpoint and Azure Functions you deployed earlier.
2. **Modify the database functions**: Adapt the code to work with the NextGB database.
3. **Add an algorithm function**: Create a function that calls Enza Zaden's algorithm API.
4. **Configure the agent**: Update the system message and instructions to work with plant data.
5. **Test and iteratively improve**: Test the agent with various queries and make improvements.

## Key Concepts

Throughout this lab, we'll explore several important concepts:

- **System Messages**: Configuring the agent's behavior and capabilities
- **Function Registration**: Making functions available to the agent
- **API Integration**: Connecting to APIs through APIM
- **Database Access**: Executing queries against SQL databases
- **Agent Orchestration**: How the agent decides which functions to call
- **Context Management**: Maintaining conversation state across interactions
- **Error Handling**: Dealing with errors or missing information

## Extending the Agent

A key part of this lab will be extending the agent with new functions. You'll learn how to:

- Define function schemas
- Register new functions with the agent
- Test and debug agent integrations

## Resources

- [Azure AI Agent Service Documentation](https://learn.microsoft.com/azure/ai-services/prompt-flow/concepts-features-ai-agent)
- [Azure API Management Documentation](https://learn.microsoft.com/azure/api-management/)
- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)
