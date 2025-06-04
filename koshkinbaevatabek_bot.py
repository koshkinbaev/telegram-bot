from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CallbackQueryHandler,
    CommandHandler, ContextTypes, MessageHandler, filters
)
import asyncio
import re

user_state = {}

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("💻 IT yangiliklar", callback_data='yangilik')],
        [InlineKeyboardButton("🧠 Foydali maslahatlar", callback_data='maslahat')],
        [InlineKeyboardButton("📚 IT Resurslar", callback_data='resurs')],
        [InlineKeyboardButton("📝 Kursga yozilish", callback_data='kurs')],
        [InlineKeyboardButton("🧪 Test (Quiz)", callback_data='test')],
    ]
    return InlineKeyboardMarkup(keyboard)

def submenu_keyboard(include_next=False, include_back=True):
    keyboard = []
    if include_next:
        keyboard.append([InlineKeyboardButton("➡️ Keyingi maslahat", callback_data='maslahat')])
    if include_back:
        keyboard.append([InlineKeyboardButton("⬅️ Bosh menyuga", callback_data='back_to_menu')])
    return InlineKeyboardMarkup(keyboard)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom! Bu yerda siz IT bo‘yicha turli ma’lumotlar, maslahatlar, testlar va kurslarga yozilish imkoniyatiga egasiz.",
        reply_markup=main_menu_keyboard()
    )
    user_id = update.effective_user.id
    user_state[user_id] = None
    user_state[f'{user_id}_maslahat_index'] = 0

# Yangiliklar bo‘limi
async def send_yangiliklar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    yangiliklar = [
        "📰 *Microsoft* — AI yordamida Word va Excel'ga kod yozish funksiyasini sinovdan o‘tkazmoqda.",
        "🍏 *Apple* — WWDC 2025’da iOS 19’ni AI yordami bilan namoyish etadi.",
        "🔎 *Google* — Gemini sun’iy intellekt platformasini kengaytirishni rejalashtirmoqda."
    ]
    await update.callback_query.edit_message_text(
        "\n\n".join(yangiliklar),
        reply_markup=submenu_keyboard()
    )
    user_state[update.effective_user.id] = 'yangilik'

# Maslahatlar bo‘limi
async def send_maslahatlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    maslahatlar = [
        "✅ Har kuni kamida 1 soat kod yozing — bu sizni o‘stiradi.",
        "💡 Kichik loyihalarni boshlang — o‘rganish samarali bo‘ladi.",
        "🔍 GitHub'dagi ochiq kodlarni o‘qing — sizning tajribangiz oshadi.",
        "🎓 Resurslar: freecodecamp.org, udemy.com, coursera.org — juda foydali.",
        "🧰 Portfolio yarating — real loyihalarni jamlang."
    ]
    index = user_state.get(f'{user_id}_maslahat_index', 0)
    if index >= len(maslahatlar):
        index = 0
    await update.callback_query.edit_message_text(
        maslahatlar[index],
        reply_markup=submenu_keyboard(include_next=True)
    )
    user_state[f'{user_id}_maslahat_index'] = index + 1
    user_state[user_id] = 'maslahat'

# Resurslar bo‘limi
async def send_resurslar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resurslar = [
        "🌐 *Frontend* — [Frontend Mentor](https://www.frontendmentor.io/)",
        "💻 *Backend* — [Node.js Docs](https://nodejs.org/en/docs/)",
        "📘 *Python* — [Real Python](https://realpython.com/)",
        "🧠 *AI & ML* — [Kaggle](https://www.kaggle.com/)"
    ]
    await update.callback_query.edit_message_text(
        "\n".join(resurslar),
        parse_mode='Markdown',
        reply_markup=submenu_keyboard()
    )
    user_state[update.effective_user.id] = 'resurs'

# Kursga yozilish
async def start_kurs_yozilish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        "📥 Kursga yozilish uchun quyidagi ma'lumotlarni bitta xabarda yuboring:\n\n"
        "👤 Ism Familya\n📱 Telefon raqam (+998 bilan)\n\n"
        "Masalan: `Ali Turgunov +998901234567`",
        reply_markup=submenu_keyboard(),
        parse_mode='Markdown'
    )
    user_state[update.effective_user.id] = 'waiting_for_registration'

# Ro‘yxatdan o‘tish
async def handle_registration_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_state.get(user_id) == 'waiting_for_registration':
        text = update.message.text.strip()
        phone_pattern = r'\+998\d{9}'
        if re.search(phone_pattern, text):
            await update.message.reply_text(
                f"✅ Ma'lumotlaringiz qabul qilindi:\n\n{text}\n\nBiz tez orada siz bilan bog‘lanamiz!",
                reply_markup=main_menu_keyboard()
            )
            user_state[user_id] = None
        else:
            await update.message.reply_text(
                "❌ Telefon raqami noto‘g‘ri! +998 bilan to‘g‘ri formatda kiriting.",
                reply_markup=submenu_keyboard()
            )
    else:
        await update.message.reply_text(
            "📍 Iltimos, menyudan bir bo‘limni tanlang.",
            reply_markup=main_menu_keyboard()
        )

# Test bo‘limi (oddiy versiya)
async def test_section(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        "🧪 Test bo‘limi hali ishlab chiqilmoqda. Yaqinda ishga tushadi!",
        reply_markup=submenu_keyboard()
    )
    user_state[update.effective_user.id] = 'test'

# Botni qayta boshlash
async def restart_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("🔄 Bot qayta ishga tushmoqda...")
    await asyncio.sleep(1)
    await update.callback_query.message.reply_text(
        "✅ Bot ishga tushdi! Quyidagilardan birini tanlang:",
        reply_markup=main_menu_keyboard()
    )
    user_id = update.effective_user.id
    user_state[user_id] = None
    user_state[f'{user_id}_maslahat_index'] = 0

# Callback tugmalarni boshqarish
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    await update.callback_query.answer()
    if data == 'yangilik':
        await send_yangiliklar(update, context)
    elif data == 'maslahat':
        await send_maslahatlar(update, context)
    elif data == 'resurs':
        await send_resurslar(update, context)
    elif data == 'kurs':
        await start_kurs_yozilish(update, context)
    elif data == 'test':
        await test_section(update, context)
    elif data == 'back_to_menu':
        await update.callback_query.edit_message_text(
            "🏠 Bosh menyuga qaytdingiz. Quyidagilardan birini tanlang:",
            reply_markup=main_menu_keyboard()
        )
        user_state[update.effective_user.id] = None
    else:
        await update.callback_query.edit_message_text(
            "⚠️ Bu bo‘lim hali mavjud emas.",
            reply_markup=main_menu_keyboard()
        )

# Botni ishga tushurish
if __name__ == '__main__':
    TOKEN = "7542519392:AAFYONdclrK-Yi_zDq9osK2dQ_7Q5EXKVHw"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_registration_message))

    print("✅ Bot ishga tushdi...")
    app.run_polling()
