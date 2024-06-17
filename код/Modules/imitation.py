import telebot
from telebot import types
from Modules import module
from Modules import buttons

bot = telebot.TeleBot(module.getToken())

tags =  [

    "Конструкция",
    "проектирование машин",
    "технологии производства",
    "лазерная резка",
    "автоматизация",
    "инженерная разработка",
    "современные материалы",
    "автоматизация процессов",
    "робототехника",
    "автоматическое управление процессами",
    "автомобилестроение"
]

def immitation_question(message):
    module.send_message(message, 'Введите тему тегов',
                        module.getMarkup(message))
    ontag_i(message)

def removeltag_i(message):
    from Handlers.Direct import getStep
    a = getStep(message.from_user.id)["callt"]["tags"]
    if len(a) > 0:
        a.pop(len(a) - 1)
        if getStep(message.from_user.id)["text"] != "ontag":
            buttons.updatepanel(message.from_user.id, message.chat.id,
                                getStep(message.from_user.id)["callt"]["start"])
        else:
            bot.send_message(message.chat.id, "cur tags: " + str(getStep(message.from_user.id)["callt"]["tags"]))

def ontag_i(message):
    if message.text == "Продолжить.":
        generation(message)
    elif message.text == "Убрать последний тег.":
        removeltag_i(message)
    elif message.text in tags:
        from Handlers import Direct
        if not (message.text in Direct.getStep(message.from_user.id)["callt"]["tags"]):
            Direct.getStep(message.from_user.id)["callt"]["tags"].append(message.text)
            bot.send_message(message.chat.id,
                             "Ваши тег:" + str(Direct.getStep(message.from_user.id)["callt"]["tags"]))

def generation(message):
    from freeGPT import AsyncClient
    from asyncio import run
    from Handlers import Direct
    tema = ""
    for i in range(len(Direct.getStep(message.from_user.id)["callt"]["tags"])):
        tema += (str(Direct.getStep(message.from_user.id)["callt"]["tags"][i]) + " и ")

    async def main():
        prompt = "Сгенерируй вопрос на тематику" + tema
        try:
            resp = await AsyncClient.create_completion("gpt3", prompt)

            module.send_message(message, f"ИИ: {resp}", module.getMarkup(call.message, listmenu=True))



        except Exception as e:
            module.send_message(call.message, f"🤖: Ошибка {e}", module.getMarkup(call.message, listmenu=True))

    run(main())