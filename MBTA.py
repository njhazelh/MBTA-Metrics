#!/usr/bin/env python

"""
Question???????????????????????????????????????????????
1. some alert aoosicated with tripID is not for trian delay, it could be for entire line is shutdown 
some stations are close etc, typically, in the API call, "service_effect_text" is not for "delay", 
then we know this is not about train delay alert. See screentshoot, nondelayalert!! ! 
For this particular example, it has 76 different items under "services", which they all share same 
"alert_id", but has different trip_id (differentiate by different"trip_name" e.g.(2:15pm from Worcester))

Answer: don't care about alert that is not about delayed train


2. How do we know, when the alert is acutally sent out to the rider(is that throgugh "trip name " under
"Service" ????????)

how to deal with those ????????????  (So Existence and Timeliness could be implemented, but how 
to measure accuracy????)

3. What does "stop_id" and "stop_name" represent under the service??? in the Screentshoot of "No stop_id and 
stop_name .....", didn't find stop_id and stop_name, even though the delay affects range of stops

4. When a train is delayed less than 10 mins in a certain stop and if there is alert came out, do we care about those alert???? 

5. On extracing time range on alert message, does the delay time always presented in consistant way??



Structures: 
1. for the delayed train alert, everthing is based on schedule adherece where we can find acutal delay
  of the train in between certain stops. If we have all of the delayed information for each stop in each
  line. For each tripID we have associated in each stop in each line(in shcedule adherece), 
  We first look at if acutal delay is more than 10 mins, if not, don't care about this. If it is 
  then we need to cross referece it's tripID to archived alert data(implemment it in database or 
  in pyhton calculation ??????), in order to get the information in archived alert to measure its 
  exsistence, accuracy, and timeliness (of course, need more details on implementation of each measurement)
  The details depends on how we want our final result to be presented!!! discussed the CR-Alert.csv file 
  with TEAM !!!!!!!!!! 

  	Exsistece: for every stop in each line, look up every delayed time more than 10mins, cross reference tripID to archived alert 
  	database , see if there is alert existed, Also see if the alert came out before departure 
  				Care about the create_dt 

	
	Timeliness: will only be effective when the alert go out before the train's departure
				Care about the last one before the departure 
	

	Accuracy: To measure the accuracy, the alert need to be existed first  !!!! 
			 then for every alert in the archived database, cross reference its tripID, with the ones 
				in scheduleAdherence, and put that to the corresponding bucket 





"""
"""
convert the given seconds paramenter to minute
"""

def convertSecondToMinute(second): 



"""
check whether a delayd train deserves alert, alert is needed when a train is 10 mins
later than its scheduled arrival 
later than 
"""
def deserveAlert(actualDelay):
	return actualDelay>=10

"""
takes in a tripID of delayed train, and checks wheter it deserveAlert first, 
if it does, checks whether there is an alert associated with this tripID  
"""
def isAlertExisted(tripID):
	return false

"""
measure the accuray of an alert, compare the expected delay in alert with actual delay abd measure
the accuracy
@param: alertDelay --- is represented as a list of two integers (low,high), where low 
						is the lower bound of alertdelay, and high is the higer bound of 
						alert   
 
 If the actual delay is the the range, it is accurate, if the delay in lower than lower bond, then "high", 
 if the deklay is higher than upper bound, then "low". If there is no time range speified in the message, then "didn't have time"
"""
def alertAccuray(alertDelay, actualDelay):


"""
Measure the Timeliness of an lert, takes in alertSentTime, If the alsert sent out less than 5 mins later
of trains schedueld departure, then it is timely, otherwise not timely
@param alertSentTime: the actual sent time of an alert, represneted in a list[h,m,s,,d]
@param alertSentTime: the scheduled departure time of a train, represneted in a list[h,m,s,,d]
"""
def isAlertTimeliness(alertSentTime, TrainScheduleDeparture)









if __name__=="__main__":
	requestUrl = "http://realtime.mbta.com/developer/api/v2/alerts?api_key=wX9NwuHnZU2ToO7GmGR9uw&include_access_alerts=true&include_service_alerts=true&format=json"
	r = requests.get(requestUrl)
	print(r)