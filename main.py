import csv
import matplotlib.pyplot as plt
#just setup
print("starting processing")
rows = list()
with open("GSE_2025.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        rows.append(row)

print("first row: " + str(rows[0]))
print("total row count: " + str(len(rows)))
assert(len(rows)== 1110852)

datedict = dict()
for row in rows:
    if row[0] == "service_date":
        continue
    if datedict.get(row[0]) == None:
        datedict.update({row[0] : list(row)})
    else:
        datelist = datedict.get(row[0])
        datelist.append([row])
        
        datedict.update({row[0] : datelist})

print("datedict length: " + str(len(datedict)))
# for date in datedict:
#     print(date)

ridershipdict = dict()
for date in datedict:
    ridership = 0

    for entry in datedict.get(date):
       
        try:
             ridership = ridership + float(entry[0][4])
             #print(ridership)
        except:
            print(end="")


    #print(ridership)
    
    ridershipdict.update({date : ridership})

ridershipweekly = dict()
day = 1
week = 52 #because dataset is in reverse chronological order
count = 0
for date in ridershipdict:
    
    if day % 7 == 0:
        ridershipweekly.update({week : count})
        week -= 1
        count = 0
    count += ridershipdict[date]
    day += 1

ridershipweekly.update({week : count})

ridershipmonthly = dict()
month = 1
for date in ridershipdict:
    datesplit = date.split("-")
    monthnumber = datesplit[1]
    if (ridershipmonthly.get(monthnumber)) == None:
        ridershipmonthly.update({monthnumber : 0})
    else:
        ridershipmonthly[monthnumber] += ridershipdict[date]
xweekly = list(ridershipweekly.keys())
yweekly= list(ridershipweekly.values())
xmonth = list(reversed(list(ridershipmonthly.keys())))
ymonth = list(reversed(list(ridershipmonthly.values())))
print(len(xweekly))
print(yweekly[0])


print("completed processing")
print("plotting...")
#bottom=(min(ridershipweekly.values())-10)
plt.scatter(xweekly,yweekly)
plt.title("Total Weekly Ridership")
plt.figure()
plt.bar(xmonth,ymonth)
plt.title("Total Monthly Ridership")
plt.show()