import streamlit as st
from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEndpoint # For HF Inference API
import traceback

# Load environment variables (for HUGGINGFACEHUB_API_TOKEN)
load_dotenv()

# --- LLM Initialization ---
def get_llm_instance():
    """Initializes and returns the HuggingFaceEndpoint LLM instance."""
    hf_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not hf_api_token:
        st.error("Hugging Face API Token not found. Please set HUGGINGFACEHUB_API_TOKEN in your .env file.")
        return None

    # Recommended models for generation that work well with instruction-following:
    # repo_id = "mistralai/Mistral-7B-Instruct-v0.1" # Very good, but might be slower or have stricter rate limits
    repo_id = "HuggingFaceH4/zephyr-7b-beta" # Another good instruction-tuned model
    # repo_id = "google/flan-t5-small" # Good general purpose, try this or "google/flan-t5-base" or "google/flan-t5-small"
    #repo_id = "gpt2-medium" # Simpler, faster, but less capable for complex instructions

    try:
        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            # huggingfacehub_api_token=hf_api_token,
            # Picked up from env var by default
            temperature=0.6,      # Controls randomness. Lower for more factual, higher for more creative.
            max_new_tokens=1024,  # Max tokens for the generated quiz. Adjust as needed.
                                  # For 3 questions, 512 might be enough, for more, increase.
            # top_k=50,           # Consider for sampling diversity
            # top_p=0.95,         # Consider for sampling diversity
            repetition_penalty=1.1 # Slightly penalize repetition
        )
        return llm
    except Exception as e:
        st.error(f"Error initializing Hugging Face LLM ({repo_id}): {e}")
        return None

# --- Prompt Engineering and LLM Call ---
def generate_quiz_with_llm(quiz_params, llm):
    """
    Generates a quiz using the LLM based on the provided parameters.
    """
    if not llm:
        return "LLM not initialized. Cannot generate quiz."

    # Constructing the prompt
    # This is a CRITICAL step and will require iteration.
    
    prompt_parts = [
        f"You are an expert quiz generator. Create a quiz with the following specifications:\n"
        f"Topic: {quiz_params['topic']}\n"
        f"Difficulty: {quiz_params['difficulty']}\n"
        f"Number of Questions: {quiz_params['num_questions']}\n"
        f"Question Types: {', '.join(quiz_params['question_types'])}\n"
        f"Include Explanations for answers: {'Yes' if quiz_params['include_explanations'] else 'No'}\n"
    ]

    if quiz_params.get('sub_topics'):
        prompt_parts.append(f"Specific Sub-topics: {', '.join(quiz_params['sub_topics'])}\n")
    if quiz_params.get('context_keywords'):
        prompt_parts.append(f"Context Keywords to focus on: {', '.join(quiz_params['context_keywords'])}\n")
    if quiz_params.get('target_audience') and quiz_params['target_audience'] != "general":
        prompt_parts.append(f"Target Audience: {quiz_params['target_audience']}\n")
    if quiz_params.get('max_question_length'):
        prompt_parts.append(f"Maximum words per question: {quiz_params['max_question_length']}\n")

    prompt_parts.append("\nInstructions for Quiz Format:\n")
    prompt_parts.append("Please format the quiz clearly. For each question, provide:\n")
    prompt_parts.append("1. The question number (e.g., Question 1:).\n")
    prompt_parts.append("2. The question text.\n")
    prompt_parts.append("3. If 'multiple_choice': Provide 3-4 options labeled A), B), C), D).\n")
    prompt_parts.append("4. The correct answer (e.g., Answer: B) or Answer: [correct short answer] or Answer: True/False).\n")
    if quiz_params['include_explanations']:
        prompt_parts.append("5. A brief explanation for the answer.\n")
    prompt_parts.append("\nExample of a Multiple Choice Question format:\n")
    prompt_parts.append("Question 1: What is the capital of France?\n")
    prompt_parts.append("A) London\nB) Berlin\nC) Paris\nD) Madrid\n")
    prompt_parts.append("Answer: C\n")
    if quiz_params['include_explanations']:
        prompt_parts.append("Explanation: Paris is the capital and most populous city of France.\n")
    
    prompt_parts.append("\nStart generating the quiz now based on these instructions.\n")
    
    full_prompt = "".join(prompt_parts)
    
    st.info("Sending the following prompt to the LLM (scroll to see full prompt):")
    st.text_area("Generated Prompt", full_prompt, height=200)

    try:
        with st.spinner(f"🧠 Generating {quiz_params['num_questions']}-question quiz on '{quiz_params['topic']}'... This might take a moment."):
            response = llm.invoke(full_prompt)
        return response # This will be a string from HuggingFaceEndpoint
    except Exception as e:
        st.error(f"Error during LLM invocation: {e}")
        st.text(traceback.format_exc())
        return f"Error generating quiz: {e}"


def main():
    st.set_page_config(page_title="LLM Quiz Generator", layout="centered")
    st.title("📝 LLM-Powered Quiz Generator")
    st.markdown("Fill in the details below to generate your quiz!")

    # --- LLM Instance (cached for efficiency) ---
    # Cache the LLM instance so it doesn't re-initialize on every interaction
    # if 'llm' not in st.session_state: # Simpler approach without session state first
    #     st.session_state.llm = get_llm_instance()
    # llm = st.session_state.llm
    
    # Initialize LLM once
    if 'llm_instance' not in st.session_state:
        st.session_state.llm_instance = None # Initialize
    if st.session_state.llm_instance is None: # Attempt to load if not loaded
        st.session_state.llm_instance = get_llm_instance()
    
    llm = st.session_state.llm_instance


    st.subheader("Quiz Parameters")
    with st.form("quiz_params_form"):
        topic = st.text_input("📚 Topic for the Quiz", "Python Data Types")
        difficulty_options = ["Easy", "Medium", "Hard"]
        difficulty = st.selectbox("🎯 Difficulty Level", difficulty_options, index=1)
        num_questions = st.number_input("🔢 Number of Questions", min_value=1, max_value=10, value=2) # Reduced max for quicker tests
        question_type_options = ["Multiple Choice", "Short Answer", "True/False"]
        question_types = st.multiselect("✍️ Question Types", question_type_options, default=["Multiple Choice"])
        include_explanations = st.radio("💡 Include Explanations?", ("Yes", "No"), index=0)

        st.markdown("--- Optional Parameters ---")
        sub_topics = st.text_input("🧩 Specific Sub-topics (comma-separated, optional)", placeholder="e.g., lists, dictionaries")
        context_keywords = st.text_input("🔑 Context Keywords (comma-separated, optional)", placeholder="e.g., syntax, methods")
        target_audience = st.text_input("👥 Target Audience (optional)", placeholder="e.g., Beginners")
        max_question_length = st.number_input("📏 Max Words per Question (optional, 0 for no limit)", min_value=0, value=0)
        
        submitted = st.form_submit_button("🚀 Generate Quiz")

    if submitted:
        if not llm:
            st.error("LLM could not be initialized. Please check your Hugging Face API Token and configuration.")
            return # Stop further processing

        if not topic:
            st.error("Topic is a required field.")
        elif not question_types:
            st.error("Please select at least one question type.")
        else:
            quiz_params = {
                "topic": topic,
                "difficulty": difficulty.lower(),
                "num_questions": num_questions,
                "question_types": [qt.lower().replace(" ", "_") for qt in question_types],
                "include_explanations": True if include_explanations == "Yes" else False,
                "sub_topics": [st.strip() for st in sub_topics.split(',') if st.strip()] if sub_topics else [],
                "context_keywords": [kw.strip() for kw in context_keywords.split(',') if kw.strip()] if context_keywords else [],
                "target_audience": target_audience if target_audience else "general",
                "max_question_length": max_question_length if max_question_length > 0 else None
            }

            st.success("Parameters collected! Generating quiz...")
            # st.json(quiz_params) # Can hide this later

            # --- Call LLM and Display Raw Output ---
            raw_llm_output = generate_quiz_with_llm(quiz_params, llm)
            
            st.subheader("🤖 Raw LLM Output:")
            st.markdown("```text\n" + raw_llm_output + "\n```") # Display as a text block

            # Next step will be to parse this raw_llm_output

if __name__ == "__main__":
    main()