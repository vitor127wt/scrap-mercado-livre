import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json

def chave_api():
    with open('bot_telegram.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    CHAVE_TELEGRAM = data['key']
    file.close()
    return CHAVE_TELEGRAM
