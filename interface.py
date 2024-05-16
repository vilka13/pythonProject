import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
import pandas as pd
from google.cloud import storage
import os
import requests
import re
from bs4 import BeautifulSoup

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'

def download_file():
    def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print(f'File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.')

    source_file_name = 'output1.csv'
    bucket_name = 'gratka_bucket'
    destination_blob_name = 'output1.csv'

    upload_to_gcs(bucket_name, source_file_name, destination_blob_name)
    print("File uploaded successfully!")

def display_csv_data():
    def display_data():
        df = pd.read_csv('output1.csv')

        for row in tree.get_children():
            tree.delete(row)

        for index, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))

    def sort_data_by_built_in(reverse=True):
        df = pd.read_csv('output1.csv')

        # Convert values in 'Built In' column to numeric format (if they are not 'NULL')
        df['Built In'] = pd.to_numeric(df['Built In'], errors='coerce')

        # Remove rows with NaN values
        df = df.dropna(subset=['Built In'])

        # Sort by built year from newest to oldest
        df_sorted = df.sort_values(by='Built In', ascending=reverse)

        for row in tree.get_children():
            tree.delete(row)

        for index, row in df_sorted.iterrows():
            tree.insert("", tk.END, values=list(row))

        print("Data sorted by built year.")

    data_window = tk.Toplevel(root)
    data_window.title("CSV Data Viewer")

    tree_frame = tk.Frame(data_window)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(tree_frame)
    df = pd.read_csv('output1.csv')
    tree["columns"] = df.columns.tolist()

    for col in df.columns:
        tree.heading(col, text=col)

    display_data()
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    yscroll = Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    yscroll.pack(side=tk.RIGHT, fill=tk.Y)
    xscroll = Scrollbar(data_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)

    tree.config(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

    display_button = tk.Button(data_window, text="Display CSV Data", command=display_data)
    display_button.pack(pady=10)

    sort_button_built_in = tk.Button(data_window, text="Rok budowy (od starszego do nowego)",
                                     command=lambda: sort_data_by_built_in(True))
    sort_button_built_in.pack(side=tk.LEFT, padx=5, pady=5)

    sort_button_built_in_reverse = tk.Button(data_window, text="Rok budowy(od nowego do starszego)",
                                             command=lambda: sort_data_by_built_in(False))
    sort_button_built_in_reverse.pack(side=tk.LEFT, padx=5, pady=5)

root = tk.Tk()
root.title("Google Cloud Storage Uploader")

upload_button = tk.Button(root, text="Upload File to GCS", command=download_file)
upload_button.pack(pady=10)

display_button = tk.Button(root, text="Display CSV Data", command=display_csv_data)
display_button.pack(pady=10)

# Function for centering the application window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))

    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

# Apply centering when the program launches
root.update()
center_window(root, root.winfo_width(), root.winfo_height())

root.mainloop()
