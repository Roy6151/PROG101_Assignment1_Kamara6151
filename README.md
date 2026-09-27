# EduLink SL — Education Access and Resource Link System

**PROG101: Principles of Programming Logic and Design — Individual Assignment 1**
Limkokwing University of Creative Technology, Sierra Leone
Department of Information and Communication Technology
Semester 01, September 2026 – January 2027

> Before pushing this repo, confirm it is named per the required convention:
> `PROG101_Assignment1_<YourStudentName>_<YourStudentID>`

## Overview

EduLink SL is a **logical system design** (no source code required by the assignment brief) for a
USSD/SMS-based service that helps students, parents, and guardians in rural and peri-urban
Sierra Leone:

- Check which nearby community learning centre currently has an open tutoring seat and a tutor
  on duty for the subject needed
- Check whether a specific centre has a given study material or past paper in stock
- Book a confirmed tutoring session
- Report a school disruption, which searches outward from the student's location for the nearest
  centre with a tutor on duty as an alternative

It is designed to work over basic USSD/SMS rather than a smartphone app, because that is what
is reliably accessible across Sierra Leone's rural communities, even where data connectivity is
weak.

## Why this problem

Students in rural Sierra Leone often travel long distances to a community learning centre only
to find no tutor on duty, no open tutoring seats, or no stock of the past papers they need. This
wastes transport money and study time and, when a school is disrupted, delays a student's access
to any alternative academic support. Full problem analysis and rationale to follow in the report.

## SDG Alignment

**SDG 4 — Quality Education** (Targets 4.1 and 4.5: equitable access to quality education and
elimination of rural/urban disparities).

## Repository Contents

| Path | Description |
|---|---|
| `diagrams/EduLink.drawio` | **Flowchart built in diagrams.net (Draw.io)** — one of the three flowcharting tools named in the assignment brief. Contains five diagrams as separate pages/tabs in one file. Open it free at https://app.diagrams.net (File > Open From > Device) to view or edit |
| `diagrams/fig1_drawio.png` … `fig5_drawio.png` | Rendered PNG export of each Draw.io page — one overview diagram (Figure 1) plus one full-page diagram per module (Figures 2-5), split up so every box and label stays legible when printed |
| `generate_drawio_flowchart.py` | Script used to generate `diagrams/EduLink.drawio` and the five rendered PNGs |
| `docs/pseudocode.txt` | Pseudocode for all system modules (plain text) |

## System Modules (Modular Design)

| Module | Purpose |
|---|---|
| `mainMenu()` | Displays the menu and routes the user's choice |
| `routeRequest(choice)` | Decision structure that calls the correct module |
| `checkTutorAvailability()` | Searches outward for a centre with a tutor on duty and an open seat |
| `checkMaterialStock()` | Searches nearby centres' stock records for a named study material |
| `bookTutoringSession()` | Registers the student if needed and books a confirmed seat |
| `reportDisruption()` | Flags disruption keywords and searches outward for the nearest staffed centre |
| `registerStudent()` | Creates a new student record |
| `sendNotification(phone, msg)` | Sends a confirmation or alert SMS |
| `logInteraction()` | Stores each session's outcome for reporting |

Full pseudocode: [`docs/pseudocode.txt`](docs/pseudocode.txt)

## Author

- **Name:** Alieu Kamara
- **Student ID:** 6151
- **Examiner:** Elijah Fullah
- **Checked by:** Sheik Umar Kanu

## License

This academic project is released under the MIT License (see `LICENSE`).
