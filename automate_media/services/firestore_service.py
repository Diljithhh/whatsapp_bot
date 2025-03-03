import firebase_admin
from firebase_admin import credentials, firestore
import os
import logging

logger = logging.getLogger(__name__)

# Get the path to Firebase credentials from environment variables
cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_credentials.json")

# Initialize Firebase with error handling for development/production
try:
    # Check if credentials file exists
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)

        # Initialize the Firebase app if it hasn't been initialized yet
        if not firebase_admin._apps:
            logger.info(f"Initializing Firebase with credentials from {cred_path}")
            firebase_admin.initialize_app(cred)

        firestore_client = firestore.client()
    else:
        logger.warning(f"Firebase credentials file not found at {cred_path}. Using mock implementation.")
        # Set up mock for local development when credentials not available
        class MockFirestore:
            def collection(self, name):
                return MockCollection(name)

        class MockCollection:
            def __init__(self, name):
                self.name = name

            def document(self, doc_id):
                return MockDocument(doc_id)

            def where(self, field, op, value):
                return self

            def limit(self, count):
                return self

            def get(self):
                return []

        class MockDocument:
            def __init__(self, doc_id):
                self.id = doc_id

            def set(self, data):
                logger.info(f"Mock set document {self.id}: {data}")
                return self.id

            def update(self, data):
                logger.info(f"Mock update document {self.id}: {data}")
                return True

            def delete(self):
                logger.info(f"Mock delete document {self.id}")
                return True

            def get(self):
                mock_doc = MockDocumentSnapshot(self.id)
                return mock_doc

        class MockDocumentSnapshot:
            def __init__(self, doc_id):
                self.id = doc_id
                self.exists = False

            def to_dict(self):
                return {}

        firestore_client = MockFirestore()

except Exception as e:
    logger.error(f"Error initializing Firebase: {str(e)}")
    # Provide a mock implementation as fallback
    class MockFirestore:
        def collection(self, name):
            return MockCollection(name)

    class MockCollection:
        def __init__(self, name):
            self.name = name

        def document(self, doc_id):
            return MockDocument(doc_id)

        def where(self, field, op, value):
            return self

        def limit(self, count):
            return self

        def get(self):
            return []

    class MockDocument:
        def __init__(self, doc_id):
            self.id = doc_id

        def set(self, data):
            logger.info(f"Mock set document {self.id}: {data}")
            return self.id

        def update(self, data):
            logger.info(f"Mock update document {self.id}: {data}")
            return True

        def delete(self):
            logger.info(f"Mock delete document {self.id}")
            return True

        def get(self):
            mock_doc = MockDocumentSnapshot(self.id)
            return mock_doc

    class MockDocumentSnapshot:
        def __init__(self, doc_id):
            self.id = doc_id
            self.exists = False

        def to_dict(self):
            return {}

    firestore_client = MockFirestore()

async def save_lead(lead_data):
    lead_collection = firestore_client.collection('leads')
    lead_doc = lead_collection.document(lead_data['id'])
    lead_doc.set(lead_data)
    return lead_doc.id

async def check_partner(phone_number):
    """
    Check if a phone number exists in the partners collection.

    Args:
        phone_number (str): The phone number to check

    Returns:
        dict or None: Partner data if found, None otherwise
    """
    # Remove any '+' prefix and standardize the phone number format
    phone_number = phone_number.replace('+', '').strip()

    # Query the partners collection by contactNumber field
    partners_collection = firestore_client.collection('partners')
    query = partners_collection.where('contactNumber', '==', phone_number).limit(1)
    results = query.get()

    # Check if we found a matching partner
    if len(results) > 0:
        partner_doc = results[0]
        return partner_doc.to_dict()

    return None

async def create_partner(partner_data):
    """
    Create a new partner in the database.

    Args:
        partner_data (dict): The partner data to save

    Returns:
        str: The ID of the created partner document
    """
    partners_collection = firestore_client.collection('partners')

    # Check if a partner with this phone number already exists
    existing_partner = await check_partner(partner_data['phone_number'])
    if existing_partner:
        raise ValueError(f"Partner with phone number {partner_data['phone_number']} already exists")

    # Create the new partner
    partner_doc = partners_collection.document(partner_data['id'])
    partner_doc.set(partner_data)
    return partner_doc.id

async def update_partner(partner_id, partner_data):
    """
    Update an existing partner in the database.

    Args:
        partner_id (str): The ID of the partner to update
        partner_data (dict): The updated partner data

    Returns:
        bool: True if successful, False if partner not found
    """
    partners_collection = firestore_client.collection('partners')
    partner_doc = partners_collection.document(partner_id)

    if partner_doc.get().exists:
        partner_doc.update(partner_data)
        return True
    return False

async def delete_partner(partner_id):
    """
    Delete a partner from the database.

    Args:
        partner_id (str): The ID of the partner to delete

    Returns:
        bool: True if successful, False if partner not found
    """
    partners_collection = firestore_client.collection('partners')
    partner_doc = partners_collection.document(partner_id)

    if partner_doc.get().exists:
        partner_doc.delete()
        return True
    return False

async def list_partners():
    """
    List all partners in the database.

    Returns:
        list: List of partner documents
    """
    partners_collection = firestore_client.collection('partners')
    results = partners_collection.get()

    partners = []
    for doc in results:
        partner = doc.to_dict()
        partners.append(partner)

    return partners
