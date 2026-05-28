import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json

def chave_api():
    with open('telegram_api.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    CHAVE_TELEGRAM = data['key']
    file.close()
    return CHAVE_TELEGRAM

TOKEN_TELEGRAM = chave_api()

async def comando_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá, envie o nome de um produto que buscarei no '\
        ' mercado livre e te retornarei num relatorio mais facil de ler :D')


async def buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    termo_busca = update.message.text
    arquivo_saida = f'resultados_{termo_busca.replace(' ', '_')}.csv'
    
    chat_id = update.message.chat_id
    loop_atual = asyncio.get_running_loop()
    dados_conversa = (chat_id, context, loop_atual)
    
    await update.message.reply_text(f'Iniciando busca por {termo_busca}')
    
    try:
        from main import iniciar
        await asyncio.to_thread(iniciar, busca=termo_busca, nome=arquivo_saida, paginas=3, telegram=dados_conversa)
        if os.path.exists(arquivo_saida):
            await update.message.reply_text('Busca concluida ! Enviando Arquivo')
            with open (arquivo_saida, 'rb') as resultado:
                await update.message.reply_document(document=resultado, filename=arquivo_saida)
            os.remove(arquivo_saida)
        else:
            await update.message.reply_text(f'Ocorreu algum erro durante a criação do relatorio')
    except Exception as e:
        await update.message.reply_text(f'Ocorreu um erro durante a busca: {e}')
        
        
def iniciar_bot():
    print('Bot iniciado, aguardando comandos')
    print(TOKEN_TELEGRAM)
    app = Application.builder().token(TOKEN_TELEGRAM).build()
    
    app.add_handler(CommandHandler('start', comando_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar))
    
    app.run_polling()
