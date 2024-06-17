
def sorting(a):
    return a["likes"]

def likesort(tab):
    return tab.sort(reverse=True,key=sorting)


def findbyunique(id,tab):
    for c,i in enumerate(tab):
        if "uniqueid" in tab[c] and tab[c]["uniqueid"]==id:
            return c


def sortempty(tab):
    newtab = []
    for i in tab:
        if i["id"]!=0:
            newtab.append(i)
    return newtab


def fullsort(task,taglist=[],modmode=False):
    temptab = []
    from Modules.like import get_likes
    num = 0
    for i in task:
        found = True
        if i["id"]==0: 
            num+=1 
            continue
        for c in taglist:
            if not c in i["tags"]:
                found=False
                break
        if (not len(taglist)>0 or found):
            if modmode:
                temptab.append({"number":num,"name":i["name"],"uniqueid":i["uniqueid"], "text":i["text"]})
            else:
                temptab.append({"number":num,"name":i["name"],"likes":get_likes(num),"uniqueid":i["uniqueid"], "text":i["text"], "tags":i["tags"]})
        num+=1   
    if not modmode: 
        likesort(temptab)
    return temptab