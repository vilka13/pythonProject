import customtkinter as ctk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from google.cloud import storage
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f'File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.')


def download_file():
    source_file_name = 'output1.csv'
    bucket_name = 'gratka_bucket'
    destination_blob_name = 'output1.csv'

    upload_to_gcs(bucket_name, source_file_name, destination_blob_name)
    print("File uploaded successfully!")


def display_csv_data():
    def display_data(df):
        for row in tree.get_children():
            tree.delete(row)

        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))

    def sort_data_by_built_in():
        df = pd.read_csv('output1.csv')

        # Convert values in 'Built In' column to numeric format (if they are not 'NULL')
        df['Built In'] = pd.to_numeric(df['Built In'], errors='coerce')

        # Remove rows with NaN values
        df = df.dropna(subset=['Built In'])

        # Get sort direction from combobox
        sort_direction = sort_combobox.get()

        # Sort by built year based on user selection
        if sort_direction == 'Ascending':
            df_sorted = df.sort_values(by='Built In', ascending=True)
        elif sort_direction == 'Descending':
            df_sorted = df.sort_values(by='Built In', ascending=False)
        else:
            print("Invalid input. Please select 'Ascending' or 'Descending'.")
            return

        display_data(df_sorted)

    def reset_data():
        df = pd.read_csv('output1.csv')
        display_data(df)
        print("Data reset to original state.")



    # Hide the root window
    root.withdraw()

    data_window = ctk.CTkToplevel(root)
    data_window.title("CSV Data Viewer")

    tree_frame = ctk.CTkFrame(data_window)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tree = ttk.Treeview(tree_frame)
    df = pd.read_csv('output1.csv')
    tree["columns"] = df.columns.tolist()
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)

    display_data(df)
    tree.pack(side="left", fill="both", expand=True)

    yscroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    yscroll.pack(side="right", fill="y")
    xscroll = ttk.Scrollbar(data_window, orient="horizontal", command=tree.xview)
    xscroll.pack(side="bottom", fill="x")

    tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

    sort_combobox_label = ctk.CTkLabel(data_window, text="Sort by Built In:")
    sort_combobox_label.pack(side="left", padx=5, pady=5)

    sort_combobox = ctk.CTkComboBox(data_window, values=["Ascending", "Descending"])
    sort_combobox.pack(side="left", padx=5, pady=5)
    sort_combobox.set("Ascending")

    sort_button_built_in = ctk.CTkButton(data_window, text="Sort", command=sort_data_by_built_in)
    sort_button_built_in.pack(side="left", padx=5, pady=5)

    reset_button = ctk.CTkButton(data_window, text="Reset Data", command=reset_data)
    reset_button.pack(side="left", padx=5, pady=5)


    # Show the data window
    data_window.mainloop()


root = ctk.CTk()
root.title("Google Cloud Storage Uploader")

upload_button = ctk.CTkButton(root, text="Upload File to GCS", command=download_file)
upload_button.pack(pady=10)

display_button = ctk.CTkButton(root, text="Display CSV Data", command=display_csv_data)
display_button.pack(pady=10)


# Функция для центрирования окна приложения
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))

    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


# Применяем центрирование при запуске программы
root.update()
center_window(root, root.winfo_width(), root.winfo_height())

root.mainloop()
