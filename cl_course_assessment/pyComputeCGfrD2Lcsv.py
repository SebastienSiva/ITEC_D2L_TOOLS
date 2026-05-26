import csv

# Ask user for CSV file name
filename = input("Enter the CSV file name (including .csv): ")

cg_list = [[],[],[],[],[],[],[],[],[],[]] #empty, CG1list, CG2list etc. possibke for future usage
# to list all lines pertaining to contribution to a CG: ID, name, CG#, earned_value, possible_score


try:
    # Open the CSV file
    csv_file = open(filename, 'r', newline='', encoding='utf-8')
    reader = csv.reader(csv_file)

    first_column_list = []

    for row in reader:
        if len(row) > 0:                 # make sure row is not empty
            value = row[0]
            if value not in first_column_list:   # ensure uniqueness
                first_column_list.append(value)

    print("Unique first column values:", first_column_list)

    #create dict w/ id (fr first column) as key, and total values for a CG
    ptG1 = {}
    ptG2 = {}
    ptG3 = {}
    ptG4 = {}
    ptG5 = {}
    ptGets = ["p tasks get points", ptG1, ptG2, ptG3, ptG4, ptG5]
    # now populate the initail pairs --?? may have concise notation???
    for x in first_column_list[1:]:
        ptG1[x] = [0, 0]  # [earned, possible]
        ptG4[x] = [0, 0]
        ptG5[x] = [0, 0]

    # Reset file pointer to beginning of file
    csv_file.seek(0)
    reader = csv.reader(csv_file)
    

    # Read all rows into a list
    rows = list(reader)



    if len(rows) == 0:
        print("The file is empty.")
    else:
        # Get column headings (first row)
        headings = rows[0]
        num_columns = len(headings)

        print("\nNumber of columns:", num_columns)
        print("Column headings:", headings)

        # Count content rows (excluding header)
        content_rows = rows[1:]
        num_rows = len(content_rows)

        print("\nNumber of data rows:", num_rows)

        # next to build the data list for each CG.  You may follow this
        # example and expand to include additional CG(s).

        print("\nSearching for keyword 'summary'...\n")

        def buildPersonPtListForGoal(ptGn, row): #row is the line csv line under processing
            ptGn[row[0]][0] += float(row[-2]) #row[0] is the id in a line
            ptGn[row[0]][1] += int(row[-1])
            print(ptGn[row[0]])
        
        # Search each row for keyword "summary" and/or other CG1,,2,3 and or [Goal 1] [Goal n]
        ###
        # YOU may CUSTOMIZE for your D2L quiz and csv setup
        ###
        for row in content_rows:
            # Convert entire row to lowercase string for case-insensitive search
            row_text = " ".join(row).lower()

            if "summary" in row_text and "cg1" in row_text:
                #input("Check 1: still ok, cont?")
                buildPersonPtListForGoal(ptG1, row)
            elif "summary" in row_text and"cg4" in row_text:
                buildPersonPtListForGoal(ptG4, row)
            elif ("cg5" in row_text) or ("goal 5" in row_text):
                buildPersonPtListForGoal(ptG5, row)
            #else:
                #input(":::")   # for debuging only , not needed

    more = input("display whole tables? y/n ")
                
    if more == "y" and (len(cg1_list)+len(cg4_list)+len(cg5_list)) > 0:
        print("Unique first column values:", first_column_list)
        for x in ptGets: #accumulated pts by person for G1, G.., G5
            print(x)
        

    # total CG1, ... CG4, CG5 possible, at index 1, 2, ...5.  Index 0 un-used...
    cg_totals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # rearrange for each CG, compute % from [earn, max] for each person
    def computePercentageForPerson(ptGn):
        for key in ptGn:
            print("Check pt :  key = " + key +", and value is:")
            print(ptGn[key])
            if ptGn[key][1] != 0:
                ptGn[key] = ptGn[key][0] / ptGn[key][1]
            else:
                ptGn[key] = 0
            print("now new value is : " + str(ptGn[key]))

    for n in [1, 4, 5]:
        ptGn = "ptG"+str(n)      # ptGn a string or refers to the dictionary ptG1,ptG4, ptG5???
        print("calling compute percentage for ptG" +str(n))
        computePercentageForPerson(globals()[ptGn])
    #computePercentageForPerson(ptG1)  
    #computePercentageForPerson(ptG4)
    #computePercentageForPerson(ptG5)


    
    # count CG percentage
    input("Cont? ... to the final #s --> exciting news :")
    def countCGpercent(ptGn, n):
        count = 0
        for value in ptGn.values():
            if value >= 0.7:
                count += 1
        cg_totals[n] = round(100 * count/len(ptGn))
        print("CG1 success percentage rate = : " + str(count / len(ptGn)) )
        print("CG1 round to whole number: " + str(cg_totals[n]) )

    countCGpercent(ptG1, 1)

    for n in [4, 5]:
        ptgn = "ptG" + str(n)
        print(" call to compute for " + ptGn)
        countCGpercent(globals()[ptgn], n)
    

    
    # Close the CSV file
    csv_file.close()
    print("CSV file closed.")

except FileNotFoundError:
    print("File not found. Please check the filename and try again.")
except Exception as e:
    print("An error occurred:", e)


#Prompts user for a CSV filename
#Opens the file safely
#Counts and prints: Number of columns, Column headings (as a list), Number of data rows
#Searches each row for "summary" (case-insensitive). If found: Prints first 2 elementsPrints last 2 elements
# build CG list with {id, [earn, total]}
# convert to {id, percentage}
# count the pass rate for each CG, print it out
#Closes the file at the end

#V3 introduced new functions to reduce (code) total size
