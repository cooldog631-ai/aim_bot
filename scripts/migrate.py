"""Run database migrations using Alembic."""

import subprocess
import sys


def main():
    """Run alembic upgrade head."""
    try:
        print("Running database migrations...")
        result = subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("✅ Migrations completed successfully!")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        return e.returncode
    except FileNotFoundError:
        print("❌ Alembic not found. Please install it: pip install alembic")
        return 1


if __name__ == "__main__":
    sys.exit(main())
