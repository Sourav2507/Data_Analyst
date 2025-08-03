import pandas as pd
import duckdb

def query_parquet_s3(s3_path, region="ap-south-1"):
    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute("INSTALL parquet; LOAD parquet;")
    df = con.execute(f"SELECT * FROM read_parquet('{s3_path}?s3_region={region}')").fetchdf()
    return df
