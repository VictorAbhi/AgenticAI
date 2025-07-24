# Sentiment-Aware Chatbot

This project implements a **sentiment-aware chatbot** that uses LangChain, Google Generative AI, and Hugging Face Transformers to process user inputs, detect sentiment, and respond with an adaptive tone while maintaining conversation context.

## Features

- **Sentiment Analysis**: Detects user sentiment (positive, negative, neutral) using a pre-trained model (`cardiffnlp/twitter-roberta-base-sentiment-latest`).
- **Adaptive Tone**: Adjusts responses based on sentiment:
  - Enthusiastic and warm for positive sentiment.
  - Empathetic and supportive for negative sentiment.
  - Informative and polite for neutral sentiment.
- **Conversation Memory**: Maintains context using `ConversationBufferMemory`.
- **Integration with Google Generative AI**: Uses the `gemini-1.5-flash` model for generating responses.
- Written in **Python** and runs as a standalone script.

## Project Structure

```
main.py      # Main script containing the chatbot code
.env            # Environment file for storing the Google API Key
document.pdf       # minimal documentation
README.md       # This file
```

##  How It Works

1. **User Input**: The user provides a message (e.g., "I'm so excited!" or "I'm having a terrible day").
2. **Sentiment Analysis**: The input is analyzed using a pre-trained sentiment analysis model to classify it as positive, negative, or neutral.
3. **Context Management**: Conversation history is retrieved and maintained using `ConversationBufferMemory`.
4. **Response Generation**: The Google Generative AI model generates a response, adapting its tone based on the detected sentiment and incorporating conversation context.
5. **History Update**: The user input and bot response are saved to memory for future context.

## Requirements

- Python 3.8+
- Required packages:
  - `python-dotenv`
  - `transformers`
  - `langchain`
  - `langchain-google-genai`
  - `torch`
- A Google API Key for accessing the `gemini-1.5-flash` model.

## Setup Instructions

Refer to the `setup.pdf` document for detailed instructions on setting up the environment, installing dependencies, configuring the Google API Key, and running the chatbot.

### Quick Start
1. Save the code in a file named `chatbot.py`.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install python-dotenv transformers langchain langchain-google-genai torch
   ```
4. Create a `.env` file with your Google API Key:
   ```bash
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```
5. Run the chatbot:
   ```bash
   python main.py
   ```

## Running the Application
Run `python main.py` to start the interactive chatbot:
- Enter a message to interact with the bot.
- The bot will respond with a tone adapted to the sentiment of your input.
- View the conversation history after each response.
- Type `exit` to quit.

## Example Usage
```
Start chatting with the bot (type 'exit' to stop):
You: I'm so excited!
Bot: That's awesome to hear! What's got you so pumped? 
Conversation history:
human: I'm so excited!
ai: That's awesome to hear! What's got you so pumped? 

You: I'm having a terrible day.
Bot: I'm so sorry to hear that. Want to share what's been going on? I'm here to listen.
Conversation history:
human: I'm so excited!
ai: That's awesome to hear! What's got you so pumped? 
human: I'm having a terrible day.
ai: I'm so sorry to hear that. Want to share what's been going on? I'm here to listen.
```

## Future Work
- Integrate additional sentiment analysis models for improved accuracy.
- Add support for multi-turn conversation summarization.
- Implement a graphical user interface for enhanced user experience.
- Extend the chatbot to handle specific domains (e.g., customer support, e-commerce).