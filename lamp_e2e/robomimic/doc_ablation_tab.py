"""Build the update_doc batch for the 'No-hardcoding ablation' tab of the project Google Doc.
Styles match the existing 'Stage-aware durative monitor' tab: Heading 1 sections, body spaceBelow 8pt, bullet items
with a bold label (2pt between items, 8pt after the last), tables with a shaded bold header row.
usage: doc_ablation_tab.py <tabId> <revisionId> > batch.json"""
import json
import sys

TAB, REV = sys.argv[1], sys.argv[2]

B = [
    ("h1", "Summary"),
    ("p", "The question was whether LAMP's relative-pose method can detect execution failures with no task "
          "knowledge written by hand, and if not, exactly why. It can, on both robomimic tasks, with generic "
          "settings only. Pure LAMP with its default settings detects nothing on Square and about a third of the "
          "failures on Tool Hang. Each gap was traced to one cause with a single-setting experiment."),
    ("h1", "The fully learned monitor"),
    ("p", "Everything that was written by hand in the stage-aware monitor is now learned from the training demos:"),
    ("bullets", [
        ("Stages: ", "cut at the robot's own grasp and release moments (free, carry, free, ...), not named by hand."),
        ("Carry order: ", "the most common sequence of carried objects in the training demos."),
        ("Predicates: ", "every LAMP region, and every union of regions for the same object pair, used under its "
                         "LAMP name. No 'holding' or 'nut on peg' names."),
        ("Rules: ", "every (predicate, true or false, at start / over all / at end) per stage is a candidate. It "
                    "is kept only if it held in at least a cut-off share of normal training demos (98, 95, 90 or "
                    "80%). Irrelevant relations drop out by themselves."),
        ("Near misses: ", "rules that held in most but not enough demos are logged, which shows why a useful "
                          "rule was not learned."),
    ]),
    ("p", "Each experiment starts from pure LAMP and adds one change. A failure counts as caught only if an alarm "
          "fires at or after the moment it was injected. Square is also tested on a held-out half of the other "
          "operators' demos. Results below use the 95% cut-off unless noted; the full tables are in "
          "lamp_e2e/robomimic/ABLATION.md and out/<task>/ablation_summary.md in the repo."),
    ("h1", "Square results"),
    ("table", [
        ["Step", "False alarms", "Other operators (better / okay / worse)", "Drop", "Miss", "Slip", "Stall",
         "Wrong grasp", "Wrong peg"],
        ["Pure LAMP (default bins, theta 1.0)", "1/20", "7/25, 10/50, 21/50", "0/20", "0/20", "0/17", "20/20",
         "0/12", "0/20"],
        ["+ coarser bins", "0/20", "0/25, 10/50, 20/50", "0/20", "0/20", "0/17", "20/20", "1/12", "0/20"],
        ["+ theta 0.5", "3/20", "10/25, 27/50, 35/50", "0/20", "0/20", "0/17", "20/20", "3/12", "0/20"],
        ["+ peg symmetry (hand-coded)", "5/20", "11/25, 30/50, 35/50", "20/20", "20/20", "17/17", "20/20",
         "8/12", "20/20"],
        ["+ mixed-operator training", "2/20", "2/25, 5/50, 4/50", "20/20", "20/20", "17/17", "1/20", "8/12",
         "20/20"],
        ["Generic: theta 0.2, no symmetry fix", "6/20", "14/25, 34/50, 36/50", "20/20", "20/20", "17/17",
         "20/20", "10/12", "20/20"],
    ]),
    ("bullets", [
        ("Theta 1.0 is the blocker, not bin size. ", "LAMP keeps only bins that every demo visits, and human "
                                                    "grasps vary too much for that: 0 grasp regions with fine or "
                                                    "coarse bins. At theta 0.5 the grasp regions appear."),
        ("Peg symmetry blocks the goal rule. ", "The nut can sit on the peg in 4 orientations that LAMP treats "
                                               "as different, so no nut-peg region holds at the end of the "
                                               "carry and nothing is caught. With the symmetry folded, 'nut at "
                                               "peg when the carry ends' holds in 173 of 180 demos, is learned, "
                                               "and catches every drop, miss, slip and wrong peg."),
        ("The hand fix is not needed. ", "With theta 0.2 and no fix, LAMP learns one nut-on-peg region that "
                                        "spans the seating angles, and detection is the same, for about one "
                                        "more false alarm in 20."),
        ("One operator's style causes the false alarms on other people. ", "Training on half of each operator "
                                                                          "group cuts their false alarms from "
                                                                          "44-70% to 8-10%, with no loss in "
                                                                          "pose-based detection."),
        ("Stalls become the trade-off. ", "Slow operators stretch the learned stage length, so with mixed "
                                         "training a frozen arm looks normal (stalls caught drop from 20/20 to "
                                         "1/20)."),
    ]),
    ("h1", "Tool Hang results"),
    ("table", [
        ["Step", "False alarms", "Drop", "Miss", "Slip", "Stall", "Wrong grasp"],
        ["Pure LAMP, 98% cut-off", "0/20", "6/18", "1/19", "4/18", "5/20", "8/20"],
        ["+ coarser bins, 98% cut-off", "1/20", "10/18", "12/19", "10/18", "7/20", "13/20"],
        ["+ theta 0.9", "3/20", "9/18", "12/19", "8/18", "9/20", "11/20"],
        ["+ tool frame fix (hand-coded)", "2/20", "9/18", "12/19", "8/18", "8/20", "11/20"],
        ["+ frame-tool theta 0.3 (tuned for one pair)", "2/20", "18/18", "19/19", "18/18", "15/20", "20/20"],
        ["Generic: theta 0.3 for every pair, no tool fix", "6/20", "18/18", "19/19", "18/18", "15/20", "20/20"],
    ]),
    ("bullets", [
        ("Bins that are too fine. ", "Coarser bins lift detection from about a third to about two thirds."),
        ("The 180 degree tool-angle flip does not matter. ", "The tool frame fix changes nothing."),
        ("The missing relation is 'tool on hook'. ", "Failures during the frame carry are mostly caught, but "
                                                     "failures during the tool carry are almost all missed "
                                                     "(drops 0 of 5, slips 0 of 8, stalls 0 of 10), because that "
                                                     "stage has no rule about where the tool must end up."),
        ("A lower theta makes it learnable. ", "With theta 0.3 the rule 'tool at the hook when the tool carry "
                                              "ends' is learned (171 of 180 demos) and every drop, miss, slip "
                                              "and wrong grasp is caught. The same theta for every pair works "
                                              "too, with more false alarms (6/20 instead of 2/20)."),
    ]),
    ("h1", "Conclusions"),
    ("bullets", [
        ("The relative-pose idea works without task knowledge. ", "With coarse bins, a low theta, automatic "
                                                                  "unions of regions and stages from grasp "
                                                                  "events, every pose-type failure is caught "
                                                                  "on both tasks."),
        ("LAMP's default theta of 1.0 is why it fails on human demos. ", "Real demos never all pass through the "
                                                                         "same fine bin."),
        ("Detection depends on one goal rule per carry. ", "If the relation behind 'object at its target when "
                                                          "the carry ends' is not learned (symmetric peg, tool "
                                                          "spread over bins), every failure in that carry is "
                                                          "missed."),
        ("False alarms are the cost. ", "Remaining ones come from grasp poses just outside a learned region, hard "
                                       "bin edges, and slow operators. Training on several operators is the most "
                                       "effective fix found."),
        ("The timing check conflicts with operator variety. ", "It catches stalls only when all training "
                                                              "operators are fast."),
    ]),
    ("p", "Kept fixed in every step, as choices rather than task knowledge: the motion-based grasp signal, the "
          "gripper frame convention, and LAMP's search box (plus coarser object-pair bins), which LAMP's own code "
          "also sets by hand for each domain."),
]

u16 = lambda s: len(s.encode("utf-16-le")) // 2
rng = lambda a, b: {"startIndex": a, "endIndex": b, "tabId": TAB}
paras = []          # (kind, start, end_without_newline, extra)
text_parts = []
pos = 1
tables = []
for kind, val in B:
    items = val if kind == "bullets" else [val]
    for j, it in enumerate(items):
        if kind == "table":
            s = "#"
            tables.append((pos, val))
        elif kind == "bullets":
            s = it[0] + it[1]
        else:
            s = it
        paras.append((kind, pos, pos + u16(s), dict(label=u16(it[0]) if kind == "bullets" else 0,
                                                     last=j == len(items) - 1)))
        text_parts.append(s)
        pos += u16(s) + 1
full = "\n".join(text_parts)
end = 1 + u16(full)
R = [{"insertText": {"location": {"index": 1, "tabId": TAB}, "text": full}},
     {"updateParagraphStyle": {"range": rng(1, end + 1), "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                               "fields": "namedStyleType"}},
     {"updateTextStyle": {"range": rng(1, end), "textStyle": {}, "fields": "bold,italic"}}]
for kind, a, b, x in paras:
    if kind == "h1":
        R.append({"updateParagraphStyle": {"range": rng(a, b + 1), "paragraphStyle": {"namedStyleType": "HEADING_1"},
                                           "fields": "namedStyleType"}})
i = 0
while i < len(paras):
    if paras[i][0] == "bullets":
        j = i
        while j + 1 < len(paras) and paras[j + 1][0] == "bullets" and not paras[j][3]["last"]:
            j += 1
        R.append({"createParagraphBullets": {"range": rng(paras[i][1], paras[j][2]),
                                             "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}})
        i = j + 1
    else:
        i += 1
for kind, a, b, x in paras:
    if kind == "bullets":
        R.append({"updateTextStyle": {"range": rng(a, a + x["label"]), "textStyle": {"bold": True}, "fields": "bold"}})
for kind, a, b, x in paras:
    if kind in ("p", "bullets"):
        sb = 8 if (kind == "p" or x["last"]) else 2
        R.append({"updateParagraphStyle": {"range": rng(a, b + 1),
                                           "paragraphStyle": {"spaceBelow": {"magnitude": sb, "unit": "PT"}},
                                           "fields": "spaceBelow"}})
# tables, last to first, each replacing its '#' placeholder paragraph
for p, rows in reversed(tables):
    nr, nc = len(rows), len(rows[0])
    R.append({"deleteContentRange": {"range": rng(p, p + 1)}})
    R.append({"insertTable": {"rows": nr, "columns": nc, "location": {"index": p, "tabId": TAB}}})
    cell = lambda r, c: p + 4 + r * (2 * nc + 1) + 2 * c
    for r in reversed(range(nr)):
        for c in reversed(range(nc)):
            R.append({"insertText": {"location": {"index": cell(r, c), "tabId": TAB}, "text": rows[r][c]}})
    off = 0
    for c in range(nc):
        a = cell(0, c) + off
        R.append({"updateTextStyle": {"range": rng(a, a + u16(rows[0][c])), "textStyle": {"bold": True},
                                      "fields": "bold"}})
        off += u16(rows[0][c])
    R.append({"updateTableCellStyle": {
        "tableRange": {"tableCellLocation": {"tableStartLocation": {"index": p + 1, "tabId": TAB},
                                             "rowIndex": 0, "columnIndex": 0}, "rowSpan": 1, "columnSpan": nc},
        "tableCellStyle": {"backgroundColor": {"color": {"rgbColor": {"red": 0.9098039, "green": 0.92941177,
                                                                      "blue": 0.96862745}}}},
        "fields": "backgroundColor"}})
json.dump({"requests": R, "writeControl": {"requiredRevisionId": REV}}, sys.stdout)
