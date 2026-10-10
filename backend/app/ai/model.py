import asyncio

from langchain.messages import HumanMessage

from backend.app.db.models import Order
from backend.app.ai.agents.agent import model


async def main():

    config = {
    "configurable":
    {
        "thread_id":"test-memory-v1"
    }
}


    async for chunk in model.astream(
        {
            "messages":[
                HumanMessage(
                    "im a agentic dev"
                )
            ]
        },
        config=config,
        # context=MyContext(user_id=15),
        stream_mode="updates"
    ):
        print(chunk)

    async for chunk in model.astream(
            {
                "messages":[
                    HumanMessage(
                        "You know my profecion,"
                    )
                ]
            },
            config=config,
            # context=MyContext(user_id=15),
            stream_mode="updates"
        ):
            print(chunk)


if __name__ == "__main__":
    asyncio.run(main())
