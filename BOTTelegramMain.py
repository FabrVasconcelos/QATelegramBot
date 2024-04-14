import time
import os
import telebot
import config
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from telebot import types

TOKEN = config.TeleToken
bot = telebot.TeleBot(TOKEN)

allowed_chat_ids = config.Chat_ID

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Olá! Chat ID: " + str(message.chat.id))

@bot.message_handler(commands=['testes'])
def mostrar_opcoes_teste(mensagem):
    if str(mensagem.chat.id) in allowed_chat_ids:
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton('Teste 1', callback_data='teste1'),
                   types.InlineKeyboardButton('Teste 2', callback_data='teste2'),
                   types.InlineKeyboardButton('Teste 3', callback_data='teste3'))
        bot.send_message(mensagem.chat.id, "Selecione o teste que deseja executar:", reply_markup=markup)
    else:
        bot.send_message(mensagem.chat.id, "Desculpe, você não tem permissão para executar este comando neste chat.")

@bot.callback_query_handler(func=lambda call: True)
def executar_teste(call):
    if str(call.message.chat.id) in allowed_chat_ids:
        teste_selecionado = call.data
        bot.send_message(call.message.chat.id, f"Você selecionou o {teste_selecionado}. Executando o teste...")

        if teste_selecionado in ['teste1', 'teste2', 'teste3']:
            nome_arquivo_bat = f'{teste_selecionado.capitalize()}.bat'
        else:
            bot.send_message(call.message.chat.id, "Opção inválida.")
            return

        subprocess.call([f'Executaveis\\{nome_arquivo_bat}'])

        nome_arquivo_xml = 'Resultados/output-xml.xml'
        try:
            tree = ET.parse(nome_arquivo_xml)
            root = tree.getroot()

            testsuite = root.find('testsuite')
            errors = int(testsuite.get('errors', 0))
            failures = int(testsuite.get('failures', 0))

            mensagem = f"<b>Resultado do Teste:</b>\n"
            mensagem += f"Total de testes: {testsuite.get('tests')}\n"
            mensagem += f"Erros: {errors}\n"
            mensagem += f"Failures: {failures}\n"
            mensagem += f"Tempo: {testsuite.get('time')} segundos\n"

            bot.send_message(call.message.chat.id, mensagem, parse_mode='HTML')
            if errors > 0 or failures > 0:
                with open('Img/TestFailed.gif', 'rb') as img:
                    bot.send_animation(call.message.chat.id, img)
            else:
                with open('Img/TestPassed.gif', 'rb') as img:
                    bot.send_animation(call.message.chat.id, img)

        except Exception as e:
            bot.send_message(call.message.chat.id, f"Erro ao processar arquivo XML: {str(e)}")

        nome_arquivo_resultado = f'Resultados/report.html'
        if os.path.exists(nome_arquivo_resultado):
            with open(nome_arquivo_resultado, 'rb') as arquivo:
                conteudo_arquivo = arquivo.read()

            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.html', prefix='Resultado_') as temp_file:
                temp_file.write(conteudo_arquivo)

            bot.send_document(call.message.chat.id, open(temp_file.name, 'rb'), caption="Report.html")
            os.unlink(temp_file.name)
        else:
            bot.send_message(call.message.chat.id, "Nenhum resultado disponível para este teste.")

    else:
        bot.send_message(call.message.chat.id, "Desculpe, você não tem permissão para executar este comando neste chat.")

@bot.message_handler(commands=['time'])
def responder_hora(mensagem):
    if str(mensagem.chat.id) in allowed_chat_ids:
        hora_atual = time.strftime('%H:%M:%S')
        bot.send_message(mensagem.chat.id, f"A hora atual é: {hora_atual}")
    else:
        bot.send_message(mensagem.chat.id, "Desculpe, você não tem permissão para executar este comando neste chat.")

@bot.message_handler(commands=['gato'])
def enviar_gato(message):
    if str(message.chat.id) in allowed_chat_ids:
        with open('Img/Gato.gif', 'rb') as gif:
            bot.send_animation(message.chat.id, gif)
    else:
        bot.send_message(message.chat.id, "Desculpe, você não tem permissão para executar este comando neste chat.")

@bot.message_handler(func=lambda mensagem: True)
def responder(mensagem):
    if str(mensagem.chat.id) in allowed_chat_ids:
        bot.send_message(mensagem.chat.id, "Use o comando /time para obter a hora ou /testes para executar um teste.")
    else:
        bot.send_message(mensagem.chat.id, "Desculpe, você não tem permissão para executar este comando neste chat.")

bot.polling()