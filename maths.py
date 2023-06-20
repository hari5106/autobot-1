import logging
import asyncio
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, user
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

API_TOKEN = '6115831183:AAHnoyIW1jUppDVRluIz3wnPqxhlZTsVaas'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

superscript_pattern = re.compile(
  r'\^(\((?:[^()]+|)*\)|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|[a-z]+|\w+\((?:[^(),]*,?)*\))'
)
subscript_pattern = re.compile(r'_(.*?)($|\s|[^0-9a-zA-Z])')

# Create a dispatcher instance
dispatcher = Dispatcher(bot)
subscript_replacements = {
  '0': '₀',
  '1': '₁',
  '2': '₂',
  '3': '₃',
  '4': '₄',
  '5': '₅',
  '6': '₆',
  '7': '₇',
  '8': '₈',
  '9': '₉',
}
superscript_replacements = {
  '0': '⁰',
  '1': '¹',
  '2': '²',
  '3': '³',
  '4': '⁴',
  '5': '⁵',
  '6': '⁶',
  '7': '⁷',
  '8': '⁸',
  '9': '⁹',
  '+': '⁺',
  '-': '⁻',
  '(': '⁽',
  ')': '⁾',
  'a': 'ᵃ',
  'b': 'ᵇ',
  'c': 'ᶜ',
  'd': 'ᵈ',
  'e': 'ᵉ',
  'f': 'ᶠ',
  'g': 'ᵍ',
  'h': 'ʰ',
  'i': 'ⁱ',
  'j': 'ʲ',
  'k': 'ᵏ',
  'l': 'ˡ',
  'm': 'ᵐ',
  'n': 'ⁿ',
  'o': 'ᵒ',
  'p': 'ᵖ',
  'r': 'ʳ',
  's': 'ˢ',
  't': 'ᵗ',
  'u': 'ᵘ',
  'v': 'ᵛ',
  'x': 'ˣ',
  'y': 'ʸ',
  'z': 'ᶻ',
  '/': ''
}


def split_text(text):
  words_to_remove = ["", "", ""]
  for word in words_to_remove:
    text = text.replace(word, "")

    # replace subscripts and superscripts in chemical equations
    text = subscript_pattern.sub(
      lambda match: ''.join(
        [subscript_replacements.get(char, char) for char in match.group(1)]),
      text)
    text = superscript_pattern.sub(
      lambda match: ''.join(
        [superscript_replacements.get(char, char) for char in match.group(1)]),
      text)

  words = text.split(' ')
  min_words_first_half = 15
  first_half = ''
  stop_found = False
  for i, word in enumerate(words):
    if i < min_words_first_half:
      first_half += word + ' '
    elif word.endswith('.'):
      first_half += word + ' '
      stop_found = True
      break
    else:
      first_half += word + ' '

  if not stop_found:
    last_period_idx = first_half.rfind('.')
    if last_period_idx > 0:
      first_half = first_half[:last_period_idx + 1]

  second_half = ' '.join(words[len(first_half.split()):])

  # If the first half ends on a word that's also in the second half,
  # move the endpoint of the first half to the previous sentence
  if len(second_half) > 0 and first_half.split()[-1] in second_half.split():
    for i in range(len(first_half.split()) - 2, 0, -1):
      if first_half.split()[i].endswith('.'):
        first_half = ' '.join(words[:i + 1])
        second_half = ' '.join(words[len(first_half.split()):])
        if second_half.startswith(' '):
          second_half = second_half[1:]
        break

  second_half = second_half.replace(
    '\n\n', '\n')  # replace double new lines with single new lines

  return (first_half, second_half)


@dp.message_handler()
async def start_command(message: Message):
  text = message.text.strip()

  words = []  # default value for words
  words_to_remove = ["", "", "word3"]
  for word in words_to_remove:
    text = text.replace(word, "")

  # Check if any word in the dictionary appears in the message
  found_word = False
  for word in dictionary:
    if word.lower() in text.lower():
      found_word = True
      # Replace the entire message with a capitalized version of the message
      text = text.replace(word, word.upper(), 1)
      break

  # replace subscripts and superscripts in chemical equations
    text = subscript_pattern.sub(
      lambda match: ''.join(
        [subscript_replacements.get(char, char) for char in match.group(1)]),
      text)
    text = superscript_pattern.sub(
      lambda match: ''.join(
        [superscript_replacements.get(char, char) for char in match.group(1)]),
      text)

  if 'therefore' in text.lower():
    # Split the input at 'therefore'
    parts = text.lower().split('therefore')
    # Get the first part
    first_part = parts[0].strip()
    # Get the second part
    second_part_sentences = parts[1].split('.')
    first_sentence = second_part_sentences[0].strip() + '.'
    remaining_sentences = '.'.join(second_part_sentences[1:]).strip()
    second_part = first_part + ' ' + remaining_sentences

    # Capitalize the first letter of the first sentence if necessary
    first_sentence = first_sentence.lstrip(',:;./\\').strip()
    first_sentence = first_sentence[0].upper(
    ) + first_sentence[1:] if first_sentence[0].islower() else first_sentence

    # If the first sentence in the second part has less than 10 words, pick the second sentence instead
    second_sentence = second_part_sentences[1].strip() + '.'
    if len(first_sentence.split()) < 10:
      first_half = first_sentence + second_sentence
      second_half = first_part + ' ' + remaining_sentences.replace(
        second_sentence, '').strip()
    else:
      first_half = first_sentence
      second_half = second_part.replace('\n\n', '\n').strip()
  else:
    first_half, second_half = split_text(text)

  # Define the result variable here
  result = ""

  result += f"{first_half}\n\n"
  if second_half:
    result += f"{second_half}\n\n"

  if not found_word and len(words) > 30:
    first_word = list(dictionary.keys())[0]
    result += f"Learn more about {first_word} here: \n {dictionary[first_word]} "
  elif found_word:
    first_word = list(
      filter(lambda w: w.lower() in text.lower(), dictionary.keys()))[0]
    result += f"Learn more about {first_word} here: \n{dictionary[first_word]} "
  else:
    first_word = list(dictionary.keys())[0]
    result += f"Learn more about {first_word} here: \n {dictionary[first_word]} "

  result += "\n\n#SPJ11"
  await message.reply(result)


# Dictionary to store the number of inputs sent by each user
input_count = {}


# Handler function for incoming messages
async def handle_messages(message: Message):
  # Get the user ID of the sender
  user_id = message.from_user.id

  # Increment the input count for this user
  if user_id in input_count:
    input_count[user_id] += 1
  else:
    input_count[user_id] = 1

  # Handle commands
  if message.text == "/start":
    # Send a message to you with the input count data
    data = "\n".join([
      f"{user.first_name} ({user.id}): {count}"
      for user, count in input_count.items()
    ])
    await bot.send_message(chat_id="YOUR_TELEGRAM_ACCOUNT_ID", text=data)

  # Handle other messages
  else:
    # Respond to the message
    response = f"You have sent {input_count[user_id]} inputs."
    await bot.send_message(chat_id=user_id, text=response)
  # User IDs to track


USER_IDS = [1234567890, 2345678901, 3456789012, 4567890123, 5678901234]


# Start the bot and set up the message handler
async def main():
  # Set up the message handler
  dispatcher.register_message_handler(handle_messages)

  # Start the bot
  await bot.start_polling()


# Define dictionary of words and links
dictionary = {
  "words12334": "",
  "probability": "https://brainly.com/question/32117953",
  "proportionality": "https://brainly.com/question/8598338",
  "angle": "https://brainly.com/question/31818999",
  "binomial": "https://brainly.com/question/30339327",
  "statistics": "https://brainly.com/question/30847885",
  "factorial": "https://brainly.com/question/20337219",
  "hypothesis": "https://brainly.com/question/30899146",
  "percentage": "https://brainly.com/question/16797504",
  "percentile": "https://brainly.com/question/1594020",
  "principle": "https://brainly.com/question/31909315",
  "statistical": "https://brainly.com/question/31538429",
  "denominator": "https://brainly.com/question/15007690",
  "triangle": "https://brainly.com/question/2773823",
  "variables": "https://brainly.com/question/31866372",
  "Euler": "https://brainly.com/question/31821033",
  "Divergence": "https://brainly.com/question/10773892",
  "linear": "https://brainly.com/question/31510530",
  "interest": "https://brainly.com/question/25044481",
  "compound": "https://brainly.com/question/29331176",
  "integrate": "https://brainly.com/question/30217024",
  "equivalence": "https://brainly.com/question/14307463",
  "Dividend": "https://brainly.com/question/16314350",
  "arithmetic": "https://brainly.com/question/16415816",
  "orthonormal": "https://brainly.com/question/31992754",
  "deviation": "https://brainly.com/question/23907081",
  "regression": "https://brainly.com/question/30738733",
  "Bayes": "https://brainly.com/question/30762987",
  "marginal": "https://brainly.com/question/28856941",
  "Laplace": "https://brainly.com/question/31040475",
  "geometric": "https://brainly.com/question/13008517",
  "differentiation": "https://brainly.com/question/24062595",
  "differentiation": "https://brainly.com/question/24062595",
  "theory": "https://brainly.com/question/28035099",
  "dice": "https://brainly.com/question/28198792",
  "function": "https://brainly.com/question/30721594",
  "logarithmic": "https://brainly.com/question/30226560",
  "vector": "https://brainly.com/question/24256726",
  "scalar": "https://brainly.com/question/20365259",
  "Derivative": "https://brainly.com/question/29020856",
  "integral ": "https://brainly.com/question/31059545",
  "matrix ": "https://brainly.com/question/29132693",
  "annual": "https://brainly.com/question/24786731",
  "magnitude ": " https://brainly.com/question/31616548",
  "slope ": "https://brainly.com/question/3605446",
  "proportion ": "https://brainly.com/question/31548894",
  "invertible ": "  https://brainly.com/question/31479702",
  "integers": "https://brainly.com/question/490943",
  "propositional ": "https://brainly.com/question/30895311",
  "subsets ":"https://brainly.com/question/31739353",
  "polynomial ": "https://brainly.com/question/11536910",
  "coordinates":"https://brainly.com/question/22261383",
  "convergent":"https://brainly.com/question/30326862",
  "integration":"https://brainly.com/question/31744185",
  "infinity": "https://brainly.com/question/22443880",
  "difference":"https://brainly.com/question/17377980",
  "yield":"https://brainly.com/question/11423563",
  "equation":"https://brainly.com/question/29538993",
  "expression":"https://brainly.com/question/31910577",
  "population":"https://brainly.com/question/30935898",
   "percent":"https://brainly.com/question/31323953",
  "factors":"https://brainly.com/question/29128446",

}

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=False)
