import logging

from models.common.chat import ChatMessage
from utils.agent import Agent
from utils.gcs import append_chat_message_to_gcs, get_chat_messages
from utils.llm import (
    extract_function_calls,
    extract_text,
    get_response,
    process_function_calls,
)
from utils.text import dedent_and_strip

logger = logging.getLogger(__name__)


async def generate_model_response(agent: Agent, prompt: str, user_id: str) -> str:
    """
    Generate Model response.
    """
    prompt = dedent_and_strip(prompt)
    logger.info(f"Received prompt from user {user_id}: {prompt}")

    # Retrieve user's chat history for the same day
    history = get_chat_messages(agent, user_id)

    if agent.model.startswith("google"):
        chat = agent.get_client().start_chat(history=history, response_validation=False)  # type: ignore
        response = await chat.send_message_async(prompt)
    elif agent.model.startswith("openai"):
        agent.messages.clear()
        for message in history:
            agent.messages.append(
                ChatMessage(role=message["role"], content=message["content"])
            )
        agent.messages.append(
            ChatMessage(role="system", content=agent.system_instruction)
        )
        agent.messages.append(ChatMessage(role="user", content=prompt))
        response = await get_response(agent=agent, chat=None)

    # Log Model response to prompt
    logger.info(f"Model response to prompt: {response}")

    # Final Model response
    final_response = ""

    # Function calling loop
    function_calling_in_process = True
    while function_calling_in_process:

        function_calls = extract_function_calls(agent, response)
        text_content = extract_text(agent, response)

        # Case 1: Only Function Calls
        if function_calls and not text_content:
            logger.info("Case 1: Only function calls in Model response.")
            api_responses = await process_function_calls(agent, function_calls)
            if agent.model.startswith("google"):
                response = await get_response(
                    agent=agent, chat=chat, api_responses=api_responses
                )
            elif agent.model.startswith("openai"):
                response = await get_response(agent=agent, chat=None)

            logger.info(f"Case 1: Model response to api responses: {response}")

        # Case 2: Function Calls and Text
        elif function_calls and text_content:
            logger.info("Case 2: Function calls and text in Model response.")
            api_responses = await process_function_calls(agent, function_calls)
            if agent.model.startswith("google"):
                response = await get_response(
                    agent=agent, chat=chat, api_responses=api_responses
                )
            elif agent.model.startswith("openai"):
                response = await get_response(agent=agent, chat=None)
            logger.info(f"Case 2: Model response to api responses: {response}")
            final_response += text_content

        # Case 3: Only Text
        else:
            logger.info("Case 3: Only Text in Model response.")
            function_calling_in_process = False
            final_response += extract_text(agent, response)

    role = "model" if agent.model.startswith("google") else "assistant"
    append_chat_message_to_gcs(agent, user_id, ChatMessage(role="user", content=prompt))
    append_chat_message_to_gcs(
        agent, user_id, ChatMessage(role=role, content=final_response)
    )

    return final_response
