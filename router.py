
import fastapi
from fastapi import Request

import helper
import requestHandling

router = fastapi.APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Hello"}


@router.post("/")
async def handle_request(request: Request):

    # Retrieve the JSON data from the request
    data = await request.json()
    intent_display_name = data["queryResult"]["intent"]["displayName"]
    sessionId = helper.getSessionIdFromRequest(data)

    if intent_display_name == "Menu-price":
        return requestHandling.getMenuPrice(data)
    elif intent_display_name == "Order Inquiry - order list":
        return requestHandling.makeOrder(data, sessionId)
    elif intent_display_name == "Order Inquiry - order list - more":
        return requestHandling.addMoreToOrder(data, sessionId)
    elif intent_display_name == "Order Inquiry - order list - complete":
        return requestHandling.completeOrder(data, sessionId)





