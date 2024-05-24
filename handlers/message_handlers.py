from telegram import Update
from config.openai_client import client
from jira import JIRA

CHOOSING, GIVE_ME_LINK, FREE_REQUEST, TOPIC, SEND_JIRA, SEND_REQUEST, SEND_EXCUSE, END = range(8)

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
    reply += "\n\n\n\nВыбери новую задачу или заверши общение клавишей Done"
    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)   
    
    print("user:", text)
    print("assistant:", reply)
    return CHOOSING

async def generate_excuse(update: Update, context):
    # текст входящего сообщения
    text2 = update.message.text
    text = "Придумай смешную отмазку на тему: "+text2

    # запрос
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
        max_tokens=1024,
        temperature=0.5,
    )

    # ответ
    reply = response.choices[0].message.content.strip()
    reply += "\n\n\n\nВыбери новую задачу или заверши общение клавишей Done"

    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)   
    
    print("user:", text)
    print("assistant:", reply)
    return CHOOSING

async def decompose_jira(update: Update, context):
    # текст входящего сообщения
    task_id = update.message.text
    print(task_id)
    text1 = "Декомпозируй задачу по машинному обучению: "

    jiraOptions = {'server': "https://kirillbodrin.atlassian.net", "verify": False}

    login = "volkovartem.ffbd@gmail.com"
    api = "ATATT3xFfGF0zBghLIOu7FmW_xWThRwuYrInk5cz4ts84tmjSk6MjkD9MM5hxiBYETG-UlLgClQpv2B6BkcmMi1qXTRWRiep4b-g_OY9qFMrJawAIHkazu19whwmhGUv9alWo9wOQD-45QL6ePwCq9yR_Wq5S535LdOm47j5voySW5CXXemlmH8=04C3045A"
    jira = JIRA(options=jiraOptions, basic_auth=(login, api))
    
    #jira.issue(task_id).fields.summary
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

    reply += "\n\n\n\nВыбери новую задачу или заверши общение клавишей Done"
    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)   
    
    print("user:", text)
    print("assistant:", reply)
    return CHOOSING