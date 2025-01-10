import streamlit as st
import os

# Make sure st.secrets exists and contains the key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI
from langchain import PromptTemplate, LLMChain

...

# Now that environment is set, you can initialize your model
gpt4o_mini_model = ChatOpenAI(model="gpt-4o-mini")

app_template = """You're to act as {Celebrity} ..."""
app_prompt = PromptTemplate(template=app_template, input_variables=["topic","Celebrity","number"])
app_chain = app_prompt | gpt4o_mini_model

st.header("Celebrity Tweet Generator")
st.subheader("Generate tweets for your favorite celebrity")

celebrity = st.text_input("Enter the Celebrity Name")
topic = st.text_input("Enter the topic")
number = st.number_input("Enter the number of tweets", min_value=1, max_value=10)

if st.button("Generate"):
    response = app_chain.invoke({"topic": topic, "Celebrity": celebrity, "number": number})
    st.write(response.content)

    # Buttons in columns
    col1, col2 = st.columns(2)
    with col2:
        tweet_text = response.content
        # Clean up for URL
        tweet_text = tweet_text.replace('\n', ' ').replace('#', '%23').replace(' ', '%20')
        twitter_url = f"https://twitter.com/intent/tweet?text={tweet_text}"
        st.markdown(f'<a href="{twitter_url}" target="_blank"><button style="background-color: #1DA1F2; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer;">Post to X</button></a>', unsafe_allow_html=True)
