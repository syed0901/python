
import xml.dom.minidom
import urllib2
from notif import *
import time
import sys
from datetime import datetime 

class CricbuzzParser():
    
    def __init__(self):
        # self.getXml(url)
        pass
       
    def getXml(self):
        #Change coding here
        site= "http://synd.cricbuzz.com/j2me/1.0/livematches.xml"
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

        req = urllib2.Request(site, headers=hdr)
        f = urllib2.urlopen(req)
        doc = xml.dom.minidom.parse(f)
        node = doc.documentElement
        matches = node.getElementsByTagName("match")
        return matches

    def handleMatches(self,matches):
        """This function handles the element <match> and
        avoids duplicate matches to be processed. """
        duplicate = []
        match_details = []
        for match in matches:
	# mchDesc = matches[0].getAttribute("mchDesc")
        # duplicate.append(mchDesc)
        # match_detail = self.handleMatch(matches[0])
        # match_details.append(match_detail)
        # match_detail = self.handleTestMatch(matches[0])
        # match_details.append(match_detail)       
            mchDesc = match.getAttribute("mchDesc")
            if "IND " in mchDesc or " IND" in mchDesc:
	            flag = False
	            #If list duplicate is empty, then populate it initially.
		    for entry in duplicate:
	                if entry == mchDesc: #If duplicate is found
	                    flag = True
	            if flag is not True:
	                duplicate.append(mchDesc)
	                match_detail = self.handleMatch(match)
	                match_details.append(match_detail)
	                match_detail = self.handleTestMatch(match)
	                match_details.append(match_detail)
        return match_details

    def handleTestMatch(self,match):
        """For handling Test Matches.
        To Do: Write Code for Parsing Innings detail"""
        series = match.getAttribute("srs")
        mtype = match.getAttribute("type")
        if mtype != "TEST":
            return None
        else:
            match_desc = match.getAttribute("mchDesc")
            mground = match.getAttribute("grnd")
            states = match.getElementsByTagName("state")
            for state in states:
                match_cstate = state.getAttribute("mchState")
                mstatus = state.getAttribute("status")
                if mstatus.startswith("Starts") or mstatus.startswith("Coming"):
                    return None       #Match hasn't started Yet.
        return {"Match Format":"TEST","Match":match_desc,"Venue":mground,"State":match_cstate,"Status":mstatus} 
                
            
    def handleMatch(self,match):
        """Handles ODI and T20 matches"""
        bowl_runs  = None
        bowl_wkts = None
        bowl_overs = None
        series = match.getAttribute("srs")
        mtype = match.getAttribute("type")
	if mtype == "TEST":
            return None
        match_desc = match.getAttribute("mchDesc")
        mground = match.getAttribute("grnd")
        states = match.getElementsByTagName("state")
        for state in states:
            match_cstate = state.getAttribute("mchState")
            mstatus = state.getAttribute("status")
            if mstatus.startswith("Starts") or mstatus.startswith("Coming"):
                return None       #Match hasn't started Yet.
        try:
            batting_team = match.getElementsByTagName("btTm")
            bowling_team = match.getElementsByTagName("blgTm")
            batting_team_name = batting_team[0].getAttribute("sName")
            bowling_team_name = bowling_team[0].getAttribute("sName")
            innings = match.getElementsByTagName("Inngs")
            bat_runs = innings[0].getAttribute("r")
            bat_overs = innings[0].getAttribute("ovrs")
            bat_wkts = innings[0].getAttribute("wkts")
        except Exception:
            #Match is comple. Only Result is availabe now and btTm tag has been changed to Tm
            #So, now only status of the match is important. Initialize none to other parameters.
            batting_team = None
            bowling_team = None
            batting_team_name = None
            bowling_team_name = None
            innings = None
            bat_runs = None
            bat_overs = None
            bat_wkts = None
        try:
            bowl_runs = innings[1].getAttribute("r")
            bowl_overs = innings[1].getAttribute("ovrs")
            bowl_wkts = innings[1].getAttribute("wkts")
        except Exception:
            # The opponent team hasn't yet started to Bat.
            pass
        return { "Series": series, "Match Format": mtype, "Team":match_desc, "Venue":mground, "Match State":match_cstate,"Match Status":mstatus, "Batting team":batting_team_name, "Bowling team":bowling_team_name, "Batting Team Runs":bat_runs, "Batting Team Overs":bat_overs, "Batting Team Wickets":bat_wkts, "Bowling Team Runs":bowl_runs, "Bowling Team Overs": bowl_overs, "Bowling Team Wickets": bowl_wkts }

if __name__ == '__main__':
	while(True):
	    w=WindowsBalloonTip()
	    cric = CricbuzzParser()
	    match = cric.getXml()
	    details = cric.handleMatches(match) #Returns Match details as a Dictionary. Parse it according to requirements.
	    detail = details[0]
	    suffix = ""
	    if detail["Bowling team"] is not None:
	        suffix = suffix +detail["Bowling team"] + " "
	    if detail["Bowling Team Runs"] is not None:
	        suffix = suffix + "Runs: " +detail["Bowling Team Runs"]
	    if detail["Bowling Team Wickets"] is not None:
	        suffix = suffix +"/"+detail["Bowling Team Wickets"]
	    if detail["Bowling Team Overs"] is not None:
	        suffix = suffix + " Overs: " +detail["Bowling Team Overs"]
	    else:
	        suffix = suffix + "Yet to bat"

	    print "[" + str(datetime.now()) + "] "+ detail["Match Status"] + "\n" +  detail["Batting team"] + " Runs: "+ detail["Batting Team Runs"] +"/" + detail["Batting Team Wickets"] + " Overs: " + detail["Batting Team Overs"] + "\n" + suffix
	    notifi = detail["Match Status"] + "\n" + detail["Batting team"] + " Runs: "+ detail["Batting Team Runs"] +"/" + detail["Batting Team Wickets"] + " Overs: " + detail["Batting Team Overs"] + "\n" + suffix
	    w.handleNotif("Match Status", notifi)
            time.sleep(float(sys.argv[1]))