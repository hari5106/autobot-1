import openai
import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import pyperclip
import random

# Set up the OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Set up the Telegram bot token
telegram_bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telegram.Bot(token=telegram_bot_token)

# Define the function that generates a bolded answer with links for specific words
def generate_bolded_answer(question):
    # Use the OpenAI API to generate an answer
    response = openai.Completion.create(
        engine="davinci", prompt=question, max_tokens=40, n=1, stop=None, temperature=0.5,
    )
    answer = response.choices[0].text.strip()

     # Identify the words to bold
    bolded_words = ["economy", "government", "industry", "finance"]

     # Find the words in the answer that have links
    words_with_links = []
    for word, link in bolded_words.items():
        if word in answer:
            words_with_links.append(word)

    # If none of the bolded words are present in the answer text, find any two words with more than 5 letters to bold
    if not words_to_bold:
       words_to_bold = [word for word in answer.split() if len(word) > 5][:2]  

    # Bold the identified words
    for word in words_to_bold:
        answer = answer.replace(word, f"<b>{word}</b>")

    # Use the OpenAI API to generate an explanation
    response = openai.Completion.create(
        engine="davinci", prompt=question + "\n\n", max_tokens=175, n=1, stop=None, temperature=0.5,
    )
    explanation = response.choices[0].text.strip()

    # Identify the words to bold and their links
    bolded_words = {"economy": "https://en.wikipedia.org/wiki/Economy",
                    "government": "https://en.wikipedia.org/wiki/Government"}

    # Find the first bolded word with a link in the answer
    bolded_word = ""
    for word in bolded_words.keys():
        if word in answer:
            bolded_word = word
            break

    # If no bolded word with a link is found in the answer, find one in the explanation
    if not bolded_word:
        for word in explanation.split():
            if word in bolded_words.keys():
                bolded_word = word
                break

    # Bold the first bolded word with a link and add the link to the answer
    if bolded_word:
        bolded_answer = answer.replace(bolded_word, f"<b><a href='{bolded_words[bolded_word]}'>{bolded_word}</a></b>")
    else:
        bolded_answer = answer

    # Bold other words in the answer
    BOLD_WORD = [word for word in bolded_answer.split() if len(word) > 5 and word not in ["am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "shall", "should", "may", "might", "must", "can", "could"]]
    for word in BOLD_WORD:
        bolded_answer = bolded_answer.replace(word, f"<b>{word}</b>")

    # Bold certain words in the answer
    bolded_answer = bolded_answer.replace("BOLD_WORD_1", "<b>BOLD_WORD_1</b>").replace("BOLD_WORD_2", "<b>BOLD_WORD_2</b>")

    # Bold certain words in the explanation
    bolded_word_set = set()
    bolded_explanation = explanation.replace("BOLD_WORD_1", "<b>BOLD_WORD_1</b>").replace("BOLD_WORD_2", "<b>BOLD_WORD_2</b>").replace("BOLD_WORD_3", "<b>BOLD_WORD_3</b>")
    for word in bolded_answer.split():
        if "<b>" in word:
            bolded_word_set.add(word[3:-4])
    for word in bolded_explanation.split():
        if "<b>" in word:
            bolded_word_set.add(word[3:-4])
    for word in bolded_word_set:
        bolded_explanation = bolded_explanation.replace(word, f"<b>{word}</b>")

    # Bold other words in the explanation
    BOLD_WORD = [word for word in bolded_explanation.split() if len(word) > 5 and word not in ["am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "shall", "should", "may", "might", "must", "can", "could"]]
    for word in BOLD_WORD:
        bolded_explanation = bolded_explanation.replace(word, f"<b>{word}</b>")


    # Construct the final answer with the bolded words
    final_answer = f"{bolded_answer}\n\n{bolded_explanation}\n\nLearn more about <b>{bolded_word}</b> here: {bolded_words.get(bolded_word, 'N/A')}\n\n#SPJ11"

    # Copy the final answer to the clipboard
    pyperclip.copy(final_answer)

# Define the function that handles incoming messages
def handle_message(update, context):
    message_text = update.message.text
    generate_bolded_answer(message_text)

# Set up the Telegram bot handlers
updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

# Start the Telegram bot
updater.start_polling()