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
| `diagrams/EduLink.drawio` | **Flowchart built in diagrams.net (Draw.io)** — one of the three flowcharting tools named in the assignment brief. Open it free at https://app.diagrams.net (File > Open From > Device) to view or edit |
| `generate_drawio_flowchart.py` | Script used to generate `diagrams/EduLink.drawio` |

## Author

- **Name:** Alieu Kamara
- **Student ID:** 6151
- **Examiner:** Elijah Fullah
- **Checked by:** Sheik Umar Kanu

## License

This academic project is released under the MIT License (see `LICENSE`).
