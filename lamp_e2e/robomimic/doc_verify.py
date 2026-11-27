"""Outline one tab of a saved read_doc result: style, bullet, bold label, spacing and text of each paragraph, and
table contents with header bold / shading.  usage: doc_verify.py <file> <tabId>"""
import json
import sys

J = json.load(open(sys.argv[1], encoding="utf-8"))
D = J.get("content", J)
tab = [t for t in D["tabs"] if t["tabProperties"]["tabId"] == sys.argv[2]][0]
print("tab", tab["tabProperties"]["title"], "index", tab["tabProperties"].get("index"))
for el in tab["documentTab"]["body"]["content"]:
    if "paragraph" in el:
        p = el["paragraph"]
        runs = [(e["textRun"]["content"], e["textRun"].get("textStyle", {}).get("bold", False))
                for e in p["elements"] if "textRun" in e]
        txt = "".join(r[0] for r in runs).rstrip("\n")
        sb = p["paragraphStyle"].get("spaceBelow", {}).get("magnitude")
        bold = "B:" + runs[0][0][:30] if runs and runs[0][1] and len(runs) > 1 else ""
        print("{:>5} {:<11} {:<3} sb={} {} | {}".format(el["startIndex"], p["paragraphStyle"]["namedStyleType"],
                                                       "*" if "bullet" in p else "", sb, bold, txt[:70]))
    elif "table" in el:
        print("{:>5} TABLE".format(el["startIndex"]))
        for ri, row in enumerate(el["table"]["tableRows"]):
            cells = []
            for c in row["tableCells"]:
                t = "".join(e["textRun"]["content"] for pp in c["content"] for e in pp["paragraph"]["elements"]
                            if "textRun" in e).strip()
                b = any(e["textRun"].get("textStyle", {}).get("bold") for pp in c["content"]
                        for e in pp["paragraph"]["elements"] if "textRun" in e)
                cells.append(t + ("(b)" if b else ""))
            bg = "shaded" if row["tableCells"][0].get("tableCellStyle", {}).get("backgroundColor", {}).get("color") else ""
            print("        ", bg, " | ".join(cells))
