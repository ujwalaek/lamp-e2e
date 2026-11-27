"""Summarise a saved Google Docs read_doc result: revision, tabs, and the style used in the last tab."""
import json
import sys

J = json.load(open(sys.argv[1], encoding="utf-8"))
D = J.get("content", J)
print("revisionId", D["revisionId"])


def walk(tabs, depth=0):
    for t in tabs:
        p = t["tabProperties"]
        body = t["documentTab"]["body"]["content"]
        print("  " * depth + "TAB", p["tabId"], repr(p["title"]), "elements", len(body))
        walk(t.get("childTabs", []), depth + 1)


walk(D["tabs"])
tab = [t for t in D["tabs"] if sys.argv[2] in t["tabProperties"]["title"]][0] if len(sys.argv) > 2 else D["tabs"][-1]
print("\nstyle sample from tab", tab["tabProperties"]["title"])
seen = 0
for el in tab["documentTab"]["body"]["content"]:
    if "paragraph" in el and seen < 14:
        ps = el["paragraph"]["paragraphStyle"]
        txt = "".join(e.get("textRun", {}).get("content", "") for e in el["paragraph"]["elements"])
        ts = el["paragraph"]["elements"][0].get("textRun", {}).get("textStyle", {})
        print(ps.get("namedStyleType"), {k: ps[k] for k in ("spaceAbove", "spaceBelow") if k in ps},
              "bullet" if "bullet" in el["paragraph"] else "", {k: ts[k] for k in ts if k != "link"}, repr(txt[:50]))
        seen += 1
    if "table" in el:
        c = el["table"]["tableRows"][0]["tableCells"][0]
        tr = c["content"][0]["paragraph"]["elements"][0].get("textRun", {})
        print("TABLE rows", len(el["table"]["tableRows"]), "cell style", c.get("tableCellStyle", {}).get("backgroundColor"),
              "header text style", tr.get("textStyle"))
        break
