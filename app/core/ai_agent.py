from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent
from app.config.settings import settings

def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):
    try:
        llm = ChatGroq(model=llm_id)
        tools = [TavilySearchResults(max_results=2)] if allow_search else []

        # Always include system prompt as the first message in the list
        messages = [{"role": "system", "content": system_prompt}] + [{"role": "user", "content": msg} for msg in query]

        state = {"messages": messages}

        try:
            # Try to create agent with system_prompt kwarg if supported
            agent = create_agent(model=llm, tools=tools)
        except TypeError:
            # fallback for older langchain versions without system_prompt kwarg
            agent = create_agent(model=llm, tools=tools)

        # Log details before invocation
        print("Invoking agent with state:", state)

        response = agent.invoke(state)

        print("Raw response from agent:", response)
        resp_msgs = response.get("messages", [])
        print("Response messages", resp_msgs)
        for msg in resp_msgs:
            print("Message type:", type(msg), "Content:", getattr(msg, "content", None))

        ai_messages = []
        ai_messages = [msg.content for msg in resp_msgs if hasattr(msg, "content") and getattr(msg, "content")]
        # for msg in resp_msgs:
        #     if isinstance(msg, dict):
        #         if msg.get("role") == "assistant":
        #             ai_messages.append(msg.get("content"))
        #     elif hasattr(msg, "role") and getattr(msg, "role") == "assistant":
        #         ai_messages.append(getattr(msg, "content", None))

        return ai_messages[-1] if ai_messages else None

    except Exception as e:
        # Log and raise the exception for visibility
        print("Exception in get_response_from_ai_agents:", repr(e))
        raise
