# Rehab & Move

<details>
<summary><b>US Read in English (Click to expand)</b></summary>
<a name="english-version"></a>

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

* **[x] Phase 1: Backend & REST API Development**

* Relational database design.
* Implementation of business logic and CRUD operations with FastAPI.
* Security and password hashing.

* **[x] Phase 2: Cloud Infrastructure & DevOps (Current)**

* Deployment on **AWS Elastic Beanstalk**.
* Production database on **AWS RDS**.
* Deployment automation (CI/CD) with **GitHub Actions**.

* **[ ]Phase 3: Frontend Desktop (Coming Soon)**

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

---
</details>
<details>
<summary><b>ES Leer en Español (Click para desplegar)</b></summary>
<a name="spanish-version"></a>

> **Uniendo la fisioterapia y la tecnología para mejorar la adherencia al tratamiento clínico.**

--- 

## Origen del proyecto

Como fisioterapeuta de profesión y ahora desarrollador de software (DAM), identifiqué un problema crítico en la práctica clínica: la falta de adherencia al ejercicio domiciliario. La ausencia de supervisión profesional fuera de la consulta suele desembocar en el abandono del tratamiento o en ejecuciones incorrectas del ejercicio que reduce el éxito de la rehabilitación.

**Rehab & Move** surge como solución para solventar estos inconvenientes, ofreciendo una plataforma donde la personalización clínica y el seguimiento a través de la tecnología van de la mano.

--- 

## Características principales

- **Asignación de Ejercicio Terapéutico:** Los fisioterapeutas pueden pautar ejercicios específicos con videos explicativos para garantizar la técnica correcta.

- **Registro de Adherencia:** Los pacientes pueden registrar su actividad diaria, fomentando la constancia.

- **Seguimiento del dolor (Escala EVA):** Registro del dolor (1-10) post-ejercicio con un feedback personalizado.

- **Visualización de Evolución:** Generación de gráficas de evolución clínica para profesional y paciente.

- **Calendario clínico:** Gestión de citas y sesiones de tratamiento en un solo lugar.

---

## Stack Tecnológico

### **Backend & API**

1. **Lenguaje:** Python 3.12.

2. **Framework:** FastAPI.

3. **Validación de datos:** Pydantic.

4. **Seguridad:** Passlib (Bcrypt) para gestión de contraseñas.

5. **Documentación:** Swagger UI (OpenAPI).

### Infraestructura & DevOps

1. **Servidor de Aplicaciones:** Gunicorn + Uvicorn.

2. **Proxy Inverso:** Nginx.

3. **Cloud Hosting:** AWS Elastic Beanstalk.

4. **Base de Datos:** PostgreSQL alojada en AWS RDS.

5.  **CI/CD:** Pipeline automatizado con GitHub Actions.

6. **Seguridad Cloud:** Gestión de identidades con AWS IAM.

---

## Roadmap del Proyecto

* **[x] Fase 1: Desarrollo del Backend & API REST**
    * Diseño de base de datos relacional.
    * Implementación de lógica de negocio y CRUD con FastAPI.
    * Seguridad y hashing de contraseñas.

* **[x] Fase 2: Cloud Infrastructure & DevOps (Actual)**
    * Despliegue en **AWS Elastic Beanstalk**.
    * Base de Datos productiva en **AWS RDS**.
    * Automatización de despliegue (CI/CD) con **GitHub Actions**.

* **[ ]Fase 3: Frontend Desktop (Próximamente)**
    * Interfaz gráfica multiplataforma con **PySide6**.
    * Integración de gráficas dinámicas con **Matplotlib**.

---

## Estado actual del proyecto

Actualmente, el núcleo de la aplicación (API REST) se encuentra totalmente desplegado y funcional en la nube.

- **API Live:** [Documentación Swagger](http://rehab-move-api-env-1.eba-epsm62av.us-east-1.elasticbeanstalk.com/docs)

- **Base de Datos:** Remota y sincronizada con el entorno de producción.

- **Tests:** Pruebas unitarias integradas en el flujo de despliegue continuo.

---

## Estructura del proyecto

```
.
├── .github/workflows/
│   ├── main.yml         # Configuración de CI/CD (GitHub Actions)
├── backend/             # Lógica de la API, modelos, esquemas y CRUD
│   ├── main.py          # Punto de entrada de la aplicación
│   ├── test_main.py     # Fichero test de funcionamiento de la API
│   ├── models.py        # Modelos de base de datos (SQLAlchemy)
│   ├── schemas.py       # Pydantic models (Validación)
│   ├── database.py      # Conexión con AWS RDS
│   ├── crud.py          # Lógica de operaciones DB
│   ├── security.py      # Gestión de contraseñas
│   └── db/
│       └── rehab_db.sql # Script SQL de la base de datos
├── frontend/            # Próximamente (Interfaz PySide6)
├── Procfile             # Instrucciones de arranque para AWS
├── venv/                # Entorno virtual de python
├── .env                 # Secrets de la base de datos
├── .gitignore           # Establece los ficheros a ignorar por git
├── requirements.txt     # Dependencias del proyecto
└── README.md
```

---

## Instalación Local (Desarrollo)

1. Crear el repositorio:

```bash 
 git clone https://github.com/davidprados99/Rehab-Move_Project.git
```

2. Crear el entorno virtual:

```bash
 python -m venv venv
```

3. Instalar dependencias:

```bash
 pip install -r requirements.txt
```

4. Ejecutar servidor:

```bash 
uvicorn backend.main:app --reload
```

---

## Licencia

Este proyecto ha sido desarrollado con fines educativos y como portfolio profesional.

**© 2026 David Prados Medina. Todos los derechos reservados.**

No está permitido el uso o distribución sin autorización expresa del autor.

---

Desarrollado por **David Prados Medina** - Desarrollador Multiplataforma. - 2026.

---
</details>