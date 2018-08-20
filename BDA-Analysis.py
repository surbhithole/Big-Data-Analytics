
# https://www.census.gov/search-results.html?q=population+new+york&search.x=0&search.y=0&search=submit&page=1&stateGeo=none&searchtype=web&cssp=SERP#
#
import plotly.offline as py
import plotly.graph_objs as go

#Population Data fetch

data=spark.read.csv('Cleaned_311.csv/cleaned.csv',header=True)
data.createOrReplaceTempView("table")


---------------dd1---------------------
NoiseComplaintBorough_q2=spark.sql('SELECT `COMPLAINT TYPE`,BOROUGH,SUBSTRING(`CREATED DATE`,7,4) AS YEAR,COUNT(*) AS COUNTS FROM TABLE WHERE `COMPLAINT TYPE` LIKE "Noise%" GROUP BY BOROUGH,YEAR,`COMPLAINT TYPE` ORDER BY BOROUGH,YEAR DESC,COUNTS DESC')

---------------ddtemp---------------------
numbers=spark.sql('select SUBSTRING(`created date`,0,10) AS Date,`Complaint Type`,count(`complaint type`) AS Counts FROM table group by SUBSTRING(`created date`,0,10),`complaint type` order by SUBSTRING(`created date`,0,10) desc')


--------dsadsas-------yyy20---------------------
# total complaints for each agency per year
spark.sql('SELECT AGENCY, SUBSTRING(`CREATED DATE`,7,4) AS YEAR,COUNT(*) AS COUNTS FROM TABLE WHERE AGENCY != "3-1-1" GROUP BY AGENCY,YEAR ORDER BY AGENCY,YEAR DESC,COUNTS DESC')

spark.sql('SELECT AGENCY AS YEAR,COUNT(*) AS COUNTS FROM TABLE WHERE AGENCY != "3-1-1" GROUP BY AGENCY ORDER BY COUNTS DESC')




---------------yyy21---------------------
## month wise complaints for each borough taken over the year
#Q1. Number of Complaints by borough
spark.sql('SELECT SUBSTRING(`CREATED DATE`,0,2) AS Month, COUNT(*) AS COUNTS FROM TABLE WHERE BOROUGH="BROOKLYN" GROUP BY SUBSTRING(`Created Date`,0,2) ORDER BY Month DESC, COUNTS DESC')

---------------yyy22---------------------
spark.sql('SELECT SUBSTRING(`CREATED DATE`,0,2) AS Month, COUNT(*) AS COUNTS FROM TABLE WHERE BOROUGH="QUEENS" GROUP BY SUBSTRING(`Created Date`,0,2) ORDER BY Month DESC, COUNTS DESC')

---------------yyy23---------------------
spark.sql('SELECT SUBSTRING(`CREATED DATE`,0,2) AS Month, COUNT(*) AS COUNTS FROM TABLE WHERE BOROUGH="MANHATTAN" GROUP BY SUBSTRING(`Created Date`,0,2) ORDER BY Month DESC, COUNTS DESC')

---------------yyy24---------------------
spark.sql('SELECT SUBSTRING(`CREATED DATE`,0,2) AS Month, COUNT(*) AS COUNTS FROM TABLE WHERE BOROUGH="BRONX" GROUP BY SUBSTRING(`Created Date`,0,2) ORDER BY Month DESC, COUNTS DESC')

---------------yyy25---------------------
spark.sql('SELECT SUBSTRING(`CREATED DATE`,0,2) AS Month, COUNT(*) AS COUNTS FROM TABLE WHERE BOROUGH="STATEN ISLAND" GROUP BY SUBSTRING(`Created Date`,0,2) ORDER BY Month DESC, COUNTS DESC')



--------dsadsas-------yyy26---------------------
# total complaints for each location type per year  -- these contains lots of null values
spark.sql('SELECT `Location Type`, SUBSTRING(`CREATED DATE`,7,4) AS YEAR,COUNT(*) AS COUNTS FROM TABLE WHERE `Location Type` is not null GROUP BY `Location Type`,YEAR ORDER BY `Location Type`,YEAR DESC,COUNTS DESC')


--------dsadsas-------yyy27---------------------
# total complaints for each location type per year  -- these contains lots of null values
spark.sql('SELECT `Location Type`, `Complaint Type`, SUBSTRING(`CREATED DATE`,0,2) AS Month, SUBSTRING(`CREATED DATE`,7,4) AS YEAR,COUNT(*) AS COUNTS FROM TABLE WHERE `Location Type` is not null GROUP BY `Location Type`, `Complaint Type`, YEAR, Month ORDER BY `Location Type`, `Complaint Type`, YEAR, Month DESC,COUNTS DESC')

--------dsadsas-------yyy28---------------------
spark.sql('SELECT `Location Type`, `Complaint Type`, COUNT(*) AS COUNTS FROM TABLE WHERE `Location Type` is not null GROUP BY `Location Type`, `Complaint Type` ORDER BY `Location Type`, `Complaint Type` DESC, COUNTS DESC')


--------dsadsas-------yyy29---------------------
spark.sql('select `Borough`, `Complaint Type`, SUBSTRING(`Created Date`,7,4) AS Year, SUBSTRING(`Created Date`, 0,2) AS Month, COUNT(`Complaint Type`) AS Counts FROM table group by SUBSTRING(`Created Date`,7,4), SUBSTRING(`Created Date`, 0,2), `Borough`, `Complaint Type`, order by `Borough`, `Complaint Type` SUBSTRING(`Created Date`,7,4), SUBSTRING(`Created Date`, 0,2) desc').show()



--------dsadsas-------yyy---------------------
spark.sql('SELECT `Agency`, `Complaint Type`, DATEDIFF(to_date(`Closed Date`,"MM/dd/yyyy"), to_date(`Created Date`,"MM/dd/yyyy")) AS CreateCloseDiff FROM TABLE').show()

spark.sql('SELECT *, DATEDIFF(to_date(`Closed Date`,"MM/dd/yyyy"), to_date(`Created Date`,"MM/dd/yyyy")) AS CreateCloseDiff FROM TABLE').show()

spark.sql('SELECT * from table where CreateCloseDiff > -1').show()




---------------dd3---------------------
#Q1. Number of Complaints by borough
dd3=spark.sql('SELECT COUNT(*) AS COUNTS, SUBSTRING(`CREATED DATE`,7,4) AS Year FROM TABLE WHERE BOROUGH="BROOKLYN" GROUP BY SUBSTRING(`Created Date`,7,4) ORDER BY YEAR DESC, COUNTS DESC')


---------------dd4---------------------
QueensComp_q1=spark.sql('SELECT COUNT(*) AS COUNTS, SUBSTRING(`CREATED DATE`,7,4) AS Year FROM TABLE WHERE BOROUGH="QUEENS" GROUP BY SUBSTRING(`Created Date`,7,4) ORDER BY YEAR DESC, COUNTS DESC')

---------------dd5---------------------
ManhattanComp_q1=spark.sql('SELECT COUNT(*) AS COUNTS, SUBSTRING(`CREATED DATE`,7,4) AS Year FROM TABLE WHERE BOROUGH="MANHATTAN" GROUP BY SUBSTRING(`Created Date`,7,4) ORDER BY YEAR DESC, COUNTS DESC')

---------------dd6---------------------
BronxComp_q1=spark.sql('SELECT COUNT(*) AS COUNTS, SUBSTRING(`CREATED DATE`,7,4) AS Year FROM TABLE WHERE BOROUGH="BRONX" GROUP BY SUBSTRING(`Created Date`,7,4) ORDER BY YEAR DESC, COUNTS DESC')

---------------dd7---------------------
StatenComp_q1=spark.sql('SELECT COUNT(*) AS COUNTS, SUBSTRING(`CREATED DATE`,7,4) AS Year FROM TABLE WHERE BOROUGH="STATEN ISLAND" GROUP BY SUBSTRING(`Created Date`,7,4) ORDER BY YEAR DESC, COUNTS DESC')




q1_BrooklynPlot=go.Scatter(x=dd3.toPandas()['Year'],y=dd3.toPandas()['COUNTS'],name='Brooklyn')
q1_ManhattanPlot=go.Scatter(x=ManhattanComp_q1.toPandas()['Year'],y=ManhattanComp_q1.toPandas()['COUNTS'],name='Manhattan')
q1_StatenPlot=go.Scatter(x=StatenComp_q1.toPandas()['Year'],y=StatenComp_q1.toPandas()['COUNTS'],name='Staten Island')
q1_QueensPlot=go.Scatter(x=QueensComp_q1.toPandas()['Year'],y=QueensComp_q1.toPandas()['COUNTS'],name='Queens')
q1_BronxPlot=go.Scatter(x=BronxComp_q1.toPandas()['Year'],y=BronxComp_q1.toPandas()['COUNTS'],name='Bronx')

py.plot({'data':[q1_BrooklynPlot],'layout':{'title':'Number of Complaints in Brooklyn'}},	filename='Q1_Brooklyn')
py.plot({'data':[q1_ManhattanPlot],'layout':{'title':'Number of Complaints in Manhattan'}},	filename='Q1_Manhattan')
py.plot({'data':[q1_QueensPlot],'layout':{'title':'Number of Complaints in Queens'}},	filename='Q1_Queens')
py.plot({'data':[q1_StatenPlot],'layout':{'title':'Number of Complaints in Staten Island'}},	filename='Q1_Staten')
py.plot({'data':[q1_BronxPlot],'layout':{'title':'Number of Complaints in Bronx'}},	filename='Q1_Bronx')


#Complaints Per Citizen (Estimates FROM 2016)
# https://www1.nyc.gov/site/planning/data-maps/nyc-population/current-future-populations.page
spark.sql('SELECT COUNT(*) AS Count,(COUNT(*)/2333054) AS `Per Citizen` FROM table where Borough="QUEENS" and SUBSTRING(`Created Date`,0,4)=="2016"').show()
# +------+------------------+                                                     
# | Count|       Per Citizen|
# +------+------------------+
# |503988|0.2160207179088011|
# +------+------------------+

spark.sql('SELECT COUNT(*) AS Count,(COUNT(*)/1455720) AS `Per Citizen` FROM table where Borough="BRONX" and SUBSTRING(`Created Date`,0,4)=="2016"').show()
# +------+------------------+                                                     
# | Count|       Per Citizen|
# +------+------------------+
# |428548|0.2943890308575825|
# +------+------------------+

spark.sql('SELECT COUNT(*) AS Count,(COUNT(*)/1643734) AS `Per Citizen` FROM table where Borough="MANHATTAN" and SUBSTRING(`Created Date`,0,4)=="2016"').show()
# +------+-------------------+                                                    
# | Count|        Per Citizen|
# +------+-------------------+
# |499423|0.30383444036565527|
# +------+-------------------+

spark.sql('SELECT COUNT(*) AS Count,(COUNT(*)/476015) AS `Per Citizen` FROM table where Borough="STATEN ISLAND" and SUBSTRING(`Created Date`,0,4)=="2016"').show()
# +------+------------------+                                                     
# | Count|       Per Citizen|
# +------+------------------+
# |104721|0.2199951682194889|
# +------+------------------+

# # Q1.  Number of complaints per borough vs year
# spark.sql('SELECT COUNT(*) AS `Counts for Brooklyn`, SUBSTRING(`Created Date`,0,4) AS Year FROM table WHERE BOROUGH="BROOKLYN" GROUP BY Year ORDER BY Year DESC').show()
# spark.sql('SELECT COUNT(*) AS `Counts for Bronx`, SUBSTRING(`Created Date`,0,4) AS Year FROM table WHERE BOROUGH="BRONX" GROUP BY Year ORDER BY Year DESC').show()
# spark.sql('SELECT COUNT(*) AS `Counts for Manhattan`, SUBSTRING(`Created Date`,0,4) AS Year FROM table WHERE BOROUGH="MANHATTAN" GROUP BY Year ORDER BY Year DESC').show()
# spark.sql('SELECT COUNT(*) AS `Counts for Staten Island`, SUBSTRING(`Created Date`,0,4) AS Year FROM table WHERE BOROUGH="STATEN ISLAND" GROUP BY Year ORDER BY Year DESC').show()
# spark.sql('SELECT COUNT(*) AS `Counts for Queens`, SUBSTRING(`Created Date`,0,4) AS Year FROM table WHERE BOROUGH="QUEENS" GROUP BY Year ORDER BY Year DESC').show()

---------------dd9---------------------
# Q2. Top 5 complaints for every borough
Q2_Top5_Brooklyn = spark.sql('SELECT SUBSTRING(`Created Date`,7,4) AS YEAR,COUNT(*) AS `Complaint counts for Brooklyn`,`Complaint Type` FROM table WHERE Borough="BROOKLYN" GROUP BY Year,`Complaint Type` ORDER BY Year DESC,`Complaint counts for Brooklyn` DESC LIMIT 5')

Q2_Top5Plot_Brooklyn=go.Bar(x=Q2_Top5_Brooklyn.toPandas()['Complaint Type'],y=Q2_Top5_Brooklyn.toPandas()['Complaint counts for Brooklyn'],name=Q2_Top5_Brooklyn.toPandas()['Complaint Type'])
py.plot({'data':[Q2_Top5Plot_Brooklyn],'layout':{'title':'Top 5 complaints for the borough of Brooklyn','margin':{'l':'180'}}},filename='Q2_Top5_Brooklyn')

---------------dd10---------------------
Q2_Top5_Manhattan = spark.sql('SELECT SUBSTRING(`Created Date`,7,4) AS YEAR,COUNT(*) AS `Complaint counts for Manhattan`,`Complaint Type` FROM table WHERE Borough="MANHATTAN" GROUP BY Year,`Complaint Type` ORDER BY Year DESC,`Complaint counts for Manhattan` DESC LIMIT 5')


Q2_Top5Plot_Manhattan=go.Bar(x=Q2_Top5_Manhattan.toPandas()['Complaint Type'],y=Q2_Top5_Manhattan.toPandas()['Complaint counts for Manhattan'],name=Q2_Top5_Manhattan.toPandas()['Complaint Type'])
py.plot({'data':[Q2_Top5Plot_Manhattan],'layout':{'title':'Top 5 complaints for the borough of Manhattan','margin':{'l':'180'}}},filename='Q2_Top5_Manhattan')

---------------dd11---------------------
Q2_Top5_Queens = spark.sql('SELECT SUBSTRING(`Created Date`,7,4) AS YEAR,COUNT(*) AS `Complaint counts for Queens`,`Complaint Type` FROM table WHERE Borough="QUEENS" GROUP BY Year,`Complaint Type` ORDER BY Year DESC,`Complaint counts for Queens` DESC LIMIT 5')


Q2_Top5Plot_Queens=go.Bar(x=Q2_Top5_Queens.toPandas()['Complaint Type'],y=Q2_Top5_Queens.toPandas()['Complaint counts for Queens'],name=Q2_Top5_Queens.toPandas()['Complaint Type'])
py.plot({'data':[Q2_Top5Plot_Queens],'layout':{'title':'Top 5 complaints for the borough of Queens','margin':{'l':'180'}}},filename='Q2_Top5_Queens')

---------------dd12---------------------
Q2_Top5_Staten = spark.sql('SELECT SUBSTRING(`Created Date`,7,4) AS YEAR,COUNT(*) AS `Complaint counts for Staten Island`,`Complaint Type` FROM table WHERE Borough="STATEN ISLAND" GROUP BY Year,`Complaint Type` ORDER BY Year DESC,`Complaint counts for Staten Island` DESC LIMIT 5')


Q2_Top5Plot_Staten=go.Bar(x=Q2_Top5_Staten.toPandas()['Complaint Type'],y=Q2_Top5_Staten.toPandas()['Complaint counts for Staten Island'],name=Q2_Top5_Staten.toPandas()['Complaint Type'])
py.plot({'data':[Q2_Top5Plot_Staten],'layout':{'title':'Top 5 complaints for the borough of Staten Island','margin':{'l':'180'}}},filename='Q2_Top5_Staten')


---------------dd13---------------------
Q2_Top5_Bronx = spark.sql('SELECT SUBSTRING(`Created Date`,7,4) AS YEAR,COUNT(*) AS `Complaint counts for Bronx`,`Complaint Type` FROM table WHERE Borough="BRONX" GROUP BY Year,`Complaint Type` ORDER BY Year DESC,`Complaint counts for Bronx` DESC LIMIT 5')

Q2_Top5Plot_Bronx=go.Bar(x=Q2_Top5_Bronx.toPandas()['Complaint Type'],y=Q2_Top5_Bronx.toPandas()['Complaint counts for Bronx'],name=Q2_Top5_Bronx.toPandas()['Complaint Type'])
py.plot({'data':[Q2_Top5Plot_Bronx],'layout':{'title':'Top 5 complaints for the borough of Bronx','margin':{'l':'180'}}},filename='Q2_Top5_Bronx')

# # Least 5
# spark.sql('SELECT SUBSTRING(`Created Date`,0,4) AS YEAR,COUNT(*) AS `Complaint counts for Brooklyn`,`Complaint Type` FROM table WHERE Borough="BROOKLYN" GROUP BY Year,`Complaint Type` ORDER BY Year DESC,Count').show()
# #Manhattan
# #Staten
# #Bronx
# #Queens

---------------dd14---------------------
# Q3. Proportion of Open, Closed and Pending Complaints
ComplaintStatus_Q3=spark.sql('SELECT Status,COUNT(Status) AS Counts FROM TABLE GROUP BY STATUS')

Q3_PieComplaintStatus=go.Pie(labels=ComplaintStatus_Q3.toPandas()['Status'],values=ComplaintStatus_Q3.toPandas()['Counts'],textinfo='label+percent')
py.plot({'data':[Q3_PieComplaintStatus],'layout':{'title':'Proportion of Closed and Open complaints'}},filename='Q3_ComplaintStatus',image='png')

---------------dd15---------------------
# Q4. Total Complaints over the years
Q4_TotalComplaints=spark.sql('SELECT COUNT(*) AS `Number of Complaints`,SUBSTRING(`Created Date`,7,4) AS Year FROM TABLE GROUP BY SUBSTRING(`Created Date`,7,4) ORDER BY Year desc')

Q4_plot=go.Scatter(y=Q4_TotalComplaints.toPandas()['Number of Complaints'],x=Q4_TotalComplaints.toPandas()['Year'],name='Complaints per year')
py.plot({'data':[Q4_plot],'layout':{'title':'Number of Complaints every year'}},filename='Q4_ComplaintsPerYear')

---------------dd16---------------------
#Common Complaints
CommonComplaints=spark.sql('SELECT `Complaint Type`,COUNT(*) AS `Number of Complaints` FROM table GROUP BY `Complaint Type` ORDER BY `Number of Complaints` DESC LIMIT 10')


CommonComplaints_plot=go.Bar(y=CommonComplaints.toPandas()['Complaint Type'],x=CommonComplaints.toPandas()['Number of Complaints'],name=CommonComplaints.toPandas()['Complaint Type'],orientation='h')
py.plot({'data':[CommonComplaints_plot],'layout':{'title':'Common Complaints of New Yorkers','margin':{'l':'180'}}},filename='CommonComplaints')


# #Complaints per year
# spark.sql('SELECT SUBSTRING(`Created Date`,0,4) AS Year, COUNT(*) FROM TABLE GROUP BY Year ORDER BY Year DESC').show()

---------------dd17---------------------
#Complaints per month
Q5_monthlyComplaints=spark.sql('SELECT COUNT(*) AS `Number of Complaints`, SUBSTRING(`Created Date`,0,2) AS Month FROM TABLE GROUP BY Month ORDER BY Month DESC')

Q5_monthlyComplaints_plot=go.Bar(x=['January','Feburary','March','April','May','June','July','August','September','October','November',
	'December'],y=Q5_monthlyComplaints.toPandas()['Number of Complaints'],name=CommonComplaints.toPandas()['Complaint Type'])
py.plot({'data':[Q5_monthlyComplaints_plot],'layout':{'title':'Number of complaints every month','margin':{'l':'180'}}},filename='Q5_monthlyComplaints')


---------------dd18---------------------
# Complaints per hour
Q6_hourlyComplaints_Noise=spark.sql('SELECT SUBSTRING(`Created Date`,12,2) AS Hour, COUNT(*) AS `Number of Noise Complaints` FROM TABLE WHERE `Complaint Type`="Noise Complaint" and SUBSTRING(`Created Date`,21,2)="PM" GROUP BY Hour ORDER BY Hour')

Q6_hourlyComplaints_Noise=spark.sql('SELECT SUBSTRING(`Created Date`,12,2) AS Hour, COUNT(*) AS `Number of Noise Complaints` FROM TABLE WHERE `Complaint Type`="Noise Complaint" and SUBSTRING(`Created Date`,21,2)="AM" GROUP BY Hour ORDER BY Hour')

---------------dd19---------------------
Q6_hourlyComplaints_Street=spark.sql('SELECT SUBSTRING(`Created Date`,12,2) AS Hour, COUNT(*) AS `Number of Street Complaints` FROM TABLE WHERE `Complaint Type`= "Street Complaint" and SUBSTRING(`Created Date`,21,2)="PM" GROUP BY Hour ORDER BY Hour')

Q6_hourlyComplaints_Street=spark.sql('SELECT SUBSTRING(`Created Date`,12,2) AS Hour, COUNT(*) AS `Number of Street Complaints` FROM TABLE WHERE `Complaint Type`= "Street Complaint" and SUBSTRING(`Created Date`,21,2)="AM" GROUP BY Hour ORDER BY Hour')


# Q6_hourlyComplaints_Noiseplot=go.Bar(x=['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'],y=Q6_hourlyComplaints.toPandas()['Number of Complaints'])
# py.plot({'data':[Q6_hourlyComplaints_plot],'layout':{'title':'Number of complaints every hour','margin':{'l':'180'}}},filename='Q6_hourlyComplaints')

Q6_NoiseHourly = go.Bar(x=['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'],y=Q6_hourlyComplaints_Noise.toPandas()['Number of Noise Complaints'],name='Noise Complaints')
Q6_StreetHourly = go.Bar(x=['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'],y=Q6_hourlyComplaints_Street.toPandas()['Number of Street Complaints'],name='Street Complaints')
layout = go.Layout(barmode='stack')
fig = go.Figure(data=[Q6_NoiseHourly, Q6_StreetHourly], layout=layout)
py.plot(fig, filename='Q6_HourlyStacked')

