TOKEN = 'your_token_here'
SECRET = 'your_secret_here'
DEVICE_1 = 'your_device_id_here'
DEVICE_2 = 'your_device_id_here'
DB_HOST = 'localhost'
DB_USER = 'your_DB_user_here'
DB_PASSWORD = 'your_DB_password_here'
DB_DATABASE = 'your_DB_database_here'
DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    time TIMESTAMP,
    humidity FLOAT,
    temperature FLOAT,
    battery FLOAT
);
"""
