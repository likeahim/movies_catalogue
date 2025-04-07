import csv
import sqlite3
from sqlite3 import Error
from sqlalchemy import create_engine, Table, Column, String, Float, Integer, MetaData, ForeignKey

DB_FILE = "weather.db"
CSV_STATIONS = "clean_stations.csv"
CSV_MEASURES = "clean_measure.csv"

def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        print(e)
        return None

def execute_sql(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def create_tables(conn):
    create_stations_sql = """
    CREATE TABLE IF NOT EXISTS stations (
        station TEXT PRIMARY KEY,
        latitude REAL,
        longitude REAL,
        elevation REAL,
        name TEXT,
        country TEXT,
        state TEXT
    );
    """

    create_measures_sql = """
    CREATE TABLE IF NOT EXISTS measurements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station TEXT,
        date TEXT,
        precip REAL,
        tobs INTEGER,
        FOREIGN KEY (station) REFERENCES stations (station)
    );
    """

    execute_sql(conn, create_stations_sql)
    execute_sql(conn, create_measures_sql)

def load_csv_to_stations(conn, csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO stations(station, latitude, longitude, elevation, name, country, state)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    row["station"], float(row["latitude"]), float(row["longitude"]),
                    float(row["elevation"]), row["name"], row["country"], row["state"]
                ))
            except Error as e:
                print("Error inserting station:", e)
        conn.commit()

def load_csv_to_measurements(conn, csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                conn.execute("""
                    INSERT INTO measurements(station, date, precip, tobs)
                    VALUES (?, ?, ?, ?)
                """, (
                    row["station"], row["date"],
                    float(row["precip"]) if row["precip"] else 0.0,
                    int(row["tobs"])
                ))
            except Error as e:
                print("Error inserting measurement:", e)
        conn.commit()

def show_stations_table():
    engine = create_engine("sqlite:///weather.db", echo=False)
    meta = MetaData()

    stations = Table('stations', meta,
                     Column('station', String, primary_key=True),
                     Column('latitude', Float),
                     Column('longitude', Float),
                     Column('elevation', Float),
                     Column('name', String),
                     Column('country', String),
                     Column('state', String)
                     )

    with engine.connect() as conn:
        result = conn.execute(stations.select())
        for row in result:
            print(row)

def show_measurements_table():
    engine = create_engine("sqlite:///weather.db", echo=False)
    meta = MetaData()

    measurements = Table('measurements', meta,
                     Column('id', Integer, primary_key=True),
                     Column('station', String),
                     Column('date', String),
                     Column('precip', Float),
                     Column('tobs', Integer)
                     )
    with engine.connect() as conn:
        result = conn.execute(measurements.select())
        for row in result:
            print(row)

if __name__ == "__main__":
    conn = create_connection(DB_FILE)
    if conn:
        conn.execute("DROP TABLE IF EXISTS measurements")
        conn.execute("DROP TABLE IF EXISTS stations")
        create_tables(conn)
        load_csv_to_stations(conn, CSV_STATIONS)
        load_csv_to_measurements(conn, CSV_MEASURES)
        print("Data loaded.\n")

    print("Table stations:")
    show_stations_table()
    print("Table measurements:")
    show_measurements_table()
