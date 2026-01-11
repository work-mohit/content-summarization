import os
import validators
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

# from pathlib import Path

# not needed since we are taking the api keys from the user
# kind of necessary if we're putting main.py inside app folder
# due to this streamlit is not able to get the env variables corretly
# env_path = Path(__file__).resolve().parent.parent / ".env"
# load_dotenv(dotenv_path=env_path, override=True)

HF_MODEL = "meta-llama/Llama-3.1-8B-Instruct"
OPENAI_MDDEL = "gpt-4o-mini"
GROQ_MDDEL = "llama3-70b-8192"
ANTHROPIC_MDDEL = "claude-haiku-4.5"
GEMINI_MDDEL = "gemini-2.5"

@st.cache_resource
def load_model(provider, api_key):
    """
    It return the LLM model Object from the given provider.
    
    :param provider: LLM Provider name
    :param api_key: Valid API key to get establish the connection with the model

    """
    try: 
        match provider:
            case "Open AI":
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(
                    model=OPENAI_MDDEL,
                    api_key=api_key,
                    temperature=0.3
                )

            case "Hugging Face":
                from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
                llm = HuggingFaceEndpoint(
                    repo_id=HF_MODEL,
                    task="text-generation",
                    huggingfacehub_api_token=api_key,
                    max_new_tokens=4000,
                    temperature=0.3,
                )
                return ChatHuggingFace(llm=llm)

            case "Gemini":
                from langchain_google_genai import ChatGoogleGenerativeAI
                return ChatGoogleGenerativeAI(
                    model=GEMINI_MDDEL,
                    google_api_key=api_key,
                    temperature=0.3,
                )

            case "Groq":
                from langchain_groq import ChatGroq
                return ChatGroq(
                    model=GROQ_MDDEL,        
                    groq_api_key=api_key,
                    temperature=0.3,
                )

            case "Anthropic":
                from langchain_anthropic import ChatAnthropic
                return ChatAnthropic(
                    model=ANTHROPIC_MDDEL,
                    anthropic_api_key=api_key,
                    temperature=0.3,
                )
                    
    except:
        raise ValueError("Invalid API keys!")
    

def fetch_youtube_transcript(url):
    loader = None
    try: 
        loader = YoutubeLoader.from_youtube_url(url)
        return loader.load()
    except IOError as e:
        raise IOError("Youtube Video doesn't have english transcript")

def fetch_url_content(url):
    loader = UnstructuredURLLoader(urls=[url],ssl_verify=False)
    return loader.load()

def get_content(url):
    """
    This function will call the utilities to fetch the content based on type of the url.
    This start by a checks url contains youtube.com as a string, 
    if its call fetch_youtube_transcript, otherwise fetch url
    Both will reutrn the document

    :param url: A valid link will be given as input like, a youtube video link or a website that you want to summarize.
    """
    try: 
        content_document = None
        if "youtube.com" in url:
            content_document = fetch_youtube_transcript(url)
        else:
            content_document = fetch_url_content(url)
        return content_document
    except Exception as e:
        st.error(f"Exception: {e}")

 
def get_prompt():
    prompt = """
        You are an expert teacher and technical explainer.

        Your task is to summarize the following YouTube video transcript or website content
        in a way that helps a learner understand the topic quickly and clearly.

        Follow these rules strictly:
        - Use simple, clear language
        - Avoid storytelling, introductions, or generic descriptions
        - Focus on explaining concepts, terms, and ideas
        - Be concise but informative
        - Do NOT repeat obvious or filler content

        Structure the output as follows:

        1. Topic in One Line
        - Explain the main topic in ONE simple sentence

        2. Key Concepts Explained (Most Important Section)
        - List 5–7 important concepts or terms discussed
        - For each concept:
            • What it means (simple explanation)
            • Why it matters (1 line)

        3. How Things Work (If Applicable)
        - Explain any process, flow, or mechanism step-by-step
        - Keep steps short and clear

        4. Important Examples or Use-Cases
        - Mention only examples that actually help understanding
        - Explain them briefly

        5. Key Takeaways (TL;DR)
        - 4–6 bullet points
        - Each bullet should be actionable or insight-driven

        6. One-Sentence Mental Model
        - Explain the topic using an analogy or mental shortcut

        Content to summarize:
        {content}

        Output should help someone understand the topic in under 3–4 minutes of reading.
    """
    
    return PromptTemplate(template=prompt, input_variables = ["content"])
    

def handle_summarization(model, content):
    try:
        prompt = get_prompt()
        print(prompt)
        chain = prompt | model | StrOutputParser()
        result = chain.invoke({"content":content})
        return result
    except Exception as e:
        st.exception(f"Exception {e}")


def summarize(provider, api_key, url):
    """
    Docstring for summarize
    
    :param provider: Description
    :param api_key: Description
    :param url: Description
    """
    try:
        if not api_key.strip() or api_key is None:
            raise ValueError("An API Key is required")
        if not url.strip() or url is None:
            raise ValueError("Please provide an URL!")
        if not validators.url(url):
            raise ValueError("Please provide a valid url. It can be a youtube or a website url.") 
        model = load_model(provider, api_key)
        content = get_content(url)
        summarized_text = handle_summarization(model, content)
        st.success(summarized_text)
    except ValueError as e:
        st.error(f"Error: {e}")  

def main():
    try: 
        st.set_page_config(page_title="Content Summarizer")
        st.title("An LLM Applicaton for Content Summarization")

        st.subheader("Summarize URL")
        url = st.text_input("Paste here")

        with st.sidebar:
            provider = st.selectbox("Choose your LLM provider ", ("Open AI", "Hugging Face", "Gemini", "Groq", "Anthropic"))
            api_key = st.text_input("Enter the API keys of the choosen provider", value="", type="password")
        
        
        if st.button("Summarize"):
            with st.spinner("Processing..."):
                summarize(provider, api_key, url)

        st.write("---")
        st.caption("AI App created by @ Mohit Joshi") 
    except ValueError as e:
        st.error(f"Error: {e}")
    except Exception as e:
        st.exception(f"Exception : {e}")

if __name__ == "__main__":
    main()
