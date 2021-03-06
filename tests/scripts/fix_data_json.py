import json
import os
from pathlib import Path

if __name__ == "__main__":
    path = Path(os.path.dirname(__file__), "..", "data", "data.json")
    print(f"Fixing data.json in {path.absolute()}")

    fp = open(path, "rb")
    data = json.load(fp)
    fp.close()

    try:
        data = dict((key, d[key]) for d in data for key in d)
    except TypeError:
        print("File is already fixed!")
        exit(0)

    for key in data.keys():
        data[key] = data[key][0]

    for val_row in data.values():
        for r in val_row:
            p = Path(r["reference"])
            r["reference"] = str(p.relative_to(*p.parts[:1])).replace("\\", "/")

            p = Path(r["measured"])
            r["measured"] = str(p.relative_to(*p.parts[:1])).replace("\\", "/")

    fp = open(path, "w")
    json.dump(data, fp, indent=4)
    fp.close()
