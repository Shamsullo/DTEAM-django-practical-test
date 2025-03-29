# **DTEAM - Django Developer Practical Test**  
### **Project Setup Guide**  

### **Prerequisites**  
Ensure you have the following installed:  
- **`pyenv`** (for Python version management)  
- **`Poetry`** (for dependency management)  
- **`git`** (for cloning the repository)  

---

### **1. Clone the Repository**  
```bash
git clone https://github.com/Shamsullo/DTEAM-django-practical-test
cd DTEAM-django-practical-test
```

### **2. Install the Required Python Version**  
The project uses a specific Python version defined in `.python-version`. Install it with:  
```bash
pyenv install
```  
*This reads the version from `.python-version` and installs it if missing.*  

### **3. Set the Local Python Version**  
Ensure `pyenv` uses the correct version:  
```bash
pyenv local
```  
*This automatically switches to the version specified in `.python-version`.*  

### **4. Install Dependencies with Poetry**  
Install project dependencies (including dev tools):  
```bash
poetry install
```  

### **5. Run the Django Development Server**  
Start the server with:  
```bash
poetry run python manage.py runserver
```  
*Access the app at `http://localhost:8000`.*  


### **Sample Data**
The project includes initial/testing sample data that can be loaded using Django fixtures. 
This will create:
- A CV for Shamsullo Ismatov, a backend software engineer with 4+ years of experience
- Key technical skills including Python, Django, PostgreSQL, FastAPI, and AWS
- Notable projects including Gettik Asia, Orienbank Internet Banking, and eDonish
- Professional contact information

To load the sample data:
```bash
poetry run python manage.py loaddata cv_sample_data
```

### **Testing**
The project uses Django's built-in testing framework. Tests are organized within each app's directory.

### Running Tests
Execute tests using Poetry:
```bash
poetry run python manage.py test
```

### **Running the Project with Docker Compose**

If you prefer to run the project using Docker Compose, we have introduced this
method as well. For it follow these steps:

1. **Build and Start the Docker Containers**  
   Run the following command to build the images and start the containers:
   ```bash
   docker-compose up --build
   ```

2. **Access the Application**  
   Once the containers are up and running, access the application at:
   ```plaintext
   http://localhost:8000
   ```

3. **Load Sample Data (Optional)**  
   To load the initial sample data into the database, run:
   ```bash
   docker-compose exec web poetry run python manage.py loaddata cv_sample_data
   ```

4. **Run Tests**  
   To execute tests inside the container, use the following command:
   ```bash
   docker-compose exec web poetry run python manage.py test
   ```

*The `docker-compose.yml` file defines the necessary services for the
application, including the web server and database.*
