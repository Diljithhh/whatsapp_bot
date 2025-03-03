#!/usr/bin/env python3
"""
Script to add a test partner to the Firebase database.
Usage: python add_test_partner.py <phone_number> <name>
"""

import sys
import asyncio
import json
from datetime import datetime
import uuid
from automate_media.services.firestore_service import create_partner

async def add_test_partner(phone_number, name, email=None, company=None):
    """Add a test partner to the Firebase database."""
    partner_data = {
        "id": str(uuid.uuid4()),
        "name": name,
        "phone_number": phone_number.replace('+', '').strip(),
        "email": email,
        "company": company,
        "created_at": datetime.now().isoformat()
    }

    try:
        partner_id = await create_partner(partner_data)
        print(f"Partner added successfully with ID: {partner_id}")
        print(f"Partner data: {json.dumps(partner_data, indent=2)}")
        return partner_id
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python add_test_partner.py <phone_number> <name> [email] [company]")
        sys.exit(1)

    phone_number = sys.argv[1]
    name = sys.argv[2]
    email = sys.argv[3] if len(sys.argv) > 3 else None
    company = sys.argv[4] if len(sys.argv) > 4 else None

    asyncio.run(add_test_partner(phone_number, name, email, company))