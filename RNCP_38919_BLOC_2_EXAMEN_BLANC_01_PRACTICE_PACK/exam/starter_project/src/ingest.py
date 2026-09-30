import pandas as pd

def ingest(df: pd.DataFrame) -> None:
    # TODO
    raise NotImplementedError

def main() -> None:
    df = pd.read_csv("data/processed/deliveries_clean.csv")
    ingest(df)

if __name__ == "__main__":
    main()
