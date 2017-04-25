 #!/usr/bin/env python
import urllib
from urllib.request import urlopen
import json
import datetime
from datetime import timezone
import calendar
import configparser
import sqlalchemy
import re
import sys
from sqlalchemy import MetaData, Table, select

Fairmount_line=["Readville", "Fairmount", "Morton Street", "Talbot Avenue", "Four Corners / Geneva" ,
                "Uphams Corner", "Newmarket", "South Station"] #"Four Corners/Geneva Ave" API Call
                                                                # returns empty !!!!
Fitchuburg_line=["wachusett","Fitchburg","North Leominster","Shirley","Ayer","Littleton / Rte 495",
                "South Acton","West Concord", "Concord", "Lincoln", "Silver Hill", "Hastings",
                "Kendal Green", "Brandeis/ Roberts", "Waltham", "Waverley", "Belmont", "Porter Square",
                "North Station"]

Framingham_Worcetster_line=["Worcester","Grafton","Westborough","Southborough",
                            "Ashland","Framingham","West Natick","Natick Center","Wellesley Square",
                            "Wellesley Hills","Wellesley Farms", 
                            "Auburndale", "West Newton", "Newtonville", "Yawkey",
                            "Back Bay","South Station"]
Franklin_line=["Forge Park / 495","Franklin","Norfolk","Walpole","Plimptonville","Windsor Gardens",
                "Norwood Central","Norwood Depot","Islington","Dedham Corp Center","Endicott",
                "Readville","Ruggles","Back Bay","South Station"]


Greenbush_line=["Greenbush","North Scituate","Cohasset","Nantasket Junction","West Hingham","East Weymouth",
                "Weymouth Landing/ East Braintree","Quincy Center","JFK/UMass","South Station"]

Haverhill_line=["Haverhill","Bradford","Lawrence","Andover","Ballardvale","North Wilmington",
                "Reading", "Wakefield","Greenwood","Melrose Highlands","Melrose Cedar Park","Wyoming Hill",
                "Malden Center","North Station"]
Kingston_Plymouth_line=["Kingston","Plymouth","Halifax","Hanson","Whitman","Abington","South Weymouth",
                        "Braintree","JFK/UMass","South Station"]
Lowell_line=["Lowell","North Billerica","Wilmington","Anderson/ Woburn","Mishawum","Winchester Center",
            "Wedgemere","West Medford","North Station"]

Middleborough_Lakeville_line=["Middleborough/ Lakeville","Bridgewater","Campello","Brockton","Montello",
                                "Holbrook/ Randolph","Braintree","Quincy Center","JFK/UMASS","South Station"]
Needham_line=["Needham Heights","Needham Center","Needham Junction","Hersey","West Roxbury","Highland",
                "Bellevue","Roslindale Village","Forest Hills","Ruggles","Back Bay","South Station"]

Newburyport_Rockport_line=["Rockport","Gloucester","West Gloucester","Manchester","Beverly Farms",
                            "Prides Crossing","Montserrat","Newburyport","Rowley","Ipswich","Hamilton/ Wenham",
                            "North Beverly","Beverly","Salem","Swampscott","Lynn","River Works / GE Employees Only","Chelsea","North Station"]
Providence_Stoughton_line=["Wickford Junction","TF Green Airport","Providence","South Attleboro","Attleboro",
                            "Mansfield","Sharon","Stoughton","Canton Center","Canton Junction",
                            "Route 128","Hyde Park","Ruggles","Back Bay","South Station"]

"""
Do the time conversion from real time (yy,m,d,h,m,s)
"""

def timeConversion():
    startTime=datetime.datetime.fromtimestamp(
        int("1457427600")).strftime('%Y-%m-%d %H:%M:%S')
    
    endTime=datetime.datetime.fromtimestamp(
        int("1457499992")).strftime('%Y-%m-%d %H:%M:%S')
    start=datetime.datetime(2017,4,18,3,0,0)
    finish=datetime.datetime(2017,4,19,3,0,0)
    unix_start_time=start.strftime('%s')
    unix_finish_time = finish.strftime('%s')
    return [unix_start_time,unix_finish_time,start,finish]

    #print (startTime)
    #print (endTime)
    #print (unix_start_time)
    #print (unix_finish_time)

startTime= timeConversion()[0]
endTime=timeConversion()[1]
normal_start=timeConversion()[2]
normal_finish=timeConversion()[3]

"""
convert unix time to year-month-date-hours-minutes-seconds
"""

def unixTime_to_readable(unixTime):
    return datetime.datetime.fromtimestamp(
        int(unixTime)).strftime('%Y-%m-%d %H:%M:%S')
"""
convert unix time to hours-minutes-seconds 
"""
def getTime(unixTime):
    if unixTime==None:
        return None
    else:
        return datetime.datetime.fromtimestamp(int(unixTime)).strftime('%H:%M:%S')
"""
convert UTC to GMT timeZone
"""
def UTC_to_GMT(utc):
    if utc==None:
        return None
    else:
        utc_dt=datetime.datetime.fromtimestamp(
            int(utc))
        gmt=utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
        return gmt.strftime('%s')

"""
Count number of stations for each line for the testing purposed
"""

def numberOfStation(line):
    return len(line)


"""
Read all of the schedule adherence information for each staion in commuterail and store its info 
into scheduleadherence, and return schedule adherence --> list of [trip_id, route_ud, direction, 
sch_dt, ct_dt, delay_sec]
"""
def readFromScheduleAdherence():
    #startTime= timeConversion()[0]
    #endTime=timeConversion()[1]
    
    commuterail=Fairmount_line+Fitchuburg_line+Framingham_Worcetster_line+Franklin_line+ \
                Greenbush_line+Haverhill_line+Kingston_Plymouth_line+Lowell_line+Middleborough_Lakeville_line+ \
                Needham_line+Newburyport_Rockport_line+Providence_Stoughton_line

    commuterail_station=list(set(commuterail))

    scheduleadherence=[]
    
    stationMiss=[]

    
    for station in commuterail_station:

        url=("http://realtime.mbta.com/developer/api/v2.1/scheduleadherence?api_key=wX9NwuHnZU2ToO7GmGR9uw%20&format=json&stop=" +
            station+"&from_datetime="+startTime+"&to_datetime="+endTime).replace(" ","%20")
        
        response=urllib.request.urlopen(url)
        data = json.loads(response.read()) #map{"schedule_adherences:[lists of map]"}
        s = data["schedule_adherences"]
        
        if not s:
            stationMiss.append(station)

        for i in s:
            #scheduleadherence.append([i["trip_id"] + ", " + i["route_id"] + ", " + i["direction"] + ", " + i["sch_dt"] + ", " + i["act_dt"] + \
                #", "+ i["delay_sec"]])

            scheduleadherence.append([i["trip_id"], i["route_id"],i["direction"],i["sch_dt"],i["act_dt"],i["delay_sec"],station])
    print (len(commuterail_station))        
    #print (scheduleadherence)
    #print (stationMiss) #for error checking purpose
    return scheduleadherence



    
"""
determine wheter there is an alert issued with the given trioID
"""
def isAlertIssued(trip_alert,tripID):
    if tripID in trip_alert.keys():
        if len(trip_alert[tripID])>0:
            return True 
    else:
        return False





"""
determine wheter a given trip_id deserves alert 
"""
def deserves_alert(delay):
    return int(delay)>=600

"""
compute the alert deplay time, return the delay time 
### confirm the alforthm is correct !!!!!!!
"""
def alert_delay(trip_alert,tripID,schedule_departure):

    last_modified_dt=9223372036854775807 # need to find a way to get sys.maxint
    if(isAlertIssued(trip_alert,tripID)):
        
        for alert in trip_alert[tripID]:
            if int(alert[1])<last_modified_dt:
                last_modified_dt=int(UTC_to_GMT(alert[1]))
        return str(last_modified_dt-int(schedule_departure))
    else:
        return None






"""
compute the timeliness of alert, return the bracket of  alert's timeliness 
If the alert sent out less than 5 mins later of train's scheduled depature, then it's timely, 
otherwise it's not timely 


Go for the first alert for each tripID !!!
"""
def alert_timely(trip_alert,tripID,scheduled_departure):
    delay=alert_delay(trip_alert,tripID,scheduled_departure)
    if delay ==None:
        return None
    else:
     return int(delay)<=300

"""
get correct alert to measure its accuracy, return [message,last_modified_dt] 
or None
"""
def get_alert(trip_alert,tripID,scheduled_departure):
    last_modified_dt=-1
    message=""
    if isAlertIssued(trip_alert,tripID):
        first_alert=trip_alert[tripID][0]
        if int(first_alert[1])>=int(scheduled_departure):
            message=first_alert[3]
            last_modified_dt=int(first_alert[1])
        else:
            for alert in trip_alert[tripID]:
                if int(alert[1])>last_modified_dt and int(alert[1])<int(scheduled_departure):
                    message=alert[3]
                    last_modified_dt=int(alert[1])
        return [message,last_modified_dt]
    else:
        return None


"""
get the text message of tripID's associated alert 
choose the last alert before the schduled departure if there is any 
otherwise choose first alert after the scheduled departure 
"""
def get_alert_message(trip_alert,tripID,scheduled_departure):
    if get_alert(trip_alert,tripID,scheduled_departure)==None:
        return None
    else:
        return (get_alert(trip_alert,tripID,scheduled_departure))[0]
"""
get the last modified day of alert to fill in time entry in 
alert_event table in database 
"""
def get_last_modified_dt(trip_alert,tripID,scheduled_departure):
    if get_alert(trip_alert,tripID,scheduled_departure)==None:
        return None
    else:
        return (get_alert(trip_alert,tripID,scheduled_departure))[1]

"""
parse the alet_message and get the predicted delay 
check the word "minutes" "m" or "min", and grab the time range before these words
"""
def get_predicted_delay(trip_alert,tripID,scheduled_departure):
    message=get_alert_message(trip_alert,tripID,scheduled_departure)
    delay=""
    if message==None:
        return None
    else:
        predicted_delay=message.split()
        for i in range (len(predicted_delay)):
            if predicted_delay[i]=="minutes":
                delay=predicted_delay[i-1]
            elif predicted_delay[i]=="min":
                delay=predicted_delay[i-1]
            elif predicted_delay[i]=="m":
                delay=predicted_delay[i-1]
    
        return delay




"""
measure the accuracy of the alert 
if the delaytime is in the predicted-delay time range, then 
it is accurate. if delay is less time lower bound of time range it is high, 
if delay is more than upper bound of time range, it is low 
if no predicted-delay, then no estimate 

"""
def delay_accuray(delay,trip_alert,tripID,scheduled_departure):
    predicted_delay=get_predicted_delay(trip_alert,tripID,scheduled_departure)

    high="high"
    low="low"
    accurate="accurate"
    empty=None
    if predicted_delay==None:
        return None
    elif predicted_delay=="":
        return empty
    else:
        timebound=predicted_delay.split('-')
        d=int(delay)
        if len(timebound)>1:
            if d>=int(timebound[0])*60 and d<=int(timebound[1])*60:
                return accurate
            elif d<int(timebound[0])*60:
                return high
            elif d>int(timebound[1])*60:
                return low 
        else:
            if d==int(timebound[0])*60:
                return accurate
            elif d<int(timebound[0])*60:
                return high
            elif d>int(timebound[0])*60:
                return low





"""
Connect to Postgres Database
"""

def databaseConnect():
    """Load database config settings and connect"""
    config = configparser.ConfigParser()
    config.read("settings.cfg")
    host = config.get('Database', 'host')
    port = config.get('Database', 'port')
    db = config.get('Database', 'db')
    user = config.get('Database', 'user')
    passwd = config.get('Database', 'pass')
 
    engine = sqlalchemy.create_engine('postgresql://' + user + ':' + passwd + '@'
                                      + host + ':' + port + '/' + db)
    metadata = MetaData(bind=engine)
    connection = engine.connect()
    return metadata

"""
Read past day data from alets table in the databse, and only slect alerts with effect_name="Delay"
"""
def read_alerts(metadata):
    alerts=Table('alerts',metadata,autoload=True)
    s=alerts.select((alerts.c.last_modified_dt>=normal_start) & (alerts.c.last_modified_dt<=normal_finish) &
        (alerts.c.effect_name=='Delay'))
    rs=s.execute()
    rows=rs.fetchall()
    last_modified_dt=[]

    for r in rows:
        last_modified_dt.append([r.alert_id,r.last_modified_dt.strftime('%s'),r.effect_name,
            r.short_header_text,])

    #for l in last_modified_dt:
        #print(l)
    return last_modified_dt


""" 
    Read the data from alert_affected_services table in the database
"""
def read_alert_affected_services(metadata):

    alert_affected_services=Table('alert_affected_services',metadata,autoload=True)
    s=alert_affected_services.select(alert_affected_services.c.trip_id!='None')
    rs=s.execute()
    rows=rs.fetchall()

    alert_affected = []
    for r in rows:  
        alert_affected.append([r.alert_id,r.trip_id])

    #for i in alert_affected:
        #print (i) 
    return alert_affected


"""
for the testing purpose 

def add_tripIDs_to_alerts(metadata):
    alert_affected_services=read_alert_affected_services(metadata)
    alerts_data=read_alerts(metadata)
    data_dictionary= alertID_to_tripID(alert_affected_services)


    

    for i,j in data_dictionary.items():
        for index in range(len(alerts_data)):
            if i==(alerts_data[index])[0]:
                alerts_data[index].append(j)


    for alert in alerts_data:
        print (alert)
    return alerts_data
"""



"""
Create datadictionary with key value of tripIDs and assoicated alertIDs 
"""
def tripID_to_alertID(metadata):
    tripID_to_alertID=dict()
    alert_affected_services=read_alert_affected_services(metadata)
    alerts_data=read_alerts(metadata)
    data_dictionary= alertID_to_tripID(alert_affected_services)

    for i,j in data_dictionary.items():
        for alert in alerts_data:
            if i==alert[0]:
                for trip in j:
                    if trip in tripID_to_alertID:
                        tripID_to_alertID[trip].append(alert)
                    else:
                        tripID_to_alertID[trip]=[alert]

    #for i,j in tripID_to_alertID.items():
        #print(i,j)

    return tripID_to_alertID


"""
Create data dictionary for tripID and AlertID, map each tripID to AlertIDs. return alertID_to_tripID
which contains map of alertID to tripIDs
"""
def alertID_to_tripID(data):
    alertID_to_tripID=dict()
    
    for effected_services in data:
        if effected_services[0] in alertID_to_tripID:
            if effected_services[1] not in alertID_to_tripID[effected_services[0]]:
                alertID_to_tripID[effected_services[0]].append(effected_services[1])
        else:
            alertID_to_tripID[effected_services[0]]=[effected_services[1]]

    #print(alertID_to_tripID)

    #for i,j in alertID_to_tripID.items():
        #print (i,j)

    return alertID_to_tripID

"""
takes in 1 or 0 from direction and return inbound or outbound
"""
def direction(direc):
    inbound="inbound"
    outbound="outbound"
    if direc==0:
        return inbound
    elif direc==1:
        return outbound


"""
create lists of fileds to alert_events 
"""

def alert_events(metadata):

    date=datetime.datetime.fromtimestamp(int(startTime)).strftime('%Y-%m-%d')
    time=datetime.datetime.fromtimestamp(int(endTime)).strftime('%H:%M:%S')
    day=calendar.day_name[datetime.datetime.fromtimestamp(int(startTime)).weekday()]

    alertevents=[]
    scheduleadherence=readFromScheduleAdherence()
    dic=tripID_to_alertID(metadata)

    for trip in scheduleadherence:
        if isAlertIssued(dic,trip[0]) or deserves_alert(trip[5]):
            alertevents.append([trip[0],str(date),getTime(UTC_to_GMT(get_last_modified_dt(dic,trip[0],trip[3]))),str(day),str(trip[1]),str(trip[6]),direction(int(trip[2])),str(trip[1][3:])+" Train " +trip[0][19:],
                unixTime_to_readable(str(trip[3])),unixTime_to_readable(str(trip[4])),trip[5],isAlertIssued(dic,trip[0]),deserves_alert(trip[5]),
                alert_delay(dic,trip[0],trip[3]),alert_timely(dic,trip[0],trip[3]),
                get_alert_message(dic,trip[0],trip[3]),get_predicted_delay(dic,trip[0],trip[3]),delay_accuray(trip[5],dic,trip[0],trip[3])
            
            ])

    #for a in alertevents:
        #print (a)
    return alertevents


"""
write result to alert_events table 
"""
def writeToAlertEventsTable(metadata):
    data=alert_events(metadata)
    alertevents=Table('alert_events',metadata,autoload=True)
    i=alertevents.insert()
    for entry in data: 
     
        i.execute(trip_id=entry[0],date=entry[1],time=entry[2],
            day=entry[3],
            route=entry[4],
            stop=entry[5],
            direction=entry[6],
            short_name=entry[7],scheduled_departure=entry[8],actual_departure=entry[9],
            delay=entry[10],
            alert_issued=entry[11],deserves_alert=entry[12],
            alert_delay=entry[13],
            alert_timely=entry[14],
            alert_text=entry[15],
            predicted_delay=entry[16],
            delay_accuracy=entry[17]

            )

"""
delete rows in table
"""
def deleteEntries(metadata):
    alertevents=Table('alert_events',metadata,autoload=True)
    d=alertevents.delete()
    for i in range (9286,11003):
        d.execute(id=str(i))
    

if __name__=="__main__":
    readFromScheduleAdherence()

    metadata=databaseConnect()
    #alert_events(metadata)
    #read_alerts(metadata)
    #read_alert_affected_services(metadata)
    #tripID_to_alertID(metadata)
    #writeToAlertEventsTable(metadata)
    #deleteEntries(metadata)


