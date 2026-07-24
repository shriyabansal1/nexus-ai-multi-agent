import asyncio
from agents.research_agent import ResearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.answer_agent import AnswerAgent

async def main():
    research_agent = ResearchAgent()
    summarizer_agent = SummarizerAgent()
    answer_agent = AnswerAgent()
    question = input("Ask: ")
    research = await research_agent.think(question)
    summary = await summarizer_agent.think(
        "Summarize the following research.",
        context=research,
    )
    final_answer = await answer_agent.think(
        question,
        context=summary,
    )
    print("\n" + "="*70)
    print("FINAL ANSWER")
    print("="*70)
    print(final_answer)
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())