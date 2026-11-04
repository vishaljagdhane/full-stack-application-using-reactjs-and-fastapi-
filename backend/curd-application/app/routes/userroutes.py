from fastapi import APIRouter,HTTPException
from database.databaseconnection import get_database_connection  # Import the database connection function.
from models.usermodels import userAccount,updateUserAccount,LoginUser,forgetPassword  # Import the userAccount model for user data validation.

user_router =APIRouter()  # Create an instance of APIRouter for user-related routes.

@user_router.get("/users", tags=["Users"])  # Define a GET route for retrieving users.
def get_users():  # Function to handle GET requests to the /users endpoint.
    return {"message": "List of users"}  

@user_router.post("/Database-Connection", tags=["Users"])  # Define a POST route for creating a new user.
def connect_to_database():  # Function to handle POST requests to the /users endpoint.
    connection = get_database_connection()  # Get a database connection.
    if connection:
        # Perform database operations to create a new user (not implemented in this snippet).
        return {"message": "Database connection established successfully."}  # Return a success message if the user is created successfully.
    else:
        return {"message": "Failed to connect to the database."}  # Return an error message if the database connection fails.
    
# create a new user account routes 

@user_router.post("/Create-user-account",tags=["Users"])  # Define a POST route for creating a new user account.
def create_user_account(user:userAccount):
    database_connection = get_database_connection() # get a database connection 
    if database_connection:
        try:
            cursor = database_connection.cursor()  # Create a cursor object to execute SQL queries.
            cursor.execute("INSERT INTO userAccount(user_fristname,user_lname,user_email,user_password,user_mobile,is_admin,is_active,is_super_user)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(user.user_fname,user.user_lname,user.user_email,user.user_password,user.user_phone,user.is_admin,user.is_active,user.is_super_user))  # Execute an SQL query to insert a new user into the userAccount table.
            database_connection.commit()  # Commit the transaction to save changes to the database.
            cursor.close()
            database_connection.close()  # Close the database connection.
            return {"message": "User account created successfully."}  # Return a success message if the user account is created successfully.
        except Exception as e:
            database_connection.rollback()
            database_connection.close()
            raise HTTPException(status_code=500, detail=f"Error creating user account: {e}")  # Raise an HTTPException if there is an error while creating the user account.
    else:
        return {"message": "Failed to connect to the database."}  # Return an error message if the database connection fails.
    


@user_router.put("/Update-user-account/{user_id}",tags=["Users"])  # Define a PUT route for updating an existing user account.
def update_user_account(user_id:int,user:updateUserAccount):
    
    database_connection = get_database_connection()  # Get a database connection.
    if database_connection:
        try:
            cursor = database_connection.cursor()  # Create a cursor object to execute SQL queries.
            cursor.execute("UPDATE userAccount SET user_fristname=%s, user_lname=%s, user_email=%s, user_password=%s, user_mobile=%s WHERE id=%s", (user.user_fname, user.user_lname, user.user_email, user.user_password, user.user_phone, user_id))  # Execute an SQL query to update the existing user in the userAccount table.
            database_connection.commit()  # Commit the transaction to save changes to the database.
            cursor.close()
            database_connection.close()  # Close the database connection.
            return {"message": "User account updated successfully."}  # Return a success message if the user account is updated successfully.
        except Exception as e:
            database_connection.rollback()
            database_connection.close()
            raise HTTPException(status_code=500, detail=f"Error updating user account: {e}")  # Raise an HTTPException if there is an error while updating the user account.
    else:
        return {"message": "Failed to connect to the database."}  # Return an error message if the database connection fails.
            

@user_router.delete("/Delete-user-account/{user_id}",tags=["Users"])  # Define a DELETE route for deleting an existing user account.
def delete_user_account(user_id:int):
    database_connection = get_database_connection()  # Get a database connection.
    if database_connection:
        try:
            cursor = database_connection.cursor()  # Create a cursor object to execute SQL queries.
            cursor.execute("DELETE FROM userAccount WHERE serial_id=%s", (user_id,))  # Execute an SQL query to delete the existing user from the userAccount table.
            database_connection.commit()  # Commit the transaction to save changes to the database.
            cursor.close()
            database_connection.close()  # Close the database connection.
            return {"message": "User account deleted successfully."}  # Return a success message if the user account is deleted successfully.
        except Exception as e:
            database_connection.rollback()
            database_connection.close()
            raise HTTPException(status_code=500, detail=f"Error deleting user account: {e}")  # Raise an HTTPException if there is an error while deleting the user account.
    else:
        return {"message": "Failed to connect to the database."}  # Return an error message if the database connection fails.


# login user acctount routes
@user_router.post("/Login-user-account",tags=["Users"])  # Define a POST route for user login.
def login_user_account(user:LoginUser):
    database_connection = get_database_connection()  # Get a database connection.
    if database_connection:
        try:
            cursor = database_connection.cursor()
            cursor.execute("SELECT * FROM userAccount WHERE (user_email=%s OR user_mobile=%s) and user_password=%s", (user.username, user.username, user.user_password))  # Execute an SQL query to check if the user exists in the userAccount table.
            user_data = cursor.fetchone() # Fetch the first row of the result set.
            if not user_data:
                 raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
                
            
          
            
            columns = [desc[0] for desc in cursor.description]
            user_data = dict(zip(columns, user_data)) if user_data else None  # Convert the fetched row into a dictionary with column names as keys.
            print(user_data)
            cursor.close()
            database_connection.close()  # Close the database connection.
            if user_data["is_active"] is True:  # Check if the user account is active.
                 return {
                "message": "User login successful",
                "user": {
                    "user_id": str(user_data["user_id"]),
                    "firstname": user_data["user_fristname"],
                    "lastname": user_data["user_lname"],
                    "email": user_data["user_email"],
                    "mobile": user_data["user_mobile"],
                    "is_admin": user_data["is_admin"],
                    "is_active": user_data["is_active"],
                    "is_super_user": user_data["is_super_user"]
                }
                 }
                # return {"message": "User login successful."}  # Return a success message if the user login is successful.
            
            else:
                return {"message": "Your account is deactivated. Please contact admin."}  # Return an error message if the username or password is invalid.
        except Exception as e:
            database_connection.close()
            raise HTTPException(status_code=500, detail=f"Error logging in user account: {e}")  # Raise an HTTPException if there is an error while logging in the user account.


@user_router.get("/Get-user-account",tags=["Users"])
def fetchUserAccountdata():
    database_connection = get_database_connection()  # Get a database connection.
    if database_connection:
        try:
            cursor = database_connection.cursor()
            cursor.execute("SELECT * FROM userAccount")  # Execute an SQL query to fetch all user accounts from the userAccount table.
            user_data = cursor.fetchall()  # Fetch all rows of the result set.
            cursor.close()
            database_connection.close()  # Close the database connection.
            return {"message": "User accounts fetched successfully.", "data": user_data}  # Return a success message along with the fetched user data.
        except Exception as e:
            database_connection.close()
            raise HTTPException(status_code=500, detail=f"Error fetching user accounts: {e}")  # Raise an HTTPException if there is an error while fetching user accounts.
    else:
        return {"message": "Failed to connect to the database."}  # Return an error message if the database connection fails.
    
    

@user_router.put("/forget-password/{user_id}", tags=["Users"])
def forget_password(user_id: str, user: forgetPassword):

    database_connection = get_database_connection()

    if not database_connection:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = None

    try:
        cursor = database_connection.cursor()

        # Check user exists
        cursor.execute(
            "SELECT user_id FROM userAccount WHERE user_id = %s",
            (user_id,)
        )

        user_data = cursor.fetchone()

        if not user_data:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # Check new password and confirm password
        if user.new_password != user.confirm_password:
            raise HTTPException(
                status_code=400,
                detail="New password and confirm password do not match"
            )

        # Update password
        cursor.execute(
            """
            UPDATE userAccount
            SET user_password = %s
            WHERE user_id = %s
            """,
            (user.new_password, user_id)
        )

        database_connection.commit()

        return {
            "message": "User password updated successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        database_connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Error updating password: {e}"
        )

    finally:
        if cursor:
            cursor.close()

        database_connection.close()
