#!/usr/bin/env python
import urllib
from urllib.request import urlopen
import json
import datetime
import configparser
import sqlalchemy
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
    tartTime=datetime.datetime.fromtimestamp(
        int("1457427600")).strftime('%Y-%m-%d %H:%M:%S')
    
    endTime=datetime.datetime.fromtimestamp(
        int("1457499992")).strftime('%Y-%m-%d %H:%M:%S')
    unix_start_time=datetime.datetime(2017,3,24,3,0,0).strftime('%s')
    unix_finish_time = datetime.datetime(2017,3,25,3,0,0).strftime('%s')
    return [unix_start_time,unix_finish_time]

    #print (startTime)
    #print (endTime)
    #print (unix_start_time)
    #print (unix_finish_time)
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
    startTime= timeConversion()[0]
    endTime=timeConversion()[1]
    
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
            scheduleadherence.append([i["trip_id"] + ", " + i["route_id"] + ", " + i["direction"] + ", " + i["sch_dt"] + ", " + i["act_dt"] + \
                 i["delay_sec"]])

    print (scheduleadherence)
    print (stationMiss) #for error checking purpose
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
    Read arhived alert data from the data base
"""
def readArchivedData(metadata):
    alerts=Table('alerts',metadata,autoload=True)
    s=alerts.select()
    rs=s.execute()
    row=rs.fetchone()
    
    print (row.id)
    print (row.alert_id)
    print (row.effect_name)
 #s = select([self.alerts_table]).where(self.alerts_table.c.alert_id == "344232")
 #   id_matches = self.connection.execute(s)

#   print (s)

"""
Write the result to the database
"""

def writeToDataBase(metadata):

    mockdata=["1", "CR-Newburyport-CR-Weekday-Newburyport-Dec14-152","03-29-2017","8:00:00", "CR-Newburyport",
                ]
    alertevents=Table('alert_events',metadata,autoload=True)
   
    i=alertevents.insert()
    i.execute(id='2',trip_id='CR-Newburyport-CR-Weekday-Newburyport-Dec14-152',date='03-29-2017',time='08:00:00',
                route='CR-Newburyport')
    s=alertevents.select()
    rs=s.execute()
    row=rs.fetchone()

    print (row.id)
    print (row.trip_id)
    print (row.date)
    print (row.time)

if __name__=="__main__":

    #readFromScheduleAdherence()
    metadata=databaseConnect()
    readArchivedData(metadata)
    #writeToDataBase(metadata)



