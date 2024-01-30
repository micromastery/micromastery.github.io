---
title: "Meet Your Digital Dream Team: Revolutionizing the Tech World with AI"
date: 2024-01-30 00:00:00 +0000
categories: [AI, Innovation, Automation]
tags: [AI, CrewAI, Content Creation, AI Tools, Tutorial, Python]
---


## Power of Collaborative AI
Hello, Micro Masters! Let's embark on an exciting journey into the realm of collaborative artificial intelligence (AI). Imagine your very own team of AI agents, each with unique skills, collaborating to create something extraordinary. With the recent advancements in AI, this is not just possible, but also incredibly empowering and fun!

### Introducing Crew AI: Your Virtual AI Team

Crew AI is a framework enabling you to build a team of cooperative AI agents, each playing their own role, to achieve a common goal. For instance, It's like having your own team but powered by AI agents instead of people! You can mix and match different AI models and tools from LangChain's extensive toolbox like browsing the internet, complex calculations etc... and even create your own tools.

### Getting Started with Crew AI

For demonstration purposes, let us consider two agents, one researcher(Scout), who searches the internet for latest advancements in tech and another content writer (Scribe), who geneates a 10 minute youtube video script based on the research done by the Scout.

![Crew-AI-Tutorial](https://raw.githubusercontent.com/micromastery/micromastery.github.io/main/assets/CrewAI-Tutorial-1/Crew-AI-Tutorial-1.png)
<sub><sup>*simplified diagram</sup></sub>
#### Prerequisites:

- Python 
- Basic Knowledge about LangChain ( If not, Get started [here](dshttps://python.langchain.com/docs/expression_language/get_starteda))

#### Installation:

- Run `pip install crewai` in your terminal.
- For using langchain tools, follow the instructions [here](https://python.langchain.com/docs/integrations/tools/). More on this below.
- Microsoft Visual C++ 14.0 (for Windows users)


#### Dive into the Code:

Check out this [GitHub link](https://github.com/micromastery/CrewAI-Tutorial) for a full example.

#### Building Your AI Agents:

```python
from langchain_community.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

scout = Agent(
  role='Scout',
  goal='''1. Identify trending and popular topics in technology...
  3. Determine the relevance and potential interest of these topics...''',
  backstory='''You are Scout. Scout operates in a constantly changing environment...
  Scout's role is to search the internet for trending and relevant technology topics...''',
  verbose=True,
  allow_delegation=True,
  # llm=OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.7),
  tools=[search_tool]
)
```

Each agent, like Scout, has a defined role, goal, and backstory. These elements guide the agent's actions and objectives.

#### Language Model and Tools:

Agents can utilize various language models, with GPT-4 as the default. For example, to use `gpt-3.5-turbo-instruct` model,

```
# llm=OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.7)
```

You can also integrate multiple tools like search, Wolfram Alpha, YouTube, Google Drive, and more, available in langchain. Here's the exciting part: You're not limited to just these tools. Crew AI enables you to code your own custom tools which is not in the scope of this blog post.


Remember to set your OpenAI API key if using OpenAI models.
```python
os.environ["OPENAI_API_KEY"] = "<OPENAI_API_KEY>"
```



#### Setting Up Tasks and Crew:

```python
task1 = Task(
  description='''Conduct a comprehensive analysis of the latest advancements in tech in 2024...
  Your final answer MUST be a full analysis report''',
  agent=scout
)

crew = Crew(
  agents=[scout, scribe],
  tasks=[task1, task2],
  verbose=2 # Adjust logging levels as needed
)
```

Define tasks with specific instructions and create a 'crew' with your agents and tasks. The crew operates sequentially, passing outputs from one agent to the next.

#### Launching Your AI Team:

```python
result = crew.kickoff()
print(result)
```

Start the CrewAgent Executor, and watch as your AI team works together to complete tasks and create outputs.
[Check out the detailed interaction among the agents here](https://raw.githubusercontent.com/micromastery/CrewAI-Tutorial/main/SampleOutput.txt).

#### The Outcome:


Below is a sample YouTube script on tech advancements in 2024, crafted by our AI team. 

```text
[Intro - 00:00]

(Animated logo reveal)

"Hello, tech enthusiasts! Welcome back to our channel, where we dive deep into the world of technology. If you're new here, don't forget to hit the subscribe button and the bell icon to stay updated on the latest tech trends. Today, we're exploring the most significant advancements in tech in 2024. So, let's get started!

(Title Card: 'Tech Advancements 2024')

[AI Advances - 00:30]

First up is Artificial Intelligence or AI. AI technology has taken giant strides with developments such as human-like, AI-powered chatbots and open-source pre-trained AI models. These advancements are not just tech buzzwords; they are game-changers, enabling businesses to leverage private or real-time data for accelerated growth and enhanced productivity.

(Visuals of AI chatbots and models)

[AI in Cybersecurity - 02:00]

But with great power comes great responsibility, and in the world of AI, that translates to cybersecurity. As AI technologies evolve, we're seeing a parallel increase in cyber threats. But fear not, advancements in AI are also powering automated responses and predictive analytics to tackle these challenges.

(Visuals of automated threat responses)

[Y2Q Effect - 03:30]

In the shadows of these advancements lurks the Y2Q effect, reminiscent of the Y2K panic. This indicates that quantum computing advancements could trigger new types of cyber threats. Sounds intriguing and terrifying, doesn't it?

(Visual of Y2Q text)

[Quantum Computing - 05:00]

Speaking of quantum computing, 2024 has been a breakthrough year. We're witnessing a shift towards quantum-resistant cryptography, the release of large quantum chips, and a transition from physical qubits to error-corrected logical qubits. Experts predict a promising future for quantum technology and hardware advancements.

(Visuals of quantum chips and qubits)

[AI in Data Analytics - 07:00]

The realm of data analytics is also getting a taste of AI magic. Collaboration between hyperscalers and AI models is set to revolutionize the data analytics landscape. The future looks bright and data-driven, thanks to AI!

(Visuals of data analytics tools)

[Conclusion - 08:30]

The pace of technological advancement in 2024 is breakneck, impacting a wide range of industries and driving the need for businesses and individuals to adapt quickly. As we wrap up, it's clear that staying informed and prepared for these changes is crucial.

(Visual of tech devices and industries)

[Outro - 09:30]

That's all for today's deep dive into the tech advancements of 2024. Don't forget to like, share, and comment on this video, and let us know which tech trend excites you the most. Until our next tech journey, stay curious, stay informed!

(End Card: 'Subscribe')

[End - 10:00]
```

I've tested various models like Ollama (openhermes), GPT-3.5-turbo-instruct and GPT-4, with GPT-4 outshining in performance for this use case.


This is a basic tutorial and there's a lot more to explore with Crew AI. Dive into its GitHub repo for examples and upcoming features at [Crew AI Repo](https://github.com/joaomdmoura/crewAI?tab=readme-ov-file#crewai) and [Crew AI Examples](https://github.com/joaomdmoura/crewAI-examples?tab=readme-ov-file).

I'm eager to see your collaborative intelligence projects using Crew AI. Share your creations/ideas in the comment section below.

---

It's truly remarkable how AI has evolved, transforming from a distant dream into a tool that enables us to create, collaborate, and innovate. The world of AI is brimming with possibilities, and with Crew AI, we're just scratching the surface. Stay curious and keep exploring 🚀💡