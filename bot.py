import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, CallbackContext,
    ConversationHandler, MessageHandler, Filters
)

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Estados do cadastro
NOME, EMAIL = range(2)

# Comandos do menu
def start(update: Update, context: CallbackContext):
    menu = [["/ultimojogo", "/proximojogo"],
            ["/jogadores", "/torcida"],
            ["/redes", "/loja"],
            ["/cadastro"]]
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    update.message.reply_text("👊 Bem-vindo ao Bot da FURIA!\nEscolha uma das opções abaixo:", reply_markup=reply_markup)

def ultimojogo(update: Update, context: CallbackContext):
    update.message.reply_text("🏆 FURIA 16x12 Liquid - IEM Rio (27/04/2025)")

def proximojogo(update: Update, context: CallbackContext):
    update.message.reply_text("📅 FURIA x G2 - 02/05/2025 às 18h (Brasília)")

def jogadores(update: Update, context: CallbackContext):
    update.message.reply_text("👥 KSCERATO, yuurih, chelo, FalleN, arT")

def torcida(update: Update, context: CallbackContext):
    update.message.reply_text("🔥 EU SOU FURIA!")

def redes(update: Update, context: CallbackContext):
    update.message.reply_text(
        "📱 Redes sociais da FURIA:\n"
        "🐦 Twitter: https://twitter.com/furia\n"
        "📸 Instagram: https://instagram.com/furia\n"
        "📺 Twitch: https://twitch.tv/furia\n"
        "🌐 Site oficial: https://furia.gg"
    )

def loja(update: Update, context: CallbackContext):
    update.message.reply_text("🛍️ Confira a loja oficial da FURIA:\nhttps://furia.gg/shop")

# Cadastro
def iniciar_cadastro(update: Update, context: CallbackContext):
    update.message.reply_text("📝 Vamos fazer seu cadastro!\nQual o seu nome?")
    return NOME

def receber_nome(update: Update, context: CallbackContext):
    context.user_data["nome"] = update.message.text
    update.message.reply_text("Qual o seu email?")
    return EMAIL

def receber_email(update: Update, context: CallbackContext):
    context.user_data["email"] = update.message.text
    nome = context.user_data["nome"]
    email = context.user_data["email"]
    update.message.reply_text(f"✅ Cadastro concluído!\nNome: {nome}\nEmail: {email}")
    return ConversationHandler.END

def cancelar(update: Update, context: CallbackContext):
    update.message.reply_text("❌ Cadastro cancelado.")
    return ConversationHandler.END

def sair(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Obrigado por usar o Bot da FURIA!\nVolte sempre que quiser!",
        reply_markup=ReplyKeyboardMarkup([["/start"]], resize_keyboard=True)
    )

# Main
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ultimojogo", ultimojogo))
    dp.add_handler(CommandHandler("proximojogo", proximojogo))
    dp.add_handler(CommandHandler("jogadores", jogadores))
    dp.add_handler(CommandHandler("torcida", torcida))
    dp.add_handler(CommandHandler("redes", redes))
    dp.add_handler(CommandHandler("loja", loja))
    dp.add_handler(CommandHandler("menu", start))
    dp.add_handler(CommandHandler("sair", sair))

    cadastro_handler = ConversationHandler(
        entry_points=[CommandHandler("cadastro", iniciar_cadastro)],
        states={
            NOME: [MessageHandler(Filters.text & ~Filters.command, receber_nome)],
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, receber_email)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )
    dp.add_handler(cadastro_handler)

    updater.start_polling()
    print("✅ Bot está rodando...")
    updater.idle()

if __name__ == '__main__':
    main()
