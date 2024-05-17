import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from google.cloud import storage
import os

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
    def display_data(df):
        for row in tree.get_children():
            tree.delete(row)

        for index, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))

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

    def plot_built_in_vs_square():
        df = pd.read_csv('output1.csv')

        if 'Built In' not in df.columns or 'Square' not in df.columns:
            print("The required columns are not present in the CSV file.")
            return

        # Convert values in 'Built In' and 'Square' columns to numeric format
        df['Built In'] = pd.to_numeric(df['Built In'], errors='coerce')
        df['Square'] = pd.to_numeric(df['Square'], errors='coerce')

        # Remove rows with NaN values
        df = df.dropna(subset=['Built In', 'Square'])

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df['Built In'], df['Square'], marker='o')

        ax.set_title('Built In Year vs. Square')
        ax.set_xlabel('Built In Year')
        ax.set_ylabel('Square')
        ax.grid(True)
        plt.xticks(rotation=45)

        # Create a new window for the plot
        plot_window = tk.Toplevel()
        plot_window.title("Built In Year vs. Square")

        # Embed the plot into a Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    data_window = tk.Toplevel(root)
    data_window.title("CSV Data Viewer")

    # Используем стилизацию из ttkthemes
    style = ThemedStyle(data_window)
    style.set_theme("arc")  # Выбираем тему оформления

    tree_frame = ttk.Frame(data_window)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(tree_frame)
    df = pd.read_csv('output1.csv')
    tree["columns"] = df.columns.tolist()

    for col in df.columns:
        tree.heading(col, text=col)

    display_data(df)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    yscroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    yscroll.pack(side=tk.RIGHT, fill=tk.Y)
    xscroll = ttk.Scrollbar(data_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)

    tree.config(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

    display_button = ttk.Button(data_window, text="Display CSV Data", command=lambda: display_data(df))
    display_button.pack(pady=10)

    sort_combobox_label = ttk.Label(data_window, text="Sort by Built In:")
    sort_combobox_label.pack(side=tk.LEFT, padx=5, pady=5)

    sort_combobox = ttk.Combobox(data_window, values=["Ascending", "Descending"], state="readonly")
    sort_combobox.pack(side=tk.LEFT, padx=5, pady=5)
    sort_combobox.current(0)

    sort_button_built_in = ttk.Button(data_window, text="Sort", command=sort_data_by_built_in)
    sort_button_built_in.pack(side=tk.LEFT, padx=5, pady=5)

    reset_button = ttk.Button(data_window, text="Reset Data", command=reset_data)
    reset_button.pack(side=tk.LEFT, padx=5, pady=5)

    plot_button = ttk.Button(data_window, text="Plot Built In vs. Square", command=plot_built_in_vs_square)
    plot_button.pack(side=tk.LEFT, padx=5, pady=5)


root = tk.Tk()
root.title("Google Cloud Storage Uploader")

# Используем стилизацию из ttkthemes
style = ThemedStyle(root)
style.set_theme("arc")  # Выбираем тему оформления

upload_button = ttk.Button(root, text="Upload File to GCS", command=download_file)
upload_button.pack(pady=10)

display_button = ttk.Button(root, text="Display CSV Data", command=display_csv_data)
var = display_button.pack

display_button = ttk.Button(root, text="Display CSV Data", command=display_csv_data)
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
