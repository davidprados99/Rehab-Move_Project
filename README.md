# Rehab & Move

> **Bridging Physiotherapy and Technology to enhance clinical treatment adherence.**

---

## Project Origin
As a former Physiotherapist turned Software Developer (DAM), I identified a critical issue in clinical practice: the lack of adherence to home-based exercises. The absence of professional supervision outside the clinic often leads to treatment abandonment or incorrect exercise execution, hindering recovery.

**Rehab & Move** was created to solve these challenges, offering a platform where clinical personalization and technological monitoring work in harmony.

---

## Key Features

* **Therapeutic Exercise Assignment:** Physiotherapists can prescribe specific exercises with instructional videos to ensure proper technique.

* **Adherence Logging:** Patients can log their daily activity, fostering consistency.

* **Pain Tracking (VAS Scale):** Pain level recording (1-10) post-exercise with personalized feedback for the professional.

* **Evolution Visualization:** Clinical evolution charts for both professional and patient via Matplotlib.

* **Clinical Calendar:** One-stop management for appointments and treatment sessions.

---

## Tech Stack

### **Backend & API**

1. **Language:** Python 3.12.

2. **Framework:** FastAPI.

3. **Data Validation:** Pydantic.

4. **Security:** Passlib (Bcrypt) for password management.

5. **Documentation:** Swagger UI (OpenAPI).

### **Infrastructure & DevOps**

1. **Application Server:** Gunicorn + Uvicorn.

2. **Reverse Proxy:** Nginx.

3. **Cloud Hosting:** AWS Elastic Beanstalk.

4. **Database:** PostgreSQL hosted on AWS RDS.

5. **CI/CD:** Automated pipeline with GitHub Actions.

6. **Cloud Security:** IAM (Identity and Access Management).

---

## Project Roadmap

* **Phase 1: Backend & REST API Development**

    * Relational database design.
    * Implementation of business logic and CRUD operations with FastAPI.
    * Security and password hashing.

* **Phase 2: Cloud Infrastructure & DevOps (Current)**

    * Deployment on **AWS Elastic Beanstalk**.
    * Production database on **AWS RDS**.
    * Deployment automation (CI/CD) with **GitHub Actions**.

* **Phase 3: Frontend Desktop (Coming Soon)**

    * Cross-platform graphical interface with **PySide6**.
    * Integration of dynamic graphs with **Matplotlib**.


---

## Current Project Status

Currently, the core of the application (REST API) is fully deployed and functional in the cloud.

* **API Live:** [Interactive Documentation (Swagger)](http://rehab-move-api-env-1.eba-epsm62av.us-east-1.elasticbeanstalk.com/docs)
* **Database:** Remote and synced with production environment.
* **Tests:** Unit tests integrated into the CI/CD flow.

---

## Project structure 

```
.
├── .github/workflows/
│   ├── main.yml         # CI/CD configuration (GitHub Actions)
├── backend/             # API logic, models, schemas, and CRUD
│   ├── main.py          # Application entry point
│   ├── test_main.py     # API functionality test file
│   ├── models.py        # Database models (SQLAlchemy)
│   ├── schemas.py       # Pydantic models (Validation)
│   ├── database.py      # Connection to AWS RDS
│   ├── crud.py          # Database operation logic
│   ├── security.py      # Password Management
│   └── db/
│       └── rehab_db.sql # Database SQL Script
├── frontend/            # Coming Soon (PySide6 Interface)
├── Procfile             # AWS Startup Instructions
├── venv/                # Python Virtual Environment
├── .env                 # Database Secrets
├── .gitignore           # Sets the files to ignore for Git
├── requirements.txt     # Project Dependencies
└── README.md
```

---

## Local installation (Development)

1. Create the repository:

```bash 
 git clone https://github.com/davidprados99/Rehab-Move_Project.git
```

2. Create the virtual environment:

```bash
 python -m venv venv
```

3. Install dependencies:

```bash
 pip install -r requirements.txt
```

4. Run the server:

```bash 
uvicorn backend.main:app --reload
```
---

## License
© 2026 David Prados Medina. All rights reserved.
Developed for educational purposes and professional portfolio.