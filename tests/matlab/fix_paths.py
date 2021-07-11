import json
import os
from pathlib import Path

if __name__ == "__main__":
    path = Path(os.path.dirname(__file__), "..", "data")
    print(f"Checking {path.absolute()}")

    for root, dirs, files in os.walk(path, topdown=False):
        if "data.json" in files:
            print(f"Fixing data.json in {path.absolute()}")

            fp = open(Path(root, "data.json"), "rb")
            data = json.load(fp)
            fp.close()

            for row in data:
                p = Path(row["reference"])
                row["reference"] = str(p.relative_to(*p.parts[:1]))

                p = Path(row["measured"])
                row["measured"] = str(p.relative_to(*p.parts[:1]))

            fp = open(Path(root, "data.json"), "w")
            json.dump(data, fp)
            fp.close()
