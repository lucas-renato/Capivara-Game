

import os
import psycopg2


DBNAME = os.getenv("CAPIVARA_DB", "capivara")
DBUSER = os.getenv("CAPIVARA_USER", "postgres")
DBPASS = os.getenv("CAPIVARA_PASS", "postgres")
DBHOST = os.getenv("CAPIVARA_HOST", "localhost")
DBPORT = os.getenv("CAPIVARA_PORT", "5433")


DSN = (
f"dbname={DBNAME} "
f"user={DBUSER} "
f"password={DBPASS} "
f"host={DBHOST} "
f"port={DBPORT}"
)


def get_conn():
return psycopg2.connect(DSN)