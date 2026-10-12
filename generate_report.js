const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  TableOfContents, PageBreak, ImageRun, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, LevelFormat, convertInchesToTwip,
  VerticalAlign, Header, Footer, PageNumber, NumberFormat
} = require("docx");

const FONT = "Tahoma";
const BODY_SIZE = 20; // 10pt in half-points
const LINE_SPACING = { line: 276, lineRule: "auto" }; // 1.15 lines

// ---------- palette ----------
// A deep-forest / sage palette, deliberately distinct from the navy-blue
// theme used elsewhere, so this report reads as its own visual design.
const PRIMARY = "1B4332";   // headings, cover titles
const SECONDARY = "2D6A4F"; // sub-headings, table header fill, accent bars
const TERTIARY = "40704A";  // h3 / sub-sub-headings
const ACCENT = "B45309";    // "insert screenshot" callouts
const BORDER = "A9C7B5";    // table borders / rules
const TINT = "EAF4EE";      // light shaded cells / caption boxes
const STRIPE = "F4FAF6";    // alternating table row shading
const MUTED = "6B8F7C";     // header/footer running text

// ---------- helpers ----------
function body(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { ...LINE_SPACING, after: 160 },
    children: [new TextRun({ text, font: FONT, size: BODY_SIZE, ...opts })],
  });
}

function bulletPara(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { ...LINE_SPACING, after: 80 },
    numbering: { reference: "bullet-list", level: 0 },
    children: [new TextRun({ text, font: FONT, size: BODY_SIZE, ...opts })],
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 320, after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 10, color: SECONDARY, space: 6 } },
    children: [new TextRun({ text, font: FONT, bold: true, size: 28, color: PRIMARY })],
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 120 },
    children: [
      new TextRun({ text: "▎ ", font: FONT, bold: true, size: 24, color: SECONDARY }),
      new TextRun({ text, font: FONT, bold: true, size: 24, color: SECONDARY }),
    ],
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 180, after: 100 },
    children: [new TextRun({ text, font: FONT, bold: true, italics: true, size: 22, color: TERTIARY })],
  });
}

function mono(text) {
  return new Paragraph({
    spacing: { line: 240, lineRule: "auto", after: 0 },
    children: [new TextRun({ text, font: "Consolas", size: 18 })],
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

function labelValueRow(label, value) {
  return new TableRow({
    children: [
      new TableCell({
        width: { size: 30, type: WidthType.PERCENTAGE },
        shading: { type: ShadingType.CLEAR, fill: TINT },
        verticalAlign: VerticalAlign.CENTER,
        margins: { top: 100, bottom: 100, left: 150, right: 150 },
        children: [new Paragraph({ children: [new TextRun({ text: label, font: FONT, bold: true, size: BODY_SIZE })] })],
      }),
      new TableCell({
        width: { size: 70, type: WidthType.PERCENTAGE },
        verticalAlign: VerticalAlign.CENTER,
        margins: { top: 100, bottom: 100, left: 150, right: 150 },
        children: [new Paragraph({ children: [new TextRun({ text: value, font: FONT, size: BODY_SIZE })] })],
      }),
    ],
  });
}

// ---------- images ----------
// Each figure is sized to fit the page (max width 620, max height 880 "units",
// matching docx-js's pixel-based ImageRun scale) so the printed text stays large
// and legible, rather than cramming the whole system into one diagram.
function fitImage(path, nativeW, nativeH, maxW = 600, maxH = 760) {
  const scale = Math.min(maxW / nativeW, maxH / nativeH);
  return {
    data: fs.readFileSync(path),
    width: Math.round(nativeW * scale),
    height: Math.round(nativeH * scale),
  };
}

const fig1 = fitImage("diagrams/fig1_drawio.png", 3450, 2325);
const fig2 = fitImage("diagrams/fig2_drawio.png", 2460, 2235);
const fig3 = fitImage("diagrams/fig3_drawio.png", 2340, 2595);
const fig4 = fitImage("diagrams/fig4_drawio.png", 2460, 3315);
const fig5 = fitImage("diagrams/fig5_drawio.png", 2580, 2925);

function figureParagraph(fig, caption) {
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 200, after: 140 },
      children: [new ImageRun({ type: "png", data: fig.data, transformation: { width: fig.width, height: fig.height } })],
    }),
    // Caption rendered as a tinted callout box with a left accent bar,
    // rather than a plain italic line under the image.
    new Table({
      width: { size: 78, type: WidthType.PERCENTAGE },
      alignment: AlignmentType.CENTER,
      borders: {
        top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
        bottom: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
        right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
        left: { style: BorderStyle.SINGLE, size: 24, color: SECONDARY },
        insideHorizontal: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
        insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      },
      rows: [
        new TableRow({
          children: [
            new TableCell({
              shading: { type: ShadingType.CLEAR, fill: TINT },
              margins: { top: 100, bottom: 100, left: 180, right: 180 },
              children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                spacing: { ...LINE_SPACING, after: 0 },
                children: [new TextRun({ text: caption, font: FONT, size: 18, italics: true, color: "2F4F3F" })],
              })],
            }),
          ],
        }),
      ],
    }),
    new Paragraph({ spacing: { after: 180 }, children: [] }),
  ];
}

// ========================================================================
// COVER PAGE
// ========================================================================
const coverPage = [
  new Paragraph({ spacing: { before: 400 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "LIMKOKWING UNIVERSITY OF CREATIVE TECHNOLOGY", font: FONT, bold: true, size: 30, color: PRIMARY })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
    children: [new TextRun({ text: "SIERRA LEONE", font: FONT, bold: true, size: 24, color: PRIMARY })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 400 },
    children: [new TextRun({ text: "Department of Information and Communication Technology", font: FONT, size: 22, italics: true })],
  }),
  new Paragraph({ spacing: { before: 400, after: 200 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 100 },
    children: [new TextRun({ text: "PROG101: PRINCIPLES OF PROGRAMMING LOGIC AND DESIGN", font: FONT, bold: true, size: 26 })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 400 },
    children: [new TextRun({ text: "Individual Assignment 1", font: FONT, size: 24 })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 300, after: 100 },
    children: [new TextRun({ text: "Designing Logical Solutions for Sierra Leone Community Challenges", font: FONT, bold: true, size: 24 })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 500 },
    children: [new TextRun({ text: "Project: EduLink SL — Education Access and Resource Link System", font: FONT, italics: true, size: 24, color: SECONDARY })],
  }),
  new Paragraph({ spacing: { before: 600 }, children: [] }),
  new Table({
    width: { size: 80, type: WidthType.PERCENTAGE },
    alignment: AlignmentType.CENTER,
    borders: {
      top: { style: BorderStyle.SINGLE, size: 10, color: SECONDARY },
      bottom: { style: BorderStyle.SINGLE, size: 10, color: SECONDARY },
      left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: BORDER },
      insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
    },
    rows: [
      labelValueRow("Student Name:", "Alieu Kamara"),
      labelValueRow("Student ID:", "6151"),
      labelValueRow("Examiner:", "Elijah Fullah"),
      labelValueRow("Checked by:", "Sheik Umar Kanu"),
      labelValueRow("Semester:", "01, September 2026 to January 2027"),
      labelValueRow("Submission Deadline:", "Week 4"),
      labelValueRow("Date Submitted:", "[Insert submission date]"),
    ],
  }),
  pageBreak(),
];

// ========================================================================
// TABLE OF CONTENTS
// ========================================================================
function tocLine(label, pageNum) {
  return new Paragraph({
    spacing: { after: 140 },
    tabStops: [{ type: "right", position: convertInchesToTwip(6.3), leader: "dot" }],
    children: [
      new TextRun({ text: label, font: FONT, size: BODY_SIZE }),
      new TextRun({ text: `\t${pageNum}`, font: FONT, size: BODY_SIZE }),
    ],
  });
}

const tocSection = [
  h1("Table of Contents"),
  tocLine("1. Rationale", 3),
  tocLine("    1.1 Problem Description", 3),
  tocLine("    1.2 Background", 3),
  tocLine("    1.3 Who Is Affected", 3),
  tocLine("    1.4 Proposed Solution", 3),
  tocLine("    1.5 Community Impact", 3),
  tocLine("    1.6 Computational Thinking Process", 4),
  tocLine("    1.7 Algorithm Design Summary", 4),
  tocLine("    1.8 SDG Alignment", 4),
  tocLine("    1.9 Open Source Justification", 4),
  tocLine("    1.10 Digital Public Goods (DPG) Justification", 5),
  tocLine("    1.11 Long-Term Sustainability", 5),
  tocLine("2. Step-by-Step Algorithm", 6),
  tocLine("3. Pseudocode", 7),
  tocLine("4. Flowchart", 11),
  tocLine("    Figure 1 — System Overview", 12),
  tocLine("    Figure 2 — Check Tutor Availability", 13),
  tocLine("    Figure 3 — Check Study Material Stock", 14),
  tocLine("    Figure 4 — Book Tutoring Session", 15),
  tocLine("    Figure 5 — Report School Disruption", 16),
  tocLine("5. Functional Modules", 17),
  tocLine("6. Expected Outputs — Sample Scenarios", 18),
  tocLine("7. GitHub Repository Evidence", 20),
  tocLine("8. References", 21),
  pageBreak(),
];

// ========================================================================
// 1. RATIONALE
// ========================================================================
const rationale = [
  h1("1. Rationale"),

  h2("1.1 Problem Description"),
  body("In many rural and peri-urban communities across Sierra Leone, students routinely travel long distances to the nearest community learning centre only to discover, on arrival, that no tutor is on duty, that the centre has no open seats for a tutoring session, or that it has run out of the specific study material they need (for example BECE or WASSCE past papers in a given subject). Because learning centres have no shared, real-time way of publishing their availability, students, parents, and guardians must travel first and find out second. This wastes scarce transport money and time, discourages students from seeking extra academic support at all, and in the case of a sudden school disruption (flooding, a teacher strike, or a temporary closure) can leave a student with nowhere to turn for days."),

  h2("1.2 Background"),
  body("Sierra Leone's education system is constrained by limited road and transport infrastructure, an uneven distribution of qualified tutors between urban and rural areas, and inconsistent supply of textbooks and past papers between district education offices and the community learning centres that serve outlying villages. At the same time, mobile phone penetration is comparatively high even in areas with poor internet coverage, because basic (non-smartphone) handsets are affordable and GSM network coverage reaches most districts. This combination -- poor physical and information infrastructure, but reasonably good basic mobile coverage -- is the starting point for the proposed solution: a system that does not depend on smartphones, continuous data connectivity, or new hardware, but instead works over the mobile network that already exists."),

  h2("1.3 Who Is Affected"),
  bulletPara("Students, particularly those in rural and peri-urban areas preparing for national examinations (BECE, WASSCE), who cannot afford repeated wasted trips to a centre that turns out to have no tutor or no seats."),
  bulletPara("Parents and guardians, who need a fast way to check which nearby learning centre can actually help their child before sending them there, especially during a school disruption."),
  bulletPara("Community learning centre coordinators and District Education Office administrators, who currently have no simple channel to broadcast tutor availability, seat capacity, or material stock status to the community they serve."),

  h2("1.4 Proposed Solution"),
  body("EduLink SL -- the Education Access and Resource Link System -- is a logical system design for a USSD/SMS-based service that lets a student, parent, or guardian dial a short code from any basic mobile phone and, within seconds, (1) check which nearby learning centre currently has an available tutoring seat and a tutor on duty for the subject needed, (2) check whether a specific centre has a given study material or past paper in stock, (3) book a tutoring session at a centre with capacity, or (4) report a school disruption, which triggers a search outward from the student's location until a centre with a tutor on duty is found as an alternative. Centre coordinators maintain each facility's status (tutor on duty, open seats, material stock) through a simple administrative interface. Because the student-facing side runs over USSD/SMS rather than a smartphone app, it works on the handsets people in these communities already own, and it works even where data connectivity is weak or absent."),

  h2("1.5 Community Impact"),
  body("By letting students and parents check availability before travelling, EduLink SL is designed to reduce wasted journeys and the transport costs and lost study time that come with them, shorten the time between a school disruption and a student reaching a centre that can actually help them continue learning, give centre coordinators better visibility into incoming demand so they can plan tutor rosters and material stock, and give District Education Office administrators aggregated, anonymised usage data (which subjects are searched for most, which centres are consistently out of past papers) that can inform resource allocation. The direct beneficiaries are rural and peri-urban students and the parents or guardians who support them; the indirect beneficiaries are centre coordinators and the wider district education system, which gains a low-cost early-warning signal for tutor shortages and material stock-outs."),

  h2("1.6 Computational Thinking Process"),
  body("The design followed the four standard computational thinking steps:"),
  bulletPara("Decomposition -- the broad problem (\"students cannot find available, stocked academic support nearby\") was broken into four independent sub-problems: checking tutor availability, checking material stock, booking a tutoring session, and handling a school disruption report, each implemented as its own module."),
  bulletPara("Pattern recognition -- all four sub-problems share the same underlying pattern: search outward from a location, over an expanding radius, for a learning centre that satisfies a condition (open seat, material in stock, tutor present). This pattern was generalised into a single repeated \"expanding radius search\" structure reused by the availability and disruption modules."),
  bulletPara("Abstraction -- each module hides its internal detail behind a simple function signature (for example checkMaterialStock(location, materialName)), so the main menu and the disruption module can call it without needing to know how the search is implemented."),
  bulletPara("Algorithm design -- each sub-problem was translated into an explicit, step-by-step algorithm using sequence, selection (IF/ELSE), and repetition (WHILE/FOR EACH) structures, shown in full in Sections 2 and 3."),

  h2("1.7 Algorithm Design Summary"),
  body("The full step-by-step algorithm and pseudocode appear in Sections 2 and 3. In summary, the system presents a main menu, routes the user's choice to one of four modules using a decision structure, and each module uses a repetition structure to search outward from the user's location for a learning centre that meets the required condition, stopping either when a match is found or when a maximum search radius is reached."),

  h2("1.8 SDG Alignment"),
  body("EduLink SL is designed primarily to support Sustainable Development Goal 4 -- Quality Education -- and specifically Target 4.1 and Target 4.5, which call for equitable access to quality education and the elimination of disparities between rural and urban learners. By removing a key information barrier (not knowing whether a learning centre can actually help before travelling there) and by speeding up access to an alternative centre during a disruption, EduLink SL addresses a concrete, local obstacle to equitable basic education in Sierra Leone."),

  h2("1.9 Open Source Justification"),
  body("The proposed solution should be built on open source components for three practical reasons specific to Sierra Leone:"),
  bulletPara("Cost: the Ministry of Basic Education, NGOs, and district education offices operate on constrained budgets; building on open source USSD/SMS gateway frameworks and open source databases (for example PostgreSQL) removes recurring licence fees and lets the system scale to more districts without a proportional rise in cost."),
  bulletPara("Local capacity: releasing the source lets Sierra Leonean computer science and ICT students and graduates (including at Limkokwing) maintain, audit, and extend the system themselves, rather than the country depending on a single foreign vendor."),
  bulletPara("Community contribution: an open codebase invites contributions such as translating the USSD menus into Krio, Mende, or Temne, adding new modules (for example scholarship application reminders or exam registration deadlines), or adapting the system for other districts or countries facing the same access problem."),

  h2("1.10 Digital Public Goods (DPG) Justification"),
  body("If released under an open licence (for example MIT or GPL) with open data schemas, clear documentation, platform independence, and no built-in collection of unnecessary personal data, EduLink SL would align with the core criteria of the Digital Public Goods Standard: relevance to the Sustainable Development Goals, open licensing, and a do-no-harm design. Because the student-facing interface works over USSD/SMS rather than requiring a smartphone or a data plan, it is accessible to the great majority of the population from day one. Publishing EduLink SL as a Digital Public Good would let other Ministries of Education, NGOs, or universities in similarly resourced countries adopt and adapt it at no licensing cost, multiplying its public-education benefit well beyond Sierra Leone."),

  h2("1.11 Long-Term Sustainability"),
  body("Because EduLink SL runs over basic USSD/SMS (no smartphone, app installation, or data plan required for students) and is built on open source components (no recurring licence fees), it does not depend on continued external funding to keep running. Ongoing maintenance could reasonably be handed to a local university ICT department or a Ministry of Basic Education digital learning unit, and the modular design (Section 5) means new SDG-aligned features can be added -- for example a scholarship or bursary notification module -- without redesigning the whole system."),

  pageBreak(),
];

// ========================================================================
// 2. STEP-BY-STEP ALGORITHM
// ========================================================================
const algorithmSteps = [
  "Start.",
  "A student, parent, or guardian dials the USSD short code; the system displays the main menu (Check Tutor Availability, Check Material Stock, Book Tutoring Session, Report School Disruption).",
  "Get the user's menu selection.",
  "IF selection = Report School Disruption THEN get the student's location and a short description of the disruption; IF the description matches a recognised disruption keyword THEN search outward, radius by radius, for the nearest learning centre with a tutor on duty; IF one is found, display a redirect message and notify that centre, ELSE (maximum radius reached) display the District Education Office contact.",
  "ELSE IF selection = Check Tutor Availability THEN get the student's location and the subject needed, then search outward for the nearest centre that has both a tutor on duty for that subject and at least one open seat, and display the result.",
  "ELSE IF selection = Check Material Stock THEN get the material name and the student's location, then check nearby centres' stock records and display every centre that currently holds that material.",
  "ELSE IF selection = Book Tutoring Session THEN IF the student is not yet registered, register them; get the preferred centre and date; IF a seat is available, confirm the booking, reduce the centre's open-seat count by one, and send an SMS confirmation; ELSE suggest the next available date.",
  "ELSE display an invalid-option message and return to Step 2.",
  "Log the interaction (choice made and outcome) for later District Education Office reporting and resource planning.",
  "End.",
];

const algorithmSection = [
  h1("2. Step-by-Step Algorithm"),
  body("The algorithm below describes, in plain steps, how EduLink SL responds to a single USSD session from the moment a student, parent, or guardian dials in to the moment the session ends."),
  ...algorithmSteps.map((s, i) => bulletPara(`${i + 1}. ${s}`)),
  pageBreak(),
];

// ========================================================================
// 3. PSEUDOCODE
// ========================================================================
const pseudocodeText = fs.readFileSync("docs/pseudocode.txt", "utf8");
const pseudocodeSection = [
  h1("3. Pseudocode"),
  body("The pseudocode below implements the algorithm in Section 2 as a set of modules (functions), each using variables, constants, decision structures (IF / ELSE IF / ELSE) and repetition structures (WHILE, FOR EACH), as required by the assignment brief."),
  ...pseudocodeText.split("\n").map((line) => mono(line.length ? line : " ")),
  pageBreak(),
];

// ========================================================================
// 4. FLOWCHART
// ========================================================================
const flowchartSection = [
  h1("4. Flowchart"),
  body("The flowcharts below are the visual equivalent of the pseudocode in Section 3, built in diagrams.net (Draw.io) -- one of the flowcharting tools named in the assignment brief. To keep every box and label legible when printed, the system is shown as one simple overview diagram (Figure 1) plus one full-page diagram per module (Figures 2-5), rather than a single diagram with all branches combined. The source file (diagrams/EduLink.drawio, containing all five diagrams as separate pages) is included in the project's GitHub repository and can be opened and edited directly at https://app.diagrams.net (File > Open From > Device)."),
  body("The same logic was additionally rebuilt as an executable flowchart in Flowgorithm (diagrams/EduLink.fprg, also in the repository), with each module as its own linked flowchart using Flowgorithm's Declare, Input, Output, If, While, For, and Call symbols. Because Flowgorithm has no record/struct data type, each learning centre's details are represented as parallel arrays (centerName, centerTutorOnDuty, centerOpenSeats, centerPastPaperStock) rather than the LearningCenter record shown in Section 3 -- the decision and repetition logic is otherwise identical. This version can be run directly to produce the sample outputs in Section 6.", { italics: true }),
  body("Insert a screenshot of the Flowgorithm flowchart below before printing.", { italics: true, color: ACCENT }),
  new Paragraph({ spacing: { before: 100, after: 200 }, children: [new TextRun({ text: "[ Insert Flowgorithm screenshot here ]", font: FONT, size: BODY_SIZE, italics: true, color: MUTED })] }),
  pageBreak(),

  h2("Figure 1 — System Overview"),
  ...figureParagraph(fig1, "Figure 1: Main menu and routing to each module."),
  pageBreak(),

  h2("Figure 2 — Check Tutor Availability"),
  ...figureParagraph(fig2, "Figure 2: checkTutorAvailability() — expanding-radius search for a centre with a tutor on duty and an open seat."),
  pageBreak(),

  h2("Figure 3 — Check Study Material Stock"),
  ...figureParagraph(fig3, "Figure 3: checkMaterialStock() — scans nearby centres' stock records for the requested study material."),
  pageBreak(),

  h2("Figure 4 — Book Tutoring Session"),
  ...figureParagraph(fig4, "Figure 4: bookTutoringSession() — registers the student if needed, then confirms or suggests an alternative date."),
  pageBreak(),

  h2("Figure 5 — Report School Disruption"),
  ...figureParagraph(fig5, "Figure 5: reportDisruption() — bypasses the open-seat requirement and searches only for a tutor on duty."),
  pageBreak(),
];

// ========================================================================
// 5. FUNCTIONAL MODULES
// ========================================================================
// rowIndex (0-based, counting only data rows, i.e. excluding the header) is
// used to band every other row with a light tint instead of drawing a full
// grid of vertical/horizontal borders — a "minimal/banded" table style.
function moduleRow(name, purpose, inputs, outputs, rowIndex = 0) {
  const fill = rowIndex % 2 === 1 ? STRIPE : "FFFFFF";
  const cell = (text, width, bold = false) => new TableCell({
    width: { size: width, type: WidthType.PERCENTAGE },
    shading: { type: ShadingType.CLEAR, fill },
    margins: { top: 90, bottom: 90, left: 120, right: 120 },
    children: [new Paragraph({ children: [new TextRun({ text, font: FONT, size: 18, bold })] })],
  });
  return new TableRow({
    children: [
      cell(name, 20, true),
      cell(purpose, 35),
      cell(inputs, 25),
      cell(outputs, 20),
    ],
  });
}

function headerRow(cells) {
  return new TableRow({
    tableHeader: true,
    children: cells.map((t) => new TableCell({
      shading: { type: ShadingType.CLEAR, fill: SECONDARY },
      margins: { top: 90, bottom: 90, left: 120, right: 120 },
      children: [new Paragraph({ children: [new TextRun({ text: t, font: FONT, size: 18, bold: true, color: "FFFFFF" })] })],
    })),
  });
}

const modulesTable = new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  borders: {
    top: { style: BorderStyle.SINGLE, size: 10, color: SECONDARY },
    bottom: { style: BorderStyle.SINGLE, size: 10, color: SECONDARY },
    left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
    right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
    insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: BORDER },
    insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  },
  rows: [
    headerRow(["Module", "Purpose", "Inputs", "Outputs"]),
    moduleRow("mainMenu()", "Displays the menu and routes the user's choice.", "userChoice", "Calls routeRequest()", 0),
    moduleRow("routeRequest(choice)", "Decision structure that calls the correct module for the selected option.", "choice", "Module call", 1),
    moduleRow("checkTutorAvailability()", "Searches outward for a centre with a tutor on duty and an open seat.", "studentLocation, subjectNeeded", "List of available centres", 2),
    moduleRow("checkMaterialStock()", "Searches nearby centres' stock records for a named study material.", "studentLocation, materialName", "List of centres with stock", 3),
    moduleRow("bookTutoringSession()", "Registers the student if needed and books a confirmed seat.", "studentPhone, centerID, date", "Booking confirmation / SMS", 4),
    moduleRow("reportDisruption()", "Flags disruption keywords and searches outward for the nearest staffed centre.", "studentLocation, disruptionDescription", "Redirect message / DEO contact", 5),
    moduleRow("registerStudent()", "Creates a new student record.", "name, age, phone, location", "studentID", 6),
    moduleRow("sendNotification(phone, msg)", "Sends a confirmation or alert SMS.", "phone, message", "SMS sent", 7),
    moduleRow("logInteraction()", "Stores each session's outcome for reporting.", "choice, outcome, timestamp", "Log entry", 8),
  ],
});

const modulesSection = [
  h1("5. Functional Modules"),
  body("The system is decomposed into nine independent, reusable modules, each with a single responsibility. This modular design means any one module (for example the disruption-report search logic) can be tested, maintained, or improved without affecting the others."),
  modulesTable,
  pageBreak(),
];

// ========================================================================
// 6. EXPECTED OUTPUTS (sample scenarios)
// ========================================================================
const sampleDataTable = new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  borders: {
    top: { style: BorderStyle.SINGLE, size: 10, color: SECONDARY },
    bottom: { style: BorderStyle.SINGLE, size: 10, color: SECONDARY },
    left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
    right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
    insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: BORDER },
    insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  },
  rows: [
    headerRow(["#", "Learning Centre", "Tutor on duty", "Open seats", "Past paper stock"]),
    moduleRow("1", "Njala Community School", "Yes", "0", "0", 0),
    moduleRow("2", "Gondama Learning Hub", "Yes", "4", "0", 1),
    moduleRow("3", "Kenema Secondary Resource Center", "Yes", "6", "15", 2),
    moduleRow("4", "Bo Community Learning Center", "No", "3", "0", 3),
    moduleRow("5", "Serabu Education Point", "No", "0", "8", 4),
  ],
});

const scenariosSection = [
  h1("6. Expected Outputs — Sample Scenarios"),
  body("The scenarios below use the fixed five-centre sample dataset built into the Flowgorithm program (diagrams/EduLink.fprg), so they can be reproduced exactly by running that file -- these are not illustrative-only figures."),
  sampleDataTable,
  body(" ", {}),

  h2("Scenario A: Routine tutor availability check (Menu option 1)"),
  body("Input: Select \"1. Check Tutor Availability\".", {}),
  body("Processing: The system scans centres nearest-first for the first one with both a tutor on duty and an open seat. Njala (#1) has a tutor but 0 open seats, so it is skipped; Gondama (#2) has a tutor and 4 open seats.", {}),
  body("Output: \"Gondama Learning Hub - 4 seat(s) available\"", { bold: true }),

  h2("Scenario B: Study material stock check (Menu option 2)"),
  body("Input: Select \"2. Check Study Material Stock\" for BECE Mathematics Past Papers.", {}),
  body("Processing: The system checks every centre's past-paper stock level, not just the nearest.", {}),
  body("Output: \"Kenema Secondary Resource Center has 15 copies in stock\" and \"Serabu Education Point has 8 copies in stock\"", { bold: true }),

  h2("Scenario C: Successful tutoring session booking (Menu option 3)"),
  body("Input: Select \"3. Book Tutoring Session\", then enter centre number 2 (Gondama Learning Hub).", {}),
  body("Processing: Gondama has 4 open seats, so the booking is confirmed.", {}),
  body("Output: \"Tutoring session confirmed at Gondama Learning Hub\"", { bold: true }),

  h2("Scenario D: School disruption report (Menu option 4)"),
  body("Input: Select \"4. Report School Disruption\", then enter true when asked whether the school is currently disrupted.", {}),
  body("Processing: Unlike Scenario A, this search only requires a tutor on duty -- it does not require an open seat, because a disrupted student cannot wait for a routine booking seat to free up. Njala (#1) is the nearest centre with a tutor, so it is selected immediately even though Scenario A had to skip it for having no open seats.", {}),
  body("Output: \"REDIRECT: Nearest open centre is Njala Community School\"", { bold: true }),
  body("This contrast between Scenario A and Scenario D is deliberate: it demonstrates why the disruption-report branch is a separate module with its own, less restrictive condition, rather than reusing the availability-check logic.", { italics: true }),

  pageBreak(),
];

// ========================================================================
// 7. GITHUB EVIDENCE (placeholder instructions)
// ========================================================================
const githubSection = [
  h1("7. GitHub Repository Evidence"),
  body("This project's report, pseudocode, and flowchart source (both the diagrams.net/Draw.io file behind the five figures in Section 4, EduLink.drawio, and the runnable Flowgorithm program, EduLink.fprg) are version-controlled in a GitHub repository named using the required convention PROG101_Assignment1_StudentName_StudentID. The repository contains a README.md describing the project, the pseudocode file, the flowchart source files, and this report, with regular commits made during development."),
  body("Repository URL: [Insert GitHub repository URL once the repository has been created and pushed]", { bold: true, italics: true, color: ACCENT }),
  body("Insert a screenshot of the repository's file listing below before printing.", { italics: true, color: ACCENT }),
  new Paragraph({ spacing: { before: 100, after: 200 }, children: [new TextRun({ text: "[ Insert repository file-listing screenshot here ]", font: FONT, size: BODY_SIZE, italics: true, color: MUTED })] }),
  body("Insert a screenshot of the commit history below before printing.", { italics: true, color: ACCENT }),
  new Paragraph({ spacing: { before: 100, after: 200 }, children: [new TextRun({ text: "[ Insert commit-history screenshot here ]", font: FONT, size: BODY_SIZE, italics: true, color: MUTED })] }),
  pageBreak(),
];

// ========================================================================
// 8. REFERENCES
// ========================================================================
const referencesSection = [
  h1("8. References"),
  bulletPara("United Nations. (2015). Sustainable Development Goal 4: Quality Education. https://sdgs.un.org/goals/goal4"),
  bulletPara("Digital Public Goods Alliance. (n.d.). Digital Public Goods Standard. https://digitalpublicgoods.net/standard/"),
  bulletPara("World Bank. (2022). Sierra Leone Education Sector and Digital Learning Overview. https://www.worldbank.org"),
  bulletPara("GSMA. (2023). The Mobile Economy: Sub-Saharan Africa. https://www.gsma.com"),
  bulletPara("Limkokwing University of Creative Technology, Sierra Leone. (2026). PROG101: Principles of Programming Logic and Design — Assignment Brief."),
  bulletPara("JGraph Ltd (diagrams.net / Draw.io). (n.d.). Documentation. https://www.drawio.com/doc/"),
];

// ========================================================================
// DOCUMENT ASSEMBLY
// ========================================================================
const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullet-list",
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: convertInchesToTwip(0.35), hanging: convertInchesToTwip(0.2) } } } },
        ],
      },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 }, // A4
          margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            children: [new TextRun({ text: "PROG101 — EduLink SL Assignment Report", font: FONT, size: 16, color: MUTED })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Page ", font: FONT, size: 16, color: MUTED }),
              new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: MUTED }),
              new TextRun({ text: " of ", font: FONT, size: 16, color: MUTED }),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 16, color: MUTED }),
            ],
          })],
        }),
      },
      children: [
        ...coverPage,
        ...tocSection,
        ...rationale,
        ...algorithmSection,
        ...pseudocodeSection,
        ...flowchartSection,
        ...modulesSection,
        ...scenariosSection,
        ...githubSection,
        ...referencesSection,
      ],
    },
  ],
  styles: {
    default: {
      document: {
        run: { font: FONT, size: BODY_SIZE },
      },
    },
  },
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync("EduLink_Assignment_Report.docx", buffer);
  console.log("Report written.");
});
