# Day 1 – Agent Foundations & Message-Based Communication

## Introduction

The objective of Day 1 was not to build a chatbot, but to design the foundation of a reusable AI agent framework.

Instead of creating independent agents that duplicate code, the goal was to design a common architecture where every agent shares the same capabilities while specializing only in its own role. This makes the system modular, easier to maintain, and much easier to extend as more agents are added.

The architecture built today serves as the foundation for the rest of the NEXUS AI project.

---

# Understanding an AI Agent

An AI agent is more than a language model. A language model generates text, while an agent is responsible for managing the complete reasoning workflow.

An agent must:

- Receive a goal from the user.
- Understand its assigned role.
- Build the appropriate prompt.
- Maintain conversation history.
- Communicate with the language model.
- Return a response.
- Update its memory.

The LLM performs the reasoning, but the agent manages everything around that reasoning.

---

# Agent Architecture

Instead of placing all logic inside every individual agent, a common `BaseAgent` class was designed.

The BaseAgent contains functionality that every future agent requires:

- Agent identity
- System prompt management
- Conversation memory
- Message construction
- Communication with Ollama
- Response generation

Specialized agents simply inherit these capabilities rather than implementing them again.

This significantly reduces duplicated code and follows object-oriented programming principles.

---

# Role-Based Intelligence

Every agent in the system has only one responsibility.

The Research Agent is responsible for gathering information.

The Summarizer Agent only summarizes information.

The Answer Agent only produces the final user response.

Because every agent performs exactly one task, responsibilities never overlap and the system remains modular.

---

# System Prompts

Each agent receives its own system prompt during initialization.

The system prompt defines:

- the identity of the agent,
- its responsibilities,
- its limitations,
- and the style in which it should respond.

The system prompt is fixed throughout the lifetime of the agent and becomes part of its identity rather than being recreated for every request.

---

# Short-Term Memory

Large Language Models do not remember previous conversations automatically.

Memory is simulated by sending previous conversation history together with the new user request.

To achieve this efficiently, every BaseAgent maintains its own conversation history using a bounded `deque`.

The memory window is limited to a configurable size so that older messages are automatically discarded while recent context is preserved.

This provides conversational continuity without exceeding the model's context window.

---

# Message Construction

Instead of sending raw strings to the LLM, every request follows the standard chat message format.

Before contacting the language model, BaseAgent constructs a message list containing:

- the system prompt,
- optional contextual information,
- recent conversation history,
- and the latest user message.

Separating message construction into its own method keeps the code modular and follows the Single Responsibility Principle.

---

# Centralized LLM Communication

Communication with Ollama is handled through a dedicated `OllamaClient`.

No agent communicates with the language model directly.

The client is responsible for:

- establishing the connection,
- sending requests,
- receiving responses,
- retrying failed requests,
- timeout handling,
- and error management.

This design ensures that if the underlying language model changes in the future, only one file needs to be modified.

---

# BaseAgent Implementation

The BaseAgent contains four primary methods.

`__init__()` initializes the agent and creates its conversation history.

`_build_messages()` constructs the structured message list sent to the language model.

`_update_history()` stores both the user's message and the assistant's response inside the bounded memory window.

`think()` orchestrates the complete reasoning workflow by building messages, contacting the language model, updating memory, and returning the final response.

These four methods provide all core functionality required by every future agent.

---

# Specialized Agents

Three specialized agents were implemented.

### ResearchAgent

Responsible for collecting information and producing detailed research.

### SummarizerAgent

Responsible for reducing research into concise summaries while preserving important information.

### AnswerAgent

Responsible for generating the final user-facing response using the summarized information.

Each of these agents only defines its own identity and system prompt while inheriting all common behavior from BaseAgent.

---

# Configuration System

All configurable values were centralized inside `config.py`.

This follows the Single Source of Truth principle.

Instead of hardcoding values throughout the project, every component reads configuration from one location.

The configuration currently includes model information, memory settings, server settings, retry limits, timeout values, and other application-wide parameters.

---

# Software Engineering Principles Applied

During this implementation several important software engineering principles were followed.

**Single Responsibility Principle**

Each class and method performs only one well-defined task.

**Separation of Concerns**

Networking, memory management, configuration, and reasoning are handled by different components.

**Inheritance**

Specialized agents inherit common functionality from BaseAgent instead of duplicating code.

**Loose Coupling**

Agents communicate with the language model through OllamaClient rather than directly depending on Ollama.

**Single Source of Truth**

Configuration values exist in one location instead of being repeated throughout the codebase.

**High Cohesion**

Related functionality is grouped together within dedicated classes.

---

# Outcome

By the end of Day 1, a reusable multi-agent framework was successfully implemented.

The system now supports:

- reusable agent architecture,
- role-based specialization,
- centralized LLM communication,
- configurable short-term memory,
- structured message construction,
- asynchronous execution,
- and a simple multi-agent pipeline consisting of a Research Agent, Summarizer Agent, and Answer Agent.

This architecture forms the foundation upon which planning, orchestration, tool usage, memory systems, and autonomous reasoning will be built in the upcoming stages of the NEXUS AI project.
