"""Generates docs/diagrams/*.svg from a run trace (the committed one is source-trace.json).

    python3 -I docs/diagrams/generate.py . docs/diagrams/source-trace.json

Some labels (snapshot source counts, week 1 decision count) are typed in for that run.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

REPO, TRACE = Path(sys.argv[1]), Path(sys.argv[2])
OUT = REPO / "docs" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)

FONT = "-apple-system, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
INK, MUTED, LINE, BG = "#1b2430", "#5b6675", "#6f7a89", "#ffffff"
KIND = {  # fill, stroke
    "entry": ("#eef1f5", "#8e99a8"), "svc": ("#e7f0fb", "#3f78c0"), "port": ("#fff4df", "#c98a14"),
    "adp": ("#e6f4ea", "#3e8e5a"), "ext": ("#f1ecfa", "#7a5bb8"), "hot": ("#fde9e3", "#cf4f2f"),
    "review": ("#fbeeee", "#b8473f"), "plain": ("#ffffff", "#9aa5b4"), "note": ("#fffbea", "#d8c27a"),
}
HOT, BLUE, GREEN, RED = "#cf4f2f", "#3f78c0", "#3e8e5a", "#b8473f"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Svg:
    def __init__(self, w, h, label):
        self.w, self.h, self.label, self.parts, self.markers = w, h, label, [], set()

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill, stroke, rx=8, dash=None, sw=1.3):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=13, weight=400, fill=INK, anchor="start", mono=False, halo=False, italic=False):
        fam = MONO if mono else FONT
        h = ' stroke="#ffffff" stroke-width="4" stroke-linejoin="round" paint-order="stroke"' if halo else ""
        it = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}" xml:space="preserve"{h}{it}>{esc(s)}</text>')

    def box(self, x, y, w, h, title, lines=(), kind="svc", center=False, size=13.5, mono_title=False, line_size=12):
        fill, stroke = KIND[kind]
        self.rect(x, y, w, h, fill, stroke)
        tx, anc = (x + w / 2, "middle") if center else (x + 12, "start")
        n = 1 + len(lines)
        block = 17 + (n - 1) * 16
        ty = y + (h - block) / 2 + 13
        self.text(tx, ty, title, size=size, weight=650, anchor=anc, mono=mono_title)
        for i, l in enumerate(lines):
            self.text(tx, ty + 17 + i * 16, l, size=line_size, fill=MUTED, anchor=anc)

    def _marker(self, color, size=9):
        size = round(size)
        mid = f"a{color.lstrip('#')}-{size}"
        self.markers.add((mid, color, size))
        return mid

    def line(self, x1, y1, x2, y2, color=LINE, sw=1.5, dash=None, arrow=True):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{self._marker(color)})"' if arrow else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}{m}/>')

    def path(self, d, color=LINE, sw=1.5, dash=None, arrow=True, cap="round"):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{self._marker(color, max(9, sw * 2.2))})"' if arrow else ""
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="{cap}" '
                 f'stroke-linejoin="round"{da}{m}/>')

    def write(self, name):
        defs = "".join(
            f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{sz}" markerHeight="{sz}" '
            f'markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
            for mid, c, sz in sorted(self.markers))
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
               f'height="{self.h}" role="img" aria-label="{esc(self.label)}">\n<title>{esc(self.label)}</title>\n'
               f'<defs>{defs}</defs>\n<rect width="100%" height="100%" fill="{BG}"/>\n'
               + "\n".join(self.parts) + "\n</svg>\n")
        (OUT / name).write_text(svg)


# ---------------------------------------------------------------- 1. components
def components():
    W, H = 1310, 700
    s = Svg(W, H, "Components: the CLI calls services, services call ports only, adapters implement ports "
                  "and talk to Laya, Ollama, Bedrock and local disk; the container chooses adapters.")
    r = lambda i: 70 + i * 60
    RH = 46
    cols = [(20, 150, "Entry"), (230, 250, "Services"), (530, 200, "Ports  (ports.py)"),
            (780, 270, "Adapters"), (1100, 190, "Outside the process")]
    for x, w, t in cols:
        s.text(x, 40, t, size=14, weight=700)
    s.text(230, 56, "depend only on ports", size=11.5, fill=MUTED)

    ports = [("DecisionModel", ""), ("FallbackClassifier", ""), ("Extractor", ""),
             ("DecisionLog", "LabelRepository"), ("TextStore", "SnapshotStore"), ("GoldenSetRegistry", ""),
             ("Trainer", "ModelRegistry"), ("ReviewQueue", ""), ("Tracer", "")]
    adapters = [("LayaModel", "SimulatedLaya"), ("OllamaFallback", "BedrockFallback, SimulatedFallback"),
                ("SchemaExtractor x4", "sov, loss_run, acord, broker_email"),
                ("JsonlDecisionLog", "JsonlLabelRepository"), ("InMemoryTextStore", "FileSnapshotStore"),
                ("StaticGoldenSet", "golden-v1.jsonl"), ("ExportTrainer, LayaTrainer", "SimulatedTrainer, ModelRegistry"),
                ("InMemoryReviewQueue", ""), ("OtelTracer", "NullTracer")]
    for i, (p, p2) in enumerate(ports):
        s.box(530, r(i), 200, RH, p, [p2] if p2 else [], kind="port", mono_title=True, size=12.5)
        a, a2 = adapters[i]
        s.box(780, r(i), 270, RH, a, [a2] if a2 else [], kind="adp", size=13)
        s.line(780, r(i) + RH / 2, 733, r(i) + RH / 2, color=KIND["port"][1], dash="5 4")
    s.text(756, r(0) - 6, "implements", size=11, fill=KIND["port"][1], anchor="middle")

    # outside
    s.box(1100, r(0), 190, RH, "Hugging Face", ["convaiinnovations/laya"], kind="ext", size=13)
    s.box(1100, r(1), 190, RH, "Ollama", ["localhost:11434"], kind="ext", size=13)
    s.box(1100, r(2), 190, RH, "AWS Bedrock", ["Converse API"], kind="ext", size=13)
    dy, dh = r(3), r(8) + RH - r(3)
    s.rect(1100, dy, 190, dh, *KIND["ext"])
    s.text(1112, dy + 22, "Local disk", size=13.5, weight=650)
    for i, l in enumerate(["var/runs/<ts>/", "  decisions.jsonl", "  labels.jsonl", "  fcci/snapshots/.../",
                           "    manifest.json", "  eval.json", "  trace.json", "data/golden, data/production",
                           "models/<version>/", "  train.jsonl"]):
        s.text(1112, dy + 44 + i * 18, l, size=11.5, fill=MUTED, mono=True)
    s.line(1050, r(0) + 23, 1097, r(0) + 23)
    s.text(1074, r(0) + 16, "load", size=11, fill=MUTED, anchor="middle")
    s.line(1050, r(1) + 17, 1097, r(1) + 17)
    s.text(1074, r(1) + 10, "POST", size=11, fill=MUTED, anchor="middle")
    s.path(f"M1050,{r(1) + 31} C1075,{r(1) + 31} 1072,{r(2) + 23} 1097,{r(2) + 23}")
    for i, verb in [(3, "append"), (4, "write"), (5, "read"), (6, "export"), (8, "write")]:
        s.line(1050, r(i) + 23, 1097, r(i) + 23)
        s.text(1074, r(i) + 16, verb, size=11, fill=MUTED, anchor="middle")

    # services
    sx, sw = 230, 250
    s.box(sx, 70, sw, 156, "IntakeService", ["+ ExtractionRouter", "predict, gate, fallback,", "extract, label, review",
                                             "", "ports: DecisionModel, Fallback,", "Extractor, TextStore,",
                                             "ReviewQueue, Tracer"], kind="svc")
    s.box(sx, 270, sw, 100, "LabelStoreService", ["decision log, audit sample,", "labels with trust, snapshots",
                                                  "ports: DecisionLog, LabelRepository,",
                                                  "SnapshotStore, GoldenSetRegistry"], kind="svc")
    s.box(sx, 404, sw, 76, "TrainingPipeline", ["snapshot, eval, fine-tune,", "eval, promote"], kind="svc")
    s.box(sx, 524, sw, 52, "EvalService", ["+ PromotionPolicy, golden set"], kind="svc")
    s.box(sx, 600, sw, 52, "calibration", ["fit T and threshold on audits"], kind="svc")
    cx = sx + sw / 2
    s.line(cx, 226, cx, 267, color=BLUE)
    s.text(cx + 10, 251, "records decisions, labels", size=11, fill=BLUE)
    s.line(cx, 404, cx, 373, color=BLUE)
    s.text(cx + 10, 392, "build_snapshot", size=11, fill=BLUE)
    s.line(cx, 480, cx, 521, color=BLUE)
    s.text(cx + 10, 505, "evaluate", size=11, fill=BLUE)
    # services to the ports column: one bracket, the boundary that matters
    s.path("M480,148 L505,148", color=BLUE)
    s.path("M480,315 L505,315", color=BLUE)
    s.path("M480,442 L505,442", color=BLUE)
    s.path("M480,550 L505,550", color=BLUE)
    s.path("M507,70 L507,604", color=KIND["port"][1], sw=2.5, arrow=False)
    s.text(507, 616, "services call", size=11, fill=MUTED, anchor="middle")
    s.text(507, 630, "through ports only", size=11, fill=MUTED, anchor="middle")

    # entry
    s.box(20, 70, 150, 120, "cli.py", ["demo, eval", "classify, probe", "plays ops reviewer", "runs calibration"],
          kind="entry")
    s.box(20, 300, 150, 92, "container.py", ["composition root:", "the only place", "adapters are chosen"],
          kind="entry")
    s.line(170, 110, 227, 110, color=INK)
    s.text(199, 102, "process()", size=11, fill=INK, anchor="middle")
    s.path("M170,160 L200,160 L200,442 L227,442", color=INK)
    s.text(205, 436, "run()", size=11, fill=INK)
    s.path("M170,175 L188,175 L188,626 L227,626", color=INK)
    s.text(193, 620, "fit", size=11, fill=INK)
    s.path("M95,392 L95,684 L915,684 L915," + str(r(8) + RH + 3), color=KIND["adp"][1], sw=1.6)
    s.text(505, 678, "chooses one adapter per port from Settings (env, .env, CLI flags)", size=11.5,
           fill=KIND["adp"][1], anchor="middle", halo=True)
    s.line(95, 190, 95, 297, color=INK, arrow=True)
    s.text(103, 248, "build_app()", size=11, fill=INK)
    s.write("components.svg")


# ---------------------------------------------------------------- 2. run timeline
def timeline(T):
    t0 = datetime.fromisoformat(T["start"])
    off = lambda n: (datetime.fromisoformat(n["start"]) - t0).total_seconds()
    total = T["duration_ms"] / 1000
    W, H = 1120, 640
    x0, x1 = 170, 1090
    sc = (x1 - x0) / 32.0
    X = lambda t: x0 + t * sc
    s = Svg(W, H, f"Timeline of one real demo run: {total:.1f} s, of which the LLM fallback takes most; "
                  "calibration and training take under half a second.")
    s.text(20, 32, f"One demo run, {total:.1f} s  (Laya typed-decisions, fallback qwen3.8:27b-mlx, 28 documents)",
           size=14, weight=700)
    # axis
    for t in range(0, 33, 4):
        s.line(X(t), 52, X(t), 330, color="#e3e7ec", sw=1, arrow=False)
        s.text(X(t), 346, f"{t}s", size=11, fill=MUTED, anchor="middle")
    rows = {"demo": 64, "week": 104, "docs": 150, "other": 236}
    s.text(20, rows["demo"] + 17, "demo", size=12.5, weight=600, mono=True)
    s.rect(X(0), rows["demo"], X(total) - X(0), 24, *KIND["entry"], rx=4)
    s.text(20, rows["week"] + 17, "week", size=12.5, weight=600, mono=True)
    weeks = [c for c in T["children"] if c["name"] == "week"]
    for w in weeks:
        a, b = off(w), off(w) + w["duration_ms"] / 1000
        s.rect(X(a), rows["week"], X(b) - X(a), 24, *KIND["svc"], rx=4)
        s.text((X(a) + X(b)) / 2, rows["week"] + 17, f'{w["attributes"]["week"]}: {w["attributes"]["documents"]} documents',
               size=11.5, anchor="middle")
    s.text(20, rows["docs"] + 14, "intake.document", size=12.5, weight=600, mono=True)
    s.text(20, rows["docs"] + 31, "one block each", size=11, fill=MUTED)
    fb_total = pr_total = 0
    for w in weeks:
        for d in [c for c in w["children"] if c["name"] == "intake.document"]:
            a = off(d)
            dur = d["duration_ms"] / 1000
            kids = {c["name"]: c for c in d["children"]}
            pr = kids["model.predict"]["duration_ms"] / 1000
            fb = kids["fallback.classify"]["duration_ms"] / 1000 if "fallback.classify" in kids else 0
            fb_total += fb
            pr_total += pr
            s.rect(X(a), rows["docs"], max(X(a + dur) - X(a), 1), 56, "#eef1f5", "#ffffff", rx=0, sw=1)
            s.rect(X(a), rows["docs"], max(X(a + pr) - X(a), 1.2), 56, BLUE, "#ffffff", rx=0, sw=0.6)
            if fb:
                fa = off(kids["fallback.classify"])
                s.rect(X(fa), rows["docs"], max(X(fa + fb) - X(fa), 1.2), 56, HOT, "#ffffff", rx=0, sw=0.6)
    first = weeks[0]["children"][0]
    ffb = [c for c in first["children"] if c["name"] == "fallback.classify"][0]["duration_ms"] / 1000
    s.text(X(0) + 4, rows["docs"] + 78, f"first fallback call {ffb:.1f} s: model loads into memory", size=11.5, fill=HOT)
    s.line(X(0) + 60, rows["docs"] + 66, X(0) + 60, rows["docs"] + 59, color=HOT, sw=1.2)
    # the brief middle section, zoomed
    mid = [c for c in T["children"] if c["name"] in ("calibration", "training.run")]
    ops1 = [c for c in weeks[0]["children"] if c["name"] == "ops.review"][0]
    za, zb = off(ops1), off(weeks[1])
    s.text(20, rows["other"] + 17, "between weeks", size=12.5, weight=600)
    s.rect(X(za) - 1, rows["other"], max(X(zb) - X(za), 3) + 2, 24, "#ffffff", INK, rx=2, sw=1.2)
    zy, zx0, zx1 = 380, 170, 1090
    s.path(f"M{X(za) - 1},{rows['other'] + 24} L{zx0},{zy}", color="#9aa5b4", sw=1, arrow=False, dash="3 3")
    s.path(f"M{X(zb) + 1},{rows['other'] + 24} L{zx1},{zy}", color="#9aa5b4", sw=1, arrow=False, dash="3 3")
    tr = [c for c in T["children"] if c["name"] == "training.run"][0]
    items = [(ops1, "review")] + [(c, "svc") for c in mid] + [(c, "adp") for c in tr["children"]]
    s.rect(zx0, zy, zx1 - zx0, 48 + 30 * len(items), "#fbfcfd", "#9aa5b4", rx=6, sw=1)
    zs = (zx1 - zx0 - 40) / (zb - za)
    Z = lambda t: zx0 + 20 + (t - za) * zs
    s.text(zx0 + 12, zy + 22, f"zoom: {za:.2f} s to {zb:.2f} s  ({(zb - za) * 1000:.0f} ms)", size=12, weight=600)
    for i, (n, kind) in enumerate(items):
        a, b = off(n), off(n) + n["duration_ms"] / 1000
        y = zy + 36 + i * 30
        indent = "  " if kind == "adp" else ""
        s.text(zx0 - 8, y + 15, indent + n["name"], size=11.5, anchor="end", mono=True)
        wpx = max(Z(b) - Z(a), 3)
        s.rect(Z(a), y, wpx, 20, *KIND[kind], rx=3)
        lbl = f"{n['duration_ms']:.0f} ms" if n["duration_ms"] >= 1 else f"{n['duration_ms']:.1f} ms"
        if wpx > 80:
            s.text(Z(a) + wpx / 2, y + 14, lbl, size=11, anchor="middle")
        elif Z(b) > zx1 - 90:
            s.text(Z(a) - 6, y + 14, lbl, size=11, anchor="end", fill=MUTED)
        else:
            s.text(Z(b) + 6, y + 14, lbl, size=11, fill=MUTED)
    # legend and totals
    ly = 625
    s.rect(20, ly - 11, 12, 12, BLUE, BLUE, rx=2)
    s.text(38, ly, f"model.predict (Laya): {pr_total:.1f} s", size=12)
    s.rect(270, ly - 11, 12, 12, HOT, HOT, rx=2)
    s.text(288, ly, f"fallback.classify (Ollama): {fb_total:.1f} s, {fb_total / total:.0%} of the run", size=12)
    s.rect(640, ly - 11, 12, 12, "#eef1f5", "#9aa5b4", rx=2)
    s.text(658, ly, "gate, extract, review: under 20 ms in total", size=12)
    s.write("run-timeline.svg")


# ---------------------------------------------------------------- 3. one document, sequence
def sequence():
    W, H = 1130, 850
    s = Svg(W, H, "Sequence for one document: Laya predicts, the gate logs the decision, an optional audit is queued, "
                  "then either Laya's type or the LLM fallback's type goes to extraction or review.")
    L = {"Intake": 200, "Laya": 365, "Store": 530, "Review": 695, "Fallback": 860, "Extract": 1030}
    heads = [("Intake", "IntakeService", "svc"), ("Laya", "DecisionModel", "adp"), ("Store", "LabelStore", "svc"),
             ("Review", "ReviewQueue", "review"), ("Fallback", "FallbackClassifier", "hot"),
             ("Extract", "ExtractionRouter", "svc")]
    subs = {"Laya": "LayaModel", "Fallback": "Ollama / Bedrock", "Extract": "SchemaExtractor x4",
            "Intake": "process(doc)", "Store": "LabelStoreService", "Review": "ops picks up"}
    for k, t, kind in heads:
        s.box(L[k] - 78, 20, 156, 46, t, [subs[k]], kind=kind, center=True, size=13)
        s.line(L[k], 66, L[k], H - 20, color="#c3cad3", sw=1.2, dash="4 4", arrow=False)
    s.text(20, 46, "span in", size=11, fill=MUTED)
    s.text(20, 60, "trace.json", size=11, fill=MUTED)

    def tag(y, name):
        s.rect(14, y - 13, 112, 20, "#f5f7fa", "#c3cad3", rx=10, sw=1)
        s.text(70, y + 1, name, size=11, anchor="middle", mono=True)

    def msg(y, a, b, label, ret=False, color=INK, span=None):
        xa, xb = L[a], L[b]
        sgn = 1 if xb > xa else -1
        s.line(xa, y, xb - sgn * 2, y, color=color if not ret else MUTED, sw=1.5, dash="5 4" if ret else None)
        s.text((xa + xb) / 2, y - 7, label, size=12, anchor="middle", halo=True, fill=color if not ret else MUTED,
               mono=not ret and "(" in label)
        if span:
            tag(y, span)

    def frame(y0, y1, op, guard, x0=150, x1=1100, dividers=()):
        s.rect(x0, y0, x1 - x0, y1 - y0, "none", "#8e99a8", rx=4, sw=1.1)
        s.add(f'<path d="M{x0},{y0 + 20} L{x0 + 44},{y0 + 20} L{x0 + 52},{y0 + 12} L{x0 + 52},{y0}" '
              f'fill="#eef1f5" stroke="#8e99a8" stroke-width="1.1"/>')
        s.text(x0 + 7, y0 + 15, op, size=11.5, weight=700)
        s.text(x0 + 60, y0 + 15, guard, size=11.5, fill=MUTED, italic=True)
        for dy, g in dividers:
            s.line(x0, dy, x1, dy, color="#8e99a8", sw=1, dash="6 4", arrow=False)
            s.text(x0 + 60, dy + 15, g, size=11.5, fill=MUTED, italic=True)

    msg(105, "Intake", "Laya", "predict(text)", span="model.predict")
    msg(138, "Laya", "Intake", "probabilities over 5 types", ret=True)
    msg(183, "Intake", "Store", "record_decision(p, threshold)", span="gate")
    s.rect(548, 160, 300, 64, *KIND["note"], rx=4, sw=1)
    for i, l in enumerate(["append to decisions.jsonl, before routing", "route = auto if max p >= threshold",
                           "audited = random() < audit_rate"]):
        s.text(560, 178 + i * 17, l, size=11.5, fill=INK)
    msg(246, "Store", "Intake", "Decision(route, audited)", ret=True)

    frame(268, 330, "opt", "[audited]")
    msg(310, "Intake", "Review", 'push("audit sample")', span="review.queue")

    frame(348, 530, "alt", "[route = auto]", dividers=[(410, "[route = fallback]")])
    s.path(f"M{L['Intake']},378 L{L['Intake'] + 40},378 L{L['Intake'] + 40},394 L{L['Intake'] + 3},394")
    s.text(L["Intake"] + 48, 390, "type = Laya's choice", size=12, fill=INK)
    msg(448, "Intake", "Fallback", "classify(text)", color=HOT, span="fallback.classify")
    msg(478, "Fallback", "Intake", "doc_type", ret=True)
    msg(512, "Intake", "Store", "add_label(LLM_FALLBACK)", color=INK)

    frame(548, 830, "alt", "[type = other]", dividers=[(610, "[typed]")])
    msg(590, "Intake", "Review", 'push("typed as other")', span="review.queue")
    msg(650, "Intake", "Extract", "extract(doc, type)", span="extract")
    msg(682, "Extract", "Intake", "accepted, or another extractor's type, or none", ret=True)
    frame(700, 755, "opt", "[another extractor accepted]", x0=170, x1=1080)
    msg(740, "Intake", "Store", "add_label(DOWNSTREAM)")
    frame(765, 820, "opt", "[nothing accepted]", x0=170, x1=1080)
    msg(805, "Intake", "Review", 'push("no extractor accepted")', span="review.queue")
    s.write("intake-sequence.svg")


# ---------------------------------------------------------------- 4. routes with counts
def routes(T):
    docs = [d for w in T["children"] if w["name"] == "week" for d in w["children"] if d["name"] == "intake.document"]
    kid = lambda d, n: [c for c in d["children"] if c["name"] == n]
    n = len(docs)
    audited = sum(any(c["attributes"]["reason"] == "audit sample" for c in kid(d, "review.queue")) for d in docs)
    auto = sum(kid(d, "gate")[0]["attributes"]["route"] == "auto" for d in docs)
    fb = n - auto
    other = sum(d["attributes"]["final_type"] == "none" and not kid(d, "extract") for d in docs)
    ext = sum(bool(kid(d, "extract")) for d in docs)
    ok = sum(any(c["attributes"]["ok"] for c in kid(d, "extract")) for d in docs)
    rec = sum(any(c["attributes"].get("recovered_type") for c in kid(d, "extract")) for d in docs)
    none = ext - ok - rec
    W, H = 1180, 520
    s = Svg(W, H, f"Routes taken by the {n} documents of a real run: {audited} audited, {auto} auto-routed, "
                  f"{fb} sent to the LLM fallback, {other} typed as other, {ok} extracted.")
    s.text(20, 32, f"Where the {n} documents went  (real run; line width = number of documents)", size=14, weight=700)
    sw = lambda k: 1.4 + 11 * k / n

    def edge(d, k, lx, ly, color=INK, anchor="middle"):
        s.path(d, color=color if k else "#9aa5b4", sw=sw(k), dash=None if k else "5 4", cap="butt")
        s.text(lx, ly, str(k), size=12.5, weight=700, fill=color if k else "#9aa5b4", anchor=anchor, halo=True)

    s.box(20, 205, 130, 56, f"{n} documents", ["week1 + week2"], kind="entry", center=True)
    s.box(200, 205, 170, 56, "model.predict + gate", ["decision logged"], kind="svc", center=True)
    edge("M150,233 L196,233", n, 173, 225)
    # audit branch
    s.box(420, 60, 180, 56, "review.queue", ["audit sample, for ops"], kind="review", center=True)
    edge("M300,205 C300,140 340,88 416,88", audited, 330, 120, color=RED)
    s.text(372, 150, "random 25%,", size=11, fill=MUTED)
    s.text(372, 164, "either route", size=11, fill=MUTED)
    # gate diamond
    cx, cy = 505, 233
    s.add(f'<polygon points="{cx - 70},{cy} {cx},{cy - 38} {cx + 70},{cy} {cx},{cy + 38}" fill="#ffffff" stroke="{INK}" stroke-width="1.3"/>')
    s.text(cx, cy - 2, "max p", size=12, anchor="middle", weight=600)
    s.text(cx, cy + 14, ">= 0.85 ?", size=12, anchor="middle", weight=600)
    edge("M370,233 L431,233", n, 400, 225)
    s.box(640, 140, 180, 56, "auto", ["type = Laya's choice"], kind="adp", center=True)
    edge(f"M{cx},{cy - 38} C{cx},170 560,168 636,168", auto, 585, 160, color=GREEN)
    s.text(612, 132, "yes", size=11, fill=MUTED)
    s.box(640, 250, 180, 56, "fallback.classify", ["LLM types it"], kind="hot", center=True)
    edge(f"M{cx + 70},{cy} C600,233 600,278 636,278", fb, 600, 262, color=HOT)
    s.text(590, 300, "no", size=11, fill=MUTED)
    s.text(730, 330, "every document: confidences", size=11, fill=HOT, anchor="middle")
    s.text(730, 344, "ran 0.26 to 0.72", size=11, fill=HOT, anchor="middle")
    # other?
    gx, gy = 925, 233
    s.add(f'<polygon points="{gx - 62},{gy} {gx},{gy - 34} {gx + 62},{gy} {gx},{gy + 34}" fill="#ffffff" stroke="{INK}" stroke-width="1.3"/>')
    s.text(gx, gy - 2, "type =", size=12, anchor="middle", weight=600)
    s.text(gx, gy + 14, "other ?", size=12, anchor="middle", weight=600)
    edge(f"M820,168 C845,168 845,224 860,228", auto, 848, 186, color=GREEN)
    edge(f"M820,278 C845,278 845,240 860,238", fb, 848, 268, color=HOT)
    s.box(990, 60, 175, 56, "review.queue", ["typed as other"], kind="review", center=True)
    edge(f"M{gx},{gy - 34} C{gx},130 940,88 986,88", other, 942, 150, color=RED)
    s.box(1000, 205, 165, 56, "extract", ["typed extractor"], kind="svc", center=True)
    edge(f"M{gx + 62},{gy} L996,{gy}", ext, 975, 225)
    # extraction outcomes
    oy = 400
    s.box(1000, oy, 165, 56, "accepted", ["typed, fields out"], kind="adp", center=True)
    s.box(810, oy, 170, 56, "another accepts", ["DOWNSTREAM label"], kind="svc", center=True)
    s.box(620, oy, 170, 56, "none accepts", ["review.queue"], kind="review", center=True)
    edge(f"M1082,261 L1082,{oy - 4}", ok, 1094, 335, anchor="start")
    edge(f"M1040,261 C1040,330 895,330 895,{oy - 4}", rec, 960, 322)
    edge(f"M1020,261 C1020,350 705,320 705,{oy - 4}", none, 760, 345)
    s.text(20, 500, "Dashed grey: no documents took that route in this run. The simulated model auto-routes 10 of 28.",
           size=12, fill=MUTED)
    s.write("routes.svg")


# ---------------------------------------------------------------- 5. labels and trust
def labels():
    W, H = 1180, 430
    s = Svg(W, H, "Label trust tiers: HUMAN 1.0, DOWNSTREAM 0.7, LLM_FALLBACK 0.4, encoded as soft training "
                  "targets; the highest tier wins and disagreement below HUMAN drops the label.")
    s.text(20, 32, "Labels: where they come from, how much they count, how conflicts resolve", size=14, weight=700)
    s.text(20, 62, "source", size=12, weight=650, fill=MUTED)
    s.text(380, 62, "training target (soft gold over 5 types)", size=12, weight=650, fill=MUTED)
    s.text(640, 62, "in this run's", size=12, weight=650, fill=MUTED)
    s.text(640, 76, "snapshot", size=12, weight=650, fill=MUTED)
    tiers = [("HUMAN", "ops.review: audit sample, typed as", "other, no extractor accepted", 1.0, 7, "review"),
             ("DOWNSTREAM", "extract: another extractor's", "schema accepted the document", 0.7, 0, "svc"),
             ("LLM_FALLBACK", "fallback.classify: the LLM's", "answer for a low-confidence doc", 0.4, 11, "hot")]
    for i, (name, l1, l2, w, cnt, kind) in enumerate(tiers):
        y = 92 + i * 96
        s.box(20, y, 330, 76, name, [l1, l2], kind=kind, mono_title=True)
        bars = [w] + [(1 - w) / 4] * 4
        for j, b in enumerate(bars):
            bx = 384 + j * 44
            bh = 60 * b
            s.rect(bx, y + 66 - bh, 30, max(bh, 1), KIND[kind][1] if j == 0 else "#c3cad3", "none", rx=2, sw=0)
            s.text(bx + 15, y + 66 - bh - 5, f"{b:.2f}".rstrip("0").rstrip(".") if b else "0", size=10.5,
                   anchor="middle", fill=MUTED)
        s.text(384 + 15, y + 80, "label", size=10.5, anchor="middle", fill=MUTED)
        s.text(384 + 2 * 44 + 37, y + 80, "the other four", size=10.5, anchor="middle", fill=MUTED)
        s.text(660, y + 46, str(cnt), size=22, weight=700, anchor="middle", fill=INK if cnt else "#9aa5b4")
    s.line(18, 380, 18, 96, color=INK, sw=1.3)
    s.text(26, 404, "more trusted upward", size=11.5, fill=MUTED)
    # resolution examples
    rx0 = 730
    s.text(rx0, 62, "resolve(decision): worked cases", size=12, weight=650, fill=MUTED)

    def chip(x, y, src, t, kind):
        w = 22 + 7.2 * (len(src) + len(t) + 1)
        s.rect(x, y, w, 24, *KIND[kind], rx=12, sw=1)
        s.text(x + 11, y + 16, f"{src} {t}", size=11.5, mono=True)
        return x + w + 6

    cases = [([("HUMAN", "sov", "review"), ("LLM", "acord", "hot")], "sov", "highest tier wins"),
             ([("DOWNSTREAM", "loss_run", "svc"), ("LLM", "sov", "hot")], "loss_run", "highest tier wins"),
             ([("LLM", "sov", "hot"), ("LLM", "acord", "hot")], "no label", "disagree below HUMAN:"),
             ([("LLM", "sov", "hot")], "sov", "weight 0.4")]
    for i, (chips, out, why) in enumerate(cases):
        y = 92 + i * 72
        x = rx0
        for src, t, kind in chips:
            x = chip(x, y, src, t, kind)
        s.line(x + 4, y + 12, x + 40, y + 12, color=INK)
        s.text(x + 48, y + 17, out, size=13, weight=700, fill=RED if out == "no label" else INK, mono=out != "no label")
        s.text(rx0, y + 44, why + (" to review, not training" if out == "no label" else ""), size=11.5, fill=MUTED)
    s.write("labels.svg")


# ---------------------------------------------------------------- 6. training run
def training(T):
    tr = [c for c in T["children"] if c["name"] == "training.run"][0]
    k = {c["name"]: c["attributes"] for c in tr["children"]}
    snap, ev = k["snapshot.build"], k["eval.current"]
    W, H = 1240, 470
    s = Svg(W, H, "Training run: snapshot excludes golden documents, the current model is evaluated on the golden set, "
                  "the trainer either exports data or returns a candidate that must pass the promotion gate.")
    s.text(20, 32, "training.run  (real run values; the export trainer stops after exporting)", size=14, weight=700)
    y = 70
    s.box(20, y, 190, 120, "LabelStore", ["week1: 20 decisions", "with labels from", "fallback and ops"], kind="svc")
    s.box(260, y, 230, 120, "snapshot.build", [f"- {snap['excluded.golden']} golden hash",
                                               f"- {snap['excluded.template']} golden template group",
                                               f"- {snap['excluded.conflict']} conflicts, {snap['excluded.below_floor']} below floor",
                                               f"= {snap['examples']} examples (11 LLM, 7 HUMAN)"], kind="svc", mono_title=True)
    s.line(210, y + 60, 256, y + 60, color=BLUE)
    s.box(540, y, 210, 120, "eval.current", [f"{ev['golden_version']}, {ev['n']} docs",
                                             f"accuracy {ev['accuracy']:.2f}", f"ECE {ev['ece']:.2f}",
                                             f"coverage@0.85 {ev['coverage']:.2f}"], kind="svc", mono_title=True)
    s.line(490, y + 60, 536, y + 60, color=BLUE)
    s.text(513, y + 52, "manifest", size=10.5, fill=MUTED, anchor="middle")
    s.box(800, y, 190, 120, "trainer.fine_tune", ["base: current model", "trainer: " + k["trainer.fine_tune"]["trainer"]],
          kind="adp", mono_title=True)
    s.line(750, y + 60, 796, y + 60, color=BLUE)
    s.box(1040, y, 180, 120, "ExportTrainer", ["writes models/", "candidate-v2/", "train.jsonl", "no candidate"],
          kind="note")
    s.line(990, y + 60, 1036, y + 60, color=INK)
    s.text(1013, y + 52, "this run", size=10.5, fill=INK, anchor="middle")
    s.text(1130, y + 146, "stops: promoted = false", size=12, weight=650, fill=RED, anchor="middle")
    # candidate branch
    y2 = 300
    s.path(f"M895,{y + 120} L895,{y2 - 4}", color=INK)
    s.text(905, 250, "LayaTrainer or SimulatedTrainer:", size=11.5, fill=INK)
    s.text(905, 266, "returns a candidate model", size=11.5, fill=INK)
    s.box(800, y2, 190, 120, "eval.candidate", ["same golden set,", "same threshold"], kind="svc", mono_title=True)
    s.box(480, y2, 270, 120, "promotion.decide", ["accuracy not lower", "no class recall drop > 0.05",
                                                  "ECE rise <= 0.02", "(PromotionPolicy)"], kind="port", mono_title=True)
    s.line(800, y2 + 60, 754, y2 + 60, color=INK)
    s.box(250, y2, 180, 52, "promote", ["registry points at it"], kind="adp")
    s.box(250, y2 + 68, 180, 52, "keep current", ["reasons recorded"], kind="review")
    s.path(f"M480,{y2 + 40} L434,{y2 + 26}", color=GREEN)
    s.text(457, y2 + 22, "pass", size=11, fill=GREEN, anchor="middle")
    s.path(f"M480,{y2 + 80} L434,{y2 + 94}", color=RED)
    s.text(457, y2 + 106, "fail", size=11, fill=RED, anchor="middle")
    s.text(20, 330, "The golden set is the exam:", size=12, weight=650)
    s.text(20, 348, "never in a snapshot, never", size=12, fill=MUTED)
    s.text(20, 366, "used to fit temperature", size=12, fill=MUTED)
    s.text(20, 384, "or threshold.", size=12, fill=MUTED)
    s.write("training.svg")


T = json.load(open(TRACE))[0]
components()
timeline(T)
sequence()
routes(T)
labels()
training(T)
print("wrote", sorted(p.name for p in OUT.iterdir()))
