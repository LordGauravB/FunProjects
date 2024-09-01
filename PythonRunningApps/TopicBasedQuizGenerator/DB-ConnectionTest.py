import pyodbc
import tkinter as tk

# Function to retrieve username from the database
def get_username():
    try:
        # Establish the database connection
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=GAURAVS_DESKTOP\SQLEXPRESS;'  # Replace with your server name
            'DATABASE=InteliQuiz;'  # Replace with your database name
            'Trusted_Connection=yes;'
        )
        
        cursor = conn.cursor()
        
        # Execute the SQL query with the table name correctly quoted
        cursor.execute("SELECT username FROM [dbo].[USER];")
        
        # Fetch the result
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            return "No data found"
        
    except Exception as e:
        return str(e)
    finally:
        conn.close()

# Function to display username in Tkinter window
def display_username():
    username = get_username()
    label.config(text=f"Username: {username}")

# Create the main Tkinter window
root = tk.Tk()
root.title("SQL Server Username Display")

# Create a label to display the username
label = tk.Label(root, text="Fetching username...", font=('Arial', 14))
label.pack(pady=20)

# Create a button to fetch and display the username
button = tk.Button(root, text="Fetch Username", command=display_username)
button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
