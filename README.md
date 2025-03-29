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