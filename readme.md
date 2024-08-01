# Demo Video

https://www.loom.com/share/cce3b705f9b24089bb8dea94187a12ed

# Fireworks Application

This application consists of a backend built with FastAPI in Python and a frontend built with Node.js. Follow the instructions below to set up and run the application.

## Backend Setup

1. **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv env
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```bash
        .\env\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source env/bin/activate
        ```

4. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```

    The backend server will start on `http://127.0.0.1:8000`.

## Frontend Setup

1. **Navigate to the frontend directory:**
    ```bash
    cd ../frontend
    ```

2. **Install the required dependencies:**
    ```bash
    npm install
    ```

3. **Run the frontend development server:**
    ```bash
    npm start
    ```

    The frontend server will start on `http://localhost:3000`.

## Running Tests

### Backend Tests

1. **Ensure the virtual environment is activated.**
2. **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
3. **Run the tests:**
    ```bash
    pytest
    ```