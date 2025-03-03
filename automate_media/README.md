# WhatsApp Bot with Firebase Integration

This project integrates a WhatsApp bot with an existing Firebase Firestore database to manage partners and user interactions.

## Firebase Connection Setup

1. **Get Firebase Service Account Credentials**:
   - Go to your Firebase Console > Project Settings (LEROC Retail Dev) > Service Accounts
   - Click "Generate new private key" for Firebase Admin SDK
   - Save the JSON file securely in your project directory (make sure it's in .gitignore)

2. **Set Environment Variables**:
   Add to your .env file:
   ```
   FIREBASE_CREDENTIALS_PATH=/path/to/your/firebase_credentials.json
   ```

3. **Restart Your Application**:
   - Make sure to restart your application after setting up the credentials

## Existing Partner Database Structure

The application is configured to work with your existing partners collection structure:

```
partners (collection)
  ├── partner_id (document)
  │     ├── contactNumber: string (phone number)
  │     ├── contactPerson: string (person name)
  │     ├── partnerName: string (company name)
  │     ├── count: string
  │     ├── createdAt: timestamp
  │     ├── createdBy: string
  │     └── other fields...
```

## WhatsApp Bot Flow

When a user messages the bot:
1. The bot checks if the phone number exists in the partners collection (using the `contactNumber` field)
2. If the user is a registered partner, the bot responds with a personalized greeting using their `partnerName` or `contactPerson`
3. If not, the bot informs the user they're not a registered partner

## Testing the Bot

To test if the bot correctly identifies a registered partner:
1. Make sure your Firebase credentials are set up correctly
2. Send a message to the WhatsApp bot from a phone number that exists in your partners collection
3. The bot should identify you as a partner and provide a personalized greeting