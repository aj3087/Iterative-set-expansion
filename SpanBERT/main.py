from googleSearchModule import returnGoogleSearchResults
from extractText import extractText
from extractTupleSetExpansion import extractTuple
import sys
import json

def main(method,googleApiKey,googleEngineId,openAiKey,r,t,query,k):
    extractedTuple = []
    keyExtractedTuple = {}
    retrievedUrl = set()
    querySet = set()
    iter = 0

    r = int(r)
    k = int(k)
    t = float(t)
    
    config = json.load(open("./Config.json"))
    relation = config["relationType"][r-1]["Relation"]

    print("Parameters:")
    print("Client key\t=",googleApiKey)
    print("Engine key\t=",googleEngineId)
    print("OpenAi key\t=",openAiKey)
    print("Method\t=",method)
    print("Relation\t=",relation)
    print("Threshold\t=",t)
    print("Query\t=",query)
    print("# of Tuples\t=",k)


    while len(extractedTuple) < k:
        message = "="*10 + " Iteration: "+ str(iter)+ " - Query:"+ query + " "+ "="*10
        print()
        print(message)  

        querySet.add(query.lower())
        searchResults = returnGoogleSearchResults(query,googleApiKey,googleEngineId)
        
        for index,result in enumerate(searchResults):
            if result.url not in retrievedUrl:
                print("URL ( "+str(index+1)+ " / 10): "+ result.url)
                retrievedUrl.add(result.url)

                text = extractText(result.url)

                # Unable to fetch the page
                if text == '':
                    continue
                
                tupleSet = extractTuple(text,method,openAiKey,r)
                
                if method == "-spanbert":
                    ctr = 0    
                    for tuples in tupleSet:
                        tuple0 = tuples[0].strip()
                        tuple1 = tuples[1].strip()
                        if tuples[2] >= t:
                            if tuple0 in keyExtractedTuple:
                                if tuples[2] > keyExtractedTuple[tuple0]:
                                    # Removing the older value
                                    ctr+=1
                                    extractedTuple = [ele for ele in extractedTuple if ele[0]!=tuple0]
                                    extractedTuple.append((tuple0,tuple1,tuples[2]))
                                    keyExtractedTuple[tuple0] = tuples[2]
                            else:
                                ctr+=1
                                extractedTuple.append((tuple0,tuple1,tuples[2]))
                                keyExtractedTuple[tuple0] = tuples[2]
                else:
                    ctr = 0 
                    for tuples in tupleSet:
                        if tuples not in extractedTuple:
                            ctr+=1
                            extractedTuple.append(tuples)

                
                print("Relations extracted from this website:"+str(ctr)+ " (Overall: " + str(len(extractedTuple))+")")

        
        if len(extractedTuple) >=k:
            break      
        
        extractedTuple.sort(key = lambda x: x[2], reverse=True)
        
        queryUpdated = False

        for value in extractedTuple:

            # Checking if the query is already used
            alreadyUsed  = False
            for entry in querySet:
                if value[0] in entry or value[1] in entry:
                    alreadyUsed = True
                    break

            if not alreadyUsed:
                query = value[0].lower()+" "+value[1].lower()
                queryUpdated = True
                break
        
        if not queryUpdated:
            break
        print("No of tuple Extracted till now:",len(extractedTuple))
    print("================== ALL RELATIONS for "+ relation + "( "+str(len(extractedTuple))+" ) =================")
    for tuple in extractedTuple:
        print("Confidence: " +str(tuple[2]) + "\t | Subject: "+ tuple[0] + "\t | Object: "+tuple[1])

data=sys.argv[1:]
main(*data)
#main('-gpt3','AIzaSyAMw1otSb1Tuh6Qe81Eo799bNSO55cqtTI','59dddcc6d7ae4afdd','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',"2","0.0","Bill gates Microsoft",10)
                





