import os
os.environ['OPENAI_API_KEY']  = st.secrets['OPENAI_API_KEY']
from langchain_openai import ChatOpenAI

gpt4o_mini_model = ChatOpenAI(model="gpt-4o-mini")

#Prompt template for tweet generation like elon musk
from langchain import PromptTemplate

app_template="""You're to act as {Celebrity} and generate a tweet on this topic:{topic}, make sure that the tweet is not more than 280 characters,
and the tweet should be in the style of {Celebrity} it should look that way and in {language} the tweet should be and make it more engaging and interesting,
and output {number} of tweets in numbered format like below:
1. (tweet1)

2. (tweet2)

3. 
..."""

app_prompt=PromptTemplate(template=app_template,input_variables=["topic","Celebrity","number"])
#response = app_prompt.format(topic="AI",Celebrity="Elon Musk",number=3)
#print(response)

#Chain
from langchain import LLMChain

app_chain=app_prompt|gpt4o_mini_model

import streamlit as st

st.header("Celebrity Tweet Generator")
st.subheader("Generate tweets for your favorite celebrity")

celebrity=st.text_input("Enter the Celebrity Name")
topic=st.text_input("Enter the topic")
number=st.number_input("Enter the number of tweets",min_value=1,max_value=10)


if st.button("Generate"):
    response=app_chain.invoke({"topic":topic,"Celebrity":"Elon Musk","number":number})
    st.write(response.content)

    # Add buttons in columns
    col1, col2 = st.columns(2)
    
    
    with col2:
        # Create X/Twitter share URL
        tweet_text = response.content
        # Clean up the tweet text for URL
        tweet_text = tweet_text.replace('\n', ' ').replace('#', '%23').replace(' ', '%20')
        twitter_url = f"https://twitter.com/intent/tweet?text={tweet_text}"
        
        # Create a button that opens Twitter
        st.markdown(f'<a href="{twitter_url}" target="_blank"><button style="background-color: #1DA1F2; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer;">Post to X</button></a>', unsafe_allow_html=True)
