import os
import datetime
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def run_dump():
    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dump_path = os.path.join(BACKUP_DIR, f"{DB_NAME}_backup_{timestamp}.sql")

    env = os.environ.copy()
    env["PGPASSWORD"] = DB_PASSWORD

    try:
        subprocess.run(
            [
            "pg_dump",
            "-U", DB_USER,
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-d", DB_NAME,
            "-F", "p",  
            "-f", dump_path
            ],
            check=True,
            env=env
        )
        print(f"✔ Backup feito com sucesso: {dump_path}")
        return dump_path
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao fazer backup: {e}")
        return None