from pathlib import Path

import pandas as pd
from sqlalchemy.engine import Engine

from validation import validate_dataframe

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SOURCE = BASE_DIR.parent.parent / "LAB_01_JSON_JUPYTER_PANDAS" / "data" / "deliveries_lab.json"
DEFAULT_DB = BASE_DIR / "deliveries.sqlite"


def ingest(df: pd.DataFrame, engine: Engine) -> int:
    # TODO : valider, créer la table, ne garder que les delivery_id inconnus,
    #        insérer, et retourner le nombre de lignes réellement insérées.
    raise NotImplementedError


def main() -> None:
    # TODO : créer un engine SQLite sur DEFAULT_DB, charger DEFAULT_SOURCE,
    #        appeler ingest() deux fois et afficher les compteurs.
    raise NotImplementedError


if __name__ == "__main__":
    main()
