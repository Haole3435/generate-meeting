from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

abstract_summary_prompt = ChatPromptTemplate.from_template("""
You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points. Return ONLY the summary text without any additional formatting or labels:

{text}
""")

key_points_prompt = ChatPromptTemplate.from_template("""
**INSTRUCTIONS:**
1. Carefully read the meeting transcript.
2. List up to 5 key points.
3. Each point must be concise (under 15 words).
4. Format: Each point on a new line, no numbering or bullet points.
5. Return ONLY the key points, one per line.

**TRANSCRIPT:**
{text}

**KEY POINTS:**
""")

action_items_prompt = ChatPromptTemplate.from_template("""
**INSTRUCTIONS:**
1. Identify action items from the transcript.
2. Format each action item as: "[Responsible Person] [Action] by [Deadline]".
3. Return ONLY the action items, one per line.
4. Include at least 2 action items.

**TRANSCRIPT:**
{text}

**ACTION ITEMS:**
""")

sentiment_prompt = ChatPromptTemplate.from_template("""
As an AI with expertise in language and emotion analysis, your task is to analyze the sentiment of the following text. Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Return ONLY a single word indicating the sentiment (Positive, Negative, or Neutral):

{text}
""")

# Update chain definitions to handle text input correctly
def get_text(state):
    return state.get("text", "")

abstract_summary_chain = (
    RunnablePassthrough.assign(text=get_text)
    | abstract_summary_prompt
    | llm
)

key_points_chain = (
    RunnablePassthrough.assign(text=get_text)
    | key_points_prompt
    | llm
)

action_items_chain = (
    RunnablePassthrough.assign(text=get_text)
    | action_items_prompt
    | llm
)

sentiment_chain = (
    RunnablePassthrough.assign(text=get_text)
    | sentiment_prompt
    | llm
)