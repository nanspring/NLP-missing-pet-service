# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import json
from ontology.ontology import load

def match_pattern_target(pattern,target,ont):
    match=False
    node_name=[]
    visited=[]
    node_name.append('root')
    visited.append('root')
    while(len(node_name)!=0):
        if(node_name[0]=='root'):
            curr_node_name=target[node_name.pop(0)]
        else:
            curr_node_name=node_name.pop(0)
        #print(target[curr_node_name]['type'],pattern['root'])
        try:
            if(target[curr_node_name]['type']==pattern['root'] or ont[pattern['root']]>target[curr_node_name]['type']):##if the current node of target match pattern root node, check match
                #print('find match')
                match=checkMatch(pattern,target,curr_node_name,ont)
                #print(match)
        except:
            pass
        if(match==True):
            return match
        for role in target[curr_node_name]['roles']:#roles == 'experiencer','neutral'...etc
            if(target[curr_node_name]['roles'][role][0:1]=='#'and target[curr_node_name]['roles'][role][1:] not in visited):
                node_name.append(target[curr_node_name]['roles'][role][1:])
                visited.append(target[curr_node_name]['roles'][role][1:])
    return match

def checkMatch(pattern,target,curr_node,ont):##use dfs to check if pattern match target
    if(pattern['root']=='NONE' or pattern['root']==target[curr_node]['type'] or pattern['root']>ont[target[curr_node]['type']]):
        #print('curr compare ',pattern['root'],target[curr_node]['type'])
        b=True
        for k, v in pattern.items():
            #print('key ',k,' value ',v)
            if(k.upper() in target[curr_node]['roles']):#experiencer
                if isinstance(v, dict):
                    #print('is in')
                    next_t_node=str(target[curr_node]['roles'][k.upper()]).partition("#")[2].partition("'")[0]
                    #print('next_t_node ',next_t_node)
                    #print('next node ',next_t_node,target[next_t_node]['type'])
                    b=(b and checkMatch(v,target,next_t_node,ont))
            elif(k!='root'):
                return False
        return b
    else:
        return False

def read_target(j,i):
    target_map={}
    for n in range(j,i):
        target_graph_file='missing-pet-service/target/'+str(n)+'.json'
        t_file=open(target_graph_file).read()
        #print(target_graph_file)
        target=json.loads(t_file)
        target=target[0]
        target_map[n]=(target)
    return target_map

def trips_command(customer_sentences,i):
    cs_dict={}
    for sentence in customer_sentences:
        sentence = '"{}"'.format(sentence)
        cs_dict[i]=sentence
        command = "trips-web "+(sentence)+(" > missing-pet-service/target/"+str(i)+".json")
        i+=1
        #print(command)
        os.system(command)
    return i,cs_dict

def read_pattern(pattern_file_name):
    pattern_dict={}
    pattern_match_dict={}
    knowledge_base={}
    for filename in pattern_file_name:
        path='missing-pet-service/pattern/'+filename+'.json'
        p_file=open(path).read()
        pattern=json.loads(p_file)
        pattern_dict[filename]=pattern
        knowledge_base[filename]=[]
        pattern_match_dict[filename]=False
    return pattern_dict,pattern_match_dict,knowledge_base

def check_match(pattern_match_dict,pattern_dict,target_map,knowledge_base,cs_dict,ont):
    for p_key in pattern_dict:
    #print('p ',p)
        p=pattern_dict[p_key]
        for t_key in target_map:
            t=target_map[t_key]
            if(match_pattern_target(p,t,ont)):
                pattern_match_dict[p_key]=True
                #print('p_key ',p_key)
                knowledge_base[p_key].append(extract_info(p,t,cs_dict[t_key],ont))
    #print(pattern_match_dict)
    return pattern_match_dict,knowledge_base

def extract_info(pattern,target,sentence,ont):
    node_name=[]
    visited=[]
    node_name.append('root')
    visited.append('root')
    key=None
    while(len(node_name)!=0):
        if(node_name[0]=='root'):
            curr_node_name=target[node_name.pop(0)]
        else:
            curr_node_name=node_name.pop(0)
        try:
            if(target[curr_node_name]['type']==pattern['root'] or ont[pattern['root']]>target[curr_node_name]['type']):##if the current node of target match pattern root node, check match
                key=target[curr_node_name]['roles']['LEX'].lower()
                break
        except:
            pass
        for role in target[curr_node_name]['roles']:#roles == 'experiencer','neutral'...etc
            if(target[curr_node_name]['roles'][role][0:1]=='#'and target[curr_node_name]['roles'][role][1:] not in visited):
                node_name.append(target[curr_node_name]['roles'][role][1:])
                visited.append(target[curr_node_name]['roles'][role][1:])
    #print('key ',key)
    output=sentence[sentence.find(key)+len(key)+1:-1]
    #print(output)
    return output

def ask_question(pattern_match_dict,pattern_rules):
    key=''
    for p_key in pattern_match_dict:
        #print(p_key)
        if(pattern_match_dict[p_key]==False):
            key=p_key
            break
    if(key==''):
        return 'Everything is done! Great Job!'
    else:
        return pattern_rules[key]
    
def all_fulfill(pattern_match_dict):
    for key in pattern_match_dict:
        if(pattern_match_dict[key]==False):
            return False
    return True


def final_message(kb):
    myname=' '.join(kb['my-name'])
    time=' '.join(kb['lost-time'])
    location=' '.join(kb['lost-location'])
    kind=' '.join(kb['pet-kind'])
    petname=' '.join(kb['petname'])
    descrip=' '.join(kb['pet-description'])
    number=' '.join(kb['contact-number'])
    result="Missing-Report \n"
    result+=myname+" lost his or her pet "+time+" "+location+"."
    result+="Pet is "+kind+". Pet name is "+petname+"."
    result+="\n Pet character: "+descrip+" \n"
    result+="Please call phone number "+number+" to contact "+myname+" if you find the pet. Thank you."
    return result
#-------------------------------------------------------------------
def missing_pet_service():    
    pattern_file_name=['pet-description','contact-number','my-name','lost-time',
                       'lost-location','pet-kind','petname']
    pattern_rules={'pet-description':'Can you describe your pet?',
                  'contact-number':'What is your phone number?',
                  'my-name':'What is your name?',
                  'petname':'What is your pet name?',
                  'lost-time':'When did your pet lost?',
                  'lost-location':'Where did your pet lost?',
                  'pet-kind':'What kind of animals is your pet?'}
    i=0
    j=0
    ont = load()   
    print('Hi. This is the missing pet service. How can I help you?')
    pattern_dict,pattern_match_dict,knowledge_base=read_pattern(pattern_file_name)
    while(all_fulfill(pattern_match_dict)==False):
        #customer_input="My name is Mary.I lost my pet.My pet is a dog.My pet name is Tom.My dog has brown hair.The dog was lost at a restaurant near Rochester.The dog was lost yesterday around 5pm.My phone number is 123456."
        customer_input=input('Your response: ')
        customer_sentences=customer_input.strip().split('.')
        customer_sentences = filter(None, customer_sentences)
        #print(customer_sentences)
        i,cs_dict=trips_command(customer_sentences,i)   
        target_map=read_target(j,i)
        j=i
        #print(pattern_match_dict)
        pattern_match_dict,knowledge_base=check_match(pattern_match_dict,pattern_dict,target_map,knowledge_base,cs_dict,ont)
        #print(knowledge_base)
        print(ask_question(pattern_match_dict,pattern_rules))
    print(final_message(knowledge_base))

def missing_pet_service_test():    
    pattern_file_name=['pet-description','contact-number','my-name','lost-time',
                       'lost-location','pet-kind','petname']
    pattern_rules={'pet-description':'Can you describe your pet?',
                  'contact-number':'What is your phone number?',
                  'my-name':'What is your name?',
                  'petname':'What is your pet name?',
                  'lost-time':'When did you lost your pet?',
                  'lost-location':'Where did you lost your pet?',
                  'pet-kind':'What kind of animals is your pet?'}
    i=0
    j=0
    ont = load()   
    print('Hi. This is the missing pet service. How can I help you?')
    pattern_dict,pattern_match_dict,knowledge_base=read_pattern(pattern_file_name)   
    print(pattern_dict.keys())
    customer_input="My name is Mary.I lost my pet.My pet is a dog.My pet name is Tom.My dog has brown hair.The dog was lost at a restaurant near Rochester.The dog was lost yesterday around 5pm.My phone number is 123456."
    #customer_input=input('Your response: ')
    customer_sentences=customer_input.strip().split('.')
    customer_sentences = filter(None, customer_sentences)
    #print(customer_sentences)
    i,cs_dict=trips_command(customer_sentences,i)   
    target_map=read_target(j,i)
    #print(pattern_match_dict)
    pattern_match_dict,knowledge_base=check_match(pattern_match_dict,pattern_dict,target_map,knowledge_base,cs_dict,ont)
    print(knowledge_base)
    print(ask_question(pattern_match_dict,pattern_rules))
    print(final_message(knowledge_base))
missing_pet_service()