import sys
from alembic.config import main

if __name__ == "__main__":
    sys.argv.append('--config')
    sys.argv.append('./alembic.ini')
    main(prog="alembic")
