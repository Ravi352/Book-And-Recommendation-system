from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

# Create the FastAPI instance
app = FastAPI()

# PostgreSQL connection parameters
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Jk_assignment"
DB_USER = "postgres"
DB_PASS = "Ravi@123"  # Replace with your actual password

# Define the Employee model for the validation to avoid validation each time
class Employee(BaseModel):
    name: str
    age: int
    department: str = None  # Optional field



# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# Create an endpoint to add an employee
@app.post("/employees/")
async def create_employee(employee: Employee):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO employees (name, age, department) VALUES (%s, %s, %s) RETURNING id;",
            (employee.name, employee.age, employee.department)
        )
        employee_id = cursor.fetchone()[0]
        conn.commit()
        return {"id": employee_id, "message": "Employee added successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@app.get("/all_employees/")
async def get_employee():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM employees;",
        )
        employee = cursor.fetchall()
        employee_list = []
        for emp in employee:
            employee_list.append(
                {
                    'name':emp[0],
                    'age':emp[1],
                    'department':emp[2]
                }
                )
        return {'Employees':employee_list}
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()



@app.put("/update_employees/{employee_id}")  # Use PUT for updates
async def update_employee(employee_id: int, employee: Employee):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE employees 
            SET name = %s, age = %s, department = %s
            WHERE id = %s;  -- Ensure there is NO extra comma here
            """,
            (employee.name, employee.age, employee.department, employee_id)
        )
        
        # Check if any rows were updated
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        conn.commit()
        return {"message": "Employee updated successfully"}
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()


