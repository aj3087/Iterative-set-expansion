import os
import json
import openai
import ast
import re
import time
import spacy

def get_openai_completion(prompt, model, max_tokens, temperature = 0.2, top_p = 1, frequency_penalty = 0, presence_penalty =0):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    response_text = response['choices'][0]['text']
    return response_text

def convertStrToList(str):
    pattern = '\((\w+\s*\w+),\s+(\w+)\)'
    res = re.findall(pattern,str)
    res = [(ele[0],ele[1],1) for ele in res]
    return res

def filterNoneEntries(tupleList):
    newTupleList = []
    for tuple in tupleList:
        if tuple[0] == "None" or tuple[1]=="None" or tuple[0] == "Unknown" or tuple[1]=="Unknown":
            continue
        newTupleList.append(tuple) 
    return newTupleList

def extractTuplesGPT3(inputFormat,relationType,openAiKey=""):
    config = json.load(open("./Config.json"))

    prompt = config["relationType"][relationType-1]["GPT3-Prompt"]
    
    if openAiKey == "":
        openAiKey = config["OpenAi_Key"]

    prompt_text = prompt

    openai.api_key = openAiKey

    model = 'text-davinci-003'
    max_tokens = 100
    temperature = 0.05
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0
    # making the call to OpenAI API to fetcch the results.
    res = []

    sentenceSet = set()
    for ele in inputFormat:
        sentence = prompt + " ".join(ele['tokens'])
        if sentence not in sentenceSet:
            sentenceSet.add(sentence)
            time.sleep(3) 
            response_text = get_openai_completion(sentence, model, max_tokens, temperature, top_p, frequency_penalty, presence_penalty)
            result_str = response_text.strip().strip('\n')
            if result_str:
                val = convertStrToList(result_str)
                res.append(filterNoneEntries(val))
            else:
                res.append([])
        else:
            res.append([])

    return res
#print(extractTuplesGPT3('''Bill Gates stepped down as chairman of Microsoft in February 2014 and assumed a new post as technology adviser to support the newly appointed CEO Satya Nadella. Zuckerberg founded the company META.''',2))


