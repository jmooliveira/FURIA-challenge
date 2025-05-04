import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, CallbackContext,
    ConversationHandler, MessageHandler, Filters
)

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Estados para o cadastro (etapas da conversa)
NOME, EMAIL = range(2)

# Estado do quiz (como há apenas uma etapa, pode ser 0)
QUIZ = 0

# Comando inicial: exibe um menu com botões
def start(update: Update, context: CallbackContext):
    menu = [["/ultimojogo", "/proximojogo"],
            ["/jogadores", "/torcida"],
            ["/redes", "/loja"],
            ["/cadastro"]]
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    update.message.reply_text("👊 Bem-vindo ao Bot da FURIA!\nEscolha uma das opções abaixo:", reply_markup=reply_markup)

# Retorna o último jogo
def ultimojogo(update: Update, context: CallbackContext):
    update.message.reply_text("🏆 FURIA 16x12 Liquid - IEM Rio (27/04/2025)")

# Retorna o próximo jogo
def proximojogo(update: Update, context: CallbackContext):
    update.message.reply_text("📅 FURIA x G2 - 02/05/2025 às 18h (Brasília)")

# Lista de jogadores
def jogadores(update: Update, context: CallbackContext):
    update.message.reply_text("👥 KSCERATO, yuurih, chelo, FalleN, arT")

# Grito da torcida
def torcida(update: Update, context: CallbackContext):
    update.message.reply_text("🔥 EU SOU FURIA!")

# Links das redes sociais
def redes(update: Update, context: CallbackContext):
    update.message.reply_text(
        "📱 Redes sociais da FURIA:\n"
        "🐦 Twitter: https://twitter.com/furia\n"
        "📸 Instagram: https://instagram.com/furia\n"
        "📺 Twitch: https://twitch.tv/furia\n"
        "🌐 Site oficial: https://furia.gg"
    )

# Link da loja
def loja(update: Update, context: CallbackContext):
    update.message.reply_text("🛍️ Confira a loja oficial da FURIA:\nhttps://furia.gg/shop")

# Início do cadastro: pergunta o nome
def iniciar_cadastro(update: Update, context: CallbackContext):
    update.message.reply_text("📝 Vamos fazer seu cadastro!\nQual o seu nome?")
    return NOME

# Salva o nome e pergunta o email
def receber_nome(update: Update, context: CallbackContext):
    context.user_data["nome"] = update.message.text
    update.message.reply_text("Qual o seu email?")
    return EMAIL

# Salva o email e finaliza o cadastro
def receber_email(update: Update, context: CallbackContext):
    context.user_data["email"] = update.message.text
    nome = context.user_data["nome"]
    email = context.user_data["email"]
    update.message.reply_text(f"✅ Cadastro concluído!\nNome: {nome}\nEmail: {email}")
    return ConversationHandler.END

# Cancela conversas
def cancelar(update: Update, context: CallbackContext):
    update.message.reply_text("❌ Cadastro cancelado.")
    return ConversationHandler.END

# Mensagem de saída
def sair(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Obrigado por usar o Bot da FURIA!\nVolte sempre que quiser!",
        reply_markup=ReplyKeyboardMarkup([["/start"]], resize_keyboard=True)
    )

# Início do quiz
def quiz(update: Update, context: CallbackContext):
    pergunta = "🤔 Quem é o capitão atual do time de CS:GO da FURIA?"
    opcoes = ["A) yuurih", "B) chelo", "C) FalleN", "D) KSCERATO"]
    resposta_correta = "C"
    context.user_data["resposta_quiz"] = resposta_correta
    texto = f"{pergunta}\n\n" + "\n".join(opcoes)
    update.message.reply_text(texto)
    return QUIZ

# Verifica a resposta do quiz
def verificar_resposta(update: Update, context: CallbackContext):
    resposta = update.message.text.strip().upper()
    resposta_certa = context.user_data.get("resposta_quiz")
    if resposta_certa:
        if resposta == resposta_certa:
            update.message.reply_text("✅ Correto! FalleN é o capitão atual.\n+1 ponto para você!")
        else:
            update.message.reply_text(f"❌ Resposta incorreta! A correta era: {resposta_certa})")
        del context.user_data["resposta_quiz"]  # Limpa para evitar reaproveitamento
    return ConversationHandler.END

# Função principal que configura os handlers
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handlers básicos
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ultimojogo", ultimojogo))
    dp.add_handler(CommandHandler("proximojogo", proximojogo))
    dp.add_handler(CommandHandler("jogadores", jogadores))
    dp.add_handler(CommandHandler("torcida", torcida))
    dp.add_handler(CommandHandler("redes", redes))
    dp.add_handler(CommandHandler("loja", loja))
    dp.add_handler(CommandHandler("menu", start))
    dp.add_handler(CommandHandler("sair", sair))

    # Conversa do quiz
    quiz_handler = ConversationHandler(
        entry_points=[CommandHandler("quiz", quiz)],
        states={QUIZ: [MessageHandler(Filters.text & ~Filters.command, verificar_resposta)]},
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )
    dp.add_handler(quiz_handler)

    # Conversa do cadastro
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

# Ponto de entrada
if __name__ == '__main__':
    main()
