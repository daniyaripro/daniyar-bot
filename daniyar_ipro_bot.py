import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = "8639851394:AAEeaPp5rnaSo6VaHRM8_IJjmlzr-ZT4tOY"
ADMIN_ID = 938066764
CHANNEL_ID = -1003714502079
NAME, CITY, EXPERIENCE, PHONE = range(4)
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Салем! Это бот Данияра iPro.\n\n"
        "🎬 Живой воркшоп по AI-видео в Алматы.\n"
        "Один воркшоп — и ты узнаешь то, что другие годами изучают сами.\n\n"
        "Что хочешь? 👇",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["🎯 Хочу на воркшоп!"],
                ["❓ Что будет на воркшопе?"],
                ["💰 Сколько стоит?"],
                ["📍 Когда и где?"]
            ],
            resize_keyboard=True
        )
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 На воркшопе ты научишься:\n\n"
        "✅ Генерировать видео из фото\n"
        "✅ Создавать AI-персонажей с любым лицом\n"
        "✅ Делать спецэффекты и трансформации\n"
        "✅ Накладывать AI-голос и озвучку\n"
        "✅ Монтировать и публиковать контент\n\n"
        "💻 Желательно прийти с ноутбуком.\n"
        "Можно и с телефоном, но менее удобно.\n\n"
        "Остались вопросы? Данияр ответит лично 👇",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["🎯 Хочу на воркшоп!"],
                ["📞 Хочу чтобы Данияр написал мне"]
            ],
            resize_keyboard=True
        )
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Стоимость участия?\n\n"
        "Данияр расскажет всё лично — цену, формат и что входит.\n\n"
        "Оставь номер и он свяжется с тобой в ближайшее время 👇",
        reply_markup=ReplyKeyboardMarkup(
            [["📞 Хочу чтобы Данияр написал мне"]],
            resize_keyboard=True
        )
    )

async def when(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📍 Алматы\n"
        "🗓 Дата и место — скоро объявим!\n\n"
        "Оставь заявку сейчас — Данияр свяжется первым "
        "и сообщит все детали 👇",
        reply_markup=ReplyKeyboardMarkup(
            [["🎯 Хочу на воркшоп!"]],
            resize_keyboard=True
        )
    )

async def contact_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отлично! Напиши свой номер телефона — "
        "Данияр свяжется с тобой лично 📱",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data['mode'] = 'contact'
    return PHONE

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отлично! Давай познакомимся 🤝\n\nКак тебя зовут?",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data['mode'] = 'register'
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text(
        f"Приятно познакомиться, {update.message.text}! 😊\n\nИз какого ты города?"
    )
    return CITY

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['city'] = update.message.text
    city = update.message.text.lower()
    if 'алмат' in city:
        reaction = "Отлично, свой человек! 🏙"
    elif 'астан' in city or 'нур' in city:
        reaction = "Из столицы! Специально приедешь — не пожалеешь 💪"
    else:
        reaction = f"Здорово, из {update.message.text}! 🌍"
    await update.message.reply_text(
        f"{reaction}\n\nКак ты сейчас относишься к AI-видео?",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["🔰 Новичок, только начинаю"],
                ["📱 Смотрю чужие, хочу сам"],
                ["🎬 Уже пробовал, хочу глубже"]
            ],
            resize_keyboard=True
        )
    )
    return EXPERIENCE

async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['experience'] = update.message.text
    exp = update.message.text
    if 'Новичок' in exp:
        reaction = "С нуля это даже лучше — поставим всё правильно сразу 🎯"
    elif 'Смотрю' in exp:
        reaction = "Пора переходить от просмотра к созданию! 🚀"
    else:
        reaction = "Уже в теме — значит сразу пойдём на глубину 🔥"
    await update.message.reply_text(
        f"{reaction}\n\nПоследний шаг — напиши номер телефона 📱",
        reply_markup=ReplyKeyboardRemove()
    )
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    user = update.message.from_user
    mode = context.user_data.get('mode', 'register')

    if mode == 'contact':
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📞 ХОЧЕТ ЧТОБЫ ТЫ НАПИСАЛ!\n\n"
                 f"📱 Телефон: {phone}\n"
                 f"📲 Telegram: @{user.username or 'нет'}\n"
                 f"🆔 ID: {user.id}"
        )
        await update.message.reply_text(
            "✅ Готово! Данияр свяжется с тобой в ближайшее время 🔥\n\n"
            "А пока подпишись на канал 👇\n@iPro_ai",
            reply_markup=ReplyKeyboardMarkup(
                [["🎯 Хочу на воркшоп!"]],
                resize_keyboard=True
            )
        )
    else:
        name = context.user_data.get('name', '')
        city = context.user_data.get('city', '')
        experience = context.user_data.get('experience', '')
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 НОВАЯ ЗАЯВКА НА ВОРКШОП!\n\n"
                 f"👤 Имя: {name}\n"
                 f"📍 Город: {city}\n"
                 f"🎬 Опыт: {experience}\n"
                 f"📱 Телефон: {phone}\n"
                 f"📲 Telegram: @{user.username or 'нет'}\n"
                 f"🆔 ID: {user.id}"
        )
        await update.message.reply_text(
            f"🔥 Всё, {name}, ты в списке!\n\n"
            "Данияр свяжется с тобой лично — расскажет детали и условия участия.\n\n"
            "А пока подпишись на канал 👇\n@iPro_ai",
            reply_markup=ReplyKeyboardMarkup(
                [["🎯 Хочу на воркшоп!"]],
                resize_keyboard=True
            )
        )
    return ConversationHandler.END

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"❓ ВОПРОС ОТ ПОЛЬЗОВАТЕЛЯ:\n\n"
             f"💬 {text}\n"
             f"📲 @{user.username or 'нет'}\n"
             f"🆔 {user.id}"
    )
    await update.message.reply_text(
        "Хороший вопрос! 😊\n\n"
        "Данияр ответит тебе лично — оставь номер и он свяжется 👇",
        reply_markup=ReplyKeyboardMarkup(
            [["📞 Хочу чтобы Данияр написал мне"]],
            resize_keyboard=True
        )
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Окей! Если передумаешь — напиши /start 😊",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Использование: /post Текст поста")
        return
    text = ' '.join(context.args)
    context.user_data['pending_post'] = text
    await update.message.reply_text(f"📝 Предпросмотр для @iPro_ai:\n\n{text}\n\n/confirm или /cancel")

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    text = context.user_data.get('pending_post')
    if not text:
        await update.message.reply_text("Нет поста.")
        return
    await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
    await update.message.reply_text("✅ Пост опубликован в @iPro_ai!")
    context.user_data['pending_post'] = None

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^🎯 Хочу на воркшоп!$"), register_start),
            MessageHandler(filters.Regex("^📞 Хочу чтобы Данияр написал мне$"), contact_request),
        ],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
            EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_experience)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", post))
    app.add_handler(CommandHandler("confirm", confirm))
    app.add_handler(MessageHandler(filters.Regex("^❓ Что будет на воркшопе\\?$"), about))
    app.add_handler(MessageHandler(filters.Regex("^💰 Сколько стоит\\?$"), price))
    app.add_handler(MessageHandler(filters.Regex("^📍 Когда и где\\?$"), when))
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))
    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()
