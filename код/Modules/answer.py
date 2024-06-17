import telebot
from telebot import types
from Modules import module
from Modules import builder
from Modules import read
from Modules import define
from Modules import buttons
from Modules import tags
bot = telebot.TeleBot(module.getToken())


def my_answer(call):
    global spl
    markup = types.InlineKeyboardMarkup()
    spl = call.data.split()
    from Handlers import Direct as f
    f.modstep(call.from_user.id,"form_ans", calln="pos",call=spl[1])
    f.modstep(call.from_user.id,"attachtoans", calln="filesa",call=[],type="file")
    return bot.send_message(call.message.chat.id, text="Напишите ответ".format(call.message.from_user), reply_markup=markup)
    #bot.register_next_step_handler(mes, form_ans)
    #bot.send_message(call.message.chat.id, text=str(builder.getTask()[int(spl[1])]["number"]).format(call.message.from_user), reply_markup=markup)

def attachfile(message,typ,id):
    from Handlers import Direct
    step = Direct.getStep(message.from_user.id)
    step["callf"]["filesa"].append({"typ":typ,"id":id})
    bot.send_message(message.chat.id, text="Файл добавлен")

def form_ans(message,cap=False):
    from Handlers import Direct as f
    module.send_message(message,'*Вы ещё можете добавить файлы.*\nПодтвердить?',module.getMarkup(message, choice=True))
    mess = None
    if cap==False:
        mess = message.text
    else:
        mess = message.caption
    f.modstep(message.from_user.id,"confirmans",calln="text",call=mess)

def confirmans(message):
    from Handlers import Direct as f
    if message.text=="Нет":
        module.cancel(message)
        return
    data = f.getStep(message.from_user.id)
    numb = builder.getTask()[int(data["callt"]["pos"])]["number"]-1
    builder.getTask3().append({"text":data["callt"]["text"],"likes":[], "attachments":data["callf"]["filesa"], "id":message.from_user.id, "name":message.from_user.first_name,"belongs":numb, "uniqueid":len(builder.getTask3())})
    builder.save_task3()
   # builder.getTask()[numb]['answers'].append({"text":data["callt"]["text"],"likes":[], "attachments":data["callf"]["filesa"], "id":message.from_user.id, "name":message.from_user.first_name})
  #  builder.save_task3()
   # c = telebot.types.InlineKeyboardButton(text="Показать", callback_data="check " + str(numb) + " " + str(len(builder.getTask()[numb]['answers'])-1))
  #  board = types.InlineKeyboardMarkup()
   # board.add(c)
    #bot.send_message(builder.getTask()[numb]["id"], text=str("На ваш вопрос ответил(а): {0.first_name} \n"+ data["callt"]["text"]).format(message.from_user), reply_markup=board) 
    builder.new_task3()
    module.send_message(message,"Ответ принят.",module.getMarkup(message, listmenu=True))
    if ("listpanel" in f.getStep(message.from_user.id)["callt"]): 
        buttons.newpanel(message, f.getStep(message.from_user.id)["callt"]["start"])
    else:
        buttons.newpanel(message, 0)
