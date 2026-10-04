from database import SessionLocal
from adapters.engine_adapter import EngineDataAdapter

db = SessionLocal()

try:
    data = EngineDataAdapter.load_engine_input_data(db)

    key = "PU-2101B Production Data Hourly"

    print("KEY EXISTS:", key in data)

    if key in data:
        df = data[key]
        print("ROWS:", len(df))
        print("COLUMNS:", df.columns.tolist())
        print("FIRST:", df.head(1).to_dict("records"))
        print("LAST:", df.tail(1).to_dict("records"))
    else:
        print("HOURLY KEYS:")
        for k in data:
            if "Hourly" in k:
                print(repr(k))
finally:
    db.close()