from django.apps import AppConfig
from django.db import connection
from .executor import create_tables_and_load_data
import psycopg2

ddl_file_path = "D:\OneDrive - Carleton University\Winter2024\COMP3005\ProjectV2\COMP3005-Project\gymmanagement\gymapp\\tables.sql"
dml_file_path = "D:\OneDrive - Carleton University\Winter2024\COMP3005\ProjectV2\COMP3005-Project\gymmanagement\gymapp\data.sql"
create_tables_and_load_data(connection,ddl_file_path,dml_file_path)

class GymappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gymapp'
