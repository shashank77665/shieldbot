Below is a comprehensive **workflow** and **explanation** document for anyone looking to understand and run the ShieldBot backend on their machine. The steps include how the backend works, how tasks are processed, and how testing is managed.

---

# **ShieldBot Backend Workflow and Setup Guide**

This document provides a high-level overview of how the **ShieldBot** backend functions and how to run, test, and maintain it on a local environment.

---

## **1. Project Architecture and Flow**

1. **Flask Application**  
   - Acts as the HTTP entry point for incoming requests.  
   - Defines routes for authentication (login/signup), attack execution, and status checks.

2. **Celery + Redis**  
   - **Celery**: A task queue system that handles asynchronous or long-running tasks.  
   - **Redis**: A fast, in-memory key-value store used by Celery as a **message broker** and for task result storage.

3. **Database (PostgreSQL / SQLite in tests)**  
   - Stores user data (`User`), test logs (`RequestLog`), and other relevant information.
   - In production, you might use **PostgreSQL**. In local tests or development, you can use **SQLite** for simplicity.

4. **Attack Scripts**  
   - Each attack (e.g., brute force, SQL injection, DoS) is defined in separate modules or functions.  
   - The main Celery task (`run_attacks`) orchestrates these individual scripts.

5. **HTTP Requests**  
   1. **User** sends a request to an endpoint like `/auth/login` or `/attack/perform-test`.  
   2. **Flask** handles the request, performs necessary validations (e.g., JWT, required fields).  
   3. **Celery** is called if an asynchronous task is needed—like running a security test.  
   4. **Results** are either stored in the database or returned to the client.

---

## **2. Local Setup and Running**

### **Step 1: Clone the Repository**
```bash
git clone <repository_url>
cd shieldbot
```

### **Step 2: Create a Virtual Environment**
```bash
python -m venv venv
```
- **Activate** it:
  - **Windows**: `venv\Scripts\activate`
  - **Linux/Mac**: `source venv/bin/activate`

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Configure Environment**
1. **Database**  
   - By default, if you’re in development, you can use `sqlite:///:memory:` or `sqlite:///shieldbot.db`.  
   - For production or more realistic tests, set `SQLALCHEMY_DATABASE_URI` to your PostgreSQL or other DB.

2. **Redis**  
   - Start the Redis server locally:
     ```bash
     redis-server
     ```
   - Or, run via Docker:
     ```bash
     docker run --name redis -p 6379:6379 -d redis
     ```

3. **Celery**  
   - Celery depends on Redis for brokering tasks. Ensure Redis is running.

### **Step 5: Run Database Migrations** (if your project uses Alembic or Flask-Migrate)
```bash
flask db upgrade
```

### **Step 6: Start Celery Worker**
```bash
celery -A tasks worker --loglevel=info
```
- **`-A tasks`**: Tells Celery to look for tasks in the `tasks.py` module.
- **`--loglevel=info`**: Outputs task-related logs in the console.

### **Step 7: Start the Flask Application**
```bash
python app.py
```
- By default, it runs on **`http://127.0.0.1:5000`** or **`http://localhost:5000`**.

---

## **3. High-Level Flow Explanation**

1. **User Authentication**  
   - Users can register via `/auth/signup` and log in via `/auth/login`.  
   - On successful login, they receive a **JWT token** which they include in the `Authorization` header for subsequent requests.

2. **Performing an Attack**  
   - The client calls `/attack/perform-test` with a JSON body specifying `base_url` and `attack_selection`.  
   - The server validates the JWT token. If valid, it enqueues a Celery task (`run_attacks`) to handle the long-running tests asynchronously.  
   - A **task_id** is returned immediately, enabling the client to poll for results.

3. **Checking Task Status**  
   - The client periodically calls `/attack/task-status/<task_id>` with the JWT token.  
   - The server checks the Celery backend (Redis) for the task’s state: `PENDING`, `SUCCESS`, `FAILURE`, etc.

4. **Storing Logs**  
   - Each request or completed attack test logs essential data in the **RequestLog** table (or relevant model).  
   - These logs can be used for reporting or auditing later.

---

## **4. Testing the Backend Locally**

1. **Run Unit Tests**  
   - The app uses `unittest` or `pytest`. Example using `unittest`:
     ```bash
     python -m unittest discover -s app_tests -p "*.py"
     ```
   - This command:
     - Discovers tests in the `app_tests` folder.
     - Runs test files ending in `.py`.

2. **View Logs**  
   - When tests run, you may see logs in the console from Flask, Celery, or your test scripts.  
   - **Debug** by adding `print()` statements or using a logging framework.

3. **Check Database**  
   - Tests typically use an in-memory database (`sqlite:///:memory:`).  
   - Verify logs or results in the console to confirm test outcomes.

4. **Postman / cURL**  
   - You can manually send requests to endpoints (`/auth/login`, `/attack/perform-test`, etc.) to verify real-world behavior.  
   - Example with cURL:
     ```bash
     curl -X POST http://127.0.0.1:5000/attack/perform-test \
        -H "Content-Type: application/json" \
        -H "Authorization: <JWT_TOKEN>" \
        -d '{"base_url": "http://example.com","attack_selection": {"dos_attack": true}}'
     ```

---

## **5. Workflow Summary**

1. **Client**: Sends request to `/auth/signup` or `/auth/login` to obtain a JWT token.  
2. **Client**: Uses token in `Authorization` header for further requests.  
3. **Flask**: Receives requests, validates token, passes longer tasks to Celery if needed.  
4. **Celery**: Uses **Redis** as broker to queue attack scripts (like brute force, SQL injection, DoS).  
5. **Database**: Logs user info, request details, results, and logs.  

---

## **6. Running on Another PC**

1. **Clone or Copy the Project**  
   - The user or developer copies this repository locally.

2. **Install Requirements & Start Services**  
   - Follow [Installation](#installation) instructions (Python env, Redis, DB, etc.).  

3. **Run Celery and Flask**  
   - Launch Celery worker.  
   - Launch the Flask server on the same or separate machine.  

4. **Access & Test**  
   - Access the API at `http://<machine-ip>:5000`.  
   - Use Postman, cURL, or Flutter app to test endpoints.

---

## **7. Deployment**

- **Docker**: Use `docker-compose` to spin up containers for Flask, Celery, Redis, and PostgreSQL.  
- **Production**: Serve the Flask app behind a WSGI server (e.g., Gunicorn or uWSGI) and a reverse proxy (Nginx).  
- **Security**: In production, use SSL/TLS, secure JWT handling, and environment-based configs.

---

## **8. Troubleshooting**

- **Celery Not Processing Tasks**: Ensure Redis is running and broker URLs match in the config.  
- **Database Errors**: Check DB URI and run migrations if using a real database.  
- **Token Expired**: Re-log in or use `/auth/refresh-token`.  
- **Incorrect Logs**: Verify your log model configurations and default fields.

---

## **Conclusion**

With this guide, you (and others) can:

1. **Understand** how ShieldBot’s backend works.  
2. **Install** dependencies and set up local services.  
3. **Run** Flask and Celery.  
4. **Test** endpoints with cURL/Postman.  
5. **Deploy** to Docker or another production environment.  

If you have questions or run into issues, refer to this document, the [README](#), or open a GitHub issue in the project’s repository. Enjoy building and testing your web application security with **ShieldBot**!