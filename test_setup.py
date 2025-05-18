# test_setup.py
import streamlit as st
from dotenv import load_dotenv
import os

# Import the specific LangChain community LLM for Hugging Face Hub
# For newer langchain-huggingface:
from langchain_huggingface import HuggingFaceEndpoint 
# Or for older langchain, it might be from langchain_community.llms
# from langchain_community.llms import HuggingFaceHub


print("Attempting to load environment variables...")
if load_dotenv():
    print(".env file loaded successfully.")
else:
    print(".env file not found or failed to load. Make sure it's in the root directory.")

st.title("LLM Setup Test - Hugging Face")

# Test Hugging Face
hf_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if hf_api_token:
    st.success("Hugging Face API Token found in environment variables!")
    try:
        # --- Using HuggingFaceEndpoint (Recommended for new projects) ---
        # Choose a model repository ID from Hugging Face Hub that supports text generation
        # and is available via the serverless Inference API.
        # Examples:
        # repo_id = "mistralai/Mistral-7B-Instruct-v0.1" # Powerful, might require Pro access or have rate limits
        # repo_id = "google/flan-t5-large" # Good all-rounder for various tasks including Q&A
        # repo_id = "google/flan-t5-small" # Smaller, faster, good for testing
        repo_id = "gpt2" # Classic, smaller model

        st.write(f"Attempting to initialize HuggingFaceEndpoint with repo_id: {repo_id}")

        # HuggingFaceEndpoint requires the token to be passed directly or set as an environment variable
        # It automatically picks up HUGGINGFACEHUB_API_TOKEN from the environment if os.environ["HUGGINGFACEHUB_API_TOKEN"] is set
        llm_hf = HuggingFaceEndpoint(
            repo_id=repo_id,
            # huggingfacehub_api_token=hf_api_token, # Explicitly pass if needed, but usually not if env var is set
            temperature=0.7, # Controls randomness
            max_new_tokens=100 # Max number of tokens to generate
        )
        st.write("HuggingFaceEndpoint LLM initialized successfully!")

        # Test a simple invocation
        st.write("Testing model invocation...")
        prompt = "What is the main purpose of a quiz?"
        try:
            response = llm_hf.invoke(prompt)
            st.write(f"Prompt: {prompt}")
            st.write("Hugging Face Model Response:")
            st.text_area("Response", response, height=100)
            st.success("Model invocation successful!")
        except Exception as e_invoke:
            st.error(f"Error during model invocation: {e_invoke}")
            st.info("This could be due to rate limits, the model not being available, or an issue with the token/repo_id.")
            st.info("Check the Hugging Face Hub page for your chosen model for its status and API availability.")


        # --- Older HuggingFaceHub (if HuggingFaceEndpoint gives issues or for specific legacy reasons) ---
        # from langchain_community.llms import HuggingFaceHub # Make sure to import this
        # st.write(f"Attempting to initialize HuggingFaceHub with repo_id: {repo_id}")
        # # Ensure your HUGGINGFACEHUB_API_TOKEN is set as an environment variable,
        # # HuggingFaceHub will pick it up automatically.
        # llm_hf_hub = HuggingFaceHub(
        #     repo_id=repo_id,
        #     model_kwargs={"temperature": 0.7, "max_length": 64} # max_length for older API
        # )
        # st.write("HuggingFaceHub LLM initialized successfully!")
        # response_hf_hub = llm_hf_hub.invoke("What is the capital of France?")
        # st.write("HuggingFace Hub Model Response (HuggingFaceHub):", response_hf_hub)


    except Exception as e:
        st.error(f"Error initializing or using Hugging Face LLM: {e}")
        st.info("Make sure your HUGGINGFACEHUB_API_TOKEN is correct and the model repo_id is valid and available for inference.")
else:
    st.warning("Hugging Face API Token (HUGGINGFACEHUB_API_TOKEN) not found in environment variables.")
    st.info("Please ensure it is set in your .env file to use Hugging Face Hub models.")

st.write("Setup test complete.")
print("Streamlit app can be run now.")
