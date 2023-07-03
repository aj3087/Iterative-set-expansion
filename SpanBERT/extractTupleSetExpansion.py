import spacy
from spanBertSetExpansion import spanBertResults 
from spacy_help_functions import extract_relations,create_entity_pairs
from GPT3SetExpansion import extractTuplesGPT3
import json

def extractTuple(text,method,openAiKey,relationType=0):
    '''
    Takes in a text blurb. Converts into a list of sentences. In each sentence we extract the text and the enitty label associated with it.
    returns list of (sentence,[(text,entity label)])
    '''
    #spacy.cli.download("en_core_web_lg")
    print("Annotating the webpage using spacy...")
    nlp = spacy.load("en_core_web_lg")
    config = json.load(open("./Config.json"))

    processedDoc = nlp(text)

    # Convert the text blurb into sentences
    sentences = list(processedDoc.sents)
    sentences = [ele for ele in sentences]

    print("Extracted " + str(len(sentences)) +" sentences. Processing each sentence one by one to check for presence of right pair of named entity types; if so, will run the second pipeline ...")
    
    subjEntity = config["relationType"][relationType-1]["Subject"]
    objEntity = config["relationType"][relationType-1]["Object"]
    relation = config["relationType"][relationType-1]["Relation"]

    extractedTuple = set()

    sentWithRes = 0
    for index,sent in enumerate(sentences):
        # Obtain the entity pairs in sentence object
        entity_pair = create_entity_pairs(sent,subjEntity+objEntity)
        
        if (index)%5==0 and index:
            print("Processed "+str(index)+" / "+str(len(sentences))+" sentences")
        
        # Empty Sentence skip it
        if len(entity_pair) == 0:
            continue

        # If the sentence does not contain both the entity type skip it.
        subjEntityPresence, objectEntityPresence = False, False
        
        for token,subj,object in entity_pair:
            if len(set(subjEntity).intersection(set([subj[1]]))) != 0 or len(set(subjEntity).intersection(set([object[1]]))) != 0:
                subjEntityPresence = True 
            
            if len(set(objEntity).intersection(set([subj[1]]))) != 0 or len(set(objEntity).intersection(set([object[1]]))) != 0:
                objectEntityPresence = True 

            # We found mathcing entity for both subject and object so we can break now
            if subjEntityPresence and objectEntityPresence:
                break
        
        if subjEntityPresence and objectEntityPresence:
            # Convert into SPAN BERT input Form
            formatInput = [{'tokens':ele[0] , "subj": ele[1], "obj": ele[2]} for ele in entity_pair]
            sentWithRes+=1
            # Obtaining the predictions
            if method == "-spanbert":
                prediction = spanBertResults(formatInput)
                n = len(prediction)
                for i in range(n):
                    if method == "-spanbert":
                        pred = list(prediction[i][0].split(":"))
                        if len(pred)>1 and pred[1] == relation:
                            extractedTuple.add((formatInput[i]["subj"][0],formatInput[i]["obj"][0],prediction[i][1]))

                            print("\t == "+"Extracted Relation"+" ==")
                            print("Input tokens:",formatInput[i]['tokens'])
                            print("Output Confidence:",prediction[i][1],"; Subject:",formatInput[i]["subj"][0],";Object:",formatInput[i]["obj"][0])
                            print("Adding to set of Extracted relations")
                            print("====================================")
            else:
                prediction = extractTuplesGPT3(formatInput,relationType,openAiKey)
                n = len(prediction)
                for i in range(n):
                    for ele in prediction[i]:     
                        extractedTuple.add(ele)
                        print("\t == "+"Extracted Relation"+" ==")
                        print("Input tokens:",formatInput[i]['tokens'])
                        print("Output Confidence:",ele[2],"; Subject:",ele[0],";Object:",ele[1])
                        print("Adding to set of Extracted relations")
                        print("====================================")


    
    print("Extracted annotations for "+str(sentWithRes)+ " out of total " + str(len(sentences))+ " sentences")
    return extractedTuple



    

        
    

#print(processText("Bill Gates stepped down as chairman of Microsoft in February 2014 and assumed a new post as technology adviser to support the newly appointed CEO Satya Nadella.",2))
