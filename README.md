# Social Network API

## Overview

This project provides a social networking API using Django REST Framework. The API includes user authentication, friend requests, and search functionalities.

## Project Structure

- **`accounts`**: Manages user accounts, including login, signup, and authentication.
- **`friendships`**: Handles friend requests, managing relationships between users.

## Setup Instructions

### **1. Clone the Repository**

```sh
git clone https://github.com/vivekjha1213/social_network.git
cd social_network
```

### **2. Set Up a Virtual Environment**

Create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3. Install Dependencies**

Install the required packages:

```sh
pip install -r requirements.txt
```

### **4. Configure the Database**

For SQLite (default setup), there is no additional configuration needed.

For PostgreSQL (if using Docker), configure the environment variables in `docker-compose.yml`.

### **5. Apply Migrations**

Run the initial migrations to set up the database:

```sh
python manage.py migrate
```

### **6. Create a Superuser**

Create a superuser for accessing the Django admin:

```sh
python manage.py createsuperuser
```

### **7. Run the Development Server**

Start the development server:

```sh
python manage.py runserver
```

### **8. Docker Setup**

To build and run the Docker container, follow these steps:

1. **Build Docker Image**

   ```sh
   docker build -t django-sqlite-app .
   ```

2. **Run Docker Container**

   ```sh
   docker run -p 8000:8000 django-sqlite-app
   ```

### **API Endpoints**

Replace `{BASE_URL}` with `http://127.0.0.1:8000` in the following endpoints:

- **Health Check**
  - **Check API Health**: `{BASE_URL}/health-check/`

- **User Authentication**
  - **Signup**: `{BASE_URL}/api/v1/accounts/signup/`
  - **Login**: `{BASE_URL}/api/v1/accounts/login/`

- **User Management**
  - **Search Users**: `{BASE_URL}/api/v1/accounts/search/`
  
- **Friendship Management**
  - **Send Friend Request**: `{BASE_URL}/api/v1/friendships/`
  - **Accept/Reject Friend Request**: `{BASE_URL}/api/v1/friendships/{id}/`
  - **List Friends**: `{BASE_URL}/api/v1/friendships/friends/`
  - **List Pending Requests**: `{BASE_URL}/api/v1/friendships/pending_requests/`

### **Postman Collection**

A Postman collection is provided to help you quickly test the API endpoints. You can import the `social_network_rest_api.postman_collection.json` file into Postman to get started.

- **[Download Postman Collection](social_network_rest_api.postman_collection.json)**

To use the collection:

1. Open Postman.
2. Click on the "Import" button.
3. Select the downloaded `social_network_rest_api.postman_collection.json` file.
4. The collection will be added to your Postman workspace, and you can start testing the API endpoints.

### **Testing**

Use the Postman collection or any other API testing tool to validate the functionality of the endpoints.

### **Contributing**

Feel free to fork the repository, make changes.
