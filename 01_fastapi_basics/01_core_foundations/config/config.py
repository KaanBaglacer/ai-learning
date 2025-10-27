from pathlib import Path
import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session
from sqlalchemy.exc import OperationalError

# .env dosyasını yükle (proje kök dizinine koyun)
load_dotenv(Path(__file__).parent.parent / ".env")

DB_USER = os.getenv("POSTGRES_USER", "postgres2")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres3")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "todo_app_db")
DB_SCHEMA = os.getenv("POSTGRES_SCHEMA", "todo_app_schema")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?options=-csearch_path%3D{DB_SCHEMA}"
)

# pool_pre_ping=True bağlantı öncesi ping ile stale bağlantıları engeller
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)


def get_session():
    with Session(engine) as session:
        yield session



def check_db_connection():
    try:
        with engine.connect() as conn:
            # basit bir sorgu ile doğrulama (isteğe bağlı)
            conn.execute("SELECT 1")
    except OperationalError as exc:
        # daha kullanıcı dostu hata mesajı
        raise RuntimeError(
            "Veritabanına bağlanılamadı. Lütfen `POSTGRES_USER` / `POSTGRES_PASSWORD` değerlerini "
            "ve PostgreSQL sunucusunun çalıştığını kontrol edin."
        ) from exc