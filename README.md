# Rehab & Move

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

* **[]Fase 3: Frontend Desktop (Próximamente)**
    * Interfaz gráfica multiplataforma con **PySide6**.
    * Integración de gráficas dinámicas con **Matplotlib**.

---

## Estado actual del proyecto.

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