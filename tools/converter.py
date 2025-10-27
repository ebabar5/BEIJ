import json, csv

#todo:

filename = "test.csv"
headers = []
items = []
outputFile = "target.json"
with open(filename, newline='', encoding="Latin1") as csvfile:

    filereader = csv.reader(csvfile)

    i=0
    for row in filereader:
        if i==0:
            headers = row
        else:
            for j in range(len(row)):
                #replace double quotes with single to avoid issues with json
                row[j] = row[j].replace("\"","'")
                #Avoid escape character  problems
                row[j] = row[j].replace("\\","\\\\")
                
                
            #Parse the category string into a list of category tags
            row[2] = row[2].split("|")
            #remove currency characters from price fields
            row[3] = row[3][3:]
            row[4] = row[4][3:]
            #Parse review info[user_id, user_name, review_id, review_content] into lists
            for j in range(4):

                row[j+9] = row[j+9].split(",")
            
            items.append(row)
        i += 1
        '''limited to 5 items for testing
        if i>5:
            break
        '''

#json encoding
with open(outputFile, "w", encoding="Latin1") as jsonOut:
    jsonOut.writelines("[") #Start list of json items
    firstItem = True
    for item in items:
        itemProperties = []#data to write to the json file for this item
        if not (firstItem):
            itemProperties.append(",\n{")
        else:
            itemProperties.append("{")
        firstItem = False

        for i in range(len(headers)):
            #final header(data tag), thus that line doesn't need a trailing comma
            trailingcomma = i != len(headers)-1
            
            if type(item[i]) is list:
                line = "\"%s\":["%headers[i]
                first = True
                for tag in item[i]:
                    if not first:
                        line+=","
                    first = False
                    line += "\"%s\""%tag
                line += "],\n"
                itemProperties.append(line)
            else:
                comma = ","
                if trailingcomma == False:
                    comma = ""
                itemProperties.append("\"%s\":\"%s\"%s\n"%(headers[i],item[i],comma))
            
            
        itemProperties.append("}")
        jsonOut.writelines(itemProperties)
    jsonOut.writelines("]")
        
        
        



