# ShieldBot

## Overview

ShieldBot is a comprehensive application designed for testing web vulnerabilities, including brute force attacks, SQL injection, and DoS simulations. The project consists of a **Flutter-based front-end** and a **Flask-based backend**, integrated with Firebase and other technologies for real-time updates and robust functionality.

---

## **Frontend**

### Overview

The frontend of ShieldBot is built with Flutter and provides a user-friendly interface for simulating security tests. It connects with the backend for executing tasks and displaying real-time results.

### Features

- **Brute Force Attack Simulation**: Test for common password vulnerabilities.
- **SQL Injection Simulation**: Identify weak query sanitization practices.
- **Denial of Service Simulation**: Evaluate server resilience under high traffic.
- **Firebase Integration**: Real-time updates and data synchronization.
- **Interactive UI**: Built with Flutter for a responsive and engaging experience.

### Getting Started

#### Prerequisites

- Install Flutter SDK.
- Use an IDE like Android Studio or Visual Studio Code for Flutter development.

#### Steps to Run the Frontend

### Clone the Repository

To clone the repository, run the following command:



```bash
git clone https://github.com/shashank77665/shieldbot.git
```
- Navigate to Project directory

```bash
cd shieldbot
```


```bash
cd frontend
```

- Clean the Project
```bash
flutter clean
```
- Get dependencies

```bash
flutter pub get
```

- Run Project

```bash
Flutter run
```

# Backend

## Overview

The backend of **ShieldBot** is a Flask application designed for simulating security tests. It uses asynchronous processing with **Celery** and **Redis** for scalability and stores results in a **PostgreSQL** database.

---

## Features

- Brute Force, SQL Injection, and DoS Simulations.
- Asynchronous Processing with **Celery** and **Redis**.
- Database Logging for test results and logs.
- APIs for Frontend Integration.

---

## Prerequisites

- **Python 3.10** or later  
- **PostgreSQL 14** or later  
- **Redis**  
- **Docker** (optional, for containerized deployment)

---

## Installation

### **1. Clone the Repository:

```bash
git clone https://github.com/shashank77665/shieldbot.git
cd shieldbot


### **2. Set Up Python Environment**
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### **3. Configure PostgreSQL**
1. Start the PostgreSQL server.
2. Create a database and user:
   ```sql
   CREATE DATABASE shieldbot_db;
   CREATE USER shieldbot_user WITH ENCRYPTED PASSWORD 'shieldbot_pass';
   GRANT ALL PRIVILEGES ON DATABASE shieldbot_db TO shieldbot_user;
   ```

### **4. Set Up Redis**
Start Redis:
- If Redis is installed locally:
  ```bash
  redis-server
  ```
- Using Docker:
  ```bash
  docker run --name redis -p 6379:6379 -d redis
  ```

### **5. Initialize the Database**
Run the following SQL commands to create the required tables:
```sql
CREATE TABLE attack_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attack_type VARCHAR(50),
    base_url TEXT,
    details JSONB
);

CREATE TABLE task_results (
    id SERIAL PRIMARY KEY,
    task_id UUID,
    base_url TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    results JSONB
);
```

---

## **Usage**

### **1. Start the Celery Worker**
Run the Celery worker to process background tasks:
```bash
celery -A tasks worker --loglevel=info
```

### **2. Start the Flask Application**
Start the Flask application to serve the API:
```bash
python app.py
```

---

## **Testing the Application**

### **Using Postman**
#### **Endpoint: `/test-website`**
- **URL**: `http://127.0.0.1:5000/test-website`
- **Method**: `POST`
- **Payload**:
  ```json
  {
    "base_url": "http://example.com/login",
    "options": {
      "brute_force": {"passwords": ["admin", "password123"]},
      "sql_injection": {"payloads": ["' OR '1'='1", "' UNION SELECT NULL--"]},
      "dos": {"request_count": 5}
    }
  }
  ```
- **Response**:
  ```json
  {
    "task_id": "unique-task-id",
    "message": "Attack tasks started"
  }
  ```

#### **Endpoint: `/task-status/<task_id>`**
- **URL**: `http://127.0.0.1:5000/task-status/<task_id>`
- **Method**: `GET`
- **Response**:
  - **Pending**:
    ```json
    {
      "status": "Pending"
    }
    ```
  - **Success**:
    ```json
    {
      "status": "Completed",
      "result": {
        "brute_force": {...},
        "sql_injection": {...},
        "dos": {...}
      }
    }
    ```

---

## **Deployment**

### **Docker Deployment**
#### **Docker Compose Configuration**
`docker-compose.yml`:
```yaml
version: '3.8'

services:
  flask-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://shieldbot_user:shieldbot_pass@db:5432/shieldbot_db
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - redis
      - db

  redis:
    image: redis:latest
    ports:
      - "6379:6379"

  db:
    image: postgres:14
    environment:
      POSTGRES_USER: shieldbot_user
      POSTGRES_PASSWORD: shieldbot_pass
      POSTGRES_DB: shieldbot_db
    ports:
      - "5432:5432"
```

#### **Run the Application**
```bash
docker-compose up --build
```

---

## **Troubleshooting**

### **1. Redis Issues**
Verify Redis is running:
```bash
redis-cli ping
```
Expected response: `PONG`.

### **2. PostgreSQL Issues**
Verify the database connection:
```bash
psql -U shieldbot_user -d shieldbot_db
```

---

## **Contributing**
To contribute to the project:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Submit a pull request.

---

## **License**
This project is licensed under the **MIT License**.

---

