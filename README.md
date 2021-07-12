
# 🇿🇼 WhatsApp Chatbot – ZANU PF Youth League Registration Bot - 2021

This project is a WhatsApp-based chatbot built with Flask and Twilio that facilitates digital membership registration for the ZANU PF Youth League. It automates user onboarding, profile management, and provides access to a centralized database of registered members.

---

## 📌 Features

- 📲 **WhatsApp Chatbot** using Twilio API
- 🗂️ Step-by-step **user registration**
- 🏠 District and province selection (Zimbabwe-specific)
- 🧾 User **profile view**
- 📸 Profile photo upload support
- 🔒 Secure **password setup** for portal access
- 📥 Admin **database download** as Excel
- 🔑 Token-based sign-in and API authentication
- 🔄 CORS-enabled for cross-origin API requests

---

## 🚀 Tech Stack

- **Backend:** Python (Flask)
- **Messaging:** Twilio WhatsApp API
- **Database:** MongoDB (via `mongoengine`)
- **Security:** Password encryption (custom or `bcrypt`)
- **Others:** Pandas (for Excel export), ImageAI (optional image prediction), CORS, Ngrok (for development tunneling)

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/whatsapp-chatbot.git
cd whatsapp-chatbot
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> _You will also need MongoDB installed and running locally or remotely._

### 4. Configure Environment

Update the following in your `bot.py` or create a `.env`:

```python
account_sid = 'your_twilio_account_sid'
auth_token = 'your_twilio_auth_token'
phonenumber = 'your_twilio_whatsapp_number'
server_url = 'your_public_ngrok_url_or_domain'
```

### 5. Run the Application

```bash
python bot.py
```

---

## 📞 Twilio Webhook Setup

In your Twilio Console:

- Go to your WhatsApp sender number.
- Under "Webhook Configuration", set the **Incoming Message webhook** to:

```
https://your-ngrok-url.ngrok.io/bot
```

Use tools like **ngrok** for local testing:

```bash
ngrok http 5000
```

---

## 💬 Commands Overview

| User Message      | Action                            |
|------------------|-----------------------------------|
| `hie` / `join`   | Start the bot                     |
| `1`              | Begin registration                |
| `2`              | View about info                   |
| `3`              | View your profile                 |
| `set password`   | (Admin only) Set portal password  |

---

## 🔐 Portal API Endpoints

| Endpoint                              | Method | Description                          |
|--------------------------------------|--------|--------------------------------------|
| `/signin`                            | POST   | Sign in using phone number + password|
| `/downloadDatabase`                  | GET    | Download Excel file of all members   |
| `/deactivateAccessToken/<token>`     | GET    | Deactivate a user's access token     |
| `/getUserDetailsByAccessToken/<token>` | GET  | Fetch user data via access token     |

---

## 📷 Profile Image Upload

- Users can optionally upload a profile image during registration.
- Image is saved under `./profile-images/` and served via `/media/<filename>`.

---

## 📊 Excel Export

- Admins can export all registered user data to an Excel file (`members.xlsx`).
- Uses `pandas` for data processing and formatting.

---

## 🔒 Security Notes

- Phone numbers and passwords are stored securely using encryption.
- Restricted functions (like setting passwords) are limited to whitelisted numbers.

---

## 📁 Project Structure

```
.
├── bot.py                # Main Flask application
├── database.py           # MongoDB initialization
├── models.py             # MongoEngine data models
├── encrypt.py            # Password hashing utilities
├── profile-images/       # Directory for user selfies
└── members.xlsx          # Exported member data (generated)
```

---

## 🤝 Contributing

Pull requests and forks are welcome. Please ensure new features are tested and follow the existing code style.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
