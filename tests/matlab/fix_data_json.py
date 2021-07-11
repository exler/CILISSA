import json
import os
from pathlib import Path

if __name__ == "__main__":
    path = Path(os.path.dirname(__file__), "..", "data", "data.json")
    print(f"Fixing data.json in {path.absolute()}")

    fp = open(path, "rb")
    data = json.load(fp)
    fp.close()

    data = dict((key, d[key]) for d in data for key in d)

    for val_row in data.values():
        for row in val_row:
            for r in row:
                p = Path(r["reference"])
                r["reference"] = str(p.relative_to(*p.parts[:1]))

                p = Path(r["measured"])
                r["measured"] = str(p.relative_to(*p.parts[:1]))

    fp = open(path, "w")
    json.dump(data, fp)
    fp.close()
