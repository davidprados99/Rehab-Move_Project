# Rehab & Move

> **Bridging Physiotherapy and Technology to enhance clinical treatment adherence.**

---

## Project Origin
As a former Physiotherapist turned Software Developer (DAM), I identified a critical issue in clinical practice: the lack of adherence to home-based exercises. The absence of professional supervision outside the clinic often leads to treatment abandonment or incorrect exercise execution, hindering recovery.

**Rehab & Move** was created to solve these challenges, offering a platform where clinical personalization and technological monitoring work in harmony.

---

## Key Features

* **For Professionals**:

    * **Therapeutic Exercise Assignment:** Physiotherapists can prescribe specific exercises with instructional videos to ensure proper technique.

    * **Clinical Evolution:** Data-driven monitoring via Matplotlib.

    * **Patient Management:** Centralized dashboard for appointments and clinical history.

* **For Patients**:

    * **Daily Adherence Logging:** One click exercise competion tracking.

    * **Pain tracking (VAS Scale):** 1-10 pain level reporting with qualitative feedback.

    * **Interactive Calendar:** Visual schedule of treatment sessions.


---

## Full Stack Architecture

The project follows a hybrid-cloud architecture:

* **Database**: PostreSQL managed via AWS RDS.
* **Backend API**: FastAPI (Python 3.12) deployed on AWS Elastic Beanstalk.
* **Desktop App**: Cross-platform interface built with PySide6.
* **Web App**: React 18 (TypeScript) + Vite deployed on Vercel.


---

## Tech Stack

* **Backend & API**
    * **Framework:** FastAPI.
    * **ORM:** SQLAlchemy.
    * **Security:** Passlib + JWT (JSON Web Tokens).
    * **Validation:** Pydantic models.

* **DevOps & Infraestructure**
    * **CI/CD:** GitHub Actions (Automated testing & deployment).
    * **Hosting:** AWS (API & DB) + Vercel (Web).
    * **Reverse Proxy** Nginx (configured via AWS EB).

* **Frontend (Web & Desktop)**
    * **Desktop:** Python, PySide 6, Matplotlib, Requests.
    * **Web:** TypeScript, React, Tailwind CSS, Axios.

---

## Live Demo & Documentation

* **API Documentation** [Interactive Documentation (Swagger)](http://rehab-move-api-env-1.eba-epsm62av.us-east-1.elasticbeanstalk.com/docs)
* **Web Application:** [Rehab&Move Web](rehab-move-project.vercel.app)


---

## Project structure 

```
.
├── backend/                # FastAPI logic, models, and CRUD
    └── db/                 # DB directory with .sql file
├── frontend-web/           # React + TypeScript App (Vercel)
│   └──  vercel.json        # Vercel Deployment & Proxy Rules
├── frontend-desktop/       # PySide6 Desktop Application
├── .github/workflows/      # CI/CD Pipelines
├── requirements.txt        # Backend dependencies
├── Procfile                # AWS Elastic Beanstalk Instructions
└── README.md
```

---

## Local installation 

1. Create the repository:

```bash 
 git clone https://github.com/davidprados99/Rehab-Move_Project.git
```

2. Setup Backend:

```bash
 python -m venv venv
 source venv/bin/activate
 pip install -r requirements.txt
 uvicorn backend.main:app --reload
```

3. Run desktop app:

```bash
 python -m venv venv
 source venv/bin/activate
 pip install -r requirements.txt
 python -m frontend-desktop.main
```

4. Run web app:

```bash 
 cd frontend-web
 npm install
 npm run dev
```
---

## License
© 2026 David Prados Medina. All rights reserved.
Developed for educational purposes and professional portfolio.