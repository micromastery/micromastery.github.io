---
title: "Enhancing LLMs with Custom Capabilities: A Guide to Langchain and Text-to-Speech"
date: 2024-02-06 00:00:00 +0000
categories: [AI, Development, Langchain]
tags: [AI, Langchain, Custom Capabilities, Text-to-Speech, Python, Tutorial]
---

# Enhancing Large Language Models with Custom Capabilities Using Langchain

In the rapidly evolving landscape of AI and machine learning, the ability to extend and customize large language models (LLMs) has become increasingly important. Langchain, a powerful framework for building applications on top of LLMs, offers a streamlined approach for integrating custom capabilities. This blog post will guide you through a practical example of how to use Langchain to create a custom capability—specifically, converting text to speech—and how to integrate it with an OpenAI model.

Note: The same concept can be used for customizing Crew AI agents discussed in this post [Meet Your Digital Dream Team: Revolutionizing the Tech World with AI](https://micromastery.github.io/posts/meet-your-digital-dream-team-revolutionizing-tech-world-with-ai/#language-model-and-tools)


## Setting Up Your Environment

Before diving into the code, ensure you have Langchain and the necessary libraries installed. This example uses `langchain`, `langchain-openai`, and `gtts` for Google Text-to-Speech conversion. Install them using `pip` if you haven't done so already.

Full code can be found [here](https://github.com/micromastery/LangChainTutorial-CustomTool).

## Defining a Custom Capability

To start, we define a custom capability for converting text to speech as an example. This is achieved by creating a class that inherits from `BaseModel` and uses the `@tool` decorator to register the function as a Langchain tool. 

Below is a snippet illustrating how to define a `TextToSpeech` capability:

```python
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from gtts import gTTS 

class TextToSpeech(BaseModel):
    text: str = Field(description="The text to convert to speech")
    filename: str = Field(description="The name of the file to save the speech to.")

@tool("text-to-speech", args_schema=TextToSpeech)
def text_to_speech(text: str, filename: str) -> None:
    """Converts text to speech using Google Text-to-Speech API and saves it to a file."""
    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False) 
    myobj.save(filename)
```

This code snippet defines a `TextToSpeech` model with two fields: `text` for the input text and `filename` for the file name where the speech will be saved. The `text_to_speech` function then uses the Google TTS API to convert the text to speech and save it to the specified file.

## Integrating with OpenAI's Chat Model

To integrate this capability with an OpenAI chat model, you'll need to set your OpenAI API key in your environment variables. Then, create an instance of the chat model, pull a Langchain prompt, and create an agent with your custom tools. Below is how you can set up the integration:

```python
import os
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain import hub

# Set your OpenAI API Key
os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"

# Initialize the LLM with specific parameters
llm = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0.7)

# Pull the prompt configuration from Langchain's hub
prompt = hub.pull("hwchase17/openai-tools-agent")

# Create an agent with the custom tool
tools = [text_to_speech]
agent = create_openai_tools_agent(llm, tools, prompt)

# Execute the agent with the custom capability
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = agent_executor.invoke({"input": "Write a children's story about a dragon and convert it to speech."})

print(result["output"])
```

## Execution and Output

When you run the above code, the agent will process the input prompt, generate a children's story about a dragon using the OpenAI model, and then convert the generated text to speech, saving it to the specified file.

This is the output that the above code generated

<audio controls>
  <source type="audio/mp3" src="https://github.com/micromastery/micromastery.github.io/raw/main/assets/CustomizingLlmsWithLangchain/dragon_story.mp3"></source>
  <p>Your browser does not support the audio element.</p>
</audio>



This example demonstrates the flexibility and power of Langchain for extending LLMs with custom capabilities. Whether you're looking to add text-to-speech, integrate external APIs, or create entirely new functionalities, Langchain provides a robust foundation for your AI applications.


More information on the custom tools can be found here: [Defining Custom Tools](https://python.langchain.com/docs/modules/agents/tools/custom_tools)


Let me know what all custom capabilities you have created or want someone to create. Stay curious and keep exploring 🚀💡
