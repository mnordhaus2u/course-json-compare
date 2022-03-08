import json
import tkinter as tk
from tkinter import filedialog

outFile = open("compare-output.txt", 'w')

root = tk.Tk()
root.withdraw()

#first file
file_path1 = filedialog.askopenfilename()
file_path2 = filedialog.askopenfilename()

outFile.write("===================================\n")
outFile.write("Comparing with first file as source")
outFile.write("\n===================================\n")

# Opening JSON files, load returns dictionary
# worst hack ever. We're just going to run this whole thing twice
# just load the jsons in opposite order *eye twitches*
for comparePass in range(2):
    if not comparePass:
        # the origin file
        f = open(file_path1)
        data1 = json.load(f)
        f.close()

        # the target file
        f = open(file_path2)
        data2 = json.load(f)
        f.close()
    else:
        # the origin file
        f = open(file_path2)
        data1 = json.load(f)
        f.close()

        # the target file
        f = open(file_path1)
        data2 = json.load(f)
        f.close()

    # this is brute force loop inside loop. 
    for week in data1['weeks']:
        allMatch = True
        outFile.write("\nWEEK ORDER " + str(week['order']) + ": " + week["name"] + "\n")
        foundWeek = False
        for week2 in data2['weeks']:
            if week['name'] == week2['name']:
                foundWeek = True

                # we've found a match, check the contents
                foundActivity = False
                for activity in week['activities']:
                    for activity2 in week2['activities']:
                        if activity['name'] == activity2['name']:
                            foundActivity = True
                # if no match then the activity doesn't exist in the target
                if not foundActivity:
                    allMatch = False
                    outFile.write("\tActivity '" + activity['name'] + "' not found\n")

                # we've found a match, check the contents
                foundSegment = False
                for segment in week['segments']:
                    for segment2 in week2['segments']:
                        if segment['name'] == segment2['name']:
                            foundSegment = True

                            #check elements within the segment
                            foundElement = False
                            for element in segment['elements']:
                                for element2 in segment2['elements']:
                                    if element['name'] == element2['name']:
                                        foundElement = True
                            
                            #no match, the element doesn't exist in the target
                            if not foundElement:
                                allMatch = False
                                outFile.write("\t\tElement '" + element['name'] + "' not found\n")
                                                
                # if no match then the segment doesn't exist in the target
                if not foundSegment:
                    allMatch = False
                    outFile.write("\tSegment '" + segment['name'] + "' not found\n")
                
        # we can't find the origin week in the target
        if not foundWeek:
            allMatch = False
            outFile.write("\t***Target course does not contain this week***\n")
        
        if allMatch:
            outFile.write("\tAll Contents Match\n")
    
    #divider between the two comparisons
    if not comparePass: 
        outFile.write("\n\n====================================\n")
        outFile.write("Comparing with second file as source")
        outFile.write("\n====================================\n")

# Closing file
outFile.close()
