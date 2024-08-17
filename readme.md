# **🏢 Alpha Apartments**

**Alpha Apartments is a comprehensive web portal designed to streamline apartment management and communication for tenants and non-tenants (technicians). The platform features user-friendly interfaces and robust backend support to ensure a seamless experience.**

## **🚀 Features**

### **Authentication**
- Google OAuth login
- User email/password registration
- User email/password login
- User logout
- JWT Cookie authentication

### **Profiles**
- View all tenants' profiles
- View all non-tenants' (technicians) profiles
- Get the logged-in user's profile
- Update user profile
- Upload image for user avatar

### **Apartments**
- Add apartment
- View all apartments for the logged-in user

### **Issues**
- List all issues
- List all assigned issues
- View all issues created by the logged-in user
- Create a new issue for a specified apartment
- View details of an issue
- Update an issue
- Delete an issue

### **Reports**
- Create a new report for another tenant
- View reports created about the logged-in user
- **Note:** First report serves as a warning, and if a user accumulates 5 reports, the account will be deactivated

### **Ratings**
- Create a rating for non-tenants (technicians)
- Display average rating for technicians

### **Posts**
- List all posts
- Get list of posts by tags
- Get top posts (most replies and content views)
- List popular tags (most used tags)
- Create a new post
- List logged-in user's posts
- View details of a post
- Update a post
- Bookmark a post
- Unbookmark a post
- View list of bookmarked posts
- Add a reply to a post
- Get all replies for a post
- Upvote a post
- Downvote a post

## **🛠️ Tech Stack**

### **Backend**
- **Django**: Web framework
- **Django REST Framework**: API development
- **PostgreSQL**: Database
- **Celery**: Asynchronous task queue
- **Redis**: Message broker for Celery
- **MinIO**: Object storage for static and media files

### **Frontend**
- **NextJS**: Frontend Web Framework
- **Heroicons**: Icon Library
- **TailwindCSS**: CSS Utility Class Package
- **Redux**: Statement Management
- **Zod**: Data and Schema Validation
- **Axios**: HTTP Request and Response Package

## **📦 Deployment**

### **Docker**
**The application is containerized using Docker for easy deployment and management. Below is a brief overview of the Docker setup:**

- **Services**: 
  - `server`: Django backend
  - `client`: NextJS frontend
  - `postgres`: PostgreSQL database
  - `minio`: MinIO object storage
  - `mailpit`: Mail server for development
  - `redis`: Redis message broker
  - `celeryworker`: Celery worker
  - `celerybeat`: Celery beat scheduler
  - `flower`: Celery monitoring tool
  - `nginx`: Reverse proxy server

### **Volumes**
- `local_postgres_data`
- `local_postgres_data_backups`
- `local_minio_data`
- `local_mailpit_data`
- `local_redis_data`
- `local_logs_nginx`

### **Networks**
- `alpha_apartments_network`

## **🔧 Setup and Installation**

### **Prerequisites**
- **Docker and Docker Compose installed on your system**

### **Installation**
1. **Clone the repository:**
    ```bash
    git clone https://github.com/DataRohit/Django-Apartment-Management.git
    cd alpha-apartments
    ```

2. **Build and start the container:**
    ```bash
    docker-compose -f docker-compose.local.yml up --build
    ```

3. **Access the application:**
    - **Backend:** `http://localhost:8080/api/v1/`
    - **Frontend** `http://localhost:8080/`
    - **Swagger Redoc:** `http://localhost:8080/api/v1/redoc/`
    - **Swagger Playground:** `http://localhost:8080/api/v1/swagger/`
    - **Minio:** `http://localhost:9090/`
    - **Mailpit:** `http://localhost:8025/`
    - **Flower:** `http://localhost:5555/`

## **📝 License**
**This project is licensed under the MIT License - see the [LICENSE](https://github.com/DataRohit/Django-Apartment-Management/blob/master/license) file for details.**

## 📞 Contact
**For any inquiries or support, please reach out to [rohit.vilas.ingole@gmail.com](mailto:rohit.vilas.ingole@gmail.com).**

---

Made with ❤️ by [Rohit Vilas Ingole](https://github.com/datarohit)
