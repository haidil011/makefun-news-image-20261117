"""Copy the committed entry.png to /output, byte for byte."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path("/output")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "entry.png").write_bytes((HERE / "entry.png").read_bytes())


if __name__ == "__main__":
    main()
