# Fireworks Application

## Demo Video

I run through the challenge: 

https://www.loom.com/share/cce3b705f9b24089bb8dea94187a12ed


## Running the Project with Docker

To run the project using Docker:

1. Clone the repository:

    ```bash
    git clone https://github.com/janvi-kalra/loadtester.git
    cd loadtester
    ```

2. Build and start the Docker containers:

    ```bash
    docker-compose up --build
    ```

3. Access the services:

    - The backend will be accessible at `http://localhost:8000`
    - The frontend will be accessible at `http://localhost:3000`
  
I've tested on Docker and it WAI. It should look something like:
![Screen Shot 2024-08-01 at 3 48 43 PM](https://github.com/user-attachments/assets/4e58a2a7-67b4-476a-adda-13e7414cf0bf)

## Running the Project Locally

If you prefer to run the project locally without Docker, follow these steps:

### Backend Setup

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

### Frontend Setup

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
