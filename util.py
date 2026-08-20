import os
import re
from dotenv import load_dotenv
# from google import genai
# from openai import OpenAI
import requests
import json


load_dotenv()


# MODEL = "gemini-3.7-flash"
# OPENROUTER_API_KEY = os.getenv("OPEN_ROUTER")


def llm_call(prompt: str, system_prompt: str = "") -> str:
    # Build messages array, including system prompt if provided
    api_key = os.getenv("OPEN_ROUTER_KEY")
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "model": "openrouter/free",  # Note: ensure this model ID is active on OpenRouter
                "messages": messages,
                "reasoning": {"enabled": False},
            }
        ),
    )

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract the assistant's reply from the standard OpenAI-compatible response format
        return data["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")


# def llm_call(
#     prompt: str,
#     system_prompt: str = "",
#     model="deepseek-ai/DeepSeek-V4-Pro-0813:novita",
# ) -> str:
#     """
#     Calls the model with the given prompt and returns the response.

#      Args:
#         prompt (str): The user prompt to send to the model.
#          system_prompt (str, optional): The system prompt to send to the model. Defaults to "".
#          model (str, optional): The model to use for the call. Defaults to "claude-sonnet-4-6".

#      Returns:
#          str: The response from the language model.
#     """
#     client = OpenAI(
#         base_url="https://router.huggingface.co/v1",
#         api_key=os.getenv["HF_TOKEN"],
#     )

#     completion = client.chat.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}],
#     )

#     return completion.choices[0].message


# def llm_call(prompt: str, system_prompt: str = "", model="gemini-3.7-flash") -> str:
#     """
#     Calls the model with the given prompt and returns the response.

#     Args:
#         prompt (str): The user prompt to send to the model.
#         system_prompt (str, optional): The system prompt to send to the model. Defaults to "".
#         model (str, optional): The model to use for the call. Defaults to "claude-sonnet-4-6".

#     Returns:
#         str: The response from the language model.
#     """
#     client = genai.Client()
#     response = client.interactions.create(
#         model=model,
#         input=prompt,
#         system_instruction=system_prompt,
#     )

#     return response.output_text


def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    match = re.search(f"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return match.group(1) if match else ""


# Second API call - model continues reasoning from where it left off
# response2 = requests.post(
#     url="https://openrouter.ai/api/v1/chat/completions",
#     data=json.dumps(
#         {
#             "model": "openrouter/free",
#             "messages": messages,  # Includes preserved reasoning_details
#             "reasoning": {"enabled": True},
#         }
#     ),
# )
