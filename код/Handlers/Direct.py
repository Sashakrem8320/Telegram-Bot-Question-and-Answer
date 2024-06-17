import telebot
from Modules import answer
from Modules import authorization
from Modules import builder
from Modules import buttons
from Modules import define
from Modules import module
from Modules import read
from Modules import tags
from Modules import like
from Handlers import moderation
from Modules import imitation


steps = {

}

def nilfun(message):
    print("undefined.")

s = {
    "my_answer":answer.my_answer,
    "form_ans":answer.form_ans,
    "addacc":authorization.addacc,
    "checklog":authorization.checklog,
    "getaccname":authorization.getaccname,
    "logout":authorization.logout,
    "mainauth":authorization.mainauth,
    "refresh":authorization.authrefresh,
    "reqrank":authorization.reqrank,
    "updateauth":authorization.updateauth,
    "new_task":builder.new_task,
    "getTask":builder.getTask,
    "save_task":builder.save_task,
    "new_task2":builder.new_task2,
    "getTask2":builder.getTask2,
    "save_task2":builder.save_task2,
    "request_for_knowledge":buttons.request_for_knowledge,
    "ask_user_to_insert_a_tag":define.ask_user_to_insert_a_tag,
    "get_form":define.get_form,
    "cancel":module.cancel,
    "getExcept":module.getExcept,
    "getMarkup":module.getMarkup,
    "getToken":module.getToken,
    "send_message":module.send_message,
    "openanswer":read.openanswer,
    "openquestion":read.openquestion,
    "in_tag":tags.in_tag,
    "get_likes":like.get_likes,
    "get_alikes":like.get_alikes,
    "upd_like":like.upd_like,
    "upd_alike":like.upd_alike,
    "questionMarkup":buttons.questionMarkup,
    "answerMarkup":read.answerMarkup,
    "send_file":module.send_file,
    "attach":define.attachfile,
    "attachtoans":answer.attachfile,
    "confirmans":answer.confirmans,
    "ontag":tags.ontag,
    "onreview":buttons.onreview,
    "reviewstep":buttons.reviewstep,
    "ansonreview":buttons.ansonreview,
    "ansreviewstep":buttons.ansreviewstep,
    "tagfind":tags.tagfind,
    "confirmupload":moderation.confirmupload,
    "confirmansupload":moderation.confirmansupload,
    "showQuestion":buttons.showQuestion,
    "declineupload":moderation.declineupload,
    "declineansupload":moderation.declineansupload,
    "questdict":buttons.questdict,
    "scroll":buttons.scroll,
    "newpanel":buttons.newpanel,
    "nilfun":nilfun,
    "list_remuwe_answer":buttons.list_remuwe_answer,
    "ontag":tags.ontag,
    "tagfind":tags.tagfind,
    "remuwe_mes":buttons.remuwe_mes,
    "text_new":buttons.text_new,
    "text_confirm":buttons.text_confirm,
    "deliteM":buttons.deliteM,
    "attachfileedit":buttons.attachfileedit,
    "confirmdel":buttons.confirmdel,
    "gpt": buttons.gpt,
    "immitation_question":imitation.immitation_question,
    "blok": moderation.blok,
    "newanswer": buttons.newanswer,
    "text_new_answer":buttons.text_new_answer,
    "text_confirm_ans":buttons.text_confirm_ans,
}

types = [
    "video",
    "audio",
    "voice",
    "photo",
]

bot = telebot.TeleBot(module.getToken())

def createblank(id):
    if (id in steps) and ("listpanel" in steps[id]["callt"]): bot.delete_message(id,steps[id]["callt"]["listpanel"])
    steps[id]={"text":"nilfun","file":"nilfun","callt":{},"callf":{}}
    return steps[id]

def modstep(message,func,type="text", calln="Empty", call=None, act=False):
    id = None
    if isinstance(message,int):
        id = message
    else:
        id = message.from_user.id
    if not id in steps:
        createblank(id)
    steps[id][type]=func
    if call!=None:
        modvars(id,calln,call,type)
    if act==True:
        onText(message)

def modvars(id,calln,call,type="text"):
    steps[id]["call" + type[0:1]][calln]=call

def getStep(id):
    if id in steps:
        return steps[id]
    else:
        return createblank(id)


def onText(message):

    if s["getExcept"](message.text)==True:
        s["cancel"](message)
        return
    typ = "text"
    if message.content_type in types:
        typ = "file"
    act = None
    if not steps[message.from_user.id]:
        createblank(id)
    s[steps[message.from_user.id][typ]](message)