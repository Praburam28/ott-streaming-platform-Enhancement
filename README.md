<div align="center">

# 🎬 OTT Streaming Platform

### Secure Video & Music Streaming Platform with Subscription & Admin Management

![Python](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-Styling-1572B6?style=for-the-badge&logo=css3)

Production-ready OTT Streaming Platform built using **FastAPI**, **MySQL**, **JWT Authentication**, **API Keys**, and **Vanilla JavaScript**.

</div>

---

# 📖 Overview

The OTT Streaming Platform is a full-stack web application that enables users to securely stream video and music content based on subscription plans.

The platform includes secure authentication, API key management, subscription management, streaming, watch history, favorites, automated reporting, and advanced admin controls.

---

# ✨ Features

## 👤 User Module

- User Registration
- Secure Login (JWT Authentication)
- Profile Management
- API Key Generation
- Watch History
- Favorites
- Video Streaming
- Music Streaming

---

## 💳 Subscription Module

- Free Plan
- Basic Plan
- Premium Plan
- Subscribe
- Upgrade Plan
- Downgrade Plan
- Cancel Subscription
- Current Subscription
- Proration Preview

---

## 🛠 Admin Module

### Advanced Admin Controls

- Force Upgrade Subscription
- Force Downgrade Subscription
- Pause Subscription
- Resume Subscription
- Apply Manual Discounts
- Apply Manual Credits

### Admin Audit Log

Tracks:

- Admin User
- Action Performed
- Affected User
- Timestamp

---

# 📊 Reports Automation

Implemented Reports

- Monthly Revenue Report
- Active vs Cancelled Subscription Report
- Plan-wise Subscription Distribution

Exports

- CSV
- PDF

Automation

- Scheduled Report Generation
- Email Reports to Admin

---

# 🎨 Frontend Enhancements

### Subscription UX

- Confirmation Modal before Cancellation
- Proration Preview
- Current Subscription View
- Renew Subscription CTA

### Dashboard

- Usage Metrics
- Progress Bars
- 80% Warning Indicator
- Usage Limit Warning

### Error Handling

- Payment Failure Retry
- Subscription Expired State
- Network/API Failure Handling

---

# 🏗 Technology Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- MySQL
- JWT Authentication
- Passlib
- APScheduler
- ReportLab

## Frontend

- HTML5
- CSS3
- JavaScript
- Fetch API

---

# 📂 Project Structure

```text
OTT-Streaming-Platform
│
├── backend
│   ├── app
│   │   ├── api
│   │   ├── core
│   │   ├── db
│   │   ├── dependencies
│   │   ├── middleware
│   │   ├── models
│   │   ├── repositories
│   │   ├── reports
│   │   ├── scheduler
│   │   ├── schemas
│   │   ├── services
│   │   └── main.py
│   │
│   ├── uploads
│   ├── logs
│   ├── tests
│   ├── requirements.txt
│   └── .env
│
└── frontend
    ├── assets
    ├── css
    ├── js
    ├── login.html
    ├── signup.html
    ├── dashboard.html
    ├── subscription.html
    ├── profile.html
    ├── reports.html
    ├── video-player.html
    ├── music-player.html
    └── admin-upload.html
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/<your-github-username>/ott-streaming-platform.git
```

---

## Backend

```bash
cd backend
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn app.main:app --reload
```

Backend

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## Frontend

```bash
cd frontend
```

Run

```bash
python -m http.server 5500
```

Open

```
http://127.0.0.1:5500/login.html
```

---

# 🔐 Security

- JWT Authentication
- Password Hashing
- Protected APIs
- API Key Validation
- Subscription Validation
- Role-Based Authorization
- Security Headers Middleware

---

# 📡 API Modules

### Authentication

- Signup
- Login
- Current User

### Subscription

- Subscription Plans
- Subscribe
- Cancel Subscription
- Current Subscription
- Proration Preview

### Profile

- Profile
- Watch History
- Favorites
- Usage Metrics

### Streaming

- Video Streaming
- Music Streaming

### Admin

- Change Subscription
- Pause Subscription
- Resume Subscription
- Discount / Credit
- Audit Logs

### Reports

- Monthly Revenue
- Subscription Summary
- Plan Distribution
- Export CSV
- Export PDF

---

# 📷 Screenshots

Add screenshots here.

Example:

```
screenshots/
    login.png
    dashboard.png
    subscription.png
    reports.png
```

---

# 🌟 Future Enhancements

- Online Payment Gateway
- Recommendation Engine
- Multi-language Support
- Mobile Application
- Watch Later
- AI-based Content Suggestions

---

# 👨‍💻 Author

## **Prabu Ram**

**Python Full Stack Developer**

- Python
- FastAPI
- MySQL
- REST APIs
- SQLAlchemy
- JavaScript
- HTML & CSS

GitHub: **https://github.com/Praburam28**


---

<div align="center">

### ⭐ If you found this project useful, consider giving it a star!

</div>
