import tkinter as tk
from tkinter import messagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

root = tk.Tk()
root.title("Medical Expert System")
root.geometry("500x650")

# Patient Name
tk.Label(root, text="Enter Patient Name:", font=("Arial", 12)).pack()
patient_name = tk.Entry(root)
patient_name.pack(pady=5)

# Simple Diseases (easy words)
rules = [
    {"disease": "Fever", "symptoms": ["fever", "weakness"], "advice": "Take rest and drink water"},
    {"disease": "Cold", "symptoms": ["cough", "cold", "throat pain"], "advice": "Drink warm water and take steam"},
    {"disease": "Flu", "symptoms": ["fever", "cough", "weakness"], "advice": "Take rest and proper medicine"},
    {"disease": "Headache", "symptoms": ["headache"], "advice": "Take rest and avoid mobile"},
    {"disease": "Food Poisoning", "symptoms": ["feeling like vomiting", "vomiting"], "advice": "Drink ORS and stay hydrated"},
    {"disease": "Stomach Pain", "symptoms": ["feeling like vomiting", "weakness"], "advice": "Eat light food and rest"},
]

# Simple Symptoms
symptoms_list = [
    "fever", "cough", "weakness", "headache",
    "feeling like vomiting", "vomiting", "throat pain", "cold"
]

var_list = []
result_text = ""

# Diagnose
def diagnose():
    global result_text

    user_symptoms = [symptoms_list[i] for i in range(len(symptoms_list)) if var_list[i].get() == 1]

    if not user_symptoms:
        messagebox.showwarning("Warning", "Please select symptoms")
        return

    results = []

    for rule in rules:
        match = len(set(rule["symptoms"]) & set(user_symptoms))
        confidence = (match / len(rule["symptoms"])) * 100

        if match > 0:
            results.append((rule["disease"], confidence, rule["advice"]))

    results.sort(key=lambda x: x[1], reverse=True)

    output.delete("1.0", tk.END)
    result_text = ""

    name = patient_name.get() if patient_name.get() else "Unknown"

    header = f"Patient Name: {name}\n\nDiagnosis Report:\n\n"
    output.insert(tk.END, header)
    result_text += header

    if results:
        for disease, confidence, advice in results:
            text = f"Disease: {disease}\nConfidence: {confidence:.2f}%\nAdvice: {advice}\n\n"
            output.insert(tk.END, text)
            result_text += text
    else:
        output.insert(tk.END, "No disease matched")

# Export PDF
def export_pdf():
    global result_text

    if not result_text:
        messagebox.showerror("Error", "No result to export")
        return

    doc = SimpleDocTemplate("Diagnosis_Report.pdf")
    styles = getSampleStyleSheet()

    content = []
    for line in result_text.split("\n"):
        content.append(Paragraph(line, styles["Normal"]))
        content.append(Spacer(1, 5))

    doc.build(content)
    messagebox.showinfo("Success", "PDF saved")

# UI
tk.Label(root, text="Select Symptoms", font=("Arial", 14)).pack(pady=10)

for symptom in symptoms_list:
    var = tk.IntVar()
    chk = tk.Checkbutton(root, text=symptom, variable=var)
    chk.pack(anchor='w')
    var_list.append(var)
import tkinter as tk
from tkinter import messagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

root = tk.Tk()
root.title("Medical Expert System")
root.geometry("520x700")
root.configure(bg="#f5f7fa")

# ---------------- Patient Name ----------------
tk.Label(root, text="Medical Expert System", font=("Arial", 18, "bold"), bg="#f5f7fa").pack(pady=10)

tk.Label(root, text="Enter Patient Name:", font=("Arial", 12), bg="#f5f7fa").pack()
patient_name = tk.Entry(root, font=("Arial", 12))
patient_name.pack(pady=5)

# ---------------- Rules ----------------
rules = [
    {"disease": "Fever", "symptoms": ["fever", "weakness"], "advice": "Take rest and drink water"},
    {"disease": "Cold", "symptoms": ["cough", "cold", "throat pain"], "advice": "Drink warm water and take steam"},
    {"disease": "Flu", "symptoms": ["fever", "cough", "weakness"], "advice": "Take rest and proper medicine"},
    {"disease": "Headache", "symptoms": ["headache"], "advice": "Take rest and avoid mobile"},
    {"disease": "Food Poisoning", "symptoms": ["feeling like vomiting", "vomiting"], "advice": "Drink ORS and stay hydrated"},
    {"disease": "Stomach Pain", "symptoms": ["feeling like vomiting", "weakness"], "advice": "Eat light food"},
]

symptoms_list = [
    "fever", "cough", "weakness", "headache",
    "feeling like vomiting", "vomiting", "throat pain", "cold"
]

selected = set()
buttons = []
result_text = ""

# ---------------- Toggle Button ----------------
def toggle(symptom, btn):
    if symptom in selected:
        selected.remove(symptom)
        btn.config(bg="#e0e0e0")
    else:
        selected.add(symptom)
        btn.config(bg="#4CAF50", fg="white")

# ---------------- UI Buttons ----------------
tk.Label(root, text="Select Symptoms", font=("Arial", 14, "bold"), bg="#f5f7fa").pack(pady=10)

frame = tk.Frame(root, bg="#f5f7fa")
frame.pack()

for symptom in symptoms_list:
    btn = tk.Button(frame, text=symptom, width=18, bg="#e0e0e0",
                    command=lambda s=symptom, b=None: None)
    btn.pack(pady=5)

    # Fix lambda binding
    btn.config(command=lambda s=symptom, b=btn: toggle(s, b))
    buttons.append(btn)

# ---------------- Diagnose ----------------
def diagnose():
    global result_text

    if not selected:
        messagebox.showwarning("Warning", "Select symptoms")
        return

    results = []

    for rule in rules:
        match = len(set(rule["symptoms"]) & selected)
        confidence = (match / len(rule["symptoms"])) * 100

        if match > 0:
            results.append((rule["disease"], confidence, rule["advice"]))

    results.sort(key=lambda x: x[1], reverse=True)

    output.delete("1.0", tk.END)
    result_text = ""

    name = patient_name.get() if patient_name.get() else "Unknown"

    header = f"Patient Name: {name}\n\nDiagnosis Report:\n\n"
    output.insert(tk.END, header)
    result_text += header

    if results:
        for disease, confidence, advice in results:
            text = f"Disease: {disease}\nConfidence: {confidence:.2f}%\nAdvice: {advice}\n\n"
            output.insert(tk.END, text)
            result_text += text
    else:
        output.insert(tk.END, "No disease matched")

# ---------------- Export PDF ----------------
def export_pdf():
    global result_text

    if not result_text:
        messagebox.showerror("Error", "No result")
        return

    doc = SimpleDocTemplate("Diagnosis_Report.pdf")
    styles = getSampleStyleSheet()

    content = []
    for line in result_text.split("\n"):
        content.append(Paragraph(line, styles["Normal"]))
        content.append(Spacer(1, 5))

    doc.build(content)
    messagebox.showinfo("Success", "PDF saved")

# ---------------- Buttons ----------------
tk.Button(root, text="Diagnose", command=diagnose,
          bg="#4CAF50", fg="white", width=20, height=2).pack(pady=10)

tk.Button(root, text="Export PDF", command=export_pdf,
          bg="#2196F3", fg="white", width=20, height=2).pack()

# ---------------- Output ----------------
output = tk.Text(root, height=15, width=60)
output.pack(pady=10)

tk.Label(root, text="⚠️ Not a real medical system", fg="red", bg="#f5f7fa").pack()

root.mainloop()

tk.Button(root, text="Diagnose", command=diagnose, bg="green", fg="white").pack(pady=10)
tk.Button(root, text="Export PDF", command=export_pdf, bg="blue", fg="white").pack(pady=5)

output = tk.Text(root, height=18, width=60)
output.pack()

tk.Label(root, text="⚠️ Not a real medical system", fg="red").pack()

root.mainloop()
