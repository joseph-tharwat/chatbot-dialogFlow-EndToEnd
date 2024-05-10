
from fastapi.responses import JSONResponse
import databaseHandling

inProgressOrder = {}

#Shoud be in database
#not_found
#in_transit
ordersStatus = {}


def getMenuPrice(data):
    itemNames = data["queryResult"]["parameters"]["menuitem"]
    if not isinstance(itemNames, list):
        itemNames = [itemNames]

    textResponse = "the price of "
    for item in itemNames:
        textResponse = textResponse + item + " :$" + str(databaseHandling.getItemPrice(item)) + ", "
    return JSONResponse(content={"fulfillmentText": textResponse})


def makeOrder(data, sessionId):
    itemNames = data["queryResult"]["parameters"]["menuitem"]
    itemNumbers = data["queryResult"]["parameters"]["number"]
    totalCost = 0
    textResponse = ""

    newDictionary = {}
    for item, num in zip(itemNames, itemNumbers):
        newDictionary[item] = int(num)

    if sessionId not in inProgressOrder:
        inProgressOrder[sessionId] = {}

    # add the new items to the inProgress order Dictionary
    for item, num in newDictionary.items():
        if item in inProgressOrder[sessionId]:
            inProgressOrder[sessionId][item] = inProgressOrder[sessionId][item] + num
        else:
            inProgressOrder[sessionId][item] = num

    for item, num in inProgressOrder[sessionId].items():

        totalCost = totalCost + databaseHandling.getItemPrice(item) * num
        textResponse = textResponse + ", " + str(int(num)) + " " + item + ": " + str(databaseHandling.getItemPrice(item) * num)

    textResponse = textResponse + " so the total price is $" + str(totalCost) + ". Anything else?"
    return JSONResponse(content={"fulfillmentText": textResponse})


def completeOrder(data, sessionId):
    global orderId
    fulfillmentBasicResponse = data["queryResult"]["fulfillmentText"]
    textResponse = fulfillmentBasicResponse

    # get a new id from database
    # store the order in database
    orderId = databaseHandling.storeNewOrder(sessionId, inProgressOrder)
    textResponse = textResponse + " " + str(orderId)

    del inProgressOrder[sessionId]
    ordersStatus[orderId] = "in_transit"

    return JSONResponse(content={"fulfillmentText": textResponse})


def addMoreToOrder(data, sessionId):
    if sessionId not in inProgressOrder:
        return JSONResponse(content={"fulfillmentText": "sorry, I do not understand you."})

    itemNames = data["queryResult"]["parameters"]["menuitem"]
    itemNumbers = data["queryResult"]["parameters"]["number"]

    totalCost = 0
    textResponse = ""
    newDictionary = {}
    for item, num in zip(itemNames, itemNumbers):
        newDictionary[item] = int(num)

    # add the new items to the inProgress order Dictionary
    for item, num in newDictionary.items():
        if item in inProgressOrder[sessionId]:
            inProgressOrder[sessionId][item] = inProgressOrder[sessionId][item] + num
        else:
            inProgressOrder[sessionId][item] = num

    for item, num in inProgressOrder[sessionId].items():
        totalCost = totalCost + databaseHandling.getItemPrice(item) * num
        textResponse = textResponse + ", " + str(int(num)) + " " + item + ": " + str(databaseHandling.getItemPrice(item) * num)

    textResponse = textResponse + " so the total price is $" + str(totalCost) + ". Somthing else?"

    return JSONResponse(content={"fulfillmentText": textResponse})

