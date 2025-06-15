import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers

# Function to get response from LLaMA 2 model
def get_llama_response(input_text, no_words, blog_style):
    llm = CTransformers(
        model="Models/llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type="llama",
        config={
            'max_new_tokens': no_words,
            'temperature': 0.5,
            'threads': 2  # Limit CPU usage
        }
    )

    template = """
    Write a blog with the following details:

    Topic: {topic}
    Style: {style}

    Blog:
    """

    prompt = PromptTemplate(input_variables=["topic", "style"], template=template)
    formatted_prompt = prompt.format(topic=input_text, style=blog_style)
    # response = llm(formatted_prompt)
    response = llm.invoke(formatted_prompt)
    return response

# Streamlit UI
st.set_page_config(page_title="LLaMA 2 Blog Generator")
st.header("🦙 LLaMA 2 Blog Generator")

input_text = st.text_input("Enter the Blog Topic")

col1, col2 = st.columns(2)

with col1:
    no_words = st.slider("Number of Words", min_value=50, max_value=300, step=50, value=100)

with col2:
    blog_style = st.selectbox("Writing Style", ["Professional", "Casual", "Informative"])

submit = st.button("Generate Blog")

if submit and input_text:
    with st.spinner("Generating..."):
        response = get_llama_response(input_text, no_words, blog_style)
        st.subheader("Generated Blog")
        st.write(response)
