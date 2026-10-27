import csv
import statistics as stats
import matplotlib.pyplot as plt
import numpy 
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
        datedict.update({row[0] : [[row]]})
    else:
        datelist = datedict.get(row[0])
        datelist.append([row])
        datedict.update({row[0] : datelist})

print("datedict length: " + str(len(datedict)))
# for date in datedict:
#     print(date)
shorttermridershipdict = dict()

for date in datedict:
    print(datedict.get(date)[0])
    for entry in datedict.get(date):

        if shorttermridershipdict.get(entry[0][1]) == None:
            shorttermridershipdict.update({entry[0][1] : float(entry[0][4])})
        else:
            ridership = shorttermridershipdict[entry[0][1]] + float(entry[0][4])
            shorttermridershipdict.update({entry[0][1] : ridership})


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
xshort = list(shorttermridershipdict.keys())
yshort = list(shorttermridershipdict.values())
xweekly = list(ridershipweekly.keys())
yweekly= list(ridershipweekly.values())
xmonth = list(reversed(list(ridershipmonthly.keys())))
ymonth = list(reversed(list(ridershipmonthly.values())))
print(len(xweekly))
print(yweekly[0])


print("completed processing")

#month summary statistics 
monthmean = stats.mean(ymonth)

monthquartiles = stats.quantiles(ymonth)
monthmedian = monthquartiles[1]
monthQ1 = monthquartiles[0]
monthQ3 = monthquartiles[2]

monthmax = max(ymonth)
monthmin = min(ymonth)

print(f"month mean: {monthmean}\n")
print(f"month five number summary: \nmin:{monthmin}\nQ1: {monthQ1}\nmedian (Q2): {monthmedian}\nQ3: {monthQ3}\nmax: {monthmax}\n\n")

weekmean = stats.mean(yweekly)

weekquartiles = stats.quantiles(yweekly)
weekmedian = weekquartiles[1]
weekQ1 = weekquartiles[0]
weekQ3 = weekquartiles[1]

weekmin = min(yweekly)
weekmax = max(yweekly)

print(f"week mean: {weekmean}\n")
print(f"week five number summary: \nmin:{weekmin}\nQ1: {weekQ1}\nmedian (Q2): {weekmedian}\nQ3: {weekQ3}\nmax: {weekmax}\n\n")

print("plotting...")
plt.boxplot(yweekly)
plt.title("Weekly Boxplot")
plt.figure()

plt.boxplot(ymonth)
plt.title("Monthly Boxplot")
plt.figure()

#bottom=(min(ridershipweekly.values())-10)
plt.scatter(xweekly,yweekly)
plt.title("Total Weekly Ridership")

plt.figure()
plt.bar(xmonth,ymonth)
plt.title("Total Monthly Ridership")

plt.figure()
plt.scatter(xshort, yshort)
plt.title("Short Term Ridership (per 30 minutes)")
plt.show()