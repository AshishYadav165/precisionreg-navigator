import pandas as pd
from src.db import init_db, get_session, FDAPrecedent

SQLITE_PATH = "data/sqlite/fda_precedents.db"
CSV_PATH = "data/raw/precedents/fda_precedents_seed.csv"

def main():
    init_db(SQLITE_PATH)
    session = get_session(SQLITE_PATH)
    df = pd.read_csv(CSV_PATH)

    session.query(FDAPrecedent).delete()

    for _, row in df.iterrows():
        record = FDAPrecedent(
            trade_name=row["trade_name"],
            sponsor=row["sponsor"],
            disease_use=row["disease_use"],
            biomarker=row["biomarker"],
            platform=row["platform"],
            specimen_type=row["specimen_type"],
            route=row["route"],
            submission_number=row["submission_number"],
            cdx_flag=str(row["cdx_flag"]).lower() == "true",
            summary_url=row["summary_url"],
        )
        session.add(record)

    session.commit()
    print(f"Loaded {len(df)} precedent records into SQLite.")

if __name__ == "__main__":
    main()
