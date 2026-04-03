#!/usr/bin/env python3
"""
🤖 TopUp Zone's Games Bot
Yangiliklar:
  - SAT savollar (ball diapazonini foydalanuvchi tanlaydi)
  - Yangi foydalanuvchi -> ownerga xabar
  - Owner: barcha profillarni ko'rish
  - Donat so'rasa -> @Nobody_ff6_bot
  - O'yinlar ro'yxati saytdagi bilan sinxron

O'RNATISH:
  pip install pyTelegramBotAPI
"""

import os, time, threading, random, json
from datetime import datetime
import telebot
from telebot import types

# ═══════════════════════════════════════════════
#  SOZLAMALAR
# ═══════════════════════════════════════════════
TELEGRAM_TOKEN    = "8613062943:AAFnkw-Fp5ru0OvNc-3sNf5wQDzhtP-KxQ8"
OWNER_ID          = 7362457858
SITE_URL          = "https://sakura-on.github.io/TopUp-Zone-s-Games/"  # <- O'zgartiring!
DONATE_BOT        = "@Nobody_ff6_bot"

bot       = telebot.TeleBot(TELEGRAM_TOKEN)
user_data : dict = {}

# ═══════════════════════════════════════════════
#  O'YINLAR RO'YXATI
# ═══════════════════════════════════════════════
BUILTIN_GAMES = [
    ("snake",        "🐍 Snake Classic",   "Ilon o'yini — ovqat ye, o'sib bor"),
    ("tetris",       "🟦 Tetris",          "Bloklarni joylashtir"),
    ("pong",         "🏓 Pong Duel",       "AI ga qarshi raketa o'yni"),
    ("breakout",     "🧱 Breakout",        "G'ishtlarni sindir"),
    ("flappy",       "🐦 Flappy Bird",     "Trubalardan o'tkazib ber"),
    ("minesweeper",  "💣 Minesweeper",     "Minalarni top"),
    ("aimtrainer",   "🎯 Aim Trainer",     "Reaksiyangizni sinab ko'ring"),
    ("puzzle2048",   "🔢 2048 Puzzle",     "Raqamlarni birlashtir"),
    ("tictactoe",    "❌ Tic Tac Toe",     "AI ga qarshi X-O o'yni"),
    ("spaceshooter", "🚀 Space Shooter",   "Kosmosda dushmanlarni yo'q qil"),
    ("dodge",        "⚡ Dodge Master",    "To'siqlardan qoching"),
]

# ═══════════════════════════════════════════════
#  SAT SAVOLLAR BANKI
# ═══════════════════════════════════════════════
SAT_QUESTIONS = {
    "math": [
        ("If 3x + 7 = 22, what is the value of x?",
         "3", "5", "6", "7", "B", 400),
        ("What is the slope of the line passing through (2, 3) and (4, 7)?",
         "1", "2", "3", "4", "B", 500),
        ("If f(x) = 2x2 - 3x + 1, what is f(3)?",
         "8", "9", "10", "12", "C", 550),
        ("A circle has area 49pi. What is its circumference?",
         "7pi", "14pi", "21pi", "28pi", "B", 500),
        ("If |2x - 4| = 10, what are the possible values of x?",
         "x=7 or x=-3", "x=5 or x=-5", "x=7 or x=3", "x=3 or x=-7", "A", 600),
        ("What is 30% of 250?",
         "60", "65", "75", "80", "C", 400),
        ("Solve: 2(x-3) + 4 = 3(x+1) - 5",
         "x = -4", "x = 4", "x = -2", "x = 2", "C", 550),
        ("In a right triangle, if one leg is 5 and hypotenuse is 13, the other leg is:",
         "8", "10", "11", "12", "D", 500),
        ("What is the value of sqrt(144) + sqrt(25)?",
         "13", "17", "19", "21", "B", 400),
        ("If the mean of 5, 8, 12, x is 9, what is x?",
         "9", "10", "11", "13", "C", 500),
        ("A function g(x) = x2 - 4x + 4. For what value of x is g(x) = 0?",
         "x = -2", "x = 2", "x = 4", "x = 0", "B", 600),
        ("If 4^x = 64, what is x?",
         "2", "3", "4", "6", "B", 550),
        ("The sum of two consecutive even integers is 46. What is the smaller?",
         "20", "22", "24", "26", "B", 500),
        ("A train travels 240 miles in 4 hours. What is its speed in mph?",
         "50", "55", "60", "65", "C", 400),
        ("Simplify: (x2 - 9)/(x - 3)",
         "x - 3", "x + 3", "x2 - 3", "x + 9", "B", 600),
        ("If sin(theta) = 3/5, what is cos(theta) in first quadrant?",
         "3/4", "4/5", "5/3", "4/3", "B", 650),
        ("How many solutions does 2x2 + 3x + 5 = 0 have?",
         "0", "1", "2", "Infinitely many", "A", 700),
        ("A rectangle has perimeter 40 and length 12. What is its area?",
         "88", "96", "100", "112", "B", 500),
        ("What is the y-intercept of y = 3x - 7?",
         "(0, 3)", "(0, -7)", "(7, 0)", "(-7, 0)", "B", 450),
        ("If 5! = 120, what is 6!/5!?",
         "5", "6", "30", "720", "B", 600),
    ],
    "reading": [
        ("The word 'ephemeral' most nearly means:",
         "Eternal", "Short-lived", "Mysterious", "Vibrant", "B", 500),
        ("Which literary device is used in 'The wind whispered secrets'?",
         "Simile", "Metaphor", "Personification", "Alliteration", "C", 450),
        ("What is the main purpose of a thesis statement?",
         "To summarize the conclusion", "To state the main argument",
         "To list evidence", "To introduce the topic broadly", "B", 400),
        ("The prefix 'anti-' means:",
         "Before", "Against", "After", "Around", "B", 400),
        ("'Benevolent' most nearly means:",
         "Harmful", "Neutral", "Kind", "Angry", "C", 500),
        ("An 'inference' is best described as:",
         "A direct quote from the text", "A conclusion drawn from evidence",
         "A summary of the passage", "An author's opinion", "B", 550),
        ("The word 'ambiguous' means:",
         "Clear and certain", "Open to multiple interpretations",
         "Very important", "Completely false", "B", 550),
        ("Which sentence uses 'incredulous' correctly?",
         "She was incredulous about the sunny weather.",
         "He looked incredulous at the impossible claim.",
         "The incredulous story was easy to believe.",
         "She told an incredulous joke.", "B", 600),
        ("'Pragmatic' means:",
         "Idealistic", "Practical", "Emotional", "Theoretical", "B", 500),
        ("The author's 'tone' refers to:",
         "The topic of the passage", "The author's attitude or feeling",
         "The main argument", "The conclusion", "B", 450),
        ("What does 'corroborate' mean?",
         "To contradict", "To ignore", "To confirm or support", "To disprove", "C", 600),
        ("'Ubiquitous' most nearly means:",
         "Rare", "Present everywhere", "Invisible", "Dangerous", "B", 600),
        ("Which is an example of 'irony'?",
         "A firefighter afraid of heights", "A tall mountain",
         "A fast runner", "A bright sun", "A", 500),
        ("The prefix 'mal-' means:",
         "Good", "Bad", "Many", "One", "B", 450),
        ("'Loquacious' means:",
         "Quiet", "Talkative", "Intelligent", "Aggressive", "B", 550),
    ],
    "writing": [
        ("Which sentence is grammatically correct?",
         "Neither of the boys have done their homework.",
         "Neither of the boys has done his homework.",
         "Neither of the boy have done his homework.",
         "Neither of boys has done their homework.", "B", 500),
        ("Choose the correct word: 'The team ___ celebrating their victory.'",
         "is", "are", "were", "been", "A", 450),
        ("Identify the error: 'Between you and I, this is wrong.'",
         "Between", "you", "I", "wrong", "C", 550),
        ("Which correctly uses a semicolon?",
         "I went to the store; and bought milk.",
         "I went to the store; I bought milk.",
         "I went; to the store and bought milk.",
         "I; went to the store and bought milk.", "B", 600),
        ("'Affect' vs 'Effect': 'The medicine had a positive ___ on his health.'",
         "affect", "effect", "effecting", "affecting", "B", 500),
        ("Which sentence avoids a dangling modifier?",
         "Running quickly, the bus was missed.",
         "Running quickly, she missed the bus.",
         "The bus was missed, running quickly.",
         "She was running, the bus quickly missed.", "B", 550),
        ("Choose the correct form: 'If I ___ you, I would apologize.'",
         "am", "was", "were", "be", "C", 600),
        ("Which word correctly completes: 'It is ___ turn to speak'?",
         "your", "you're", "ur", "youre", "A", 400),
        ("Identify the passive voice:",
         "The chef cooked the meal.",
         "The meal was cooked by the chef.",
         "She enjoys cooking meals.",
         "They cook every Sunday.", "B", 500),
        ("Which sentence is most concise?",
         "Due to the fact that it was raining, we stayed inside.",
         "Because it was raining, we stayed inside.",
         "We stayed inside on account of the rain falling.",
         "The reason we stayed inside was that it rained.", "B", 550),
    ]
}

# ═══════════════════════════════════════════════
#  TILLAR
# ═══════════════════════════════════════════════
T = {
    "uz": {
        "welcome"    : "🎮 *TopUp Zone's Games'ga xush kelibsiz, {name}!*\n\n🕹 *{game_count} ta o'yin* sizni kutmoqda!\n\nPastdagi tugmani bosib o'ynang yoki /help yozing 👇",
        "play"       : "🕹 O'yinlarni ochish",
        "sat"        : "📚 SAT Savollar",
        "stats"      : "📊 Statistika",
        "help"       : "❓ Yordam",
        "lang"       : "🌍 Til",
        "stats_text" : "📊 *Sizning statistikangiz*\n\n🎮 Sessiyalar: {sess}\n📚 SAT testlar: {sat}\n📅 Qo'shilgan: {date}",
        "help_text"  : "❓ *Yordam — TopUp Zone's Games Bot*\n\n🕹 /play — O'yinlarni ochish\n📚 /sat — SAT savollar\n📊 /stats — Statistikangiz\n🌍 /lang — Til o'zgartirish\n🎮 /games — O'yinlar ro'yxati\n🏠 /menu — Asosiy menyu\n\n*O'yinlar:* Snake · Tetris · Pong · Breakout\nFlappy Bird · Minesweeper · Aim Trainer · 2048\nTic Tac Toe · Space Shooter · Dodge Master",
        "choose_lang": "🌍 Tilni tanlang:",
        "lang_ok"    : "✅ Til o'zgartirildi: O'zbek",
        "back"       : "⬅️ Orqaga",
        "sat_choose" : "📚 *SAT Savollar*\n\nQaysi ball diapazonida savollar olishni xohlaysiz?",
        "sat_section": "📖 Qaysi bo'limdan savol olishni xohlaysiz?",
        "donate_reply": "💰 *Donat va to'lov xizmatlar uchun:*\n\n👉 @Nobody_ff6_bot botiga murojaat qiling!\n\nU yerda barcha to'lov va donat xizmatlari mavjud ✅",
    },
    "ru": {
        "welcome"    : "🎮 *Добро пожаловать в TopUp Zone's Games, {name}!*\n\n🕹 *{game_count} игр* ждут вас!\n\nНажмите кнопку ниже! 👇",
        "play"       : "🕹 Открыть игры",
        "sat"        : "📚 SAT Вопросы",
        "stats"      : "📊 Статистика",
        "help"       : "❓ Помощь",
        "lang"       : "🌍 Язык",
        "stats_text" : "📊 *Ваша статистика*\n\n🎮 Сессий: {sess}\n📚 SAT тестов: {sat}\n📅 Дата: {date}",
        "help_text"  : "❓ *Помощь — TopUp Zone's Games Bot*\n\n🕹 /play — Открыть игры\n📚 /sat — SAT вопросы\n📊 /stats — Статистика\n🌍 /lang — Сменить язык\n🎮 /games — Список игр\n🏠 /menu — Главное меню",
        "choose_lang": "🌍 Выберите язык:",
        "lang_ok"    : "✅ Язык изменён: Русский",
        "back"       : "⬅️ Назад",
        "sat_choose" : "📚 *SAT Вопросы*\n\nВыберите диапазон баллов:",
        "sat_section": "📖 Выберите раздел:",
        "donate_reply": "💰 *Для донатов и оплаты:*\n\n👉 Обратитесь к @Nobody_ff6_bot!\n\nТам доступны все платёжные услуги ✅",
    },
    "en": {
        "welcome"    : "🎮 *Welcome to TopUp Zone's Games, {name}!*\n\n🕹 *{game_count} games* await you!\n\nTap the button below! 👇",
        "play"       : "🕹 Open Games",
        "sat"        : "📚 SAT Questions",
        "stats"      : "📊 Statistics",
        "help"       : "❓ Help",
        "lang"       : "🌍 Language",
        "stats_text" : "📊 *Your statistics*\n\n🎮 Sessions: {sess}\n📚 SAT tests: {sat}\n📅 Registered: {date}",
        "help_text"  : "❓ *Help — TopUp Zone's Games Bot*\n\n🕹 /play — Open games\n📚 /sat — SAT questions\n📊 /stats — Statistics\n🌍 /lang — Change language\n🎮 /games — Game list\n🏠 /menu — Main menu",
        "choose_lang": "🌍 Choose language:",
        "lang_ok"    : "✅ Language set: English",
        "back"       : "⬅️ Back",
        "sat_choose" : "📚 *SAT Questions*\n\nChoose your target score range:",
        "sat_section": "📖 Choose a section:",
        "donate_reply": "💰 *For donations and payments:*\n\n👉 Contact @Nobody_ff6_bot!\n\nAll payment services are available there ✅",
    },
}

# ═══════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════
def get_user(uid, name=""):
    if uid not in user_data:
        user_data[uid] = {
            "lang"        : "uz",
            "mode"        : "menu",
            "name"        : name or "O'yinchi",
            "username"    : "",
            "sessions"    : 0,
            "sat_sessions": 0,
            "sat_state"   : None,
            "registered"  : datetime.now().strftime("%d.%m.%Y %H:%M"),
            "banned"      : False,
        }
    return user_data[uid]

def t(uid, key, **kw):
    u    = get_user(uid)
    lang = u.get("lang", "uz")
    text = T.get(lang, T["uz"]).get(key, T["uz"].get(key, key))
    return text.format(**kw) if kw else text

def game_count():
    return len(BUILTIN_GAMES)

def main_kb(uid):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton(t(uid, "play"), web_app=types.WebAppInfo(url=SITE_URL)),
        types.InlineKeyboardButton(t(uid, "sat"),  callback_data="mode_sat"),
    )
    kb.add(
        types.InlineKeyboardButton(t(uid, "stats"), callback_data="mode_stats"),
        types.InlineKeyboardButton(t(uid, "help"),  callback_data="mode_help"),
    )
    kb.add(
        types.InlineKeyboardButton(t(uid, "lang"), callback_data="mode_lang"),
    )
    return kb

def back_kb(uid):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton(t(uid, "back"), callback_data="back_menu"))
    return kb

def lang_kb():
    kb = types.InlineKeyboardMarkup(row_width=3)
    kb.add(
        types.InlineKeyboardButton("🇺🇿 O'zbek",  callback_data="lang_uz"),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
    )
    return kb

def sat_score_kb(uid):
    kb = types.InlineKeyboardMarkup(row_width=2)
    ranges = [
        ("📗 400-600 (Boshlangich)", "sat_range_400"),
        ("📘 600-800 (Orta)",        "sat_range_600"),
        ("📙 800-1000 (Yuqori)",     "sat_range_800"),
        ("📕 1000-1200 (Expert)",    "sat_range_1000"),
        ("🏆 1200-1600 (Elite)",     "sat_range_1200"),
        ("🎲 Aralash",               "sat_range_mix"),
    ]
    for label, cbd in ranges:
        kb.add(types.InlineKeyboardButton(label, callback_data=cbd))
    kb.add(types.InlineKeyboardButton(t(uid, "back"), callback_data="back_menu"))
    return kb

def sat_section_kb(uid, score_range):
    kb = types.InlineKeyboardMarkup(row_width=3)
    kb.add(
        types.InlineKeyboardButton("📐 Math",    callback_data=f"sat_sec_math_{score_range}"),
        types.InlineKeyboardButton("📖 Reading", callback_data=f"sat_sec_reading_{score_range}"),
        types.InlineKeyboardButton("✏️ Writing", callback_data=f"sat_sec_writing_{score_range}"),
    )
    kb.add(types.InlineKeyboardButton("🎲 Aralash", callback_data=f"sat_sec_mix_{score_range}"))
    kb.add(types.InlineKeyboardButton(t(uid, "back"), callback_data="back_menu"))
    return kb

def sat_answer_kb(uid):
    kb = types.InlineKeyboardMarkup(row_width=4)
    kb.add(
        types.InlineKeyboardButton("A", callback_data="sat_ans_A"),
        types.InlineKeyboardButton("B", callback_data="sat_ans_B"),
        types.InlineKeyboardButton("C", callback_data="sat_ans_C"),
        types.InlineKeyboardButton("D", callback_data="sat_ans_D"),
    )
    kb.add(types.InlineKeyboardButton("⏭ Keyingisi", callback_data="sat_next"))
    kb.add(types.InlineKeyboardButton(t(uid, "back"), callback_data="back_menu"))
    return kb

def get_sat_questions(section, score_range):
    pool = []
    if section == "mix":
        for sec in ["math", "reading", "writing"]:
            pool += SAT_QUESTIONS[sec]
    else:
        pool = SAT_QUESTIONS.get(section, SAT_QUESTIONS["math"])

    if score_range == "mix":
        filtered = pool
    else:
        low = int(score_range)
        high = low + 200
        filtered = [q for q in pool if low <= q[6] <= high]
        if not filtered:
            filtered = pool  # fallback

    random.shuffle(filtered)
    return filtered[:10]

def format_sat_question(q_data, num, total):
    q, a, b, c, d, ans, diff = q_data
    return (
        f"📚 *SAT Savol {num}/{total}*\n"
        f"🎯 Qiyinlik darajasi: {diff} ball\n\n"
        f"❓ *{q}*\n\n"
        f"🅐 {a}\n"
        f"🅑 {b}\n"
        f"🅒 {c}\n"
        f"🅓 {d}\n"
    )

# ═══════════════════════════════════════════════
#  DONAT KALIT SO'ZLAR
# ═══════════════════════════════════════════════
DONATE_KEYWORDS = [
    "donat", "donate", "donation", "to'lov", "tolov", "pul", "payment", "pay",
    "pullik", "premium", "subscribe", "obuna", "sotib", "buy", "purchase",
    "card", "karta", "transfer", "send money", "yuborish",
    "оплата", "деньги", "донат", "подписка", "топ-ап", "topup", "top up", "top-up",
]

def check_donate_keywords(text):
    if not text:
        return False
    tl = text.lower()
    return any(kw in tl for kw in DONATE_KEYWORDS)

# ═══════════════════════════════════════════════
#  START / MENU
# ═══════════════════════════════════════════════
@bot.message_handler(commands=["start", "menu"])
def cmd_start(msg):
    uid    = msg.from_user.id
    name   = msg.from_user.first_name or "O'yinchi"
    u      = get_user(uid, name)
    is_new = u["sessions"] == 0
    u["sessions"] += 1
    u["mode"]      = "menu"
    u["name"]      = name
    u["username"]  = msg.from_user.username or ""

    bot.send_message(
        msg.chat.id,
        t(uid, "welcome", name=name, game_count=game_count()),
        parse_mode="Markdown",
        reply_markup=main_kb(uid)
    )

    if is_new:
        try:
            uname_str = f"@{u['username']}" if u["username"] else "(username yoq)"
            bot.send_message(
                OWNER_ID,
                f"*Yangi foydalanuvchi qoshildi!*\n\n"
                f"Ism: `{name}`\n"
                f"Username: {uname_str}\n"
                f"ID: `{uid}`\n"
                f"Vaqt: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                f"Til: {u['lang'].upper()}\n\n"
                f"Jami foydalanuvchilar: `{len(user_data)}`",
                parse_mode="Markdown"
            )
        except Exception:
            pass

@bot.message_handler(commands=["play"])
def cmd_play(msg):
    uid = msg.from_user.id
    kb  = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(t(uid, "play"), web_app=types.WebAppInfo(url=SITE_URL)))
    kb.add(types.InlineKeyboardButton(t(uid, "back"), callback_data="back_menu"))
    bot.send_message(msg.chat.id, "O'yinlarni ochish uchun bosing:", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(commands=["games"])
def cmd_games_list(msg):
    uid   = msg.from_user.id
    lines = [f"{name} — _{desc}_" for _, name, desc in BUILTIN_GAMES]
    bot.send_message(
        msg.chat.id,
        "*O'yinlar ro'yxati:*\n\n" + "\n".join(lines),
        parse_mode="Markdown",
        reply_markup=back_kb(uid)
    )

@bot.message_handler(commands=["sat"])
def cmd_sat(msg):
    uid = msg.from_user.id
    u   = get_user(uid)
    u["mode"] = "sat_choose"
    bot.send_message(msg.chat.id, t(uid, "sat_choose"), parse_mode="Markdown", reply_markup=sat_score_kb(uid))

@bot.message_handler(commands=["stats"])
def cmd_stats(msg):
    uid = msg.from_user.id
    u   = get_user(uid)
    bot.send_message(
        msg.chat.id,
        t(uid, "stats_text",
          sess=u["sessions"],
          sat=u["sat_sessions"], date=u["registered"]),
        parse_mode="Markdown",
        reply_markup=back_kb(uid)
    )

@bot.message_handler(commands=["help"])
def cmd_help(msg):
    uid = msg.from_user.id
    bot.send_message(msg.chat.id, t(uid, "help_text"), parse_mode="Markdown", reply_markup=back_kb(uid))

@bot.message_handler(commands=["lang"])
def cmd_lang(msg):
    uid = msg.from_user.id
    bot.send_message(msg.chat.id, t(uid, "choose_lang"), reply_markup=lang_kb())

# ═══════════════════════════════════════════════
#  CALLBACKS
# ═══════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: True)
def cb(call):
    uid = call.from_user.id
    u   = get_user(uid)
    d   = call.data
    cid = call.message.chat.id
    mid = call.message.message_id
    bot.answer_callback_query(call.id)

    # TIL
    if d.startswith("lang_"):
        lang = d.split("_")[1]
        u["lang"] = lang
        try:
            bot.edit_message_text(T[lang]["lang_ok"], cid, mid)
        except Exception:
            pass
        time.sleep(0.4)
        name = call.from_user.first_name or "O'yinchi"
        bot.send_message(
            cid,
            t(uid, "welcome", name=name, game_count=game_count()),
            parse_mode="Markdown",
            reply_markup=main_kb(uid)
        )

    # ORQAGA
    elif d == "back_menu":
        u["mode"]      = "menu"
        u["sat_state"] = None
        name = call.from_user.first_name or "O'yinchi"
        try:
            bot.edit_message_text(
                t(uid, "welcome", name=name, game_count=game_count()),
                cid, mid, parse_mode="Markdown", reply_markup=main_kb(uid)
            )
        except Exception:
            bot.send_message(
                cid,
                t(uid, "welcome", name=name, game_count=game_count()),
                parse_mode="Markdown", reply_markup=main_kb(uid)
            )

    # SAT CHOOSE
    elif d == "mode_sat":
        u["mode"] = "sat_choose"
        try:
            bot.edit_message_text(t(uid, "sat_choose"), cid, mid, parse_mode="Markdown", reply_markup=sat_score_kb(uid))
        except Exception:
            bot.send_message(cid, t(uid, "sat_choose"), parse_mode="Markdown", reply_markup=sat_score_kb(uid))

    elif d.startswith("sat_range_"):
        score_range          = d.replace("sat_range_", "")
        u["sat_score_range"] = score_range
        try:
            bot.edit_message_text(
                t(uid, "sat_section"), cid, mid,
                parse_mode="Markdown", reply_markup=sat_section_kb(uid, score_range)
            )
        except Exception:
            bot.send_message(
                cid, t(uid, "sat_section"),
                parse_mode="Markdown", reply_markup=sat_section_kb(uid, score_range)
            )

    elif d.startswith("sat_sec_"):
        parts       = d.split("_")       # sat_sec_math_600
        section     = parts[2]
        score_range = parts[3] if len(parts) > 3 else "mix"
        questions   = get_sat_questions(section, score_range)
        u["sat_state"] = {
            "questions"  : questions,
            "current"    : 0,
            "score"      : 0,
            "answered"   : False,
            "section"    : section,
            "score_range": score_range,
        }
        u["mode"] = "sat_playing"
        send_sat_question(cid, uid)

    elif d.startswith("sat_ans_"):
        if u.get("mode") != "sat_playing" or not u.get("sat_state"):
            return
        ss = u["sat_state"]
        if ss["answered"]:
            return
        ss["answered"] = True
        chosen = d.replace("sat_ans_", "")
        q       = ss["questions"][ss["current"]]
        q_text, a, b, c, dopt, ans, diff = q
        opts        = {"A": a, "B": b, "C": c, "D": dopt}
        is_correct  = chosen == ans

        if is_correct:
            ss["score"] += 1
            result_text = f"✅ *Togri!* (+1 ball)\n\n📝 Javob: *{ans}) {opts[ans]}*"
        else:
            result_text = (
                f"❌ *Notogri!*\n\n"
                f"✅ Togri javob: *{ans}) {opts[ans]}*\n"
                f"📝 Siz tanladingiz: {chosen}) {opts.get(chosen, '?')}"
            )

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("⏭ Keyingisi", callback_data="sat_next"))
        kb.add(types.InlineKeyboardButton(t(uid, "back"), callback_data="back_menu"))
        try:
            bot.edit_message_text(
                f"{format_sat_question(q, ss['current']+1, len(ss['questions']))}\n{result_text}",
                cid, mid, parse_mode="Markdown", reply_markup=kb
            )
        except Exception:
            bot.send_message(cid, result_text, parse_mode="Markdown", reply_markup=kb)

    elif d == "sat_next":
        if not u.get("sat_state"):
            return
        ss = u["sat_state"]
        ss["current"]  += 1
        ss["answered"]  = False

        if ss["current"] >= len(ss["questions"]):
            total = len(ss["questions"])
            score = ss["score"]
            u["sat_sessions"] += 1
            pct   = round(score / total * 100)
            medal = "🥇" if pct >= 80 else "🥈" if pct >= 60 else "🥉" if pct >= 40 else "❌"
            msg_text = (
                f"📚 *SAT Test Yakunlandi!*\n\n"
                f"{medal} *Natija: {score}/{total}* ({pct}%)\n\n"
                f"{'Ajoyib natija!' if pct>=80 else 'Yaxshi urindi!' if pct>=60 else 'Koproq mashq kerak!'}\n\n"
                f"Qayta urinib koring yoki boshqa bolim tanlang 👇"
            )
            try:
                bot.edit_message_text(msg_text, cid, mid, parse_mode="Markdown", reply_markup=sat_score_kb(uid))
            except Exception:
                bot.send_message(cid, f"Test tugadi. Natija: {score}/{total}", reply_markup=sat_score_kb(uid))
            u["mode"]      = "sat_choose"
            u["sat_state"] = None
        else:
            send_sat_question(cid, uid, edit_mid=mid)

    # STATS
    elif d == "mode_stats":
        try:
            bot.edit_message_text(
                t(uid, "stats_text",
                  sess=u["sessions"],
                  sat=u["sat_sessions"], date=u["registered"]),
                cid, mid, parse_mode="Markdown", reply_markup=back_kb(uid)
            )
        except Exception:
            pass

    # HELP
    elif d == "mode_help":
        try:
            bot.edit_message_text(t(uid, "help_text"), cid, mid, parse_mode="Markdown", reply_markup=back_kb(uid))
        except Exception:
            pass

    # LANG
    elif d == "mode_lang":
        try:
            bot.edit_message_text(t(uid, "choose_lang"), cid, mid, reply_markup=lang_kb())
        except Exception:
            pass


def send_sat_question(chat_id, uid, edit_mid=None):
    u  = get_user(uid)
    ss = u["sat_state"]
    q  = ss["questions"][ss["current"]]
    text = format_sat_question(q, ss["current"] + 1, len(ss["questions"]))
    kb   = sat_answer_kb(uid)
    if edit_mid:
        try:
            bot.edit_message_text(text, chat_id, edit_mid, parse_mode="Markdown", reply_markup=kb)
            return
        except Exception:
            pass
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=kb)

# ═══════════════════════════════════════════════
#  XABARLAR
# ═══════════════════════════════════════════════
@bot.message_handler(func=lambda m: True, content_types=["text"])
def handle_msg(msg):
    uid  = msg.from_user.id
    u    = get_user(uid)
    text = msg.text or ""

    # Donat
    if check_donate_keywords(text):
        bot.send_message(msg.chat.id, t(uid, "donate_reply"), parse_mode="Markdown")
        return

    # SAT playing
    if u.get("mode") == "sat_playing":
        bot.send_message(msg.chat.id, "📚 Iltimos, A, B, C yoki D tugmasini bosing!")
        return

    # Default
    name = msg.from_user.first_name or "O'yinchi"
    bot.send_message(
        msg.chat.id,
        t(uid, "welcome", name=name, game_count=game_count()),
        parse_mode="Markdown",
        reply_markup=main_kb(uid)
    )

# ═══════════════════════════════════════════════
#  OWNER BUYRUQLAR
# ═══════════════════════════════════════════════
def owner_only(f):
    def wrapper(m):
        if m.from_user.id != OWNER_ID:
            bot.send_message(m.chat.id, "Faqat owner uchun!")
            return
        f(m)
    return wrapper

@bot.message_handler(commands=["owner"])
@owner_only
def cmd_owner(msg):
    bot.send_message(
        msg.chat.id,
        "*OWNER PANEL — TopUp Zone's Games*\n\n"
        "/users — foydalanuvchilar soni\n"
        "/allstats — umumiy statistika\n"
        "/listusers — royxat\n"
        "/profile `<id>` — profil korish\n"
        "/broadcast `<matn>` — hammaga xabar\n"
        "/ban `<id>` — bloklash\n"
        "/unban `<id>` — blokdan chiqarish\n"
        "/seturl `<url>` — sayt URL ozgartirish\n"
        "/botinfo — bot malumoti",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["users"])
@owner_only
def cmd_users(msg):
    bot.send_message(msg.chat.id, f"Jami: *{len(user_data)}* ta foydalanuvchi", parse_mode="Markdown")

@bot.message_handler(commands=["allstats"])
@owner_only
def cmd_allstats(msg):
    total_s   = sum(u.get("sessions", 0)     for u in user_data.values())
    total_sat = sum(u.get("sat_sessions", 0) for u in user_data.values())
    langs     = {}
    for u in user_data.values():
        l = u.get("lang", "uz"); langs[l] = langs.get(l, 0) + 1
    banned = sum(1 for u in user_data.values() if u.get("banned"))
    bot.send_message(
        msg.chat.id,
        f"*UMUMIY STATISTIKA*\n\n"
        f"Foydalanuvchilar: `{len(user_data)}`\n"
        f"Bloklangan: `{banned}`\n"
        f"Jami sessiyalar: `{total_s}`\n"
        f"SAT testlar: `{total_sat}`\n\n"
        f"Tillar:\n"
        f"  UZ: {langs.get('uz',0)} | RU: {langs.get('ru',0)} | EN: {langs.get('en',0)}",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["listusers"])
@owner_only
def cmd_listusers(msg):
    if not user_data:
        bot.send_message(msg.chat.id, "Bosh.")
        return
    items  = list(user_data.items())[:60]
    chunks = [items[i:i+20] for i in range(0, len(items), 20)]
    for chunk in chunks:
        lines = []
        for uid, u in chunk:
            b  = "X" if u.get("banned") else "OK"
            un = f"@{u.get('username','')}" if u.get("username") else ""
            lines.append(f"[{b}] `{uid}` {u.get('name','?')[:12]} {un} S:{u.get('sessions',0)}")
        bot.send_message(msg.chat.id, "*Foydalanuvchilar:*\n\n" + "\n".join(lines), parse_mode="Markdown")
        time.sleep(0.3)

@bot.message_handler(commands=["profile"])
@owner_only
def cmd_profile(msg):
    parts = msg.text.split()
    if len(parts) < 2:
        bot.send_message(msg.chat.id, "/profile <id>")
        return
    try:
        uid = int(parts[1])
        u   = user_data.get(uid)
        if not u:
            bot.send_message(msg.chat.id, f"`{uid}` topilmadi.")
            return
        un  = f"@{u.get('username','')}" if u.get("username") else "yoq"
        ban = "Bloklangan" if u.get("banned") else "Faol"
        bot.send_message(
            msg.chat.id,
            f"*Profil — {u.get('name','?')}*\n\n"
            f"ID: `{uid}`\n"
            f"Username: {un}\n"
            f"Til: {u.get('lang','?').upper()}\n"
            f"Qoshilgan: {u.get('registered','?')}\n"
            f"Status: {ban}\n"
            f"Sessiyalar: `{u.get('sessions',0)}`\n"
            f"SAT testlar: `{u.get('sat_sessions',0)}`",
            parse_mode="Markdown"
        )
    except ValueError:
        bot.send_message(msg.chat.id, "Notogri ID")

@bot.message_handler(commands=["broadcast"])
@owner_only
def cmd_broadcast(msg):
    parts = msg.text.split(" ", 1)
    if len(parts) < 2:
        bot.send_message(msg.chat.id, "/broadcast <matn>")
        return
    text = parts[1]
    ok = fail = 0
    sm = bot.send_message(msg.chat.id, "Yuborilmoqda...")
    for uid in list(user_data.keys()):
        try:
            bot.send_message(uid, f"📢 *Yangilik:*\n\n{text}", parse_mode="Markdown")
            ok += 1
            time.sleep(0.06)
        except Exception:
            fail += 1
    bot.edit_message_text(
        f"Yuborildi: `{ok}` | Xato: `{fail}`",
        msg.chat.id, sm.message_id, parse_mode="Markdown"
    )

@bot.message_handler(commands=["ban"])
@owner_only
def cmd_ban(msg):
    parts = msg.text.split()
    if len(parts) < 2:
        bot.send_message(msg.chat.id, "/ban <id>")
        return
    try:
        uid = int(parts[1])
        get_user(uid)["banned"] = True
        bot.send_message(msg.chat.id, f"`{uid}` bloklandi.", parse_mode="Markdown")
    except ValueError:
        bot.send_message(msg.chat.id, "Notogri ID")

@bot.message_handler(commands=["unban"])
@owner_only
def cmd_unban(msg):
    parts = msg.text.split()
    if len(parts) < 2:
        bot.send_message(msg.chat.id, "/unban <id>")
        return
    try:
        uid = int(parts[1])
        if uid in user_data:
            user_data[uid]["banned"] = False
        bot.send_message(msg.chat.id, f"`{uid}` blokdan chiqarildi.", parse_mode="Markdown")
    except ValueError:
        bot.send_message(msg.chat.id, "Notogri ID")

@bot.message_handler(commands=["seturl"])
@owner_only
def cmd_seturl(msg):
    global SITE_URL
    parts = msg.text.split(" ", 1)
    if len(parts) < 2:
        bot.send_message(msg.chat.id, "/seturl <url>")
        return
    SITE_URL = parts[1].strip()
    bot.send_message(msg.chat.id, f"URL yangilandi:\n`{SITE_URL}`", parse_mode="Markdown")

@bot.message_handler(commands=["botinfo"])
@owner_only
def cmd_botinfo(msg):
    import sys
    bot.send_message(
        msg.chat.id,
        f"*BOT INFO — TopUp Zone's Games*\n\n"
        f"Oyinlar: `{game_count()}`\n"
        f"Owner ID: `{OWNER_ID}`\n"
        f"Python: `{sys.version.split()[0]}`\n"
        f"Users: `{len(user_data)}`\n"
        f"Donat bot: {DONATE_BOT}\n"
        f"Sayt: `{SITE_URL}`",
        parse_mode="Markdown"
    )

# ═══════════════════════════════════════════════
#  BAN FILTER
# ═══════════════════════════════════════════════
orig_process = bot.process_new_updates

def filtered_updates(updates):
    clean = []
    for upd in updates:
        uid = None
        if upd.message:
            uid = upd.message.from_user.id
        elif upd.callback_query:
            uid = upd.callback_query.from_user.id
        if uid and user_data.get(uid, {}).get("banned"):
            try:
                if upd.message:
                    bot.send_message(uid, "Siz bloklangansiz.")
            except Exception:
                pass
            continue
        clean.append(upd)
    orig_process(clean)

bot.process_new_updates = filtered_updates

# ═══════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    print("=" * 60)
    print("TopUp Zone's Games Bot ishga tushdi!")
    print(f"Sayt URL   : {SITE_URL}")
    print(f"Owner ID   : {OWNER_ID}")
    print(f"SAT savollar: {sum(len(v) for v in SAT_QUESTIONS.values())} ta")
    print(f"Oyinlar    : {game_count()} ta")
    print(f"Donat bot  : {DONATE_BOT}")
    print("=" * 60)
    print()
    print("Muhim:")
    print("  1. SITE_URL ni ozgartiring (yuqoridagi SITE_URL = '...' qatorida)")
    print("  2. Kutubxonalarni urnatish:")
    print("     pip install pyTelegramBotAPI")
    print()
    bot.infinity_polling(timeout=30, long_polling_timeout=15)