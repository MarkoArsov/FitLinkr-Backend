
# **Django API Setup Guide**

### Step 1: Clone the Repository

1.  Open your terminal or command prompt.
2.  Navigate to the directory where you want to clone the project.
3.  Run the following command:

`git clone <repository-url>` 

### Step 2: Install Dependencies

1.  Install Dependencies

`pip install django Pillow` 

2.  Navigate into the cloned project directory:

`cd <project-directory>` 

3.  Install the required Python dependencies using pip:

`pip install -r requirements.txt` 

### Step 3: Make Migrations

1.  Once dependencies are installed, navigate to the project directory if you're not already there.
2.  Run the following command to make migrations:

`python manage.py makemigrations` 

### Step 4: Migrate the Database

1.  After creating the migration files, you need to apply these changes to the database. Run the following command:

`python manage.py migrate` 

**Note**: Use `python manage.py flush` to delete all data in the database 

### Step 5: Run the Django Server

1.  To run the Django development server, execute the following command:

`python manage.py runserver` 

This command will start the server, and you should see output indicating the server is running. By default, it will serve your Django application at `http://localhost:8000/`.
