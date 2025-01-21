
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
   - Save the token securely using Flutter’s secure storage (e.g., `flutter_secure_storage`).
2. **Authenticated Actions**:
   - Attach the JWT token as an `Authorization` header for every request to `/attack/*`.
3. **Token Management**:
   - Regularly check and refresh the token using `/auth/refresh-token` before it expires.

---
