import tkinter as tk
from tkinter import ttk
import pandas as pd
from google.cloud import storage
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'

def download_file():
    # Функция загрузки файла из Google Cloud Storage
    def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print(f'File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.')

    # Указываем путь к локальному файлу для загрузки
    source_file_name = 'output1.csv'
    # Указываем имя бакета в Google Cloud Storage
    bucket_name = 'gratka_bucket'
    # Указываем имя, под которым файл будет сохранен в бакете
    destination_blob_name = 'output1.csv'

    # Загружаем файл в Google Cloud Storage
    upload_to_gcs(bucket_name, source_file_name, destination_blob_name)
    print("File uploaded successfully!")

def display_csv_data():
    # Функция для отображения данных из CSV
    def display_data():
        # Чтение данных из CSV
        df = pd.read_csv('output1.csv')

        # Очистка таблицы перед отображением новых данных
        for row in tree.get_children():
            tree.delete(row)

        # Отображение данных по столбцам
        for index, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))

    # Создание нового окна для отображения данных
    data_window = tk.Toplevel(root)
    data_window.title("CSV Data Viewer")

    # Создание виджета Treeview для отображения данных
    tree = ttk.Treeview(data_window)

    # Определение колонок в Treeview
    df = pd.read_csv('output1.csv')
    tree["columns"] = df.columns.tolist()

    # Настройка заголовков колонок
    for col in df.columns:
        tree.heading(col, text=col)

    # Отображение данных при открытии окна
    display_data()

    # Пакет виджета Treeview
    tree.pack(expand=True, fill=tk.BOTH)

    # Кнопка для загрузки данных из CSV и их отображения
    display_button = tk.Button(data_window, text="Display CSV Data", command=display_data)
    display_button.pack(pady=10)

# Создание графического интерфейса
root = tk.Tk()
root.title("Google Cloud Storage Uploader")

# Кнопка для загрузки файла
upload_button = tk.Button(root, text="Upload File to GCS", command=download_file)
upload_button.pack(pady=10)

# Кнопка для отображения данных из CSV
display_button = tk.Button(root, text="Display CSV Data", command=display_csv_data)
display_button.pack(pady=10)

root.mainloop()