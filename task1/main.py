# install necessary libraries
import os
from dotenv import load_dotenv
from transformers import pipeline
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage

# Load .env variables
load_dotenv()

# Access API key from environment
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Set up LLM and memory
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.7)
memory = ConversationBufferMemory(return_messages=True)

# Define sentiment-aware prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a friendly and empathetic chatbot. Adapt your tone based on the user's sentiment:
- For positive sentiment, respond enthusiastically and warmly.
- For negative sentiment, respond with empathy and offer support.
- For neutral sentiment, respond informatively and politely.
The user's current sentiment is {sentiment}. Use the conversation history to maintain context.
"""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])


# Load sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

def get_sentiment(text):
    result = sentiment_pipeline(text)[0]
    label = result["label"].lower()  # 'POSITIVE', 'NEGATIVE'
    return label if label in ["positive", "neutral", "negative"] else "neutral"

# define chain
chain = prompt | llm

def chat_with_bot(user_input):
    # Get sentiment of user input
    sentiment = get_sentiment(user_input)
    
    # Load conversation history as a list of BaseMessage objects
    history = memory.load_memory_variables({})["history"]
    
    # Invoke the chain with sentiment and history
    response = chain.invoke({
        "input": user_input,
        "sentiment": sentiment,
        "history": history  # Pass history as a list of BaseMessage objects
    })
    
    # Explicitly save messages to memory
    memory.chat_memory.add_message(HumanMessage(content=user_input))
    memory.chat_memory.add_message(AIMessage(content=response.content))
    
    return response.content

if __name__ == "__main__":
    print("Start chatting with the bot (type 'exit' to stop):")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = chat_with_bot(user_input)
        print(f"Bot: {response}")
        print("\nConversation history:")
        history = memory.load_memory_variables({})["history"]
        for msg in history:
            print(f"{msg.type}: {msg.content}")