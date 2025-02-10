<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>ShieldBot Documentation</title>
  <style>
    body {
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      margin: 2rem;
      line-height: 1.5;
      color: #333;
      background-color: #fafafa;
    }
    h1, h2, h3 {
      margin-top: 1rem;
      margin-bottom: 0.5rem;
    }
    hr {
      border: 0;
      height: 1px;
      background-color: #ccc;
      margin: 2rem 0;
    }
    code, pre {
      background: #f4f4f4;
      padding: 0.2rem 0.4rem;
      border-radius: 4px;
    }
    pre {
      margin: 1rem 0;
      padding: 1rem;
      overflow-x: auto;
    }
    ul, li {
      margin: 0.5rem 0;
      padding-left: 1.5rem;
    }
    blockquote {
      margin: 1rem 0;
      padding: 0.5rem 1rem;
      background-color: #fff3cd;
      border-left: 5px solid #ffeeba;
      color: #856404;
    }
    .section-title {
      margin-top: 3rem;
    }
    .code-block {
      background-color: #f0f0f0;
    }
  </style>
</head>
<body>

<h1><strong>ShieldBot</strong></h1>

<p><strong>ShieldBot</strong> is a Flask-based cybersecurity testing platform that simulates various website security tests (brute force, SQL injection, etc.) and generates real-time AI-driven insights via the Hugging Face API.</p>

<hr />

<h2>Table of Contents</h2>
<ol>
  <li><a href="#about-the-project">About the Project</a></li>
  <li><a href="#disclaimer">Disclaimer</a></li>
  <li><a href="#features">Features</a></li>
  <li><a href="#prerequisites">Prerequisites</a></li>
  <li><a href="#installation">Installation</a></li>
  <li><a href="#usage">Usage</a></li>
  <li><a href="#testing-the-application">Testing the Application</a></li>
  <li><a href="#deployment">Deployment</a></li>
  <li><a href="#troubleshooting">Troubleshooting</a></li>
  <li><a href="#contributing">Contributing</a></li>
  <li><a href="#license">License</a></li>
</ol>

<hr />

<h2 id="about-the-project">About the Project</h2>
<p>ShieldBot is designed to:</p>
<ul>
  <li>Simulate real-world attacks such as brute force, SQL injection, and DoS.</li>
  <li>Assist in understanding web application vulnerabilities.</li>
  <li>Provide an asynchronous and scalable architecture using Flask, Redis, and Celery.</li>
</ul>

<hr />

<h2 id="disclaimer">Disclaimer</h2>
<blockquote>
  <strong>⚠️ For Educational Purposes Only</strong>: This project is strictly for ethical testing. Unauthorized testing of websites without proper authorization is illegal. Ensure that you have explicit permission before using this tool.
</blockquote>

<hr />

<h2 id="features">Features</h2>
<ul>
  <li><strong>Authentication & Registration:</strong>  
  • Email/password signup (with email verification and CAPTCHA)  
  • Google OAuth login  
  • Password reset ("forgot password") functionality</li>
  <li><strong>User Roles & Limitations:</strong>  
  • Regular users can run up to 2 tests concurrently  
  • Admins have access to all user data, test logs, and tool management functions</li>
  <li><strong>Core App Functions:</strong>  
  • Home page listing available tests  
  • User dashboard with test status, logs, and AI insights  
  • Test creation that can be run on separate threads or via Celery tasks</li>
  <li><strong>Custom Tests Route:</strong>  
  • Run tests with custom inputs and select which tests to skip or run  
  • Optional installation of Linux security tools (via apt-get on Ubuntu)</li>
  <li><strong>Linux Tools Installation:</strong>  
  • Admin route for installing a default suite (e.g., nmap, nikto, sqlmap, gobuster, dirb, wfuzz)</li>
  <li><strong>Deployment:</strong>  
  • Environment variables (.env) for configuration  
  • Database migrations using Flask-Migrate</li>
  <li><strong>Logging & Error Handling:</strong>  
  • Structured JSON logging for easier monitoring</li>
</ul>

<hr />

<h2 id="prerequisites">Prerequisites</h2>

<h3>System Requirements</h3>
<ul>
  <li>Operating System: Windows, macOS, or Linux</li>
  <li>Python: Version 3.10 or later</li>
  <li>PostgreSQL: Version 14 or later</li>
  <li>Redis: Latest version</li>
  <li>Docker: Optional, for containerized deployment</li>
</ul>

<h3>Installed Tools</h3>
<ul>
  <li>Python package manager (<code>pip</code>)</li>
  <li>PostgreSQL database server</li>
  <li>Redis server</li>
</ul>

<hr />

<h2 id="installation">Installation</h2>

<h3>1. Clone the Repository</h3>
<pre><code class="code-block">
git clone &lt;repository_url&gt;
cd shieldbot
</code></pre>

<h3>2. Set Up Python Environment</h3>
<ol>
  <li>Create a virtual environment:
    <pre><code class="code-block">
python -m venv venv
    </code></pre>
  </li>
  <li>Activate the virtual environment:
    <ul>
      <li><strong>Windows</strong>:
        <pre><code class="code-block">
venv\Scripts\activate
        </code></pre>
      </li>
      <li><strong>Linux/Mac</strong>:
        <pre><code class="code-block">
source venv/bin/activate
        </code></pre>
      </li>
    </ul>
  </li>
  <li>Install dependencies:
    <pre><code class="code-block">
pip install -r requirements.txt
    </code></pre>
  </li>
</ol>

<h3>3. Configure PostgreSQL</h3>
<ol>
  <li>Start the PostgreSQL server.</li>
  <li>Create a database and user:
    <pre><code class="code-block">
CREATE DATABASE shieldbot_db;
CREATE USER shieldbot_user WITH ENCRYPTED PASSWORD 'shieldbot_pass';
GRANT ALL PRIVILEGES ON DATABASE shieldbot_db TO shieldbot_user;
    </code></pre>
  </li>
</ol>

<h3>4. Set Up Redis</h3>
<ul>
  <li>If Redis is installed locally:
    <pre><code class="code-block">
redis-server
    </code></pre>
  </li>
  <li>Using Docker:
    <pre><code class="code-block">
docker run --name redis -p 6379:6379 -d redis
    </code></pre>
  </li>
</ul>

<h3>5. Initialize the Database</h3>
<p>Run the following SQL commands to create the required tables:</p>
<pre><code class="code-block">
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
</code></pre>

<hr />

<h2 id="usage">Usage</h2>

<h3>1. Start the Celery Worker</h3>
<pre><code class="code-block">
celery -A tasks worker --loglevel=info
</code></pre>

<h3>2. Start the Flask Application</h3>
<pre><code class="code-block">
python app.py
</code></pre>

<hr />

<h2 id="testing-the-application">Testing the Application</h2>

<h3>Using Postman</h3>

<h4>Endpoint: <code>/test-website</code></h4>
<ul>
  <li><strong>URL</strong>: <code>http://127.0.0.1:5000/test-website</code></li>
  <li><strong>Method</strong>: <code>POST</code></li>
  <li><strong>Payload</strong>:
    <pre><code class="code-block">
{
  "base_url": "http://example.com/login",
  "options": {
    "brute_force": {"passwords": ["admin", "password123"]},
    "sql_injection": {"payloads": ["' OR '1'='1", "' UNION SELECT NULL--"]},
    "dos": {"request_count": 5}
  }
}
    </code></pre>
  </li>
  <li><strong>Response</strong>:
    <pre><code class="code-block">
{
  "task_id": "unique-task-id",
  "message": "Attack tasks started"
}
    </code></pre>
  </li>
</ul>

<h4>Endpoint: <code>/task-status/&lt;task_id&gt;</code></h4>
<ul>
  <li><strong>URL</strong>: <code>http://127.0.0.1:5000/task-status/&lt;task_id&gt;</code></li>
  <li><strong>Method</strong>: <code>GET</code></li>
  <li><strong>Response</strong>:
    <ul>
      <li><strong>Pending</strong>:
        <pre><code class="code-block">
{
  "status": "Pending"
}
        </code></pre>
      </li>
      <li><strong>Success</strong>:
        <pre><code class="code-block">
{
  "status": "Completed",
  "result": {
    "brute_force": {...},
    "sql_injection": {...},
    "dos": {...}
  }
}
        </code></pre>
      </li>
    </ul>
  </li>
</ul>

<hr />

<h2 id="api-reference-for-backend-integration">API Reference for Backend Integration</h2>

<h3>Base URL</h3>
<ul>
  <li><strong>Development</strong>: <code>http://&lt;server-ip&gt;:5000</code></li>
  <li><strong>Production</strong>: Replace <code>&lt;server-ip&gt;</code> with your production server's IP or domain.</li>
</ul>

<hr />

<h3>Authentication Routes</h3>

<h4>Sign Up</h4>
<ul>
  <li><strong>Endpoint</strong>: <code>/auth/signup</code></li>
  <li><strong>Method</strong>: <code>POST</code></li>
  <li><strong>Headers</strong>: None</li>
  <li><strong>Request Body</strong>:
    <pre><code class="code-block">
{
  "username": "newuser",
  "email": "new@example.com",
  "password": "password123"
}
    </code></pre>
  </li>
  <li><strong>Response</strong>:
    <ul>
      <li><strong>201</strong>:
        <pre><code class="code-block">
{
  "message": "User registered successfully",
  "profile_picture": "user.jpg"
}
        </code></pre>
      </li>
      <li><strong>400</strong>:
        <pre><code class="code-block">
{
  "error": "User already exists"
}
        </code></pre>
      </li>
    </ul>
  </li>
</ul>

<h4>Login</h4>
<ul>
  <li><strong>Endpoint</strong>: <code>/auth/login</code></li>
  <li><strong>Method</strong>: <code>POST</code></li>
  <li><strong>Headers</strong>: None</li>
  <li><strong>Request Body</strong>:
    <pre><code class="code-block">
{
  "email": "user@example.com",
  "password": "password123"
}
    </code></pre>
  </li>
  <li><strong>Response</strong>:
    <ul>
      <li><strong>200</strong>:
        <pre><code class="code-block">
{
  "message": "Welcome, username!",
  "token": "<JWT-TOKEN>"
}
        </code></pre>
      </li>
      <li><strong>401</strong>:
        <pre><code class="code-block">
{
  "error": "Invalid email or password"
}
        </code></pre>
      </li>
    </ul>
  </li>
</ul>

<h4>Verify Token</h4>
<ul>
  <li><strong>Endpoint</strong>: <code>/auth/verify-token</code></li>
  <li><strong>Method</strong>: <code>GET</code></li>
  <li><strong>Headers</strong>:
    <pre><code class="code-block">
Authorization: <JWT-TOKEN>
    </code></pre>
  </li>
  <li><strong>Response</strong>:
    <ul>
      <li><strong>200</strong>:
        <pre><code class="code-block">
{
  "message": "Token is valid",
  "user_id": 1
}
        </code></pre>
      </li>
      <li><strong>400</strong>:
        <pre><code class="code-block">
{
  "error": "Token is missing"
}
        </code></pre>
      </li>
      <li><strong>401</strong>:
        <pre><code class="code-block">
{
  "error": "Token has expired"
}
        </code></pre>
      </li>
    </ul>
  </li>
</ul>

<h4>Refresh Token</h4>
<ul>
  <li><strong>Endpoint</strong>: <code>/auth/refresh-token</code></li>
  <li><strong>Method</strong>: <code>POST</code></li>
  <li><strong>Headers</strong>:
    <pre><code class="code-block">
Authorization: <JWT-TOKEN>
    </code></pre>
  </li>
  <li><strong>Response</strong>:
    <ul>
      <li><strong>200</strong>:
        <pre><code class="code-block">
{
  "token": "<NEW-JWT-TOKEN>"
}
        </code></pre>
      </li>
      <li><strong>400 / 401</strong>:
        <pre><code class="code-block">
{
  "error": "Token is still valid, no need to refresh"
}
        </code></pre>
      </li>
    </ul>
  </li>
</ul>

<hr />

<h3>Attack Routes</h3>

<h4>Perform Test</h4>
<ul>
  <li><strong>Endpoint</strong>: <code>/attack/perform-test</code></li>
  <li><strong>Method</strong>: <code>POST</code></li>
  <li><strong>Headers</strong>:
    <pre><code class="code-block">
Authorization: <JWT-TOKEN>
    </code></pre>
  </li>
  <li><strong>Request Body</strong>:
    <pre><code class="code-block">
{
  "base_url": "http://example.com",
  "attack_selection": {
    "brute_force": true,
    "sql_injection": false,
    "dos_attack": true
  },
  "username": "admin" // Required if brute_force is true
}
    </code></pre>
  </li>
  <li><strong>Response</strong>:
    <ul>
      <li><strong>202</strong>:
        <pre><code class="code-block">
{
  "task_id": "<TASK-ID>",
  "message": "Attack task submitted successfully"
}
        </code></pre>
      </li>
      <li><strong>400 / 401</strong>:
        <pre><code class="code-block">
{
  "error": "Base URL is required"
}
        </code></pre>
      </li>
    </ul>
  </li>
</ul>

<h4>Check Task Status</h4>
<ul>
  <li><strong>Endpoint</strong>: <code>/attack/task-status/&lt;task_id&gt;</code></li>
  <li><strong>Method</strong>: <code>GET</code></li>
  <li><strong>Headers</strong>:
    <pre><code class="code-block">
Authorization: <JWT-TOKEN>
    </code></pre>
  </li>
  <li><strong>Response</strong>:
    <ul>
      <li><strong>202</strong>: Task is pending
        <pre><code class="code-block">
{
  "status": "Pending"
}
        </code></pre>
      </li>
      <li><strong>200</strong>: Task completed
        <pre><code class="code-block">
{
  "status": "Completed",
  "result": {
    "sql_injection": "Passed",
    "dos_attack": "Failed"
  }
}
        </code></pre>
      </li>
      <li><strong>500</strong>: Task failed
        <pre><code class="code-block">
{
  "status": "Failed",
  "error": "Detailed error message"
}
        </code></pre>
      </li>
    </ul>
  </li>
</ul>

<hr />

<h3>Additional Notes</h3>
<ul>
  <li><strong>Authorization</strong>: Include the <code>Authorization</code> header with the JWT token for authenticated routes.</li>
  <li><strong>Error Handling</strong>: All error responses include an <code>"error"</code> field.</li>
  <li><strong>CORS</strong>: Ensure the Flutter app is making requests to the correct domain with the required headers.</li>
</ul>

<h3>Suggested Workflow for Flutter</h3>
<ol>
  <li><strong>User Authentication</strong>: Sign up or log in to receive a JWT token. Save the token securely using Flutter's secure storage (<code>flutter_secure_storage</code>).</li>
  <li><strong>Authenticated Actions</strong>: Attach the JWT token as an <code>Authorization</code> header for every request to <code>/attack/*</code>.</li>
  <li><strong>Token Management</strong>: Regularly check and refresh the token using <code>/auth/refresh-token</code> before it expires.</li>
</ol>

---

## **Deployment**

### **Docker Deployment**

#### **Docker Compose Configuration**

<code>docker-compose.yml</code>:
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

To help your frontend developer integrate the backend with Flutter, you can provide them with a clear and concise API reference. Here's the essential information they will need:

---

## **API Reference for Backend Integration**

### **Base URL**
- **Development**: `http://<server-ip>:5000`
- **Production**: Replace `<server-ip>` with your production server's IP or domain.

---

### **Authentication Routes**

#### 1. **Sign Up**
- **Endpoint**: `/auth/signup`
- **Method**: `POST`
- **Headers**: None
- **Request Body**:
  ```json
  {
    "username": "newuser",
    "email": "new@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  - **201**: User registered successfully
    ```json
    {
      "message": "User registered successfully",
      "profile_picture": "user.jpg"
    }
    ```
  - **400**: Missing fields or duplicate user
    ```json
    {
      "error": "User already exists"
    }
    ```

#### 2. **Login**
- **Endpoint**: `/auth/login`
- **Method**: `POST`
- **Headers**: None
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  - **200**: Login successful
    ```json
    {
      "message": "Welcome, username!",
      "token": "<JWT-TOKEN>"
    }
    ```
  - **401**: Invalid credentials
    ```json
    {
      "error": "Invalid email or password"
    }
    ```

#### 3. **Verify Token**
- **Endpoint**: `/auth/verify-token`
- **Method**: `GET`
- **Headers**:
  ```
  Authorization: <JWT-TOKEN>
  ```
- **Response**:
  - **200**: Token valid
    ```json
    {
      "message": "Token is valid",
      "user_id": 1
    }
    ```
  - **400**: Token is missing
    ```json
    {
      "error": "Token is missing"
    }
    ```
  - **401**: Token expired or invalid
    ```json
    {
      "error": "Token has expired"
    }
    ```

#### 4. **Refresh Token**
- **Endpoint**: `/auth/refresh-token`
- **Method**: `POST`
- **Headers**:
  ```
  Authorization: <JWT-TOKEN>
  ```
- **Response**:
  - **200**: Token refreshed
    ```json
    {
      "token": "<NEW-JWT-TOKEN>"
    }
    ```
  - **400 / 401**: Token still valid or invalid
    ```json
    {
      "error": "Token is still valid, no need to refresh"
    }
    ```

---

### **Attack Routes**

#### 1. **Perform Test**
- **Endpoint**: `/attack/perform-test`
- **Method**: `POST`
- **Headers**:
  ```
  Authorization: <JWT-TOKEN>
  ```
- **Request Body**:
  ```json
  {
    "base_url": "http://example.com",
    "attack_selection": {
      "brute_force": true,
      "sql_injection": false,
      "dos_attack": true
    },
    "username": "admin"  // Required if brute_force is true
  }
  ```
- **Response**:
  - **202**: Task submitted successfully
    ```json
    {
      "task_id": "<TASK-ID>",
      "message": "Attack task submitted successfully"
    }
    ```
  - **400 / 401**: Errors like missing token, URL, or username

#### 2. **Check Task Status**
- **Endpoint**: `/attack/task-status/<task_id>`
- **Method**: `GET`
- **Headers**:
  ```
  Authorization: <JWT-TOKEN>
  ```
- **Response**:
  - **202**: Task is pending
    ```json
    {
      "status": "Pending"
    }
    ```
  - **200**: Task completed
    ```json
    {
      "status": "Completed",
      "result": {
        "sql_injection": "Passed",
        "dos_attack": "Failed"
      }
    }
    ```
  - **500**: Task failed
    ```json
    {
      "status": "Failed",
      "error": "Detailed error message"
    }
    ```

---

### **Additional Notes**
- **Authorization**: Include the `Authorization` header with the JWT token for authenticated routes.
- **Error Handling**: All error responses include an `"error"` field.
- **CORS**: Ensure the Flutter app is making requests to the correct domain with the required headers.

---

### **Suggested Workflow for Flutter**
1. **User Authentication**:
   - Sign up or log in to receive a JWT token.
   - Save the token securely using Flutter's secure storage (e.g., `flutter_secure_storage`