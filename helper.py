
import re

def getSessionIdFromRequest(jsonData):
    sessionName = jsonData["queryResult"]["outputContexts"][0]['name']
    allResults = re.search("sessions/([a-zA-Z0-9-]*)/", sessionName)
    sessionId = allResults.group(1)
    return sessionId