#!/usr/bin/env python3
"""
Generates EduLink.fprg -- a runnable Flowgorithm program that mirrors the
EduLink SL pseudocode (Section 3 of the report) using parallel arrays, since
Flowgorithm has no record/struct data type.
"""
import base64
import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

AUTHOR = "Alieu Kamara"
NOW = datetime.datetime.now()
TS = NOW.strftime("%Y-%m-%d %H:%M:%S")

root = ET.Element("flowgorithm", fileversion="2.11")

attrs = ET.SubElement(root, "attributes")
ET.SubElement(attrs, "attribute", name="name", value="EduLink")
ET.SubElement(attrs, "attribute", name="authors", value=AUTHOR)
ET.SubElement(attrs, "attribute", name="about",
              value="Education Access and Resource Link System - PROG101 Assignment 1")
ET.SubElement(attrs, "attribute", name="saved", value=TS)
created_tok = f"{AUTHOR};LIMKOKWING;{NOW.strftime('%Y-%m-%d')};{NOW.strftime('%H:%M:%S')};1"
ET.SubElement(attrs, "attribute", name="created",
              value=base64.b64encode(created_tok.encode()).decode())
ET.SubElement(attrs, "attribute", name="edited",
              value=base64.b64encode(created_tok.encode()).decode())

CENTERS = [
    ("Njala Community School",            "true",  0,  0),
    ("Gondama Learning Hub",              "true",  4,  0),
    ("Kenema Secondary Resource Center",  "true",  6, 15),
    ("Bo Community Learning Center",      "false", 3,  0),
    ("Serabu Education Point",            "false", 0,  8),
]

def declare(parent, name, type_, array="False", size=""):
    ET.SubElement(parent, "declare", name=name, type=type_, array=array, size=size)

def assign(parent, variable, expression):
    ET.SubElement(parent, "assign", variable=variable, expression=expression)

def output(parent, expression, newline="True"):
    ET.SubElement(parent, "output", expression=expression, newline=newline)

def input_(parent, variable):
    ET.SubElement(parent, "input", variable=variable)

def call(parent, expression):
    ET.SubElement(parent, "call", expression=expression)

def comment(parent, text):
    ET.SubElement(parent, "comment", text=text)

def str_lit(s):
    return '"' + s.replace('"', '""') + '"'

# ---------------------------------------------------------------- Main ----
main_func = ET.SubElement(root, "function", name="Main", type="None", variable="")
ET.SubElement(main_func, "parameters")
mb = ET.SubElement(main_func, "body")

comment(mb, "EduLink SL - sample learning-center dataset (nearest-first, Mathematics tutor).")
comment(mb, "In production this would be populated from a live centers database.")
declare(mb, "centerName", "String", array="True", size="5")
declare(mb, "centerTutorOnDuty", "Boolean", array="True", size="5")
declare(mb, "centerOpenSeats", "Integer", array="True", size="5")
declare(mb, "centerPastPaperStock", "Integer", array="True", size="5")
declare(mb, "choice", "Integer")

for i, (name, tutor, seats, stock) in enumerate(CENTERS):
    assign(mb, f"centerName[{i}]", str_lit(name))
    assign(mb, f"centerTutorOnDuty[{i}]", tutor)
    assign(mb, f"centerOpenSeats[{i}]", str(seats))
    assign(mb, f"centerPastPaperStock[{i}]", str(stock))

output(mb, str_lit("===================================="))
output(mb, str_lit("  EduLink SL - Education Access"))
output(mb, str_lit("      and Resource Link System"))
output(mb, str_lit("===================================="))
output(mb, str_lit("1. Check Tutor Availability"))
output(mb, str_lit("2. Check Study Material Stock"))
output(mb, str_lit("3. Book Tutoring Session"))
output(mb, str_lit("4. Report School Disruption"))
output(mb, str_lit("Enter your choice (1-4):"))
input_(mb, "choice")

if1 = ET.SubElement(mb, "if", expression="choice = 1")
then1 = ET.SubElement(if1, "then")
call(then1, "checkTutorAvailability(centerName, centerTutorOnDuty, centerOpenSeats)")
else1 = ET.SubElement(if1, "else")

if2 = ET.SubElement(else1, "if", expression="choice = 2")
then2 = ET.SubElement(if2, "then")
call(then2, "checkMaterialStock(centerName, centerPastPaperStock)")
else2 = ET.SubElement(if2, "else")

if3 = ET.SubElement(else2, "if", expression="choice = 3")
then3 = ET.SubElement(if3, "then")
call(then3, "bookTutoringSession(centerName, centerOpenSeats)")
else3 = ET.SubElement(if3, "else")

if4 = ET.SubElement(else3, "if", expression="choice = 4")
then4 = ET.SubElement(if4, "then")
call(then4, "reportDisruption(centerName, centerTutorOnDuty)")
else4 = ET.SubElement(if4, "else")
output(else4, str_lit("Invalid option. Please run again and choose 1-4."))

# ------------------------------------------------ checkTutorAvailability() ----
f1 = ET.SubElement(root, "function", name="checkTutorAvailability", type="None", variable="")
p1 = ET.SubElement(f1, "parameters")
ET.SubElement(p1, "parameter", name="names", type="String", array="True")
ET.SubElement(p1, "parameter", name="tutorOnDuty", type="Boolean", array="True")
ET.SubElement(p1, "parameter", name="openSeats", type="Integer", array="True")
b1 = ET.SubElement(f1, "body")

declare(b1, "i", "Integer")
declare(b1, "found", "Boolean")
assign(b1, "i", "0")
assign(b1, "found", "false")
output(b1, str_lit("Searching nearby centers for a Mathematics tutor and an open seat..."))
w1 = ET.SubElement(b1, "while", expression="i <= 4 && found = false")
ifw1 = ET.SubElement(w1, "if", expression="tutorOnDuty[i] = true && openSeats[i] > 0")
thenw1 = ET.SubElement(ifw1, "then")
output(thenw1, 'names[i] & " - " & openSeats[i] & " seat(s) available"')
assign(thenw1, "found", "true")
ET.SubElement(ifw1, "else")
assign(w1, "i", "i + 1")
ifend1 = ET.SubElement(b1, "if", expression="found = false")
thenend1 = ET.SubElement(ifend1, "then")
output(thenend1, str_lit("No centre with a tutor and an open seat was found nearby."))
ET.SubElement(ifend1, "else")

# ------------------------------------------------ checkMaterialStock() ----
f2 = ET.SubElement(root, "function", name="checkMaterialStock", type="None", variable="")
p2 = ET.SubElement(f2, "parameters")
ET.SubElement(p2, "parameter", name="names", type="String", array="True")
ET.SubElement(p2, "parameter", name="stock", type="Integer", array="True")
b2 = ET.SubElement(f2, "body")

declare(b2, "i", "Integer")
declare(b2, "anyFound", "Boolean")
assign(b2, "anyFound", "false")
output(b2, str_lit("Checking nearby centers for BECE Mathematics Past Papers..."))
for2 = ET.SubElement(b2, "for", variable="i", start="0", end="4", direction="inc", step="1")
if2b = ET.SubElement(for2, "if", expression="stock[i] > 0")
then2b = ET.SubElement(if2b, "then")
output(then2b, 'names[i] & " has " & stock[i] & " copies in stock"')
assign(then2b, "anyFound", "true")
ET.SubElement(if2b, "else")
ifend2 = ET.SubElement(b2, "if", expression="anyFound = false")
thenend2 = ET.SubElement(ifend2, "then")
output(thenend2, str_lit("Past papers are not currently in stock at any nearby centre."))
ET.SubElement(ifend2, "else")

# -------------------------------------------------- bookTutoringSession() -----
f3 = ET.SubElement(root, "function", name="bookTutoringSession", type="None", variable="")
p3 = ET.SubElement(f3, "parameters")
ET.SubElement(p3, "parameter", name="names", type="String", array="True")
ET.SubElement(p3, "parameter", name="openSeats", type="Integer", array="True")
b3 = ET.SubElement(f3, "body")

declare(b3, "centerNumber", "Integer")
declare(b3, "idx", "Integer")
output(b3, str_lit("1=Njala  2=Gondama  3=Kenema  4=Bo Community  5=Serabu"))
output(b3, str_lit("Enter centre number to book (1-5):"))
input_(b3, "centerNumber")
assign(b3, "idx", "centerNumber - 1")
if3b = ET.SubElement(b3, "if", expression="openSeats[idx] > 0")
then3b = ET.SubElement(if3b, "then")
output(then3b, '"Tutoring session confirmed at " & names[idx]')
else3b = ET.SubElement(if3b, "else")
output(else3b, '"No seats available at " & names[idx] & ". Suggesting the next available centre..."')

# -------------------------------------------------- reportDisruption() ------
f4 = ET.SubElement(root, "function", name="reportDisruption", type="None", variable="")
p4 = ET.SubElement(f4, "parameters")
ET.SubElement(p4, "parameter", name="names", type="String", array="True")
ET.SubElement(p4, "parameter", name="tutorOnDuty", type="Boolean", array="True")
b4 = ET.SubElement(f4, "body")

declare(b4, "isDisruption", "Boolean")
declare(b4, "i", "Integer")
declare(b4, "found", "Boolean")
output(b4, str_lit("Is your school disrupted right now? (true = yes / false = no):"))
input_(b4, "isDisruption")
if4b = ET.SubElement(b4, "if", expression="isDisruption = true")
then4b = ET.SubElement(if4b, "then")
assign(then4b, "i", "0")
assign(then4b, "found", "false")
w4 = ET.SubElement(then4b, "while", expression="i <= 4 && found = false")
ifw4 = ET.SubElement(w4, "if", expression="tutorOnDuty[i] = true")
thenw4 = ET.SubElement(ifw4, "then")
output(thenw4, '"REDIRECT: Nearest open centre is " & names[i]')
assign(thenw4, "found", "true")
ET.SubElement(ifw4, "else")
assign(w4, "i", "i + 1")
ifend4 = ET.SubElement(then4b, "if", expression="found = false")
thenend4 = ET.SubElement(ifend4, "then")
output(thenend4, str_lit("No open centre available. Contact the District Education Office."))
ET.SubElement(ifend4, "else")
else4b = ET.SubElement(if4b, "else")
output(else4b, str_lit("No disruption detected. Please use Book Tutoring Session instead."))

# --------------------------------------------------------------- write ----
xml_bytes = ET.tostring(root, encoding="utf-8")
pretty = minidom.parseString(xml_bytes).toprettyxml(indent="    ")
pretty = "\n".join(line for line in pretty.split("\n") if line.strip())
pretty = pretty.replace('<?xml version="1.0" ?>', '<?xml version="1.0"?>')

with open("diagrams/EduLink.fprg", "w", encoding="utf-8") as f:
    f.write(pretty)

print("Wrote diagrams/EduLink.fprg")
