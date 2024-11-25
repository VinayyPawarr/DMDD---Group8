import pyodbc
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Define connection string
connection_string = (
    "DRIVER={SQL Server};"
    "SERVER=nl;"  # Replace with your SQL Server instance name
    "DATABASE=NBAMANAGEMENT;"  # Replace with your database name
    "Trusted_Connection=yes;"  # Use Windows authentication
)

# Create GUI

def main_menu():
    root = tk.Tk()
    root.title("NBA Management System Main Menu")
    root.geometry("600x800")

    try:
        background_image = Image.open("background2.jpg")  # Replace with the path to your basketball image
        background_image = background_image.resize((600, 800), Image.LANCZOS)
        background_photo = ImageTk.PhotoImage(background_image)

        background_label = tk.Label(root, image=background_photo)
        background_label.image = background_photo  # Keep a reference to avoid garbage collection
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error loading image: {e}")

    def open_player_management():
        root.destroy()
        player_management()

    def open_coach_management():
        root.destroy()
        coach_management()

    def open_team_management():
        root.destroy()
        team_management()

    def open_season_management():
        root.destroy()
        season_management()

    def open_sponsorship_management():
        root.destroy()
        sponsorship_management()

    def open_assignment_management():
        root.destroy()
        assignment_management()

    def open_nbagame_management():
        root.destroy()
        nbagame_management()

    # Buttons on transparent overlay
    tk.Label(root, text="NBA Management System", font=("Helvetica", 20, "bold"), fg='black', bg='white').pack(pady=20)
    tk.Button(root, text="Player", command=open_player_management, width=20, height=2, bg='white').pack(pady=5)
    tk.Button(root, text="Coach", command=open_coach_management, width=20, height=2, bg='white').pack(pady=5)
    tk.Button(root, text="Team", command=open_team_management, width=20, height=2, bg='white').pack(pady=5)
    tk.Button(root, text="Season", command=open_season_management, width=20, height=2, bg='white').pack(pady=5)
    tk.Button(root, text="Sponsorship", command=open_sponsorship_management, width=20, height=2, bg='white').pack(pady=5)
    tk.Button(root, text="Assignment", command=open_assignment_management, width=20, height=2, bg='white').pack(pady=5)
    tk.Button(root, text="NBA Game", command=open_nbagame_management, width=20, height=2, bg='white').pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit, width=20, height=2, bg='white').pack(pady=20)

    root.mainloop()

# Function for player management
def player_management():
    manage_table("Player", [
        ("PlayerID", "PlayerID"),
        ("FirstName", "First Name"),
        ("LastName", "Last Name"),
        ("Position", "Position"),
        ("Height", "Height"),
        ("Weight", "Weight"),
        ("JerseyNumber", "Jersey Number"),
        ("DateOfBirth", "Date of Birth"),
        ("NBARank", "NBA Rank"),
        ("Nationality", "Nationality"),
        ("ExperienceYears", "Experience Years")
    ])

# Function for coach management
def coach_management():
    manage_table("Coach", [
        ("CoachID", "CoachID"),
        ("FirstName", "First Name"),
        ("LastName", "Last Name"),
        ("TeamID", "TeamID"),
        ("YearsOfExperience", "Years of Experience"),
        ("DateOfBirth", "Date of Birth")
    ])

# Function for team management
def team_management():
    manage_table("Team", [
        ("TeamID", "TeamID"),
        ("TeamName", "Team Name"),
        ("City", "City"),
        ("Conference", "Conference"),
        ("Division", "Division")
    ])

# Function for season management
def season_management():
    manage_table("Season", [
        ("SeasonID", "SeasonID"),
        ("Year", "Year"),
        ("StartDate", "Start Date"),
        ("EndDate", "End Date")
    ])

# Function for sponsorship management
def sponsorship_management():
    manage_table("Sponsorship", [
        ("SponsorshipID", "SponsorshipID"),
        ("SponsorName", "Sponsor Name"),
        ("SponsorshipType", "Sponsorship Type"),
        ("SponsorshipAmount", "Sponsorship Amount")
    ])

# Function for assignment management
def assignment_management():
    manage_table("Assignment", [
        ("AssignmentID", "AssignmentID"),
        ("TeamID", "TeamID"),
        ("CoachID", "CoachID"),
        ("StartDate", "Start Date"),
        ("EndDate", "End Date"),
        ("Role", "Role")
    ])

# Function for NBA game management
def nbagame_management():
    manage_table("NBAGame", [
        ("NBAGameID", "NBAGameID"),
        ("HomeTeamID", "Home Team ID"),
        ("AwayTeamID", "Away Team ID"),
        ("SeasonID", "SeasonID"),
        ("GameDate", "Game Date"),
        ("Arena", "Arena"),
        ("GameType", "Game Type")
    ])

# Generic function to manage tables
def manage_table(table_name, columns):
    root = tk.Tk()
    root.title(f"NBA Management System - {table_name} Management")
    root.geometry("1000x600")

    def connect_db():
        try:
            return pyodbc.connect(connection_string)
        except pyodbc.Error as e:
            messagebox.showerror("Database Connection Error", str(e))
            return None

    def fetch_data():
        connection = connect_db()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            for row in tree.get_children():
                tree.delete(row)
            for row in rows:
                formatted_row = tuple(str(value).strip() for value in row)  # Format and strip extra characters
                tree.insert("", tk.END, values=formatted_row)
        except pyodbc.Error as e:
            messagebox.showerror("Query Error", str(e))
        finally:
            connection.close()

    # GUI components
    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=10)

    tk.Button(frame_buttons, text="Fetch Data", command=fetch_data).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Add Record", command=lambda: add_record()).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Delete Record", command=lambda: delete_record()).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Update Record", command=lambda: update_record()).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Query Data", command=lambda: query_data()).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_buttons, text="Back to Main Menu", command=lambda: [root.destroy(), main_menu()]).pack(side=tk.LEFT, padx=10)

    # Data table
    tree = ttk.Treeview(root, columns=[col[0] for col in columns], show="headings")
    for col_id, col_name in columns:
        tree.heading(col_id, text=col_name)
    tree.pack(fill=tk.BOTH, expand=True)

    def add_record():
        add_window = tk.Toplevel(root)
        add_window.title(f"Add Record to {table_name}")
        add_window.geometry("500x400")

        entries = {}
        for idx, (col_id, col_name) in enumerate(columns[1:]):  # Exclude ID columns from input
            tk.Label(add_window, text=f"{col_name}:").grid(row=idx, column=0, padx=10, pady=5)
            entry = tk.Entry(add_window)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[col_id] = entry

        def save_record():
            values = [entry.get() for entry in entries.values()]
            if not all(values):
                messagebox.showwarning("Input Error", "Please enter all fields.")
                return

            connection = connect_db()
            if connection is None:
                return

            cursor = connection.cursor()
            try:
                placeholders = ', '.join(['?'] * len(values))
                columns_str = ', '.join(entries.keys())
                cursor.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})", values)
                connection.commit()
                messagebox.showinfo("Success", f"Record added to {table_name} successfully.")
                fetch_data()
                add_window.destroy()
            except pyodbc.Error as e:
                messagebox.showerror("Insert Error", str(e))
            finally:
                connection.close()

        tk.Button(add_window, text="Save", command=save_record).grid(row=len(columns), column=1, pady=10)

    def delete_record():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")
            return

        record_id = tree.item(selected_item[0], 'values')[0]

        connection = connect_db()
        if connection is None:
            return

        cursor = connection.cursor()
        try:
            cursor.execute(f"DELETE FROM {table_name} WHERE {columns[0][0]} = ?", (record_id,))
            connection.commit()
            messagebox.showinfo("Success", f"Record deleted from {table_name} successfully.")
            fetch_data()
        except pyodbc.Error as e:
            messagebox.showerror("Delete Error", str(e))
        finally:
            connection.close()

    def update_record():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to update.")
            return

        record_values = tree.item(selected_item[0], 'values')
        update_window = tk.Toplevel(root)
        update_window.title(f"Update Record in {table_name}")
        update_window.geometry("500x400")

        entries = {}
        for idx, (col_id, col_name) in enumerate(columns[1:]):  # Exclude ID columns from input
            tk.Label(update_window, text=f"{col_name}:").grid(row=idx, column=0, padx=10, pady=5)
            entry = tk.Entry(update_window)
            entry.insert(0, record_values[idx + 1])  # Pre-fill with existing values
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[col_id] = entry

        def save_update():
            values = [entry.get() for entry in entries.values()]
            if not all(values):
                messagebox.showwarning("Input Error", "Please enter all fields.")
                return

            connection = connect_db()
            if connection is None:
                return

            cursor = connection.cursor()
            try:
                placeholders = ', '.join([f"{col} = ?" for col in entries.keys()])
                cursor.execute(f"UPDATE {table_name} SET {placeholders} WHERE {columns[0][0]} = ?", values + [record_values[0]])
                connection.commit()
                messagebox.showinfo("Success", f"Record updated in {table_name} successfully.")
                fetch_data()
                update_window.destroy()
            except pyodbc.Error as e:
                messagebox.showerror("Update Error", str(e))
            finally:
                connection.close()

        tk.Button(update_window, text="Save", command=save_update).grid(row=len(columns), column=1, pady=10)

    def query_data():
        query_window = tk.Toplevel(root)
        query_window.title(f"Query Records in {table_name}")
        query_window.geometry("500x400")

        tk.Label(query_window, text="Column:").grid(row=0, column=0, padx=10, pady=5)
        column_combobox = ttk.Combobox(query_window, values=[col[1] for col in columns[1:]])  # Exclude ID columns from query
        column_combobox.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(query_window, text="Condition:").grid(row=1, column=0, padx=10, pady=5)
        condition_combobox = ttk.Combobox(query_window, values=["=", "<", ">", "<=", ">=", "!="])
        condition_combobox.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(query_window, text="Value:").grid(row=2, column=0, padx=10, pady=5)
        value_entry = tk.Entry(query_window)
        value_entry.grid(row=2, column=1, padx=10, pady=5)

        def execute_query():
            column = column_combobox.get()
            condition = condition_combobox.get()
            value = value_entry.get()

            if not (column and condition and value):
                messagebox.showwarning("Input Error", "Please fill all fields.")
                return

            connection = connect_db()
            if connection is None:
                return

            cursor = connection.cursor()
            try:
                query = f"SELECT * FROM {table_name} WHERE {column} {condition} ?"
                cursor.execute(query, (value,))
                rows = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for row in rows:
                    formatted_row = tuple(str(value).strip() for value in row)  # Format and strip extra characters
                    tree.insert("", tk.END, values=formatted_row)
            except pyodbc.Error as e:
                messagebox.showerror("Query Error", str(e))
            finally:
                connection.close()

        tk.Button(query_window, text="Query", command=execute_query).grid(row=3, column=1, pady=10)

    # Initialize data
    fetch_data()

    root.mainloop()

if __name__ == "__main__":
    main_menu()
