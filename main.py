from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from sqpy.sqpy import DataBase

def Main():
    root = Tk()
    root.geometry("700x700")
    root.title("Attendance System")

    # Define StringVar for each input field
    student_var = StringVar()
    gradeLvl_var = StringVar()
    section_var = StringVar()
    date_var = StringVar()
    time_var = StringVar()

    def add_record():
        student = student_var.get()
        gradeLvl = gradeLvl_var.get()
        section = section_var.get()
        date = date_var.get()
        time = time_var.get()
        
        if student and gradeLvl and section and date and time:
            data = {
                "student": student,
                "gradeLvl": int(gradeLvl),
                "section": section,
                "date": date,
                "time": time
            }
            db.update(data)
            messagebox.showinfo("Success", "Record added/updated successfully!")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def remove_record():
        student = student_var.get()
        
        if student:
            db.remove({"student": student})
            messagebox.showinfo("Success", "Record removed successfully!")
        else:
            messagebox.showwarning("Input Error", "Please enter the student name to remove the record")

    def fetch_record():
        student = student_var.get()
        
        if student:
            record = db.get({"student": student})
            if record:
                messagebox.showinfo("Record", f"Found: {record}")
            else:
                messagebox.showinfo("Record", "No record found")
        else:
            messagebox.showwarning("Input Error", "Please enter the student name to fetch the record")

    # Database connection
    db = DataBase()
    db.create()

    # GUI elements
    Label(root, text="Student Name").pack()
    Entry(root, textvariable=student_var).pack()

    Label(root, text="Grade Level").pack()
    Entry(root, textvariable=gradeLvl_var).pack()

    Label(root, text="Section").pack()
    Entry(root, textvariable=section_var).pack()

    Label(root, text="Date").pack()
    Entry(root, textvariable=date_var).pack()

    Label(root, text="Time").pack()
    Entry(root, textvariable=time_var).pack()

    Button(root, text="Add/Update Record", command=add_record).pack()
    Button(root, text="Remove Record", command=remove_record).pack()
    Button(root, text="Fetch Record", command=fetch_record).pack()

    root.mainloop()
    db.close()

if __name__ == "__main__":
    Main()

