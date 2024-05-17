import os
from google.cloud import storage, bigquery
import parser


def main():
    # Выполняем основную логику парсера
    parser.main()

    # Задаем переменные
    source_file_name = 'output1.csv'
    bucket_name = 'gratka_bucket'
    dataset_name = 'gratka'
    table_name = 'gratka'

    # Устанавливаем путь к файлу ключа для аутентификации
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'

    # Инициализация клиентов для работы с GCS и BigQuery
    storage_client = storage.Client()
    bigquery_client = bigquery.Client()

    # Создание или получение существующего бакета
    bucket = get_or_create_bucket(storage_client, bucket_name)

    # Загрузка файла в бакет
    upload_to_gcs(bucket, source_file_name, source_file_name)

    # Загрузка данных в BigQuery
    upload_to_bigquery(bigquery_client, bucket_name, source_file_name, dataset_name, table_name)


def get_or_create_bucket(storage_client, bucket_name):
    """Проверяет существование или создает новый бакет"""
    bucket = storage_client.bucket(bucket_name)
    if not bucket.exists():
        bucket = storage_client.create_bucket(bucket_name, location='EU')
    return bucket


def upload_to_gcs(bucket, source_file_name, destination_blob_name):
    """Загружает файл в Google Cloud Storage"""
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f'File {source_file_name} uploaded to {destination_blob_name} in {bucket.name}.')


def clear_table(client, dataset_name, table_name):
    """Удаляет данные из таблицы BigQuery"""

    sql = f"TRUNCATE TABLE `{client.project}.{dataset_name}.{table_name}`"
    query_job = client.query(sql)
    query_job.result()
    print(f"Table {table_name} has been cleared.")


def upload_to_bigquery(client, bucket_name, source_file_name, dataset_name, table_name):
    """Загружает CSV-файл из Cloud Storage в таблицу BigQuery"""
    # Очистка существующей таблицы
    clear_table(client, dataset_name, table_name)

    source_uri = f"gs://{bucket_name}/{source_file_name}"
    destination_table = f"{client.project}.{dataset_name}.{table_name}"

    # Настройка задания на загрузку данных
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        field_delimiter=','
    )

    # Выполнение задания на загрузку данных
    load_job = client.load_table_from_uri(
        source_uri,
        destination_table,
        job_config=job_config
    )
    load_job.result()
    print(f"Data from {source_file_name} has been uploaded to BigQuery table {destination_table}.")


if __name__ == "__main__":
    main()
