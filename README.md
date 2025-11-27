Dynamic Table Builder System (Django and Raw SQL)

This project is a ** dynamic database builder built using Django + Raw SQL**.  
  It is allows users to:

*  Create tables dynamically  
*  Add rows dynamically  
*  Update and delete values  
*  View fields and metadata  
*  Drop tables  
*  Upload CSV files and insert data  
*  Auto match CSV headers with DB columns  
*  Display all public tables
    
**Step 1: clone the repository**
https://github.com/velmuruganwebdev-crypto/Dynamic-Table-Builder-System.git

**Step 2: Create and activate virtual environment** 

# Step 3:Create virtual environment
python -m venv .venv

**Step 4: Install Dependencies**
pip install -r requirements.txt

**Step 5: Creat Project**
django-admin startproject myroject .

**Step 6: Configure Database (PostgreSQL)**
Edit->/myproject/settings.py

Example:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

Create the database manually if needed:
CREATE DATABASE dynamic_tables;

**Step 7: Run Backend Migrations**
python manage.py makemigrations
python manage.py migrate

**Step 8: Run Backend Server**
python manage.py runserver 8000
Backend API will run on: http://127.0.0.1:8000/

**Step 9: Using the Application**
After clicking the URL, you will be redirected to the dashboard.

**Step 10: Create a Table**

    *  Enter the name of the table you want to create.
    
    *  Enter each field name for the table.
    
    *  Choose the appropriate data type for each field.
    
    *  Check the Mandatory box if the field is required.
    
    *  You can add or remove rows as needed.
    
    *  After entering all field names and selecting their types, click Create Table.

 **Step 11: Insert Table Values**

    *  After creating the table, you will be redirected to the tables data entry page.

    *  Here, you can enter values for each field you created.
    
    *  After entering the data, click Submit to save it.
    
    *  You can continue adding multiple records as needed.
    
    *  After saving the data, you can return to the table list, where all created tables will be displayed.
    
**Step 12: View Your Data**
    
    *  From the list of tables, click any table name to view its stored data.
    
    *  You will see all the records listed in a table format.
    
    *  You can update or delete any record using the edit and delete options provided.
**Step 13: Table List Options**

  *  In the table list view, you will see four options for each table:

      1. Insert
      
          *  You can manually enter new data into the table, just like we saw earlier.
      
      2. Delete
      
          *  You can delete the entire table.
      
          *  If you delete the table, all stored data inside that table will also be removed permanently.
      
      3. View Fields
      
          *  You can view all field names, their data types, and whether each field is marked as mandatory or optional.
      
      4. Upload File
      
          *  This option is used to upload a CSV file.(Detailed explanation provided below.)

**Step 14: CSV File Upload**

    *  You can upload a CSV file to insert multiple records into your table at once.
    
    *  Every table in the list has an Upload File option.
    
    *  Click Upload File, select your CSV file, and then click Upload.
    
    *  All records from the CSV file will be inserted into your selected table automatically.

APIENDPOINTS:
    path('',dynamic_table, name='dynamic_table'),
    path('showtables/',showtables, name ='showtables'),
    path('insert_values/<str:table_name>/', dynamic_insert, name='dynamic_insert'),
    path('insert/<str:table_name>/', values_get, name='values_get'),
    path('tabledetails/',tabledetails, name='tabledetails'),
    path('drop_table/<str:table_name>/',drop_table,name='drop_table'),
    path('view_fields/<str:table_name>/',view_fields,name='view_fields'),
    path('values_delete/<str:table_name>/<int:id>/', values_delete, name='values_delete'),
    path('values_update/<str:table_name>/<int:id>/',values_update,name='values_update'),
    path('insert_values/<str:table_name>/upload_file/',upload_file,name='upload_file'),

1. path('', dynamic_table, name='dynamic_table')

  This URL path calls the dynamic_table function in the views.py file.This function receives user input such as:
  
      *  Table name
    
      *  Field names
    
      *  Data types
    
      *  Mandatory checkbox
  
  After processing these inputs, it executes the sql create table query.All the user inputs for creating a table are collected from the create_table.html page.

2. path('showtables/', showtables, name='showtables')

  *  This URL path calls the showtables function.Inside this function, a SQL query is executed to fetch all table names created by the user.
  These table names are displayed in the showtables.html page, allowing the user to view all the tables they have created.

3. path('insert_values/<str:table_name>/', dynamic_insert, name='dynamic_insert')

  *  This URL path calls the dynamic_insert function.Inside this function, a sql query is executed to insert the form data submitted from insert.html.
  The entered values are saved into the respective table based on the <table_name> passed in the URL

4.path('insert/<str:table_name>/', values_get, name='values_get'),
  *  This URL path calls the values_get function.Inside the function, a sql query (select * from table_name) is executed to fetch all the inserted data from the selected table.
  All the retrieved table records and column details are displayed in the tabledetails.html page.

5.path('tabledetails/',tabledetails, name='tabledetails'),
  * This URL path calls the tabledetails function.Inside the function, jsut rendering the table details page.

6.path('drop_table/<str:table_name>/',drop_table,name='drop_table'),
  *  This URL path calls the drop_table function.Inside the function, this function, a sql query executed to "DROP TABLE {table_name}
  this is the delete table query and the table is delete into the respective of table based on the <str:table_name>  passed in the url.

7.path('view_fields/<str:table_name>/',view_fields,name='view_fields'),
  * This URL path calls the view_field function.Inside the function, this function a sql query executed to
  (SELECT column_name, data_type, is_nullable,FROM information_schema.columns,WHERE table_name= '{table_name}';
  basically this query returns the all field names, their data types, and whether each field is marked as mandatory or optional.

8. path('values_delete/<str:table_name>/<int:id>/', values_delete, name='values_delete'),
   *  This URL path calls the values_delete function.Inside the function, this function a sql query executed to DELETE FROM {table_name} WHERE {table_name}_id = {id}"
     is execute delete the table data field respective passing tablenane and the id for taking and delete the respective row.

9. path('values_update/<str:table_name>/<int:id>/',values_update,name='values_update'),
   *  This URL path calls the values_update function.Inside the function, this function a sql query executed to the update the field rspective of tablename and the id

10.path('insert_values/<str:table_name>/upload_file/',upload_file,name='upload_file'),
*  This URL path calls the upload_file function.Inside the function, this function is taking the csv file and making Read CSV into DataFrame with help of pandas and Convert DataFrame to JSON and save
  and store all multiple values into the respective tablename.


