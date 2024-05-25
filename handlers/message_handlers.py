from telegram import Update
from config.openai_client import client
from config.jira_connect import login, api_key, adress
from jira import JIRA

import config.promts as promt
import handlers.support_functions as spf
async def chatgpt_reply(update: Update, context):
    # текст входящего сообщения
    text = update.message.text

    # запрос
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
        max_tokens=1024,
        temperature=0.5,
    )

    # ответ
    reply = response.choices[0].message.content.strip()
    reply += promt.end_promt
    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)   
    
    print("user:", text)
    print("assistant:", reply)
    return spf.CHOOSING

async def generate_excuse(update: Update, context):
    # текст входящего сообщения
    text2 = update.message.text
    text = promt.funny_excus + text2

    # запрос
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
        max_tokens=1024,
        temperature=0.5,
    )

    # ответ
    reply = response.choices[0].message.content.strip()
    reply += promt.end_promt

    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)   
    
    print("user:", text)
    print("assistant:", reply)
    return spf.CHOOSING

async def decompose_jira(update: Update, context):
    # текст входящего сообщения
    task_id = update.message.text
    print(task_id)
    text1 = promt.jira_promt

    try:
        jiraOptions = {'server': adress, "verify": False}
        jira = JIRA(options=jiraOptions, basic_auth=(login, api_key))
        
        text2 = jira.issue(task_id).fields.description
        text = text1 + " " + text2
        print(text)
    
        # запрос
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            max_tokens=1024,
            temperature=0.5,
        )
    
        # ответ
        reply = response.choices[0].message.content.strip()
        jira.add_comment(task_id, reply)
    
        reply += promt.end_promt
        print("user:", text)
        print("assistant:", reply)
    except:
        reply = promt.jira_error
    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)   
    
    return spf.CHOOSING