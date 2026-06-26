import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = "8639851394:AAEeaPp5rnaSo6VaHRM8_IJjmlzr-ZT4tOY"
ADMIN_ID = 938066764
CHANNEL_ID = -1003714502079

LANGUAGE, NAME, COUNTRY, CITY, EXPERIENCE, GOAL, WHATSAPP, TELEGRAM_USERNAME = range(8)

logging.basicConfig(level=logging.INFO)

# ─── ТЕКСТЫ НА 3 ЯЗЫКАХ ───────────────────────────────────────────────────────

TEXTS = {
    'ru': {
        'welcome': (
            "👋 Привет! Это бот Данияра iPro.\n\n"
            "🎬 Живой воркшоп по AI-видео — Алматы.\n"
            "Один день — и ты умеешь то, что другие изучают годами.\n\n"
            "Что тебя интересует? 👇"
        ),
        'menu': [
            ["🎯 Хочу на воркшоп!"],
            ["❓ Что будет на воркшопе?"],
            ["💰 Сколько стоит?"],
            ["📍 Когда и где?"],
            ["📞 Хочу чтобы Данияр написал мне"]
        ],
        'about': (
            "🎬 На воркшопе ты научишься:\n\n"
            "✅ Генерировать видео из фото\n"
            "✅ Создавать AI-персонажей с любым лицом\n"
            "✅ Делать спецэффекты и трансформации\n"
            "✅ Накладывать AI-голос и озвучку\n"
            "✅ Монтировать и публиковать контент\n\n"
            "💻 Желательно прийти с ноутбуком.\n\n"
            "Готов записаться? 👇"
        ),
        'price': (
            "💰 Стоимость?\n\n"
            "Данияр расскажет всё лично — цену, формат и что входит.\n\n"
            "Оставь заявку — он свяжется с тобой 👇"
        ),
        'when': (
            "📍 Алматы\n"
            "🗓 Дата и место — уточни у Данияра лично!\n\n"
            "Оставь заявку сейчас 👇"
        ),
        'ask_name': "Отлично! Давай познакомимся 🤝\n\nКак тебя зовут?",
        'ask_country': "Из какой ты страны? 🌍",
        'ask_city': "Из какого города? 🏙",
        'ask_experience': "Как ты сейчас относишься к AI-видео?",
        'experience_options': [
            ["🔰 Новичок, только начинаю"],
            ["📱 Смотрю чужие, хочу сам"],
            ["🎬 Уже пробовал, хочу глубже"]
        ],
        'exp_reactions': {
            'Новичок': "С нуля — даже лучше, поставим всё правильно сразу 🎯",
            'Смотрю': "Пора переходить от просмотра к созданию! 🚀",
            'пробовал': "Уже в теме — значит сразу пойдём на глубину 🔥"
        },
        'ask_goal': "Зачем тебе AI-видео? 🎯",
        'goal_options': [
            ["🎨 Для своего контента / блога"],
            ["💼 Для клиентов / бизнеса"],
            ["💰 Хочу зарабатывать на этом"]
        ],
        'ask_whatsapp': "Отлично! Теперь укажи номер WhatsApp 📱\n(например: +77001234567)",
        'ask_telegram': "И последнее — твой никнейм в Telegram 📲\n(например: @username)\n\nЕсли нет — напиши «нет»",
        'done': (
            "🔥 {name}, ты в списке!\n\n"
            "Данияр свяжется с тобой лично — расскажет детали и условия участия.\n\n"
            "А пока подпишись на канал 👇\n@iPro_ai"
        ),
        'contact_done': (
            "✅ Готово! Данияр свяжется с тобой в ближайшее время 🔥\n\n"
            "Подпишись на канал 👇\n@iPro_ai"
        ),
        'ask_phone_contact': "Напиши свой номер WhatsApp — Данияр свяжется лично 📱",
        'unknown': (
            "Хороший вопрос! 😊\n\n"
            "Данияр ответит тебе лично — оставь заявку 👇"
        ),
        'cancel': "Окей! Если передумаешь — напиши /start 😊",
        'admin_new': "🔔 НОВАЯ ЗАЯВКА НА ВОРКШОП!\n\n👤 Имя: {name}\n🌍 Страна: {country}\n📍 Город: {city}\n🎬 Опыт: {experience}\n🎯 Цель: {goal}\n📱 WhatsApp: {whatsapp}\n📲 Telegram: {tg}\n🆔 ID: {uid}",
        'admin_contact': "📞 ХОЧЕТ ЧТОБЫ ТЫ НАПИСАЛ!\n\n📱 WhatsApp: {whatsapp}\n📲 Telegram: {tg}\n🌍 {country}, {city}\n🆔 ID: {uid}",
    },
    'kz': {
        'welcome': (
            "👋 Сәлем! Бұл Данияр iPro боты.\n\n"
            "🎬 AI-видео бойынша тікелей воркшоп — Алматы.\n"
            "Бір күн — және сен басқалар жылдар бойы үйренетінді білесің.\n\n"
            "Не қызықтырады? 👇"
        ),
        'menu': [
            ["🎯 Воркшопқа барғым келеді!"],
            ["❓ Воркшопта не болады?"],
            ["💰 Қанша тұрады?"],
            ["📍 Қашан және қайда?"],
            ["📞 Данияр маған жазсын"]
        ],
        'about': (
            "🎬 Воркшопта үйренесің:\n\n"
            "✅ Фотодан видео жасау\n"
            "✅ AI-кейіпкерлер жасау\n"
            "✅ Спецэффекттер мен трансформациялар\n"
            "✅ AI дауысы мен дыбыстау\n"
            "✅ Контентті монтаждау және жариялау\n\n"
            "💻 Ноутбукпен келген дұрыс.\n\n"
            "Жазылуға дайынсың ба? 👇"
        ),
        'price': (
            "💰 Бағасы?\n\n"
            "Данияр барлығын жеке айтады — баға, формат және не кіреді.\n\n"
            "Өтінім қалдыр — ол сенімен байланысады 👇"
        ),
        'when': (
            "📍 Алматы\n"
            "🗓 Күні мен орны — Даниярдан жеке сұра!\n\n"
            "Қазір өтінім қалдыр 👇"
        ),
        'ask_name': "Тамаша! Танысайық 🤝\n\nАтың кім?",
        'ask_country': "Қай елденсің? 🌍",
        'ask_city': "Қай қаладансың? 🏙",
        'ask_experience': "AI-видеоға қалай қарайсың?",
        'experience_options': [
            ["🔰 Жаңадан бастаушы"],
            ["📱 Басқалардың видеосын көремін, өзім жасағым келеді"],
            ["🎬 Байқап көрдім, тереңірек кіргім келеді"]
        ],
        'exp_reactions': {
            'Жаңадан': "Нөлден бастау тіпті жақсы — бірден дұрыс орнатамыз 🎯",
            'Басқалардың': "Көруден жасауға өту уақыты келді! 🚀",
            'Байқап': "Тақырыпта — демек тереңге кетеміз 🔥"
        },
        'ask_goal': "AI-видео не үшін керек? 🎯",
        'goal_options': [
            ["🎨 Өз контентім / блогым үшін"],
            ["💼 Клиенттер / бизнес үшін"],
            ["💰 Осыдан табыс тапқым келеді"]
        ],
        'ask_whatsapp': "Тамаша! WhatsApp нөмірін жаз 📱\n(мысалы: +77001234567)",
        'ask_telegram': "Соңғысы — Telegram никнеймің 📲\n(мысалы: @username)\n\nЖоқ болса — «жоқ» деп жаз",
        'done': (
            "🔥 {name}, тізімдесің!\n\n"
            "Данияр саған жеке байланысады — мәліметтер мен шарттарды айтады.\n\n"
            "Әзірше каналға жазыл 👇\n@iPro_ai"
        ),
        'contact_done': (
            "✅ Дайын! Данияр жақын арада саған байланысады 🔥\n\n"
            "Каналға жазыл 👇\n@iPro_ai"
        ),
        'ask_phone_contact': "WhatsApp нөмірің жаз — Данияр жеке байланысады 📱",
        'unknown': (
            "Жақсы сұрақ! 😊\n\n"
            "Данияр жеке жауап береді — өтінім қалдыр 👇"
        ),
        'cancel': "Окей! Ойыңды өзгертсең — /start жаз 😊",
        'admin_new': "🔔 ЖАҢА ӨТІНІМ!\n\n👤 Аты: {name}\n🌍 Ел: {country}\n📍 Қала: {city}\n🎬 Тәжірибе: {experience}\n🎯 Мақсат: {goal}\n📱 WhatsApp: {whatsapp}\n📲 Telegram: {tg}\n🆔 ID: {uid}",
        'admin_contact': "📞 БАЙЛАНЫСУДЫ СҰРАЙДЫ!\n\n📱 WhatsApp: {whatsapp}\n📲 Telegram: {tg}\n🌍 {country}, {city}\n🆔 ID: {uid}",
    },
    'en': {
        'welcome': (
            "👋 Hi! This is Daniyar iPro's bot.\n\n"
            "🎬 Live AI-video workshop — Almaty.\n"
            "One day — and you'll know what others spend years learning.\n\n"
            "What are you interested in? 👇"
        ),
        'menu': [
            ["🎯 I want to join the workshop!"],
            ["❓ What's in the workshop?"],
            ["💰 How much does it cost?"],
            ["📍 When and where?"],
            ["📞 I want Daniyar to contact me"]
        ],
        'about': (
            "🎬 At the workshop you'll learn:\n\n"
            "✅ Generate video from photos\n"
            "✅ Create AI characters with any face\n"
            "✅ Make VFX and transformations\n"
            "✅ Add AI voice and sound\n"
            "✅ Edit and publish content\n\n"
            "💻 Better to come with a laptop.\n\n"
            "Ready to sign up? 👇"
        ),
        'price': (
            "💰 Price?\n\n"
            "Daniyar will tell you everything personally — price, format and what's included.\n\n"
            "Leave a request — he'll contact you 👇"
        ),
        'when': (
            "📍 Almaty\n"
            "🗓 Date and venue — ask Daniyar personally!\n\n"
            "Leave a request now 👇"
        ),
        'ask_name': "Great! Let's get acquainted 🤝\n\nWhat's your name?",
        'ask_country': "Which country are you from? 🌍",
        'ask_city': "Which city? 🏙",
        'ask_experience': "How do you feel about AI-video?",
        'experience_options': [
            ["🔰 Beginner, just starting"],
            ["📱 I watch others, want to do it myself"],
            ["🎬 Already tried, want to go deeper"]
        ],
        'exp_reactions': {
            'Beginner': "Starting from scratch is even better — we'll set everything up right 🎯",
            'watch': "Time to move from watching to creating! 🚀",
            'tried': "Already in the loop — we'll go deep right away 🔥"
        },
        'ask_goal': "Why do you need AI-video? 🎯",
        'goal_options': [
            ["🎨 For my own content / blog"],
            ["💼 For clients / business"],
            ["💰 I want to earn money from it"]
        ],
        'ask_whatsapp': "Great! Now enter your WhatsApp number 📱\n(example: +77001234567)",
        'ask_telegram': "Last one — your Telegram username 📲\n(example: @username)\n\nIf you don't have one — type 'none'",
        'done': (
            "🔥 {name}, you're on the list!\n\n"
            "Daniyar will contact you personally — details and terms.\n\n"
            "Meanwhile subscribe to the channel 👇\n@iPro_ai"
        ),
        'contact_done': (
            "✅ Done! Daniyar will contact you soon 🔥\n\n"
            "Subscribe to the channel 👇\n@iPro_ai"
        ),
        'ask_phone_contact': "Enter your WhatsApp number — Daniyar will contact you personally 📱",
        'unknown': (
            "Good question! 😊\n\n"
            "Daniyar will answer personally — leave a request 👇"
        ),
        'cancel': "Okay! If you change your mind — type /start 😊",
        'admin_new': "🔔 NEW WORKSHOP REQUEST!\n\n👤 Name: {name}\n🌍 Country: {country}\n📍 City: {city}\n🎬 Experience: {experience}\n🎯 Goal: {goal}\n📱 WhatsApp: {whatsapp}\n📲 Telegram: {tg}\n🆔 ID: {uid}",
        'admin_contact': "📞 WANTS YOU TO CONTACT!\n\n📱 WhatsApp: {whatsapp}\n📲 Telegram: {tg}\n🌍 {country}, {city}\n🆔 ID: {uid}",
    }
}

def t(lang, key):
    return TEXTS.get(lang, TEXTS['ru']).get(key, TEXTS['ru'].get(key, ''))

def get_lang(context):
    return context.user_data.get('lang', 'ru')

# ─── СТАРТ И ЯЗЫК ─────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Выберите язык / Тілді таңдаңыз / Choose language:",
        reply_markup=ReplyKeyboardMarkup(
            [["🇷🇺 Русский", "🇰🇿 Қазақша", "🇺🇸 English"]],
            resize_keyboard=True
        )
    )
    return LANGUAGE

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if 'Русский' in text or '🇷🇺' in text:
        context.user_data['lang'] = 'ru'
    elif 'Қазақша' in text or '🇰🇿' in text:
        context.user_data['lang'] = 'kz'
    else:
        context.user_data['lang'] = 'en'

    lang = get_lang(context)
    await update.message.reply_text(
        t(lang, 'welcome'),
        reply_markup=ReplyKeyboardMarkup(t(lang, 'menu'), resize_keyboard=True)
    )
    return ConversationHandler.END

# ─── ИНФО ─────────────────────────────────────────────────────────────────────

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    await update.message.reply_text(
        t(lang, 'about'),
        reply_markup=ReplyKeyboardMarkup(
            [[t(lang, 'menu')[0][0]], [t(lang, 'menu')[4][0]]],
            resize_keyboard=True
        )
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    await update.message.reply_text(
        t(lang, 'price'),
        reply_markup=ReplyKeyboardMarkup(
            [[t(lang, 'menu')[4][0]]],
            resize_keyboard=True
        )
    )

async def when(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    await update.message.reply_text(
        t(lang, 'when'),
        reply_markup=ReplyKeyboardMarkup(
            [[t(lang, 'menu')[0][0]]],
            resize_keyboard=True
        )
    )

# ─── РЕГИСТРАЦИЯ ──────────────────────────────────────────────────────────────

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data['mode'] = 'register'
    await update.message.reply_text(t(lang, 'ask_name'), reply_markup=ReplyKeyboardRemove())
    return NAME

async def contact_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data['mode'] = 'contact'
    await update.message.reply_text(t(lang, 'ask_country'), reply_markup=ReplyKeyboardRemove())
    return COUNTRY

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data['name'] = update.message.text
    await update.message.reply_text(t(lang, 'ask_country'))
    return COUNTRY

async def get_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data['country'] = update.message.text
    await update.message.reply_text(t(lang, 'ask_city'))
    return CITY

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data['city'] = update.message.text
    mode = context.user_data.get('mode', 'register')

    if mode == 'contact':
        await update.message.reply_text(t(lang, 'ask_phone_contact'))
        return WHATSAPP

    await update.message.reply_text(
        t(lang, 'ask_experience'),
        reply_markup=ReplyKeyboardMarkup(t(lang, 'experience_options'), resize_keyboard=True)
    )
    return EXPERIENCE

async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data['experience'] = update.message.text
    exp = update.message.text

    reactions = t(lang, 'exp_reactions')
    reaction = next((v for k, v in reactions.items() if k in exp), "Отлично! 🔥")

    await update.message.reply_text(
        f"{reaction}\n\n{t(lang, 'ask_goal')}",
        reply_markup=ReplyKeyboardMarkup(t(lang, 'goal_options'), resize_keyboard=True)
    )
    return GOAL

async def get_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data['goal'] = update.message.text
    await update.message.reply_text(t(lang, 'ask_whatsapp'), reply_markup=ReplyKeyboardRemove())
    return WHATSAPP

async def get_whatsapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    context.user_data['whatsapp'] = update.message.text
    await update.message.reply_text(t(lang, 'ask_telegram'))
    return TELEGRAM_USERNAME

async def get_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    user = update.message.from_user
    tg = update.message.text
    if tg.lower() in ['нет', 'жоқ', 'none', 'no', '-']:
        tg = f"@{user.username}" if user.username else 'нет'

    context.user_data['tg'] = tg
    mode = context.user_data.get('mode', 'register')

    name = context.user_data.get('name', '')
    country = context.user_data.get('country', '')
    city = context.user_data.get('city', '')
    experience = context.user_data.get('experience', '')
    goal = context.user_data.get('goal', '')
    whatsapp = context.user_data.get('whatsapp', '')

    if mode == 'contact':
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=t(lang, 'admin_contact').format(
                whatsapp=whatsapp, tg=tg,
                country=country, city=city, uid=user.id
            )
        )
        await update.message.reply_text(
            t(lang, 'contact_done'),
            reply_markup=ReplyKeyboardMarkup(t(lang, 'menu'), resize_keyboard=True)
        )
    else:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=t(lang, 'admin_new').format(
                name=name, country=country, city=city,
                experience=experience, goal=goal,
                whatsapp=whatsapp, tg=tg, uid=user.id
            )
        )
        await update.message.reply_text(
            t(lang, 'done').format(name=name),
            reply_markup=ReplyKeyboardMarkup(t(lang, 'menu'), resize_keyboard=True)
        )

    return ConversationHandler.END

# ─── ПРОЧЕЕ ───────────────────────────────────────────────────────────────────

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    user = update.message.from_user
    text = update.message.text
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"❓ ВОПРОС:\n\n💬 {text}\n📲 @{user.username or 'нет'}\n🆔 {user.id}"
    )
    await update.message.reply_text(
        t(lang, 'unknown'),
        reply_markup=ReplyKeyboardMarkup(t(lang, 'menu'), resize_keyboard=True)
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    await update.message.reply_text(t(lang, 'cancel'), reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Использование: /post Текст поста")
        return
    text = ' '.join(context.args)
    context.user_data['pending_post'] = text
    await update.message.reply_text(f"📝 Предпросмотр:\n\n{text}\n\n/confirm для публикации")

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    text = context.user_data.get('pending_post')
    if not text:
        await update.message.reply_text("Нет поста.")
        return
    await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
    await update.message.reply_text("✅ Пост опубликован!")
    context.user_data['pending_post'] = None

# ─── ЗАПУСК ───────────────────────────────────────────────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()

    lang_conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    reg_conv = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("Хочу на воркшоп|Воркшопқа барғым|want to join"), register_start),
            MessageHandler(filters.Regex("Данияр написал мне|Данияр маған жазсын|Daniyar to contact"), contact_request),
        ],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_country)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
            EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_experience)],
            GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_goal)],
            WHATSAPP: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_whatsapp)],
            TELEGRAM_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_telegram)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(lang_conv)
    app.add_handler(CommandHandler("post", post))
    app.add_handler(CommandHandler("confirm", confirm))
    app.add_handler(MessageHandler(filters.Regex("Что будет|Воркшопта не|What's in"), about))
    app.add_handler(MessageHandler(filters.Regex("Сколько стоит|Қанша тұрады|How much"), price))
    app.add_handler(MessageHandler(filters.Regex("Когда и где|Қашан және|When and where"), when))
    app.add_handler(reg_conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()
