import streamlit as st
import ollama
import pygments
from numpy.ma.core import repeat
from pygments.styles.dracula import background

# Custom page style
page_style = '''
<style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://unsplash.com/photos/big-data-technology-for-business-finance-analytic-concept-modern-graphic-interface-shows-massive-information-of-business-sale-report-profit-chart-and-stock-market-trends-analysis-on-screen-monitor-9lpSbMgYm0Q");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.8);
    }
    .chat-bubble {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 75%;
    }
    .chat-bubble.user {
        background-color: #dcedf7;
        margin-left: auto;
    }
    .chat-bubble.bot {
        background-color: #f1f0f0;
    }
    .input-container {
        margin-top: 20px;
        display: flex;
    }
    .input-container input {
        flex: 1;
        padding: 10px;
        border-radius: 5px 0 0 5px;
        border: 1px solid #ccc;
    }
    .input-container button {
        padding: 10px;
        border-radius: 0 5px 5px 0;
        border: 1px solid #ccc;
        background-color: #007bff;
        color: white;
    }
</style>

'''
st.markdown(page_style, unsafe_allow_html=True)

# Title of the app
st.title("Finance Chatbot")

# Define the model creation script
modelfile = '''
You are an expert in the field of finance
'''

# Create the model (assuming the 'ollama.create' function works synchronously)
ollama.create(model='finance_chat_bot', modelfile=modelfile)

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# First input question by the user from the sidebar
st.sidebar.header("Ask your finance-related question:")
initial_query = st.sidebar.text_input("Your question:", key="initial_query")

if initial_query and 'initial_query_processed' not in st.session_state:
    response = ollama.chat(model='finance_chat_bot', messages=[
        {
            'role': 'user',
            'content': initial_query,
        },
    ])
    st.session_state.history.append({'role': 'user', 'content': initial_query})
    st.session_state.history.append({'role': 'bot', 'content': response['message']['content']})
    st.session_state.initial_query_processed = True

# Main chat window
# st.subheader("Chat History")
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.history:
        if message['role'] == 'user':
            st.markdown(f'<div class="chat-bubble user"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble bot"><strong>Bot:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input container for user query
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("", key="user_input")
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        response = ollama.chat(model='finance_chat_bot', messages=[
            {
                'role': 'user',
                'content': user_input,
            },
        ])
        st.session_state.history.append({'role': 'user', 'content': user_input})
        st.session_state.history.append({'role': 'bot', 'content': response['message']['content']})
        st.experimental_rerun()  # Rerun the app to clear the input field and display the updated history

# Scroll chat to bottom
st.write('<script>window.scrollTo(0,document.body.scrollHeight);</script>', unsafe_allow_html=True)