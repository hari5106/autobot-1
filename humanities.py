import logging
import re
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

allowed_user_ids = [
  "588065647", "733616929", "1856775946", "1107151415", "1357510282",
  "1232162200", "1026711051","1671437578"
]

bot = Bot(token="6272908545:AAFPOMIY7NdbSzKQBiEuQunQdQx7xUkcnJM")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)

superscript_pattern = re.compile(r'\^(\((?:[^()]+|)*\)|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|[a-z]+|\w+\((?:[^(),]*,?)*\))')
subscript_pattern = re.compile(r'_(.*?)($|\s|[^0-9a-zA-Z])')

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
  words_to_remove = [
    "the correct answer is",
    "correct",
    "answer",
    "option",
    "options",
    "google",
    "facebook",
    "insta",
    "sex",
    "instagram",
    "whatsapp",
    "what'sapp",
    "messenger",
    "twitter",
    "snap",
    "chat",
    "Explanation:",
    "Main  (30 words):",
    "Main answer:",
    "Explanation",
  ]

  for word in words_to_remove:
    text = text.replace(word, "")

    
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


  if len(second_half) > 0 and first_half.split()[-1] in second_half.split():
    for i in range(len(first_half.split()) - 2, 0, -1):
      if first_half.split()[i].endswith('.'):
        first_half = ' '.join(words[:i + 1])
        second_half = ' '.join(words[len(first_half.split()):])
        if second_half.startswith(' '):
          second_half = second_half[1:]
        break

  second_half = second_half.replace('\n\n', '\n')
  return (first_half, second_half)


@dp.message_handler()
async def start_command(message: Message):
  user_id = str(message.from_user.id)
  if user_id in allowed_user_ids:
    text = message.text.strip()
  else:
    await message.reply(
      "Sorry, you are not authorized to use this bot. Please contact @SGxheidinaruto."
    )

  words = []  # default value for words
  words_to_remove = [
    "The correct answer is", "option", "google", "facebook", "insta",
    "instagram", "whatsapp", "what'sapp", "messenger", "twitter", "snap",
    "chat", "sex", "fuck", "Explanation:"
  ]

  for word in words_to_remove:
    text = text.replace(word, "")

  found_word = False
  for word in dictionary:
    if word.lower() in text.lower():
      found_word = True
      text = text.replace(word, word.upper(), 1)
      break

    text = subscript_pattern.sub(
      lambda match: ''.join(
        [subscript_replacements.get(char, char) for char in match.group(1)]),
      text)
    text = superscript_pattern.sub(
      lambda match: ''.join(
        [superscript_replacements.get(char, char) for char in match.group(1)]),
      text)

  if 'therefore' in text.lower():

    parts = text.lower().split('therefore')

    first_part = parts[0].strip()

    second_part_sentences = parts[1].split('.')
    first_sentence = second_part_sentences[0].strip() + '.'
    remaining_sentences = '.'.join(second_part_sentences[1:]).strip()
    second_part = first_part + ' ' + remaining_sentences

    first_sentence = first_sentence.lstrip(',:;./\\').strip()
    first_sentence = first_sentence[0].upper(
    ) + first_sentence[1:] if first_sentence[0].islower() else first_sentence

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


dictionary = {
  "words12334": "",
  "aesthetics": "https://brainly.com/question/28660977",
  "anthropology": "https://brainly.com/question/31198095",
  "archetype": "https://brainly.com/question/31609215",
  "artifice": "https://brainly.com/question/24569013",
  "authenticity": "https://brainly.com/question/3521390",
  "baroque": "https://brainly.com/question/11325613",
  "capitalism": "https://brainly.com/question/29946431",
  "cartography": "https://brainly.com/question/28501350",
  "civilization": "https://brainly.com/question/12207844",
  "communitarianism": "https://brainly.com/question/14517246",
  "commodification": "https://brainly.com/question/31323321",
  "conformity": "https://brainly.com/question/9255382",
  "consciousness": "https://brainly.com/question/2274876",
  "consumerism": "https://brainly.com/question/29795532",
  "contingency": "https://brainly.com/question/31462453",
  "cosmopolitanism": "https://brainly.com/question/10201400",
  "creativity": "https://brainly.com/question/6116336",
  "critical theory": "https://brainly.com/question/31018837",
  "decolonization": "https://brainly.com/question/30642253",
  "democracy": "https://brainly.com/question/30466950",
  "diaspora": "https://brainly.com/question/581413",
  "diversity": "https://brainly.com/question/9279105",
  "eclecticism": "https://brainly.com/question/30052411",
  "ecological": "https://brainly.com/question/30034964",
  "economy": "https://brainly.com/question/30131108",
  "egalitarianism": "https://brainly.com/question/200458",
  "emancipation": "https://brainly.com/question/28820259",
  "empathy": "https://brainly.com/question/28258799",
  "enlightenment": "https://brainly.com/question/1600484",
  "business": "https://brainly.com/question/15826604",
  "epistemology": "https://brainly.com/question/31886604",
  "ethics": "https://brainly.com/question/26273329",
  "eurocentrism": "https://brainly.com/question/17270524",
  "existentialism": "https://brainly.com/question/30396041",
  "feminism": "https://brainly.com/question/30375867",
  "folklore": "https://brainly.com/question/14051959",
  "freedom": "https://brainly.com/question/7723076",
  "gender": "https://brainly.com/question/30730615",
  "globalization": "https://brainly.com/question/30331929",
  "hegemony": "https://brainly.com/question/29999497",
  "hermeneutics": "https://brainly.com/question/30418941",
  "historiography": "https://brainly.com/question/12022023",
  "humanism": "https://brainly.com/question/11655619",
  "ideology": "https://brainly.com/question/29759131",
  "imperialism": "https://brainly.com/question/30210572",
  "individualism": "https://brainly.com/question/15378488",
  "inequality": "https://brainly.com/question/27679119",
  "intertextuality": "https://brainly.com/question/25620548",
  "intersectionality": "https://brainly.com/question/30408006",
  "justice": "https://brainly.com/question/14830074",
  "liberalism": "https://brainly.com/question/31428681",
  "literature": "https://brainly.com/question/13098221",
  "marxism": "https://brainly.com/question/2095310",
  "materialism": "https://brainly.com/question/30627081",
  "modernity": "https://brainly.com/question/15357521",
  "multiculturalism": "https://brainly.com/question/28524624",
  "nationalism": "https://brainly.com/question/1018147",
  "neo-colonialism": "https://brainly.com/question/14535583",
  "nihilism": "https://brainly.com/question/30044377",
  "nomadism": "https://brainly.com/question/30418258",
  "norms": "https://brainly.com/question/29742768",
  "objectivity": "https://brainly.com/question/31838853",
  "orientalism": "https://brainly.com/question/23421842",
  "paradigm": "https://brainly.com/question/7463505",
  "paradox": "https://brainly.com/question/29973360",
  "phenomenology": "https://brainly.com/question/31894552",
  "philosophy": "https://brainly.com/question/28428294",
  "pluralism": "https://brainly.com/question/8737263",
  "political economy": "https://brainly.com/question/29553619",
  "postcolonialism": "https://brainly.com/question/29566396",
  "prejudice": "https://brainly.com/question/31431721",
  "postcolonialism": "https://brainly.com/question/29566396",
  "progress": "https://brainly.com/question/22899420",
  "psychology": "https://brainly.com/question/28449448",
  "queer theory": "https://brainly.com/question/30763378",
  "rationalism": "https://brainly.com/question/29493191",
  "realism": "https://brainly.com/question/30639821",
  "relativism": "https://brainly.com/question/29765134",
  "religion": "https://brainly.com/question/30228180",
  "revolution": "https://brainly.com/question/29158976",
  "rhetoric": "https://brainly.com/question/29675895",
  "secularism": "https://brainly.com/question/3098569",
  "seculat": "https://brainly.com/question/3098569",
  "semiotics": "https://brainly.com/question/21780820",
  "sexuality": "https://brainly.com/question/31519720",
  "social contract": "https://brainly.com/question/18597938",
  "socialism": "https://brainly.com/question/28218484",
  "society": "https://brainly.com/question/12006768",
  "sovereignty": "https://brainly.com/question/3135619",
  "structuralism": "https://brainly.com/question/27951722",
  "subjectivity": "https://brainly.com/question/30888634",
  "subaltern": "https://brainly.com/question/28518334",
  "surrealism": "https://brainly.com/question/30390299",
  "symbolism": "https://brainly.com/question/29753290",
  "syncretism": "https://brainly.com/question/29545868",
  "technology": "https://brainly.com/question/28288301",
  "temporality": "https://brainly.com/question/30257791",
  "textuality": "https://brainly.com/question/31065627",
  "theology": "https://brainly.com/question/30175105",
  "third World": "https://brainly.com/question/7595066",
  "totalitarianism": "https://brainly.com/question/14502003",
  "transgression": "https://brainly.com/question/31217779",
  "violence": "https://brainly.com/question/30204572",
  "virtue": "https://brainly.com/question/30189081",
  "visual culture": "https://brainly.com/question/30780484",
  "worldwar1": "https://brainly.com/question/11375126",
  "westernization": "https://brainly.com/question/29766824",
  "world system": "https://brainly.com/question/30765218",
  "humanism": "https://brainly.com/question/11655619",
  "racialism": "https://brainly.com/question/20726387",
  "traditionalism": "https://brainly.com/question/9013575",
  "materialism": "https://brainly.com/question/30627081",
  "bond": "https://brainly.com/question/31994049",
  "purchase": "https://brainly.com/question/31035675",
  "vendor": "https://brainly.com/question/28168571",
  "Income": "https://brainly.com/question/14732695",
  "budget": "https://brainly.com/question/31952035",
  "discount": "https://brainly.com/question/31870453",
  "stock": "https://brainly.com/question/31940696",
  "revenue": "https://brainly.com/question/14952769",
  "Customer": "https://brainly.com/question/31192428",
  "Centralized": "https://brainly.com/question/30009512",
  "suppliers": "https://brainly.com/question/9379790",
  "investing": "https://brainly.com/question/31781807",
  "investment": "https://brainly.com/question/15105766",
  "margin": "https://brainly.com/question/28481234",
  "consumer": "https://brainly.com/question/30132393",
  "customers": "https://brainly.com/question/31192428",
  "federal": "https://brainly.com/question/1951874",
  "financial": "https://brainly.com/question/28319639",
  "interest": "https://brainly.com/question/30393144",
  "expense": "https://brainly.com/question/29850561",
  "Company": "https://brainly.com/question/30532251",
  "volatility": "https://brainly.com/question/28557571",
  "liabilities": "https://brainly.com/question/30805836",
  "estate": "https://brainly.com/question/29649911",
  "depreciation": "https://brainly.com/question/30531944",
  "taxable": "https://brainly.com/question/30781403",
  "annual": "https://brainly.com/question/29554641",
  "corporation": "https://brainly.com/question/30029715",
  "manufacturing": "https://brainly.com/question/13439850",
  "heuristic": "https://brainly.com/question/29793101",
  "share": "https://brainly.com/question/30324507",
  "volunteering": "https://brainly.com/question/30143815",
  "service": "https://brainly.com/question/30418810",
  "maintenance": "https://brainly.com/question/29608628",
  "vamortization": "https://brainly.com/question/29807644",
  "ambiguous": "https://brainly.com/question/31273453",
  "evaluate": "https://brainly.com/question/20067491",
  "geopolitical": "https://brainly.com/question/28523582",
  "interchangeably": "https://brainly.com/question/2141502",
  "stakeholders": "https://brainly.com/question/30241824",
  "merchandise": "https://brainly.com/question/30631030",
  "Demonstrated": "https://brainly.com/question/15070998",
  "frameworks": "https://brainly.com/question/29584238",
  "willingness": "https://brainly.com/question/30461541",
  "licensees": "https://brainly.com/question/29804028",
  "enthusiastic": "https://brainly.com/question/28286881",
  "effectiveness": "https://brainly.com/question/30694590",
  "transportation": "https://brainly.com/question/29851765",
  "organizations": "https://brainly.com/question/16296324",
  "independence": "https://brainly.com/question/27765350",
  "organisms": "https://brainly.com/question/12825206",
  "mortgage": "https://brainly.com/question/31751568",
  "maturity": "https://brainly.com/question/1885754",
  "probabilities": "https://brainly.com/question/29381779",
  "sternoclavicular": "https://brainly.com/question/31541638",
  "philosophers": "https://brainly.com/question/715989",
  "recognition": "https://brainly.com/question/30159425",
  "involvement": "https://brainly.com/question/22437948",
  "Committee": "https://brainly.com/question/31624606",
  "policy": "https://brainly.com/question/13036064",
  "isolationist": "https://brainly.com/question/30276777",
  "prostitution": "https://brainly.com/question/3925621",
  "municipalities": "https://brainly.com/question/29240097",
  "municipalities": "https://brainly.com/question/29240097",
  "legalize": "https://brainly.com/question/31302898",
  "advertisement": "https://brainly.com/question/28940221",
  "interactions": "https://brainly.com/question/30670021",
  "tailored": "https://brainly.com/question/30337491",
  "constituencies": "https://brainly.com/question/29442621",
  "presidency": "https://brainly.com/question/497462",
  "leadership": "https://brainly.com/question/32010814",
  "administration": "https://brainly.com/question/31667243",
  "vice president": "https://brainly.com/question/18882530",
  "resignation": "https://brainly.com/question/28882578",
  "endorsements": "https://brainly.com/question/30417343",
  "advocating": "https://brainly.com/question/31767864",
  "Counsel": "https://brainly.com/question/30419076",
  "inability": "https://brainly.com/question/29650065",
  "advisor": "https://brainly.com/question/30639900",
  "facilitate": "https://brainly.com/question/31686548",
  "enhance": "https://brainly.com/question/29354634",
  "decisions": "https://brainly.com/question/29104188",
  "decisions": "https://brainly.com/question/29104188",
  "containers": "https://brainly.com/question/28465698",
  "Self-Reference Criterion": "https://brainly.com/question/31680081",
  "therapists": "https://brainly.com/question/9360511",
  "occupational": "https://brainly.com/question/28191849",
  "frustration": "https://brainly.com/question/28315544",
  "controversial": "https://brainly.com/question/28347863",
  "Lobbyists": "https://brainly.com/question/509906",
  "mobilization": "https://brainly.com/question/31610096",
  "Future Fear": "https://brainly.com/question/30136721",
  "amygdala": "https://brainly.com/question/28206728",
  "generalizability": "https://brainly.com/question/30746580",
  "discrepancy": "https://brainly.com/question/31669142",
  "fairness": "https://brainly.com/question/30396040",
  "Demonstration": "https://brainly.com/question/29361957",
  "revolutionized": "https://brainly.com/question/19786099",
  "Adolescents": "https://brainly.com/question/9506316",
  "credibility": "https://brainly.com/question/9783067",
  "credibility": "https://brainly.com/question/9783067",
  "anxiety": "https://brainly.com/question/30792789",
  "Depression": "https://brainly.com/question/30168903",
  "Preconceived": "https://brainly.com/question/31451073",
  "anthropologists": "https://brainly.com/question/30359602",
  "enterprises": "https://brainly.com/question/20782413",
  "Exogenous": "https://brainly.com/question/31680552",
  "persuasive": "https://brainly.com/question/30001679",
  "dihydrotestosterone": "https://brainly.com/question/31680565",
  "Republicans": "https://brainly.com/question/2605617",
  "regression": "https://brainly.com/question/28178214",
  "intersectionality": "https://brainly.com/question/30408006",
  "destruction": "https://brainly.com/question/1165953",
  "igneous": "https://brainly.com/question/31710126",
  "demonstrating": "https://brainly.com/question/29361957",
  "courtroom": "https://brainly.com/question/30364730",
  "insurance": "https://brainly.com/question/989103",
  "vulnerability": "https://brainly.com/question/30904640",
  "predicted": "https://brainly.com/question/27912663",
  "promoter": "https://brainly.com/question/5458968",
  "manipulation": "https://brainly.com/question/28459068",
  "magnitude": "https://brainly.com/question/27762393",
  "historic": "https://brainly.com/question/13436538",
  "urbanization": "https://brainly.com/question/29987047",
  "interaction": "https://brainly.com/question/31168969",
  "economic ": "https://brainly.com/question/14355320",
  "sovereignty": "https://brainly.com/question/3135619",
  "Confederation": "https://brainly.com/question/15207725",
  "republicanism": "https://brainly.com/question/2605617",
  "budgeting": "https://brainly.com/question/31952035",
  "maturation": "https://brainly.com/question/31553347",
  "psychological": "https://brainly.com/question/30399052",
  "pollution": "https://brainly.com/question/30324322",
  "collaboration": "https://brainly.com/question/30410196",
  "physiological": "https://brainly.com/question/9311395",
  "minerals": "https://brainly.com/question/15213861",
  "population": "https://brainly.com/question/31599868",
  "psychological": "https://brainly.com/question/30399052",
}

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=False)
