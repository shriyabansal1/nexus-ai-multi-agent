"""
Coordinates the execution of tasks.
"""

import asyncio
import traceback

from orchestrator.planner import Planner
from orchestrator.registry import AgentRegistry
from orchestrator.router import Router
from orchestrator.task import TaskStatus
from orchestrator.execution_context import ExecutionContext


class Orchestrator:

    def __init__(self, planner: Planner, registry: AgentRegistry):
        self.planner = planner
        self.registry = registry
        self.router = Router(registry)

    async def run(self, goal: str):

        print("\n========== ORCHESTRATOR START ==========")

        execution_context = ExecutionContext(goal)
        execution_context.start_execution()

        try:

            print("[1] Planning...")
            tasks = await self.planner.plan(goal)
            print(f"[2] Planner created {len(tasks)} tasks")

            completed = set()

            while len(completed) < len(tasks):

                ready_tasks = []

                for task in tasks:

                    if task.id in completed:
                        continue

                    if all(dep in completed for dep in task.depends_on):
                        ready_tasks.append(task)

                if not ready_tasks:
                    raise RuntimeError("Deadlock detected in task graph.")

                print(
                    f"\nRunning {len(ready_tasks)} task(s). "
                    f"Completed = {len(completed)}/{len(tasks)}"
                )

                finished = await asyncio.gather(
                    *[
                        self._execute_task(
                            task,
                            tasks,
                            goal,
                            execution_context,
                        )
                        for task in ready_tasks
                    ],
                    return_exceptions=False,
                )

                for task in finished:
                    completed.add(task.id)

            execution_context.finish_execution(True)

            answer_task = next(
                (
                    task
                    for task in tasks
                    if task.assigned_agent == "answer"
                    and task.status == TaskStatus.COMPLETED
                ),
                None,
            )

            if answer_task and answer_task.result:

                answer_agent = self.registry.get("answer")

                if (
                    answer_agent
                    and answer_agent.memory_manager
                ):
                    await answer_agent.memory_manager.remember(
                        user_input=goal,
                        assistant_response=answer_task.result,
                    )

            print("========== ORCHESTRATOR FINISHED ==========\n")

            return tasks, execution_context.summary()

        except Exception:

            print("\n========== ORCHESTRATOR FAILED ==========")
            traceback.print_exc()

            execution_context.finish_execution(False)
            raise

    async def _execute_task(
        self,
        task,
        tasks,
        goal,
        execution_context,
    ):

        agent = self.router.route(task)

        task.status = TaskStatus.RUNNING

        if task.depends_on:
            context = "\n\n".join(
                t.result
                for t in tasks
                if t.id in task.depends_on and t.result
            )
        else:
            context = None

        if task.assigned_agent in (
            "answer",
            "critic",
            "optimizer",
            "reflection",
            "reporter",
        ):
            user_input = goal

        elif task.assigned_agent == "validator":
            user_input = goal
            context = f"Original Request:\n{goal}\n\nAnswer:\n{context}"

        else:
            user_input = task.description

        trace = execution_context.start_agent(
            agent=agent.name,
            task=user_input,
            input_data=context,
        )

        print("\n===================================")
        print(f"Agent : {agent.name}")
        print(f"Task  : {task.description}")
        print("===================================")

        try:

            task.result = await agent.think(
                user_input=user_input,
                context=context,
                execution_context=execution_context,
            )

            task.status = TaskStatus.COMPLETED

            execution_context.state.mark_completed(task.id)

            execution_context.finish_agent(
                trace,
                output_data=task.result,
            )

            print(f"SUCCESS -> {agent.name}")

        except Exception:

            traceback.print_exc()

            task.status = TaskStatus.FAILED
            task.result = traceback.format_exc()

            execution_context.state.mark_failed(task.id)

            execution_context.fail_agent(
                trace,
                task.result,
            )

            # Re-raise so FastAPI shows the real traceback
            raise

        return task