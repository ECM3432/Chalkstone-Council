# Chalkstone Issue Tracking System

## Purpose
The Chalkstone Issue Tracking System was developed to support Chalkstone Council in managing and addressing public and staff-reported infrastructure issues efficiently. The platform allows users to report, track, and analyze problems such as potholes, graffiti, fly-tipping, and broken streetlights.

## Aims
- Enable public users and staff to log issues quickly and accurately.
- Allow staff to assign, update, and close issues based on progress.
- Provide meaningful analytics to staff and administrators for decision-making.
- Ensure a secure and user-friendly system with scalable architecture.

## Users' Goals:
- Public users can create accounts, log in, and report issues.
- Staff members can manage, categorize, assign, and analyze issues.
- Admins can manage user permissions and monitor overall platform activity.

## Site Goals:
- Provide a clear and accessible interface for users of varying technical skills.
- Ensure security and data integrity through Django’s built-in authentication.
- Offer real-time data analysis and visualizations to support council operations.

## Target Audience
The primary audience includes:
- Local residents and public users wishing to report service issues.
- Council staff responsible for resolving and managing logged issues.
- Administrators overseeing system use and performance.

## Features to be included
- Secure registration and login (including Google OAuth).
- Ability to report, edit, and view issues.
- Staff-only tools for assigning issues, updating status, and categorizing.
- Commenting system for user and staff communication.
- Analytics dashboard for reporting trends, resolution times, and staff workload.
- Admin controls for managing user roles and CRUD access.

# User Experience (UX)

## Development Method
The project followed an Agile methodology with iterative planning and development. The MoSCoW method was used to prioritize features:
- **Must Have**: Issue logging, user authentication, analytics, role-based access.
- **Should Have**: OAuth login, commenting system.
- **Could Have**: Advanced filters and chart-based analytics.
- **Won’t Have**: Notifications or mobile app version.

## Design

### Database Schema
The datasets for the project are:
- **Users**: Handles account credentials and permissions.
- **Issues**: Stores reports submitted by users.
- **Comments**: Captures discussion on each issue.

# Features

## Current Features:
- Public user registration/login with optional Google OAuth.
- Issue creation and edit functionality.
- Commenting system (user and staff).
- Staff-only issue assignment, categorization, and status updates.
- Issue search and filtering.
- Analytics dashboard with interactive charts (Chart.js).

### Admin Only Features
- Ability to assign or revoke staff access.
- Full CRUD access to all user, issue, and comment records.
- Management of system-level configurations and access control.

# Technologies

## Programming Languages:
- **Python** – Backend development and Django framework logic.
- **HTML/CSS** – Web page structure and styling.
- **JavaScript** – Frontend interactivity and analytics charts.

## Frameworks:
- **Django** – MVT-based web framework used to manage backend functionality.
- **Bootstrap** – Frontend CSS framework for responsive UI.

## Libraries:
- **Chart.js** – JavaScript library used for displaying analytics graphs.
- **Django-Allauth** – Provides OAuth support for Google login.
- **OS Library** – Python standard library used for environment management.

## Programs Used:
- **VSCode** – Code editor.
- **Git** – Version control.
- **GitHub** – Repository hosting.
- **Balsamiq** – Wireframe design tool.

# Deployment

## 🛠️ Getting Started

This section provides instructions for setting up and running the Chalkstone Council Issue Tracking System locally for development and testing purposes.

---

## ✅ Prerequisites

Make sure you have the following installed:

- [Python 3.11.9](https://www.python.org/downloads/release/python-3119/)
- [Git](https://git-scm.com/) – For version control
- [pip](https://pip.pypa.io/en/stable/) – Python package installer
- A virtual environment tool (e.g., `venv`)
- [SQLite3](https://www.sqlite.org/index.html) *(installed by default with Python)*

---

## 🚀 Local Setup

### 1. Clone the Repository
Open your terminal and run:

```bash
git clone https://github.com/ECM3432/Chalkstone-Council.git
cd chalkstone-council
```

### 2. Create and Activate a Virtual Environment

```
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

```

### 3. Install Project Dependencies

```
pip install -r requirements.txt
```

If you are setting up from scratch and need to manually install Django:

```
pip install django
```

### 4. Environment Variables

```
SECRET_KEY= your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

```

### 5. Apply Migrations & Start the Server

1. Run Migrations

    ```
    python manage.py migrate
    ```

2. Create superuser (for admin access)

    ```
    python manage.py createsuperuser
    ```

3. Start the Development Server

    ```
    python manage.py runserver
    ```

Visit the app at:
📍 http://127.0.0.1:8000/

### Testing

You can run unit tests using Django's built-in test runner:
```
python manage.py test {appname}
```

### Admin Panel

Access the Django admin dashboard at: 📍 http://127.0.0.1:8000/admin/
Use the superuser credentials you created earlier.

# Contributing

1. Create a feature branch from main
2. Make your changes
3. Write/update tests
4. Submit a pull request

For detailed contribution guidelines, please contact the development team.