#!/usr/bin/env python3
"""
Builds the EduLink SL flowchart as a real diagrams.net (draw.io) file --
diagrams/EduLink.drawio -- containing five pages (one per figure, split
for print legibility), and renders each page to a high-resolution PNG for
embedding in the Word report, from ONE shared layout definition so the
.drawio file and the report images always match.

diagrams.net (Draw.io) is one of the three flowchart tools explicitly
allowed by the PROG101 assignment brief (Section 2.III).
"""
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon, FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patheffects as pe

# ---------------------------------------------------------------- colors --
COL = {
    "terminator": ("#d5e8d4", "#82b366"),  # green
    "process":    ("#dae8fc", "#6c8ebf"),  # blue
    "decision":   ("#fff2cc", "#d6b656"),  # yellow
    "subroutine": ("#ffe6cc", "#d79b00"),  # orange
}
EDGE_COLOR = "#333333"
FONT = "DejaVu Sans"
SCALE = 100  # 1 inch (matplotlib unit) == 100 px in the .drawio file

# ============================================================== DATA ======
# Each diagram: id, name (drawio page name / figure title), size (w,h in
# inches), nodes [{id,kind,text,x,y,w,h}] (x,y = CENTER, inches, y grows
# downward), edges [{src,dst,label,pts,src_side,dst_side,lx,ly}]
# pts = explicit polyline waypoints (inches) for the matplotlib render;
# src_side/dst_side = exit/entry side for the drawio orthogonal edge.

diagrams = []

# ---------------------------------------------------------- FIG 1 --------
W, H = 11.5, 7.3
nodes = [
    dict(id="n1", kind="terminator", text="Start",                         x=5.75, y=0.55, w=2.0, h=0.6),
    dict(id="n2", kind="process",    text="Display Main Menu",             x=5.75, y=1.65, w=3.0, h=0.7),
    dict(id="n3", kind="decision",   text="User Selection",                x=5.75, y=3.05, w=3.2, h=1.1),
    dict(id="n4", kind="subroutine", text="1. Check Tutor Availability\n— see Figure 2",  x=1.45,  y=4.75, w=2.5, h=1.0),
    dict(id="n5", kind="subroutine", text="2. Check Material Stock\n— see Figure 3",      x=4.15,  y=4.75, w=2.5, h=1.0),
    dict(id="n6", kind="subroutine", text="3. Book Tutoring Session\n— see Figure 4",     x=6.85,  y=4.75, w=2.5, h=1.0),
    dict(id="n7", kind="subroutine", text="4. Report Disruption\n— see Figure 5",         x=9.55,  y=4.75, w=2.5, h=1.0),
    dict(id="n8", kind="terminator", text="End",                           x=5.75, y=6.6, w=2.0, h=0.6),
]
edges = [
    dict(src="n1", dst="n2", label=None, pts=[(5.75,0.85),(5.75,1.3)], src_side="bottom", dst_side="top"),
    dict(src="n2", dst="n3", label=None, pts=[(5.75,2.0),(5.75,2.5)], src_side="bottom", dst_side="top"),
    dict(src="n3", dst="n4", label="1", pts=[(4.6,3.3),(1.45,3.3),(1.45,4.25)], src_side="left", dst_side="top"),
    dict(src="n3", dst="n5", label="2", pts=[(5.3,3.6),(4.15,3.6),(4.15,4.25)], src_side="left", dst_side="top"),
    dict(src="n3", dst="n6", label="3", pts=[(6.2,3.6),(6.85,3.6),(6.85,4.25)], src_side="right", dst_side="top"),
    dict(src="n3", dst="n7", label="4", pts=[(6.9,3.3),(9.55,3.3),(9.55,4.25)], src_side="right", dst_side="top"),
    dict(src="n3", dst="n2", label="Invalid option", pts=[(7.35,3.05),(10.6,3.05),(10.6,1.65),(7.25,1.65)], src_side="right", dst_side="right"),
    dict(src="n4", dst="n8", label=None, pts=[(1.45,5.25),(1.45,6.6),(4.75,6.6)], src_side="bottom", dst_side="left"),
    dict(src="n5", dst="n8", label=None, pts=[(4.15,5.25),(4.15,6.0),(5.75,6.0),(5.75,6.3)], src_side="bottom", dst_side="top"),
    dict(src="n6", dst="n8", label=None, pts=[(6.85,5.25),(6.85,6.0),(5.75,6.0),(5.75,6.3)], src_side="bottom", dst_side="top"),
    dict(src="n7", dst="n8", label=None, pts=[(9.55,5.25),(9.55,6.6),(6.75,6.6)], src_side="bottom", dst_side="right"),
]
diagrams.append(dict(id="fig1", name="Figure 1 - System Overview (Main Menu)", w=W, h=H, nodes=nodes, edges=edges))

# ---------------------------------------------------------- FIG 2 --------
W, H = 8.2, 7.0
nodes = [
    dict(id="n1", kind="terminator", text="Start: Check Tutor\nAvailability",              x=3.9, y=0.55, w=3.0, h=0.7),
    dict(id="n2", kind="process",    text="Get student location\nand subject needed",      x=3.9, y=1.75, w=3.0, h=0.7),
    dict(id="n3", kind="decision",   text="Centre found within radius with\ntutor on duty and open seat?", x=3.9, y=3.25, w=3.6, h=1.3),
    dict(id="n4", kind="process",    text="Increase search radius",                        x=6.9, y=3.25, w=2.3, h=0.8),
    dict(id="n5", kind="process",    text="Display centre name\nand open seats",            x=2.1, y=5.1, w=2.6, h=0.9),
    dict(id="n6", kind="process",    text="Display: No availability\nfound nearby",         x=5.7, y=5.1, w=2.6, h=0.9),
    dict(id="n7", kind="terminator", text="Log interaction and End",                       x=3.9, y=6.5, w=3.2, h=0.7),
]
edges = [
    dict(src="n1", dst="n2", label=None, pts=[(3.9,0.9),(3.9,1.4)], src_side="bottom", dst_side="top"),
    dict(src="n2", dst="n3", label=None, pts=[(3.9,2.1),(3.9,2.6)], src_side="bottom", dst_side="top"),
    dict(src="n3", dst="n4", label="No — radius < max", pts=[(5.7,3.25),(5.75,3.25)], src_side="right", dst_side="left"),
    dict(src="n4", dst="n3", label=None, pts=[(6.9,2.85),(6.9,2.2),(3.9,2.2),(3.9,2.6)], src_side="top", dst_side="top"),
    dict(src="n3", dst="n5", label="Yes", pts=[(3.3,3.9),(2.1,3.9),(2.1,4.65)], src_side="left", dst_side="top"),
    dict(src="n3", dst="n6", label="No — max radius reached", pts=[(4.5,3.9),(5.7,3.9),(5.7,4.65)], src_side="right", dst_side="top"),
    dict(src="n5", dst="n7", label=None, pts=[(2.1,5.55),(2.1,6.5),(2.3,6.5)], src_side="bottom", dst_side="left"),
    dict(src="n6", dst="n7", label=None, pts=[(5.7,5.55),(5.7,6.5),(5.5,6.5)], src_side="bottom", dst_side="right"),
]
diagrams.append(dict(id="fig2", name="Figure 2 - Check Tutor Availability", w=W, h=H, nodes=nodes, edges=edges))

# ---------------------------------------------------------- FIG 3 --------
W, H = 7.8, 8.2
nodes = [
    dict(id="n1", kind="terminator", text="Start: Check Material Stock",                    x=3.9, y=0.55, w=3.4, h=0.7),
    dict(id="n2", kind="process",    text="Get material name\nand student location",        x=3.9, y=1.75, w=3.2, h=0.9),
    dict(id="n3", kind="process",    text="Search nearby centres'\nstock records",          x=3.9, y=3.1, w=3.2, h=0.9),
    dict(id="n4", kind="decision",   text="Material in stock\nat any centre?",              x=3.9, y=4.7, w=3.0, h=1.1),
    dict(id="n5", kind="process",    text="Display every centre\nthat has it in stock",     x=2.1, y=6.3, w=2.7, h=0.9),
    dict(id="n6", kind="process",    text="Display: Not currently\nin stock nearby",         x=5.7, y=6.3, w=2.7, h=0.9),
    dict(id="n7", kind="terminator", text="Log interaction and End",                       x=3.9, y=7.7, w=3.2, h=0.7),
]
edges = [
    dict(src="n1", dst="n2", label=None, pts=[(3.9,0.9),(3.9,1.3)], src_side="bottom", dst_side="top"),
    dict(src="n2", dst="n3", label=None, pts=[(3.9,2.2),(3.9,2.65)], src_side="bottom", dst_side="top"),
    dict(src="n3", dst="n4", label=None, pts=[(3.9,3.55),(3.9,4.15)], src_side="bottom", dst_side="top"),
    dict(src="n4", dst="n5", label="Yes", pts=[(3.3,5.2),(2.1,5.2),(2.1,5.85)], src_side="left", dst_side="top"),
    dict(src="n4", dst="n6", label="No", pts=[(4.5,5.2),(5.7,5.2),(5.7,5.85)], src_side="right", dst_side="top"),
    dict(src="n5", dst="n7", label=None, pts=[(2.1,6.75),(2.1,7.7),(2.3,7.7)], src_side="bottom", dst_side="left"),
    dict(src="n6", dst="n7", label=None, pts=[(5.7,6.75),(5.7,7.7),(5.5,7.7)], src_side="bottom", dst_side="right"),
]
diagrams.append(dict(id="fig3", name="Figure 3 - Check Study Material Stock", w=W, h=H, nodes=nodes, edges=edges))

# ---------------------------------------------------------- FIG 4 --------
W, H = 8.2, 10.6
nodes = [
    dict(id="n1", kind="terminator", text="Start: Book Tutoring Session",                  x=4.1, y=0.55, w=3.2, h=0.7),
    dict(id="n2", kind="process",    text="Get student phone number",                      x=4.1, y=1.7, w=3.2, h=0.7),
    dict(id="n3", kind="decision",   text="Student already\nregistered?",                  x=4.1, y=3.0, w=3.0, h=1.1),
    dict(id="n4", kind="process",    text="Register new student",                          x=1.7, y=4.5, w=2.6, h=0.8),
    dict(id="n5", kind="process",    text="Get preferred centre and date",                 x=4.1, y=5.8, w=3.3, h=0.8),
    dict(id="n6", kind="decision",   text="Seat available\non that date?",                 x=4.1, y=7.2, w=3.0, h=1.1),
    dict(id="n7", kind="process",    text="Confirm booking, reduce open\nseats, send SMS confirmation", x=2.2, y=8.9, w=3.1, h=1.0),
    dict(id="n8", kind="process",    text="Suggest next\navailable date",                   x=6.1, y=8.9, w=2.6, h=1.0),
    dict(id="n9", kind="terminator", text="Log interaction and End",                       x=4.1, y=10.2, w=3.2, h=0.7),
]
edges = [
    dict(src="n1", dst="n2", label=None, pts=[(4.1,0.9),(4.1,1.35)], src_side="bottom", dst_side="top"),
    dict(src="n2", dst="n3", label=None, pts=[(4.1,2.05),(4.1,2.45)], src_side="bottom", dst_side="top"),
    dict(src="n3", dst="n4", label="No", pts=[(3.2,3.35),(1.7,3.35),(1.7,4.1)], src_side="left", dst_side="top"),
    dict(src="n3", dst="n5", label="Yes", pts=[(5.0,3.35),(6.4,3.35),(6.4,5.8),(5.75,5.8)], src_side="right", dst_side="right"),
    dict(src="n4", dst="n5", label=None, pts=[(1.7,4.9),(1.7,5.8),(2.45,5.8)], src_side="bottom", dst_side="left"),
    dict(src="n5", dst="n6", label=None, pts=[(4.1,6.2),(4.1,6.65)], src_side="bottom", dst_side="top"),
    dict(src="n6", dst="n7", label="Yes", pts=[(3.4,7.9),(2.2,7.9),(2.2,8.4)], src_side="left", dst_side="top"),
    dict(src="n6", dst="n8", label="No", pts=[(4.8,7.9),(6.1,7.9),(6.1,8.4)], src_side="right", dst_side="top"),
    dict(src="n7", dst="n9", label=None, pts=[(2.2,9.4),(2.2,10.2),(2.5,10.2)], src_side="bottom", dst_side="left"),
    dict(src="n8", dst="n9", label=None, pts=[(6.1,9.4),(6.1,10.2),(5.7,10.2)], src_side="bottom", dst_side="right"),
]
diagrams.append(dict(id="fig4", name="Figure 4 - Book Tutoring Session", w=W, h=H, nodes=nodes, edges=edges))

# ---------------------------------------------------------- FIG 5 --------
W, H = 8.6, 9.3
nodes = [
    dict(id="n1", kind="terminator", text="Start: Report Disruption",                      x=4.3, y=0.55, w=3.3, h=0.7),
    dict(id="n2", kind="process",    text="Get student location and\ndisruption description", x=4.3, y=1.75, w=3.3, h=0.9),
    dict(id="n3", kind="decision",   text="Description matches a\ndisruption keyword?",     x=4.3, y=3.25, w=3.1, h=1.1),
    dict(id="n4", kind="process",    text="Redirect to Book\nTutoring Session",             x=1.5, y=4.8, w=2.4, h=0.9),
    dict(id="n5", kind="decision",   text="Centre with tutor on duty\nfound within radius?", x=4.3, y=4.9, w=3.3, h=1.2),
    dict(id="n6", kind="process",    text="Increase search radius",                        x=7.4, y=4.9, w=2.2, h=0.8),
    dict(id="n7", kind="process",    text="Display redirect message\nand notify\nthat centre", x=2.3, y=6.9, w=2.7, h=1.1),
    dict(id="n8", kind="process",    text="Display: Contact District\nEducation Office",     x=6.1, y=6.9, w=2.7, h=1.0),
    dict(id="n9", kind="terminator", text="Log interaction and End",                       x=4.3, y=8.5, w=3.2, h=0.7),
]
edges = [
    dict(src="n1", dst="n2", label=None, pts=[(4.3,0.9),(4.3,1.3)], src_side="bottom", dst_side="top"),
    dict(src="n2", dst="n3", label=None, pts=[(4.3,2.2),(4.3,2.7)], src_side="bottom", dst_side="top"),
    dict(src="n3", dst="n4", label="No", pts=[(2.75,3.25),(1.5,3.25),(1.5,4.35)], src_side="left", dst_side="top"),
    dict(src="n3", dst="n5", label="Yes", pts=[(4.3,3.8),(4.3,4.3)], src_side="bottom", dst_side="top"),
    dict(src="n5", dst="n6", label="No — radius < max", pts=[(5.95,4.9),(6.3,4.9)], src_side="right", dst_side="left"),
    dict(src="n6", dst="n5", label=None, pts=[(7.4,4.5),(7.4,3.9),(4.3,3.9),(4.3,4.3)], src_side="top", dst_side="top"),
    dict(src="n5", dst="n7", label="Yes", pts=[(3.5,5.5),(2.3,5.5),(2.3,6.35)], src_side="left", dst_side="top"),
    dict(src="n5", dst="n8", label="No — max radius reached", pts=[(5.1,5.5),(6.1,5.5),(6.1,6.4)], src_side="right", dst_side="top"),
    dict(src="n4", dst="n9", label=None, pts=[(1.5,5.25),(1.5,8.5),(2.7,8.5)], src_side="bottom", dst_side="left"),
    dict(src="n7", dst="n9", label=None, pts=[(2.3,7.45),(2.3,8.5),(2.7,8.5)], src_side="bottom", dst_side="left"),
    dict(src="n8", dst="n9", label=None, pts=[(6.1,7.4),(6.1,8.5),(5.9,8.5)], src_side="bottom", dst_side="right"),
]
diagrams.append(dict(id="fig5", name="Figure 5 - Report School Disruption", w=W, h=H, nodes=nodes, edges=edges))

# ===================================================== MATPLOTLIB RENDER ==
def wrap_text_lines(text):
    return text.split("\n")

def draw_node(ax, n):
    cx, cy, w, h = n["x"], n["y"], n["w"], n["h"]
    y = -cy  # flip: matplotlib y grows up, our layout y grows down
    fill, stroke = COL[n["kind"]]
    if n["kind"] == "terminator":
        patch = FancyBboxPatch((cx - w/2, y - h/2), w, h,
                                boxstyle=f"round,pad=0,rounding_size={h/2}",
                                linewidth=1.4, edgecolor=stroke, facecolor=fill, zorder=3)
        ax.add_patch(patch)
    elif n["kind"] == "process":
        patch = Rectangle((cx - w/2, y - h/2), w, h, linewidth=1.4,
                           edgecolor=stroke, facecolor=fill, zorder=3)
        ax.add_patch(patch)
    elif n["kind"] == "decision":
        pts = [(cx, y + h/2), (cx + w/2, y), (cx, y - h/2), (cx - w/2, y)]
        patch = Polygon(pts, closed=True, linewidth=1.4, edgecolor=stroke, facecolor=fill, zorder=3)
        ax.add_patch(patch)
    elif n["kind"] == "subroutine":
        patch = Rectangle((cx - w/2, y - h/2), w, h, linewidth=1.4,
                           edgecolor=stroke, facecolor=fill, zorder=3)
        ax.add_patch(patch)
        bar = w * 0.07
        ax.add_line(plt.Line2D([cx - w/2 + bar, cx - w/2 + bar], [y - h/2, y + h/2], color=stroke, linewidth=1.2, zorder=4))
        ax.add_line(plt.Line2D([cx + w/2 - bar, cx + w/2 - bar], [y - h/2, y + h/2], color=stroke, linewidth=1.2, zorder=4))
    lines = wrap_text_lines(n["text"])
    fs = 9.3 if len(lines) <= 2 else 8.6
    ax.text(cx, y, "\n".join(lines), ha="center", va="center", fontsize=fs,
            family=FONT, zorder=5, linespacing=1.3,
            path_effects=[pe.withStroke(linewidth=0, foreground="white")])

def draw_edge(ax, e, nodes_by_id):
    pts = [(x, -y) for (x, y) in e["pts"]]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=EDGE_COLOR, linewidth=1.2, zorder=2, solid_joinstyle="round")
    # arrowhead at the final segment
    x0, y0 = pts[-2]
    x1, y1 = pts[-1]
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=EDGE_COLOR, lw=1.2,
                                 mutation_scale=14, shrinkA=0, shrinkB=0), zorder=2)
    if e["label"]:
        # place label near the midpoint of the first segment (usually near the source/decision)
        mx = (pts[0][0] + pts[1][0]) / 2
        my = (pts[0][1] + pts[1][1]) / 2
        dx = pts[1][0] - pts[0][0]
        dy = pts[1][1] - pts[0][1]
        offx, offy = (0, 0.14) if abs(dx) > abs(dy) else (0.12, 0)
        ax.text(mx + offx, my + offy, e["label"], ha="left" if offx else "center",
                va="bottom" if offy else "center", fontsize=8.3, family=FONT, color="#000000",
                zorder=6, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9))

def render_png(d, out_path):
    W, H = d["w"], d["h"]
    TOP_MARGIN = 0.45
    fig, ax = plt.subplots(figsize=(W, H + TOP_MARGIN), dpi=300)
    ax.set_xlim(0, W)
    ax.set_ylim(-H, TOP_MARGIN)
    ax.set_aspect("equal")
    ax.axis("off")
    nodes_by_id = {n["id"]: n for n in d["nodes"]}
    for e in d["edges"]:
        draw_edge(ax, e, nodes_by_id)
    for n in d["nodes"]:
        draw_node(ax, n)
    ax.text(W/2, TOP_MARGIN - 0.1, d["name"], ha="center", va="top", fontsize=12.5,
             family=FONT, weight="bold", transform=ax.transData)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.995, bottom=0.01)
    fig.savefig(out_path, dpi=300, facecolor="white")
    plt.close(fig)

# ========================================================= DRAWIO EXPORT ==
SIDE_POINT = {
    "top":    (0.5, 0.0),
    "bottom": (0.5, 1.0),
    "left":   (0.0, 0.5),
    "right":  (1.0, 0.5),
}

def build_drawio(diagrams, out_path):
    mxfile = ET.Element("mxfile", host="Electron", agent="EduLink report generator",
                         version="24.7.17", type="device")
    for d in diagrams:
        diagram_el = ET.SubElement(mxfile, "diagram", id=d["id"], name=d["name"])
        model = ET.SubElement(diagram_el, "mxGraphModel",
                               dx="900", dy="600", grid="1", gridSize="10", guides="1",
                               tooltips="1", connect="1", arrows="1", fold="1", page="1",
                               pageScale="1", pageWidth=str(int(d["w"] * SCALE)),
                               pageHeight=str(int(d["h"] * SCALE)), math="0", shadow="0")
        root = ET.SubElement(model, "root")
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")

        style_map = {
            "terminator": "rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=12;fontFamily=Helvetica;",
            "process":    "rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;fontFamily=Helvetica;",
            "decision":   "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;fontFamily=Helvetica;",
            "subroutine": "shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=12;fontFamily=Helvetica;",
        }
        cell_id = {}
        idx = 2
        for n in d["nodes"]:
            cid = f"c{idx}"; idx += 1
            cell_id[n["id"]] = cid
            x = (n["x"] - n["w"]/2) * SCALE
            y = (n["y"] - n["h"]/2) * SCALE
            w = n["w"] * SCALE
            h = n["h"] * SCALE
            cell = ET.SubElement(root, "mxCell", id=cid, value=n["text"].replace("\n", "<br>"),
                                  style=style_map[n["kind"]], vertex="1", parent="1")
            ET.SubElement(cell, "mxGeometry", x=str(int(x)), y=str(int(y)),
                          width=str(int(w)), height=str(int(h)), **{"as": "geometry"})

        for e in d["edges"]:
            eid = f"c{idx}"; idx += 1
            ex, ey = SIDE_POINT[e["src_side"]]
            tx, ty = SIDE_POINT[e["dst_side"]]
            style = (f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;jettySize=auto;"
                     f"orthogonalLoop=1;exitX={ex};exitY={ey};exitDx=0;exitDy=0;"
                     f"entryX={tx};entryY={ty};entryDx=0;entryDy=0;fontSize=11;fontFamily=Helvetica;")
            cell = ET.SubElement(root, "mxCell", id=eid, value=(e["label"] or ""),
                                  style=style, edge="1", parent="1",
                                  source=cell_id[e["src"]], target=cell_id[e["dst"]])
            ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})

    xml_bytes = ET.tostring(mxfile, encoding="utf-8")
    from xml.dom import minidom
    pretty = minidom.parseString(xml_bytes).toprettyxml(indent="  ")
    pretty = "\n".join(line for line in pretty.split("\n") if line.strip())
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(pretty)

# ================================================================= MAIN ===
if __name__ == "__main__":
    import os
    os.makedirs("diagrams", exist_ok=True)
    for d in diagrams:
        out = f"diagrams/{d['id']}_drawio.png"
        render_png(d, out)
        print("wrote", out)
    build_drawio(diagrams, "diagrams/EduLink.drawio")
    print("wrote diagrams/EduLink.drawio")
