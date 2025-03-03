from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from automate_media.models.partner import Partner
from automate_media.services.firestore_service import (
    check_partner,
    create_partner,
    update_partner,
    delete_partner,
    list_partners,
    firestore_client
)

router = APIRouter(tags=["Partners"])

@router.post("/", response_model=dict)
async def add_partner(partner: Partner):
    """
    Create a new partner in the database.
    """
    try:
        partner_id = await create_partner(partner.dict())
        return {"status": "success", "id": partner_id, "message": "Partner created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create partner: {str(e)}")

@router.get("/", response_model=List[Partner])
async def get_all_partners():
    """
    Get all partners from the database.
    """
    try:
        return await list_partners()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch partners: {str(e)}")

@router.get("/{partner_id}", response_model=Optional[Partner])
async def get_partner(partner_id: str):
    """
    Get a specific partner by ID.
    """
    try:
        partners_collection = firestore_client.collection('partners')
        partner_doc = partners_collection.document(partner_id).get()

        if partner_doc.exists:
            return partner_doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail=f"Partner with ID {partner_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch partner: {str(e)}")

@router.get("/check/{phone_number}", response_model=dict)
async def check_phone_number(phone_number: str):
    """
    Check if a phone number is registered as a partner.
    """
    try:
        partner = await check_partner(phone_number)
        if partner:
            return {"exists": True, "partner": partner}
        else:
            return {"exists": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check phone number: {str(e)}")

@router.put("/{partner_id}", response_model=dict)
async def update_partner_info(partner_id: str, partner_update: dict):
    """
    Update an existing partner.
    """
    try:
        success = await update_partner(partner_id, partner_update)
        if success:
            return {"status": "success", "message": "Partner updated successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Partner with ID {partner_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update partner: {str(e)}")

@router.delete("/{partner_id}", response_model=dict)
async def remove_partner(partner_id: str):
    """
    Delete a partner.
    """
    try:
        success = await delete_partner(partner_id)
        if success:
            return {"status": "success", "message": "Partner deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Partner with ID {partner_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete partner: {str(e)}")