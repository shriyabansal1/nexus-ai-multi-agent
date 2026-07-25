import json
from config import settings
from llm.ollama_client import OllamaClient
from orchestrator.task import Task
class Planner:
    """
    Breaks a user's goal into executable tasks.
    """
    async def plan(self, goal: str) -> list[Task]:
        messages = [
            {
                "role": "system",
                "content": self._build_prompt(),
            },
            {
                "role": "user",
                "content": goal,
            },
        ]
        print("Planner model:", settings.llm.planner_model)
        response = await OllamaClient.chat(
            model=settings.llm.planner_model,
            messages=messages,
            temperature=0.0,
            num_predict=400,
        )
        try:
            response = response.strip()
            response = response.replace("```json", "").replace("```", "").strip()
            decoder = json.JSONDecoder()
            try:
                data, _ = decoder.raw_decode(response)
            except json.JSONDecodeError:
                print("Invalid JSON received:")
                print(response)
                raise
            tasks = []
            if isinstance(data, list):
                items = data
            else:
                items = data["tasks"]

            for item in items:
                tasks.append(
                    Task(
                        description=item["description"],
                        assigned_agent=item["agent"],
                    )
                )     
            if not tasks:
                return [
                    Task(
                        description="Generate the final answer.",
                        assigned_agent="answer",
                    )
                ]
            research_tasks = [
                t for t in tasks
                if t.assigned_agent == "research"
            ]
            summarizer = next(
                (t for t in tasks if t.assigned_agent == "summarizer"),
                None,
            )
            answer = next(
                (t for t in tasks if t.assigned_agent == "answer"),
                None,
            )
            reflection = next(
                (t for t in tasks if t.assigned_agent == "reflection"),
                None,
            )
            validator = next(
                (t for t in tasks if t.assigned_agent == "validator"),
                None,
            )
            analyst = next(
                (t for t in tasks if t.assigned_agent == "analyst"),
                None,
            )
            critic = next(
                (t for t in tasks if t.assigned_agent == "critic"),
                None,
            )
            optimizer = next(
                (t for t in tasks if t.assigned_agent == "optimizer"),
                None,
            )
            reporter = next(
                (t for t in tasks if t.assigned_agent == "reporter"),
                None,
            )
            specialized = next(
                (
                    t for t in tasks
                    if t.assigned_agent in {"research", "code", "db", "file"}
                ),
                None,
            )
            if analyst:
                analyst.depends_on = [t.id for t in research_tasks]
            if summarizer:
                if analyst:
                    summarizer.depends_on = [analyst.id]
                else:
                    summarizer.depends_on = [t.id for t in research_tasks]
            if answer:
                if summarizer:
                    answer.depends_on = [summarizer.id]
                elif specialized:
                    answer.depends_on = [specialized.id]
            if critic:
                if answer:
                    critic.depends_on = [answer.id]
                else:
                    raise ValueError("Critic task requires an Answer task.")
            if optimizer:
                if critic:
                    optimizer.depends_on = [critic.id]
                else:
                    optimizer.depends_on = [answer.id]
            if reflection:
                if optimizer:
                    reflection.depends_on = [optimizer.id]
                else:
                    reflection.depends_on = [answer.id]
            if validator:
                if reflection:
                    validator.depends_on = [reflection.id]
                elif optimizer:
                    validator.depends_on = [optimizer.id]
                elif answer:
                    validator.depends_on = [answer.id]
            if reporter:
                if validator:
                    reporter.depends_on = [validator.id]
                else:
                    raise ValueError("Reporter task requires a Validator task.")
            return tasks

        except Exception as e:
            print("\nPlanner failed to parse JSON.")
            print(response)
            print(e)
            return [
                Task(
                    description=f"Research information about: {goal}",
                    assigned_agent="research",
                ),
                Task(
                    description=f"Answer the user's request: {goal}",
                    assigned_agent="answer",
                ),
                Task(
                    description="Validate the generated answer.",
                    assigned_agent="validator",
                ),
            ]

    def _build_prompt(self) -> str:
        return """
You are the Planner Agent of the NEXUS AI Multi-Agent System.

Your job is to convert the user's request into an executable task graph.

Return ONLY valid JSON.

Schema:

{
  "tasks": [
    {
      "id": "task_1",
      "agent": "<agent_name>",
      "description": "<task description>",
      "depends_on": []
    }
  ]
}

Available Agents

research
- Research concepts.
- Explain topics.
- Collect information.

analyst
- Analyze research.

summarizer
- Summarize research.

answer
- Produce the final answer.

critic
- Review the answer.

optimizer
- Improve the answer.

reflection
- Improve reasoning.

validator
- Validate correctness.

reporter
- Generate execution report.

code
- Execute Python code.
- Perform calculations.
- Run algorithms.

db
- Access uploaded SQLite databases.
- Show tables.
- Show schema.
- Execute SQL queries.

file
- Read uploaded PDFs.
- Read uploaded CSV files.
- Read text files.
- Write text files.
- List uploaded files.

==============================
ROUTING RULES
==============================

Research questions

research
→ analyst
→ summarizer
→ answer
→ critic
→ optimizer
→ reflection
→ validator
→ reporter

Python / algorithm requests

code
→ answer
→ validator

Database requests
Examples
- show tables
- list tables
- schema employees
- schema students
- show schema
- show columns
- show columns of students
- list columns
- describe table
- table structure
- pragma table_info
- sqlite database
- uploaded database
- SELECT * FROM employees
- SELECT * FROM students
Always use
db

→ answer
→ validator
→ answer
→ validator

File requests

Examples:
- read uploaded pdf
- summarize uploaded pdf
- read uploaded csv
- read report.pdf
- read notes.txt
- write notes.txt hello
- list uploaded files

Route to:

file
→ answer
→ validator

Conversation

Simple greetings,
memory questions,
personal questions

↓

answer

==============================
IMPORTANT
==============================

Never use research for:

- uploaded pdf
- uploaded csv
- uploaded database
- sql
- sqlite
- database
- read file
- write file

Use:

file

or

db

instead.

==============================
Return ONLY valid JSON.
No markdown.
No explanations.

Additional Rules

- Use multiple independent research tasks whenever possible.
- Use code only for computation, scripting, algorithms or Python execution.
- Use db only for SQLite operations.
- Use file only for reading or writing local files.
- Do not create research tasks for code, database or file operations.
- Do not create summarizer unless research exists.
- Do not create reflection unless research exists.
- Do not create duplicate tasks.
- Do not create unnecessary tasks.

Example

{
  "tasks": [
    {
      "id": "task_1",
      "agent": "research",
      "description": "Research the user's requested topic",
      "depends_on": []
    },
    {
      "id": "task_2",
      "agent": "analyst",
      "description": "Analyze the research findings",
      "depends_on": ["task_1"]
    },
    {
      "id": "task_3",
      "agent": "summarizer",
      "description": "Summarize the analyzed research",
      "depends_on": ["task_2"]
    },
    {
      "id": "task_4",
      "agent": "answer",
      "description": "Generate the final answer",
      "depends_on": ["task_3"]
    },
    {
      "id": "task_5",
      "agent": "critic",
      "description": "Review the generated answer",
      "depends_on": ["task_4"]
    },
    {
      "id": "task_6",
      "agent": "optimizer",
      "description": "Improve the answer",
      "depends_on": ["task_5"]
    },
    {
      "id": "task_7",
      "agent": "reflection",
      "description": "Perform final reasoning improvements",
      "depends_on": ["task_6"]
    },
    {
      "id": "task_8",
      "agent": "validator",
      "description": "Validate the final answer",
      "depends_on": ["task_7"]
    },
    {
      "id": "task_9",
      "agent": "reporter",
      "description": "Generate the execution report",
      "depends_on": ["task_8"]
    }
  ]
}

User Request:
{goal}"""