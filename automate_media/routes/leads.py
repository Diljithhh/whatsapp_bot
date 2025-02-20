from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
# from ..services.firestore_service import firestore_client
from ..services.firestore_service import firestore_client

router = APIRouter()

@router.get("/leads/{phone}")
async def get_lead_by_phone(phone: str):
    try:
        leads_ref = firestore_client.collection('leads')
        query = leads_ref.where('phone', '==', phone).limit(1)
        leads = query.stream()

        lead_data = None
        for lead in leads:
            lead_data = lead.to_dict()
            break

        if lead_data:
            return JSONResponse(content=lead_data)
        else:
            raise HTTPException(status_code=404, detail="Lead not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
