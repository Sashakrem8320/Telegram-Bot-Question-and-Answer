import telebot
from telebot import types
import json
from Modules import module
from Handlers import workers
from Handlers import Direct as f
bot = telebot.TeleBot(f.s["getToken"]())
task = f.s["getTask"]()
try:
    @bot.message_handler(commands=['votive_account'])
    def votive_account(message):
        if f.s["checklog"](message) == True:
            f.s["send_message"](message, 'Вы уже в аккаунте.', f.s["getMarkup"](message))
            return
        f.s["send_message"](message, 'Введите логин и пароль, например:\n*"iamanal apelsinka11"*',
                            f.s["getMarkup"](message, cancel=True))
        f.modstep(message, "mainauth")


    @bot.message_handler(commands=['start'])
    def start(message):
        f.createblank(message.from_user.id)
        f.s["send_message"](message,"Здравствуйте, *{0.first_name}*! Я бот для поиска инструкций и заданий по машиностроению.".format(message.from_user),f.s["getMarkup"](message))


    def default(message):
        try:
            if (message.text == "Задать вопрос"):
                f.s["request_for_knowledge"](message)
                f.modstep(message, "get_form")
                f.modstep(message, "attach", type="file", calln="files", call=[])
            elif (message.text == "Посмотреть вопрсы"):
                f.modvars(message.from_user.id, "tags", [])
                f.s["questdict"](message)
            elif (message.text == "Вызвать панель"):
                f.s["newpanel"](message)
            elif (message.text == "Посмотреть задержанные вопросы." and f.s["reqrank"](message.from_user.id) > 5):
                # f.modvars(message.from_user.id,"tabtocheck",True)
                f.s["onreview"](message)
            elif (message.text == "Посмотреть задержанные ответы." and f.s["reqrank"](message.from_user.id) > 5):
                # f.modvars(message.from_user.id,"tabtocheck",True)
                f.s["ansonreview"](message)

            elif (message.text == "Войти в аккаунт"):
                if f.s["checklog"](message) == True:
                    f.s["send_message"](message, 'Вы уже в аккаунте.', f.s["getMarkup"](message))
                    return
                f.s["send_message"](message, 'Введите логин и пароль, например:\n*"iamanal apelsinka11"*',
                                    f.s["getMarkup"](message, cancel=True))
                f.modstep(message, "mainauth")
            elif (message.text[0:17] == "Выйти из аккаунта"):
                f.s["logout"](message.from_user.id, message)
            elif (message.text == "В меню"):
                f.createblank(message.from_user.id)
                f.s["send_message"](message, "Возвращаем вас", f.s["getMarkup"](message))
            elif (message.text == "Поиск по тегам"):
                f.s["send_message"](message, 'Введите тег(и) в таком формате с помощью кнопок.',
                                    f.s["getMarkup"](message, tagmenu=True))
                f.modstep(message, "tagfind", calln="tags", call=[])

            elif (message.text == "Изменить свой ответ"):
                f.s["list_remuwe_answer"](message)
            elif (message.text == "Эмитировать вопрос пользователя."):
                f.s["immitation_question"](message)

                module.send_message(message,
                                    'Имитция пользователя',
                                    f.s["getMarkup"](message, definetag=True, tagmenu=True))

        except Exception as e:
            print("Error")

    @bot.message_handler(content_types=['text'])
    def main(message):
        dummies = workers.getTask()
        if f.s["getExcept"](message.text)==True:
            f.s["cancel"](message)
            return
        if not message.chat.id in dummies:
            dummies.append(message.chat.id)
            workers.save_task()
        if f.getStep(message.from_user.id)["text"]!="nilfun":
            f.onText(message)
        else:
            default(message)


    def getfileid(message):
        if message.content_type=="video":
            return message.video.file_id
        elif message.content_type=="audio":
            return message.audio.file_id
        elif message.content_type=="voice":
            return message.voice.file_id
        elif message.content_type=="photo":
            return message.photo[len(message.photo)-1].file_id

    @bot.message_handler(content_types=f.types)
    def mainfile(message):
        if f.getStep(message.from_user.id)["text"]=="get_form" and message.caption!=None:
            f.s["get_form"](message,adjust=True)
            fileid = getfileid(message)
            if fileid!=None:
                f.s["attach"](message,message.content_type,fileid)
        elif "files" in (f.getStep(message.from_user.id)["callf"]):
            fileid = getfileid(message)
            if fileid!=None:
                f.s["attach"](message,message.content_type,fileid)
        elif f.getStep(message.from_user.id)["text"]=="form_ans" and message.caption!=None:
            f.s["form_ans"](message,cap=True)
            fileid = getfileid(message)
            if fileid!=None:
                f.s["attachtoans"](message,message.content_type,fileid)
        elif "filesa" in (f.getStep(message.from_user.id)["callf"]):
            fileid = getfileid(message)
            if fileid!=None:
                f.s["attachtoans"](message,message.content_type,fileid)

    @bot.callback_query_handler(func=lambda call:True)
    def onquery(call):
        spl = call.data.split()
        if spl[0]=="check":
            f.s["openanswer"](call, int(spl[1]), int(spl[2]))
        elif spl[0]=="doanswer":
            f.s["my_answer"](call)
        elif spl[0]=="checkanswers":
            if spl[1].isdigit():
                f.s["openquestion"](call,int(spl[1]))
        elif spl[0]=="checkquestion":
            if spl[1].isdigit():
                f.s["showQuestion"](call.message,call.from_user.id,int(spl[1]),f.s["questionMarkup"],False,int(spl[2]))
        elif spl[0]=="callquestion":
            f.s["showQuestion"](call.message,call.from_user.id,int(spl[1]),f.s["questionMarkup"],False,int(spl[2]))
        elif spl[0]=="scroll":
            f.s["scroll"](call,int(spl[1]))
        elif spl[0] == "like":
           f.s["upd_like"](call)
        elif spl[0] == "confirmupload":
            f.s["confirmupload"](call)
        elif spl[0] == "declineupload":
            f.s["declineupload"](call)
        elif spl[0] == "confirmansupload":
            f.s["confirmansupload"](call)
        elif spl[0] == "declineansupload":
            f.s["declineansupload"](call)
        elif spl[0] == "alike":
           f.s["upd_alike"](call)
        elif spl[0] == "remuwe":
            f.s["remuwe_mes"](call)
        elif spl[0] == "delite":
            f.s["deliteM"](call)
        elif spl[0] == "GPT":
            f.s["gpt"](call)
        elif spl[0] == "newanswer":
            f.s["newanswer"](call)





    bot.polling(none_stop=True, interval=1)
except Exception as e:
    print("Error", e)