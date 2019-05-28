#!/usr/bin/env python
# coding: utf-8

# In[1]:


import string
from zhon.hanzi import punctuation
import copy
import numpy as np
import operator
from tqdm import tqdm
from functools import reduce


# In[2]:


f = open(r'C:\Users\sdfj\Desktop\NLP第二次实验\corpus_for_ass2train.txt','r',encoding='gb18030',errors='ignore')
text = f.read()
f.close()
#text = text.split()


# In[3]:


print(len(text))
print(type(text))
{key: None for key in punctuation}


# In[4]:


temp_dic = {key: None for key in punctuation}
temp_dic = { '！':'。','？':'。','﹔':'。','，':'。'}#表示句子结尾的全部变为句号
trantab = str.maketrans(temp_dic)
out = text.translate(trantab)
out = out.split()
print(out)
#with open("out.txt","w") as f:
#        f.write(out) 


# In[5]:


dic_table = list({}.fromkeys(out).keys())
v_len = len(dic_table)
print(len(out))
print(type(out))


# In[6]:


#创建字典
dic = dict.fromkeys(dic_table,None)
dic = {key:dict.fromkeys(['head'],0) for key in dic}


# In[7]:


out.insert(0,'。')#在文首加入句号，便于表示原文首为句首
print(len(out))


# In[8]:


print(out[15479],out[15480])
print(dic[out[1]])


# In[9]:


for each in range(len(out)):
    if out[each-1] == '。':        
        dic[out[each]]['head'] += 1
        continue            
    if out[each] == '。':
            continue            
    else:
        if out[each] in dic[out[each-1]]:
            dic[out[each-1]][out[each]] += 1
        else:
            dic[out[each-1]][out[each]] = 1
        continue            


# In[10]:


head_sum = 0
for key in dic:
    head_sum += dic[key]["head"]
print(head_sum)


# In[11]:


def gailv(whole):
    #print("whole,",whole)
    temp = 0
    whole_max = []
    for each in whole:
        p = 1
        for count in range(len(each)):
            temp_down = 0
            
            if each[count] in punctuation:
                #print("he:",each[count-1])
                continue
           # print(each[count])
            if each[count-1] in dic and each[count] in dic[each[count-1]]:
                if count == 0:
                    temp_up = dic[each[0]]["head"]
                else:
                    temp_up = dic[each[count-1]][each[count]]
            else:
                    temp_up = 0
                    
            if each[count] in dic:
                if each[count-1] in dic:
                    temp_down = sum(dic[each[count-1]].values())
                else:
                    temp_down = 0
            if count == 0:
                p *= (1+temp_up)/(v_len + head_sum)
            else:  
                p *= (1+temp_up)/(v_len + temp_down)
        if p > temp:
            temp = p
            #print("each:",each)
            whole_max = each.copy()
    return whole_max
        


# In[12]:


max_len = 8
txt = '江主席分别会见美国客人新华社北京１月１６日电（记者谭国器）国家主席江泽民今天在中南海会见了美国联邦快递公司董事长弗雷德里克·史密斯及由他率领的该公司董事会代表团。'#党/却/一直/无微不至/地/关心/我们
def cut(txt,before=[]):
    """切到词就停"""
    if len(txt) == 0:
        return 0
    for part in range(min(max_len,len(txt)),0,-1):
        if txt[:part] in dic_table or txt[:part] in punctuation:#在字典中 
            #print(txt[:part])
            before.append(txt[:part])
           # print("txt:",txt[:part],"len",len(txt[part:]),'after',txt[part:])
            cut(txt[part:],before)
            break
        else:#不在
            if(len(txt[:part]) == 1):
                before.append(txt[:part])
                cut(txt[part:],before)
            continue
    return 0

whole = []
cut(txt,whole)
print(whole)


# In[13]:


max_len = 8
txt = '江主席分别会见'#党/却/一直/无微不至/地/关心/我们
def cuthou(txt,after=[]):
    """切到词就停"""
    if len(txt) == 0:
        return 0
   # print(txt)
    for part in range(min(max_len,len(txt)),0,-1):
        if txt[-part:] in dic_table or txt[-part:] in punctuation:#在字典中 
            #print('here',txt[-part:])
            after.append(txt[-part:])
           # print("txt:",txt[:-part],"len",len(txt[-part:]),'after',txt[-part:])
            cuthou(txt[:-part],after)
            break
        else:#不在
            if(len(txt[-part:]) == 1):
                after.append(txt[-part:])
                cuthou(txt[:-part],after)
            continue
    return 0

result = []
cuthou(txt,result)
print(list(reversed(result)))


# In[14]:


max_len = 8
txt = '全国各地积极开展走访慰问困难企业和特困职工的送温暖活动，'#党/却/一直/无微不至/地/关心/我们
def cut_all(txt,whole,before=[]):
    """切出所有词"""
    #if len(txt) == 0:
        #print(result)
       # whole.append(temp)
        #return result
    for part in range(min(max_len,len(txt)),0,-1):
        temp = copy.deepcopy(before)
        if txt[:part] in dic_table or txt[:part] in punctuation:#在字典中或是标点 
            #print(txt[:part])
            temp.append(txt[:part])
            #print("txt:",txt[:part],"len",len(txt[part:]),'after',txt[part:])
            #print("temp:",temp)
            if len(txt[part:]) == 0:
                whole.append(temp)
            cut_all(txt[part:],whole,temp)
        else:#不在
            if(len(txt[:part]) == 1):
                temp.append(txt[:part])
                cut_all(txt[part:],whole,temp)
            continue
    return 0
#whole = []
#result = []
#cut_all(txt,whole,result)
#print(whole)


# In[19]:


#for i in whole:
#    print(i,"\n")


# In[ ]:


#test = gailv(whole)
#print(test)


# In[20]:


#for each in test:
#    print(each," ",end="")


# In[35]:


def open_f(path):
    f = open(path,'r',errors='ignore')
    txt = f.read()
    #print("txt:",txt)
   # txt.replace("\n","")
    f.close()
    #print(txt)
    pos = -1
    t = []
    for each in range(len(txt)):
        #print(txt[each])
        if txt[each] == '，' or txt[each] == '。' or txt[each] == '？' or txt[each] == '！' or txt[each] == '；' or txt[each] == '、'or txt[each] == '（' or txt[each] == '）':
            t.append(txt[pos+1:each + 1])
            pos = each
    #print(t)
    return t 
t = open_f(r'C:\Users\sdfj\Desktop\corpus_for_ass2test.txt')
ad = 0
#print(t)


# In[36]:


#def main(): 
txt = open_f(r'C:\Users\sdfj\Desktop\corpus_for_ass2test.txt')
#txt = open_f(r'C:\Users\sdfj\Desktop\t.txt')
#txt = r'江主席分别会见美国客人新华社北京１月１６日电（记者谭国器）国家主席江泽民今天在中南海会见了美国联邦快递公司董事长弗雷德里克·史密斯及由他率领的该公司董事会代表团。'
#print(type(txt))
final = []
for s in tqdm(txt):
    #print("s:",s)  
    whole = []
    result = []
    if len(s) > 20:
        cut(s,whole)
        #print("q:",whole)
        cuthou(s,result)
        #print("h",list(reversed(result)))
        t = gailv([whole,list(reversed(result))])
        final.append(t)
    else:
        cut_all(s,whole,result)
        #print(whole)
        t = gailv(whole)
        final.append(t)
print(final)
    
#if __name__=='__main__': 
 #   main()


# In[37]:


print(final)


# In[21]:


for i in final:
    for each in range(len(i)):
        if i[each]=='\n':
            print(i[each],end='')
        else:
            print(i[each],"",end='')


# In[40]:


with open('out.txt','w') as f:
    for i in final:
        for each in range(len(i)):
            if i[each]=='\n':
                print(i[each],end='',file=f)
            else:
                print(i[each],"",end='',file=f)    


# In[ ]:


#dic = dict.fromkeys(dic_table,None)
#dic = {key:dict.fromkeys(dic_table,None) for key in dic}


# In[ ]:


#list_table = list({}.fromkeys(out).keys())
#leng = len(list_table)
#list_in = [None]*leng#内部列表
#list_table = []
#for i in range(leng):
#    list_table.append(copy.deepcopy(list_in))

