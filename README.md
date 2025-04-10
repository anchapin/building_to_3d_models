# Building to 3D Models

This project uses Python 3.10+ and Node.js 14+.

## Setup

### Prerequisites

*   Python 3.8+
*   Node.js 14+
*   Git

### Backend Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install backend dependencies:**
    ```bash
    pip install -r deployment/api/requirements.txt
    ```
    *Note: When you are finished working on the backend, you can deactivate the virtual environment by running `deactivate`.*

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend/building-to-3d-app
    ```

2.  **Install frontend dependencies:**
    ```bash
    npm install
    ```

3.  **Start the frontend development server:**
    ```bash
    npm run dev
    ```

The frontend should now be running, typically at `http://localhost:3000`. The backend (API) might need to be started separately depending on its implementation (e.g., using `flask run` or `python app.py` from the `deployment/api` directory after activating the venv), but the developer guide doesn't explicitly mention a command to start the backend server. Let's proceed with the setup first.
