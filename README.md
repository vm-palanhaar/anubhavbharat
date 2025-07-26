# Indian Railways Super App

This project is a Django-based backend for the Indian Railways Super App, supporting user management, business organizations, railway data, and shop/stall management.

## Setup Instructions

1. **Clone the repository**
2. **Create and activate a Python virtual environment**
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure environment variables**

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY="your_secret_key"
ALLOWED_HOST_1="localhost"

# Database config
DB_1_PGSQL_NAME="anubhavbharat"
DB_1_PGSQL_USER="postgres"
DB_1_PGSQL_PWD="admin"
DB_1_PGSQL_HOST="localhost"
DB_1_PGSQL_PORT="5432"
```

5. **Apply migrations**
   ```sh
   python manage.py migrate
   ```

6. **Run the development server**
   ```sh
   python manage.py runserver
   ```

## Project Structure

- `users/` - User authentication and profile management
- `business/` - Business organization and employee management
- `indrail/` - Indian Railways data, stations, trains, shops
- `anubhavbharat/` - Project configuration and settings

## API Endpoints

See [anubhavbharat/api_urls.py](anubhavbharat/api_urls.py) for all available API routes.

## Requirements

See [requirements.txt](requirements.txt) for Python package dependencies.