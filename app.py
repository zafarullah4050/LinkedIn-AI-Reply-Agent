import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Long reply rules
LONG_PROMPT = """
You are a friendly LinkedIn assistant.
Always follow these steps:
1. Acknowledge the message
2. Give a relevant compliment
3. Ask a smart question
4. Add light humor
5. Respond based on conversation
6. Share value subtly
7. Suggest a meeting politely
8. Keep conversation friendly if no meeting yet
"""

# Short reply rules
SHORT_PROMPT = """
You are a friendly LinkedIn assistant.
Rules for short reply:
1. Greet and acknowledge the message
2. Give 1 relevant compliment
3. Ask 1 short open-ended question
4. Keep it under 3 sentences
"""

# Function to get AI reply
def ai_reply(message, style="Long", conversation_history=[]):
    # Add system prompt if conversation is empty
    if len(conversation_history) == 0:
        conversation_history.append({
            "role": "system",
            "content": LONG_PROMPT if style == "Long" else SHORT_PROMPT
        })

    # Add user message to history
    conversation_history.append({"role": "user", "content": message})

    # Call Groq API for reply
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=conversation_history,
        max_tokens=250 if style == "Long" else 100,
        temperature=0.7
    )

    # Extract reply and save in history
    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})

    return reply, conversation_history

# Streamlit page setup
st.set_page_config(page_title="LinkedIn AI Reply Agent", page_icon="💬")
st.title("🤖 LinkedIn AI Reply Agent")
st.write("Generate LinkedIn-style replies using Groq API.")

# Choose reply style
style_choice = st.radio("Select Reply Style:", ["Long", "Short"])

# Create memory for conversation
if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = []

# Input for user's LinkedIn message
user_message = st.text_input("Enter incoming LinkedIn message:")

# Button to generate reply
if st.button("Generate Reply"):
    if not user_message.strip():
        st.warning("Please enter a message.")
    else:
        reply, st.session_state.conversation_memory = ai_reply(
            user_message,
            style_choice,
            st.session_state.conversation_memory
        )
        st.subheader("AI Reply")
        st.write(reply)

# Show conversation history
with st.expander("📝 Conversation History"):
    for msg in st.session_state.conversation_memory:
        role = "System" if msg["role"] == "system" else ("User" if msg["role"] == "user" else "AI")
        st.markdown(f"**{role}:** {msg['content']}")
