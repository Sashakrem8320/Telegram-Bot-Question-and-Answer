import telebot
from telebot import types
from Modules import module
from Modules import builder
from Modules import like
from Modules import sorting

bot = telebot.TeleBot(module.getToken())
fill = 3

photoid = open('photo.jpg', "rb")


def reviewstep(message):
    if message.text.isdigit():
        task = builder.getTask2()
        id = int(message.text) - 1
        from Handlers import Direct
        if id + 1 > len(Direct.getStep(message.from_user.id)["callt"]["Checktable"]) or id < 0: return
        trueid = Direct.getStep(message.from_user.id)["callt"]["Checktable"][id]
        if not sorting.findbyunique(trueid["uniqueid"], task): return
        if len(trueid["attachments"]) == 1:
            module.send_file(message, trueid["attachments"][0]["typ"], trueid["attachments"][0]["id"],
                             caption=trueid["text"], reply_markup=defineMarkup(0, 0, trueid["uniqueid"]))
        else:
            for i in trueid["attachments"]:
                module.send_file(message, i["typ"], i["id"])
            mess = bot.send_message(message.chat.id, text=str(trueid["text"]),
                                    reply_markup=defineMarkup(0, 0, trueid["uniqueid"]))


def onreview(message):
    num = 0
    task = builder.getTask2()
    newtab = sorting.sortempty(task)
    txt = "На удержании: " + str(len(newtab))
    for c, i in enumerate(newtab):
        if newtab[c]["id"] != 0:
            ftxt = newtab[c]["text"]
            if len(ftxt) > 75: ftxt = ftxt[0:75] + "..."
            txt += "\n" + str(c + 1) + ". От " + newtab[c]["name"] + " `(" + str(newtab[c]["id"]) + ")`: " + ftxt
    from Handlers import Direct
    module.send_message(message, txt, module.getMarkup(message, cancel=True))
    Direct.modstep(message, "reviewstep", calln="Checktable", call=newtab)


def ansreviewstep(message):
    if message.text.isdigit():
        task = builder.getTask3()
        id = int(message.text) - 1
        from Handlers import Direct
        if id + 1 > len(Direct.getStep(message.from_user.id)["callt"]["Checktable"]) or id < 0: return
        trueid = Direct.getStep(message.from_user.id)["callt"]["Checktable"][id]
        truestid = builder.getTask()[trueid["belongs"]]
        if not "answers" in truestid or not sorting.findbyunique(trueid["uniqueid"], task): return
        if len(trueid["attachments"]) == 1:
            module.send_file(message, trueid["attachments"][0]["typ"], trueid["attachments"][0]["id"],
                             caption=trueid["text"],
                             reply_markup=define2Markup(trueid["uniqueid"], trueid["belongs"], truestid["uniqueid"]))
        else:
            for i in trueid["attachments"]:
                module.send_file(message, i["typ"], i["id"])
            mess = bot.send_message(message.chat.id, text=str(trueid["text"]),
                                    reply_markup=define2Markup(trueid["uniqueid"], trueid["belongs"],
                                                               truestid["uniqueid"]))


def ansonreview(message):
    num = 0
    task = builder.getTask3()
    newtab = sorting.sortempty(task)
    txt = "На удержании: " + str(len(newtab))
    for c, i in enumerate(newtab):
        if newtab[c]["id"] != 0:
            ftxt = newtab[c]["text"]
            if len(ftxt) > 75: ftxt = ftxt[0:75] + "..."
            txt += "\n" + str(c + 1) + ". От " + newtab[c]["name"] + " `(" + str(newtab[c]["id"]) + ")`: " + ftxt
    from Handlers import Direct
    module.send_message(message, txt, module.getMarkup(message, cancel=True))
    Direct.modstep(message, "ansreviewstep", calln="Checktable", call=newtab)


def questionMarkup(id, num, uid):
    c = telebot.types.InlineKeyboardButton(text="Ответы", callback_data="checkanswers " + str(num))
    d = telebot.types.InlineKeyboardButton(text="Ответить", callback_data="doanswer " + str(num))

    l = telebot.types.InlineKeyboardButton(text=str(like.get_likes(num)) + " 👍",
                                           callback_data="like " + str(num) + " " + str(id), row_width=4)
    board = types.InlineKeyboardMarkup()
    board.add(l, c, d)
    if builder.getTask()[num]["gpt"] == 0:
        g = telebot.types.InlineKeyboardButton(text="Сгенерировать ответ с ИИ", callback_data="GPT " + str(num))
        board.add(g)
    if builder.getTask()[num]["id"] == id:
        x = telebot.types.InlineKeyboardButton(text="Изменить", callback_data="remuwe " + str(num))
        y = telebot.types.InlineKeyboardButton(text="Удалить", callback_data="delite " + str(num))

        board.add(x, y)
    return board


def defineMarkup(id, num, uid):
    c = telebot.types.InlineKeyboardButton(text="Сохранить", callback_data="confirmupload " + str(uid))
    d = telebot.types.InlineKeyboardButton(text="Отклонить", callback_data="declineupload " + str(uid))
    board = types.InlineKeyboardMarkup()
    board.add(c, d)
    return board


def define2Markup(id1, id2, uid):
    c = telebot.types.InlineKeyboardButton(text="Сохранить", callback_data="confirmansupload " + str(id1))
    d = telebot.types.InlineKeyboardButton(text="Отклонить", callback_data="declineansupload " + str(id1))
    b = telebot.types.InlineKeyboardButton(text="Показать", callback_data="checkquestion " + str(id2) + " " + str(uid))
    board = types.InlineKeyboardMarkup()
    board.add(c, b, d)
    return board


def scroll(call, start):
    taglist = []
    from Handlers import Direct
    modmode = "modmode" in Direct.getStep(call.from_user.id)["callt"]
    if "tags" in Direct.getStep(call.from_user.id)["callt"]:
        taglist = Direct.getStep(call.from_user.id)["callt"]["tags"]
    temptab = sorting.fullsort(builder.getTask(), taglist, modmode)
    if len(temptab) > 0:
        text, but = createdict(temptab, start, taglist)
        bot.edit_message_caption(text, call.message.chat.id, call.message.id, reply_markup=but, parse_mode="Markdown")
        # bot.edit_message_text(text,call.message.chat.id,call.message.id,reply_markup=but,parse_mode="Markdown")


def showQuestion(message, id, i, markupfunc, mod, uid):
    task = builder.getTask()
    if task[i]["id"] == 0: return
    if mod:
        task = builder.getTask2()
    if len(task[i]["attachments"]) == 1:
        module.send_file(message, task[i]["attachments"][0]["typ"], task[i]["attachments"][0]["id"],
                         reply_markup=markupfunc(id, i, uid),
                         caption="От " + task[i]["name"] + "\n" + str(task[i]["text"]))
    else:
        for c in task[i]["attachments"]:
            module.send_file(message, c["typ"], c["id"])
        mess = bot.send_message(message.chat.id, text="От " + task[i]["name"] + "\n" + str(task[i]["text"]),
                                reply_markup=markupfunc(id, i, uid))


def createdictbuttons(tab, start):
    newtab = []
    board = types.InlineKeyboardMarkup()
    minn = min([fill, len(tab) - start])
    for i in range(fill):
        if minn <= i:
            newtab.append(telebot.types.InlineKeyboardButton(text="---", callback_data="empty", row_width=4))
        else:
            newtab.append(telebot.types.InlineKeyboardButton(text=str(start + i + 1),
                                                             callback_data="callquestion " + str(
                                                                 tab[i + start]["number"]) + " " + str(
                                                                 tab[i + start]["uniqueid"]), row_width=4))

    board.add(*newtab)
    a = telebot.types.InlineKeyboardButton(text="<----", callback_data="scroll " + str(start - fill))
    if start - fill < 0:
        a = None
    c = telebot.types.InlineKeyboardButton(text="---->", callback_data="scroll " + str(start + fill))
    if start + fill + 1 > len(tab):
        c = None
    if a and c:
        board.add(a, c)
    elif a:
        board.add(a)
    elif c:
        board.add(c)
    return board


def newpanel(message, start=0):
    num = 0
    task = builder.getTask()
    taglist = []
    from Handlers import Direct
    modmode = "modmode" in Direct.getStep(message.from_user.id)["callt"]
    if "tags" in Direct.getStep(message.from_user.id)["callt"]:
        taglist = Direct.getStep(message.from_user.id)["callt"]["tags"]
    temptab = sorting.fullsort(task, taglist, modmode)
    st = True
    if ("listpanel" in Direct.getStep(message.from_user.id)["callt"]): bot.delete_message(message.chat.id,
                                                                                          Direct.getStep(
                                                                                              message.from_user.id)[
                                                                                              "callt"]["listpanel"])
    if len(temptab) > 0:
        mess, but = createdict(temptab, start, taglist)
        mes = bot.send_photo(message.chat.id, open('photo.jpg', "rb"), mess, reply_markup=but, parse_mode="Markdown")
        Direct.modvars(message.from_user.id, "listpanel", mes.message_id)
        Direct.modvars(message.from_user.id, "start", start)
        # for i in range(minn):
        # showQuestion(message.chat.id,message.from_user.id,i["n"],markupfunc,modmode,i["uid"])
    else:
        txt = "Вопросов нет"
        if "tags" in Direct.getStep(message.from_user.id)["callt"] and len(
                Direct.getStep(message.from_user.id)["callt"]["tags"]) > 0:
            txt += "\n`(Теги: "
            for i in Direct.getStep(message.from_user.id)["callt"]["tags"]:
                txt += i + ","
            txt = txt[0:-1] + ")`"
        mess = bot.send_photo(message.chat.id, open('photo.jpg', "rb"), txt, parse_mode="Markdown")
        # mess = bot.send_message(message.chat.id,txt,parse_mode="Markdown")
        Direct.modvars(message.from_user.id, "listpanel", mess.message_id)
        Direct.modvars(message.from_user.id, "start", 0)


def updatepanel(userid, chatid, start=0):
    from Handlers.Direct import getStep
    if "listpanel" in getStep(userid)["callt"]:
        taglist = []
        from Handlers import Direct
        modmode = "modmode" in Direct.getStep(userid)["callt"]
        if "tags" in Direct.getStep(userid)["callt"]:
            taglist = Direct.getStep(userid)["callt"]["tags"]
        temptab = sorting.fullsort(builder.getTask(), taglist, modmode)
        if len(temptab) > 0:
            text, but = createdict(temptab, start, taglist)
            # bot.edit_message_media(text,chatid,getStep(userid)["callt"]["listpanel"],reply_markup=but,parse_mode="Markdown")
            bot.edit_message_caption(text, chatid, getStep(userid)["callt"]["listpanel"], reply_markup=but,
                                     parse_mode="Markdown")
        else:
            txt = "Вопросов нет"
            if "tags" in getStep(userid)["callt"] and len(getStep(userid)["callt"]["tags"]) > 0:
                txt += "\n`(Теги: "
                for i in getStep(userid)["callt"]["tags"]:
                    txt += i + ","
                txt = txt[0:-1] + ")`"
            bot.edit_message_caption(txt, chatid, getStep(userid)["callt"]["listpanel"], parse_mode="Markdown")
            # bot.edit_message_text(txt,chatid,getStep(userid)["callt"]["listpanel"],parse_mode="Markdown")

def newanswer(call):
    module.send_message(call.message, 'Новый ответ:', module.getMarkup(call.message, cancel=True))
    from Handlers import Direct
    spl = call.data.split()
    id = int(spl[1])
    Direct.modstep(call.from_user.id, "text_new_answer", calln="text_new_answer", call=id)
def text_new_answer(message):
    from Handlers import Direct
    # builder.getTask()[a]["text"] = message.text
    module.send_message(message, 'Подтвердить?\n*Вы ещё можете добавить файлы.*',
                        module.getMarkup(message, choice=True))
    Direct.modstep(message.from_user.id, "text_confirm_ans", calln="textname", call=message.text)
def text_confirm_ans(message):
    start = 0
    from Handlers import Direct
    if message.text != "Да":
        if "listpanel" in Direct.getStep(message.from_user.id)["callt"]:
            start = Direct.getStep(message.from_user.id)["callt"]["start"]
        Direct.createblank(message.from_user.id)
        module.send_message(message, "Возвращаем в меню", module.getMarkup(message, listmenu=True))
        newpanel(message, start)
        return
    a = Direct.getStep(message.from_user.id)["callt"]["text_new_answer"]
    builder.getTask2().append(
        {"number": len(builder.getTask2()), "uniqueid": (builder.getTask()[a]["uniqueid"]), "likes": [],
         "attachments": "",
         "text": Direct.getStep(message.from_user.id)["callt"]["textname"], "name": message.from_user.first_name,
         "id": message.from_user.id, "tags": [], "answers": []})
    builder.save_task2()
    builder.new_task2()
    if "listpanel" in Direct.getStep(message.from_user.id)["callt"]:
        start = Direct.getStep(message.from_user.id)["callt"]["start"]
    Direct.createblank(message.from_user.id)
    newpanel(message, start)
    module.send_message(message, 'Изменение на рассмотрение', module.getMarkup(message, listmenu=True))




def createdict(tab, start, tags=[]):
    minn = min([fill, len(tab) - start])
    txt = "Всего " + str(len(tab)) + " вопросов\n"
    if len(tags) > 0:
        txt += "`(Теги: "
        for i in tags:
            txt += i + ","
        txt = txt[0:-1] + ")`\n"
    txt += "Вопросы: " + str(start + 1) + "-" + str(start + minn) + ""
    but = []
    for i in range(minn):
        if len(tab[start + i]["text"]) > 79:
            txt += "\n*" + str(start + i + 1) + ". (" + tab[start + i]["name"] + ")* " + tab[start + i]["text"][
                                                                                         0:80] + "..." + " (" + str(
                tab[start + i]["likes"]) + "👍)"
            if len(tab[start + i]["tags"]) > 0:
                txt += "\n`(Теги: "
                for c in tab[start + i]["tags"]:
                    txt += c + ","
                txt = txt[0:-2] + ")`"
            txt += "\n"
        else:
            txt += "\n*" + str(start + i + 1) + ". (" + tab[start + i]["name"] + ")* " + tab[start + i]["text"][
                                                                                         0:80] + " (" + str(
                tab[start + i]["likes"]) + "👍)"
            if len(tab[start + i]["tags"]) > 0:
                txt += "\n`(Теги:"
                for c in tab[start + i]["tags"]:
                    txt += c + ","
                txt = txt[0:-1] + ")`"
            txt += "\n"
        but.append(str(start + i))
    return txt, createdictbuttons(tab, start)


def questdict(message, taglist=[]):
    task = builder.getTask()
    modmode = False
    markupfunc = questionMarkup
    from Handlers.Direct import getStep
    if "tabtocheck" in getStep(message.from_user.id)["callt"] and getStep(message.from_user.id)["callt"][
        "tabtocheck"] != False:
        task = builder.getTask2()
        markupfunc = defineMarkup
        modmode = True
    module.send_message(message, "Вы вошли в просмотр запросов.", markup=module.getMarkup(message, listmenu=True))
    newpanel(message)


def request_for_knowledge(message):
    module.send_message(message, 'Вы зашли в функцию по добавлению Вопросов',
                        module.getMarkup(message, cancel=True))
    module.send_message(message,
                        'Пришлите запрос \n Пример \n Какое напряжение нужно для воспламенения смеси бензина и воздуха в целиндре',
                        module.getMarkup(message, cancel=True))


def remuwe_answer(message, num):
    c = telebot.types.InlineKeyboardButton(text="Изменить", callback_data="remuwe " + str(num))
    d = telebot.types.InlineKeyboardButton(text="Удалить", callback_data="delite " + str(num))
    board = types.InlineKeyboardMarkup()
    board.add(c, d)
    return board


def list_remuwe_answer(message):
    module.send_message(message, 'Ваши вопросы', module.getMarkup(message))
    num = 0
    temptab = []
    task = builder.getTask()

    for i in range(len(task)):
        if task[i]["id"] == message.chat.id:
            bot.send_message(message.chat.id, text=str(task[i]["text"]).format(message.from_user),
                             reply_markup=remuwe_answer(message, i))


def remuwe_mes(call):
    module.send_message(call.message, 'Новый вопрос', module.getMarkup(call.message, cancel=True))
    from Handlers import Direct
    spl = call.data.split()
    id = int(spl[1])
    Direct.modstep(call.from_user.id, "attachfileedit", type="file", calln="filesa", call=[])
    Direct.modstep(call.from_user.id, "text_new", calln="text_new", call=id)


def text_new(message):
    from Handlers import Direct
    # builder.getTask()[a]["text"] = message.text
    module.send_message(message, 'Подтвердить?\n*Вы ещё можете добавить файлы.*',
                        module.getMarkup(message, choice=True))
    Direct.modstep(message.from_user.id, "text_confirm", calln="textname", call=message.text)


def attachfileedit(message, typ, id):
    from Handlers import Direct
    step = Direct.getStep(message.from_user.id)
    step["callf"]["filesa"].append({"typ": typ, "id": id})
    bot.send_message(message.chat.id, text="Файл добавлен")


def text_confirm(message):
    start = 0
    from Handlers import Direct
    if message.text != "Да":
        if "listpanel" in Direct.getStep(message.from_user.id)["callt"]:
            start = Direct.getStep(message.from_user.id)["callt"]["start"]
        Direct.createblank(message.from_user.id)
        module.send_message(message, "Возвращаем в меню", module.getMarkup(message, listmenu=True))
        newpanel(message, start)
        return

    a = Direct.getStep(message.from_user.id)["callt"]["text_new"]
    builder.getTask2().append(
        {"number": len(builder.getTask2()), "uniqueid": (builder.getTask()[a]["uniqueid"]), "likes": [],
         "attachments": Direct.getStep(message.from_user.id)["callf"]["filesa"],
         "text": Direct.getStep(message.from_user.id)["callt"]["textname"], "name": message.from_user.first_name,
         "id": message.from_user.id, "tags": [], "answers": []})
    builder.save_task2()
    builder.new_task2()
    if "listpanel" in Direct.getStep(message.from_user.id)["callt"]:
        start = Direct.getStep(message.from_user.id)["callt"]["start"]
    Direct.createblank(message.from_user.id)
    newpanel(message, start)
    module.send_message(message, 'Изменение на рассмотрение', module.getMarkup(message, listmenu=True))


def deliteM(call):
    from Handlers import Direct
    spl = call.data.split()
    id = int(spl[1])
    Direct.modstep(call.from_user.id, "confirmdel", calln="remid", call=id)
    module.send_message(call.message, "Подтвердить?", module.getMarkup(call.message, choice=True))


def confirmdel(message):
    from Handlers import Direct
    start = 0
    if message.text != "Да":
        if "listpanel" in Direct.getStep(message.from_user.id)["callt"]:
            start = Direct.getStep(message.from_user.id)["callt"]["start"]
        Direct.createblank(message.from_user.id)
        module.send_message(message, "Возвращаем в меню", module.getMarkup(message, listmenu=True))
        newpanel(message, start)
        return
    id = Direct.getStep(message.from_user.id)["callt"]["remid"]
    builder.getTask()[id] = {"id": 0}
    builder.save_task()
    builder.new_task()
    if "listpanel" in Direct.getStep(message.from_user.id)["callt"]:
        start = Direct.getStep(message.from_user.id)["callt"]["start"]
    Direct.createblank(message.from_user.id)
    newpanel(message, start)
    module.send_message(message, "Вопрос удалён", module.getMarkup(message, listmenu=True))


def gpt(call):
    spl = call.data.split()
    id = int(spl[1])
    from freeGPT import AsyncClient
    from asyncio import run
    from Handlers import Direct as f
    lt = 0
    if lt!=0:

        module.send_message(call.message, str("Ожидайте"), module.getMarkup(call.message, listmenu=True))

        async def main():
            builder.getTask()[id]["gpt"] = 1
            prompt = builder.getTask()[id]["text"]
            try:
                resp = await AsyncClient.create_completion("gpt3", prompt)

                module.send_message(call.message, f"ИИ: {resp}", module.getMarkup(call.message, listmenu=True))


                markup = types.InlineKeyboardMarkup()

                from Handlers import Direct as f
                f.modstep(call.from_user.id, "form_ans", calln="pos", call=spl[1])
                f.modstep(call.from_user.id, "attachtoans", calln="filesa", call=[], type="file")




                builder.getTask3().append(
                    {"text": resp, "likes": [], "attachments": [],
                     "id": 1467501113, "name": "ИИ", "belongs": id,
                     "uniqueid": len(builder.getTask3())})
                builder.save_task3()



            except Exception as e:
                module.send_message(call.message, f"🤖: Ошибка {e}", module.getMarkup(call.message, listmenu=True))
    else:
         module.send_message(call.message, str("Модератором была включина лайт версия, эта функция не работает попробуйте позже."), module.getMarkup(call.message, listmenu=True))
    run(main())





