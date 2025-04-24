# OpenAI Function Calling Mechanism

OpenAI's function calling mechanism allows language models to interact with external tools or APIs in a structured way. Instead of generating plain text, the model can return a function name and a set of arguments, which can then be used to call external code or services. This enables more reliable and controlled integrations between AI and your applications.

How it works:

1. You define one or more functions, specifying their names, descriptions, and expected parameters.
2. When you send a prompt to the model, you include these function definitions.
3. If the model determines that a function should be called, it returns a JSON object with the function name and arguments.
4. Your application receives this response, executes the function, and can optionally send the result back to the model for further processing.

This mechanism is useful for tasks like querying databases, calling APIs, or performing calculations, allowing the model to act as an intelligent orchestrator between user input and your backend logic.

For more details about this please refer to the [docs](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling).

---

Now that we deployed all the needed resources to Azure, let's try the function calling mechanism.
