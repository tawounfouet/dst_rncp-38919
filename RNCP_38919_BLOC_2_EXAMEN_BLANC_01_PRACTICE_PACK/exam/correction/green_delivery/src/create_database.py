from src.database import engine
from src.models import Base


def main() -> None:
    Base.metadata.create_all(engine, checkfirst=True)
    print("Database tables created")


if __name__ == "__main__":
    main()
