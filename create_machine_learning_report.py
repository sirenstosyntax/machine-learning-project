from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "Machine_Learning_Analysis_Report.pdf"
FIGURES = ROOT / "figures"

NAVY = colors.HexColor("#14324A")
TEAL = colors.HexColor("#2A8F85")
BLUE = colors.HexColor("#3F7594")
LIGHT_BLUE = colors.HexColor("#EAF3F8")
LIGHT_GRAY = colors.HexColor("#F2F4F5")
MID_GRAY = colors.HexColor("#D8E0E5")
DARK_GRAY = colors.HexColor("#36454F")
RED = colors.HexColor("#C94C4C")


def register_fonts():
    candidates = [
        (
            Path("C:/Windows/Fonts/aptos.ttf"),
            Path("C:/Windows/Fonts/aptosb.ttf"),
            Path("C:/Windows/Fonts/aptosi.ttf"),
        ),
        (
            Path("C:/Windows/Fonts/calibri.ttf"),
            Path("C:/Windows/Fonts/calibrib.ttf"),
            Path("C:/Windows/Fonts/calibrii.ttf"),
        ),
    ]
    for regular, bold, italic in candidates:
        if regular.exists() and bold.exists() and italic.exists():
            pdfmetrics.registerFont(TTFont("Report", str(regular)))
            pdfmetrics.registerFont(TTFont("Report-Bold", str(bold)))
            pdfmetrics.registerFont(TTFont("Report-Italic", str(italic)))
            return "Report", "Report-Bold", "Report-Italic"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"


FONT, FONT_BOLD, FONT_ITALIC = register_fonts()


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        "BodySmall",
        fontName=FONT,
        fontSize=8.35,
        leading=11.1,
        textColor=DARK_GRAY,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        "BodyTiny",
        parent=styles["BodySmall"],
        fontSize=7.25,
        leading=9.25,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        "Section",
        fontName=FONT_BOLD,
        fontSize=15,
        leading=18,
        textColor=NAVY,
        spaceAfter=7,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        "Subsection",
        fontName=FONT_BOLD,
        fontSize=9.4,
        leading=11.5,
        textColor=BLUE,
        spaceBefore=4,
        spaceAfter=3,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        "BulletSmall",
        parent=styles["BodySmall"],
        leftIndent=12,
        firstLineIndent=-6,
        bulletIndent=3,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        "Caption",
        fontName=FONT,
        fontSize=6.5,
        leading=8,
        textColor=colors.HexColor("#6C7A84"),
        alignment=TA_CENTER,
        spaceBefore=2,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        "CoverKicker",
        fontName=FONT_BOLD,
        fontSize=7.2,
        leading=9,
        textColor=BLUE,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        "CoverTitle",
        fontName=FONT_BOLD,
        fontSize=23,
        leading=25,
        textColor=NAVY,
        spaceAfter=9,
    )
)
styles.add(
    ParagraphStyle(
        "CoverSubtitle",
        fontName=FONT,
        fontSize=10.2,
        leading=13.2,
        textColor=colors.HexColor("#5C6C76"),
        spaceAfter=18,
    )
)
styles.add(
    ParagraphStyle(
        "MetricNumber",
        fontName=FONT_BOLD,
        fontSize=15,
        leading=17,
        textColor=NAVY,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        "MetricLabel",
        fontName=FONT,
        fontSize=6.7,
        leading=8,
        textColor=colors.HexColor("#647681"),
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        "Callout",
        fontName=FONT_BOLD,
        fontSize=9,
        leading=12,
        textColor=NAVY,
        leftIndent=8,
        rightIndent=8,
        spaceBefore=4,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        "Reference",
        fontName=FONT,
        fontSize=6.9,
        leading=8.7,
        textColor=DARK_GRAY,
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=4,
    )
)


def p(text, style="BodySmall"):
    return Paragraph(text, styles[style])


def bullet(text):
    return Paragraph(f"&bull; {text}", styles["BulletSmall"])


def section(title):
    return KeepTogether([Paragraph(title, styles["Section"])])


def subsection(title):
    return KeepTogether([Paragraph(title, styles["Subsection"])])


def styled_table(data, widths, font_size=7.1, header=True, alignments=None):
    converted = []
    for row_index, row in enumerate(data):
        row_items = []
        for item in row:
            style = ParagraphStyle(
                f"Cell{row_index}",
                fontName=FONT_BOLD if header and row_index == 0 else FONT,
                fontSize=font_size,
                leading=font_size + 2,
                textColor=colors.white if header and row_index == 0 else DARK_GRAY,
            )
            row_items.append(Paragraph(str(item), style))
        converted.append(row_items)
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY if header else colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, MID_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    for row in range(1 if header else 0, len(data)):
        if row % 2 == 0:
            commands.append(("BACKGROUND", (0, row), (-1, row), LIGHT_GRAY))
    if alignments:
        for col, alignment in enumerate(alignments):
            commands.append(("ALIGN", (col, 1 if header else 0), (col, -1), alignment))
    table.setStyle(TableStyle(commands))
    return table


def callout(text):
    box = Table([[Paragraph(text, styles["Callout"])]], colWidths=[6.65 * inch])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.7, BLUE),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return box


def report_image(filename, width, height):
    path = FIGURES / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing required figure: {path}")
    return Image(str(path), width=width, height=height)


def page_header_footer(canvas, doc):
    page = canvas.getPageNumber()
    canvas.saveState()
    if page > 1:
        canvas.setFont(FONT, 6.5)
        canvas.setFillColor(colors.HexColor("#6A7A84"))
        canvas.drawString(0.75 * inch, 10.55 * inch, "NEMSIS Cardiac-Arrest ROSC Prediction")
        canvas.setStrokeColor(MID_GRAY)
        canvas.setLineWidth(0.4)
        canvas.line(0.75 * inch, 10.45 * inch, 7.75 * inch, 10.45 * inch)
    canvas.setStrokeColor(MID_GRAY)
    canvas.setLineWidth(0.4)
    canvas.line(0.75 * inch, 0.48 * inch, 7.75 * inch, 0.48 * inch)
    canvas.setFont(FONT, 6.3)
    canvas.setFillColor(colors.HexColor("#6A7A84"))
    canvas.drawString(0.75 * inch, 0.31 * inch, "Grant Collings | Machine Learning Capstone | July 2026")
    canvas.drawRightString(7.75 * inch, 0.31 * inch, f"Page {page}")
    canvas.restoreState()


def build_story():
    story = []

    # Page 1: Cover
    story += [
        Spacer(1, 0.62 * inch),
        p("MACHINE LEARNING ANALYSIS REPORT", "CoverKicker"),
        p(
            "Predicting Return of Spontaneous<br/>Circulation in Out-of-Hospital Cardiac<br/>Arrest",
            "CoverTitle",
        ),
        p(
            "A NEMSIS 2025 analysis of EMS system response time, clinical context, and "
            "Utstein-style cohorts",
            "CoverSubtitle",
        ),
    ]
    metric_data = [
        [p("17,198", "MetricNumber"), p("1,777", "MetricNumber"), p("0.7321", "MetricNumber")],
        [
            p("Broad cohort records", "MetricLabel"),
            p("Classic Utstein records", "MetricLabel"),
            p("Best broad ROC AUC", "MetricLabel"),
        ],
    ]
    metrics = Table(metric_data, colWidths=[2.2 * inch] * 3)
    metrics.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                ("GRID", (0, 0), (-1, -1), 0.5, BLUE),
                ("TOPPADDING", (0, 0), (-1, 0), 5),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 5),
            ]
        )
    )
    story += [
        p("<b>Prepared by Grant Collings</b>", "BodySmall"),
        p("AI Mastery Capstone - Project 4", "BodySmall"),
        Spacer(1, 0.18 * inch),
        metrics,
        Spacer(1, 0.26 * inch),
        callout(
            "Research question: Does EMS system response time add predictive value for ROSC beyond "
            "age, geography, arrest etiology, witness category, pre-arrival AED use, and initial rhythm?"
        ),
        Spacer(1, 0.16 * inch),
        p(
            "Data source: National Highway Traffic Safety Administration, National Emergency Medical "
            "Services Information System (NEMSIS). Derived content remains NHTSA property. NHTSA is "
            "not responsible for claims arising from this analysis.",
            "BodyTiny",
        ),
        p(
            "This report describes predictive associations. It does not estimate a causal effect of "
            "response time and does not report survival to hospital discharge.",
            "BodyTiny",
        ),
        PageBreak(),
    ]

    # Page 2: Executive summary
    story += [
        section("Executive Summary"),
        p(
            "This project used a supervised binary-classification workflow to predict any return of "
            "spontaneous circulation (ROSC) among out-of-hospital cardiac-arrest EMS activations. A "
            "50,000-record cardiac-arrest sample was linked to NEMSIS computed response-time, "
            "resuscitation, ROSC, and witness tables without extracting the 43 GB primary events file."
        ),
        bullet(
            "The final broad modeling cohort contained 17,198 first-unit, primary-area emergency "
            "responses with attempted resuscitation, known ROSC, and recorded response time."
        ),
        bullet(
            "The classic presumed-cardiac Utstein-style subgroup contained 1,777 "
            "bystander-witnessed arrests with an initially shockable rhythm."
        ),
        bullet("ROSC occurred in 29.64% of the broad cohort and 53.91% of the classic Utstein subgroup."),
        bullet(
            "Within the classic subgroup, ROSC declined from 62.92% in the fastest response-time "
            "decile to 43.68% in the slowest decile."
        ),
        bullet(
            "Adding response time improved cross-validated ROC AUC for both logistic regression and "
            "random forest in both cohorts."
        ),
        bullet(
            "The enhanced random forest produced the highest threshold-independent performance: ROC "
            "AUC 0.7321 in the broad cohort and 0.6095 in the classic subgroup."
        ),
        callout(
            "Primary conclusion: response time contributed consistent but modest incremental predictive "
            "value. Initial rhythm and other arrest characteristics remained central. The results support "
            "including response time in cardiac-arrest outcome models while avoiding causal or "
            "clinical-decision claims."
        ),
        Spacer(1, 5),
        subsection("Project Design"),
        p("The project was designed around two nested analyses:"),
        styled_table(
            [
                ["Cohort", "Purpose", "Records", "ROSC rate"],
                ["Broad", "Develop and compare general ROSC classifiers", "17,198", "29.64%"],
                ["Utstein-style", "Bystander-witnessed and shockable rhythm", "2,054", "53.21%"],
                ["Classic Utstein", "Adds presumed cardiac etiology", "1,777", "53.91%"],
            ],
            [1.15 * inch, 3.45 * inch, 0.8 * inch, 0.85 * inch],
        ),
        Spacer(1, 4),
        p(
            "The classic subgroup is described as Utstein-style ROSC analysis, not Utstein survival. "
            "The available target is any ROSC recorded during EMS care; survival to hospital discharge "
            "was not established.",
            "BodyTiny",
        ),
        PageBreak(),
    ]

    # Page 3: Source and cohort
    story += [
        section("1. Data Source and Cohort Construction"),
        subsection("Data source"),
        p(
            "The analysis used the 2025 NEMSIS Public-Release Research Dataset, which contains "
            "63,635,893 EMS activations submitted by 14,801 agencies serving 54 states and territories "
            "(National Emergency Medical Services Information System [NEMSIS], 2026). NEMSIS describes "
            "the data as a de-identified convenience sample rather than a population-based dataset. "
            "Source tables were streamed directly from the compressed release to limit storage and "
            "preserve the original archive."
        ),
        subsection("Cohort flow"),
        styled_table(
            [
                ["Stage", "Eligibility rule", "Records"],
                ["Starting cardiac-arrest sample", "Cardiac arrest before EMS arrival", "50,000"],
                ["Attempted resuscitation", "Defibrillation, ventilation, or chest compressions attempted", "34,773"],
                ["Known ROSC", "Unambiguous positive or negative eArrest.12 outcome", "33,608"],
                ["Response time recorded", "EMSSystemResponseTimeMin present", "33,574"],
                ["First EMS unit", "eScene.01 = Yes", "17,802"],
                ["Primary emergency response", "eResponse.05 = Primary Response Area", "17,198"],
                ["Classic Utstein", "Clean bystander witness + shockable rhythm + presumed cardiac", "1,777"],
            ],
            [1.85 * inch, 4.15 * inch, 0.65 * inch],
            font_size=6.8,
        ),
        Spacer(1, 5),
        subsection("Outcome definition"),
        p(
            "ROSC was coded positive when eArrest.12 contained Yes at ED arrival, Yes prior to ED "
            "arrival, or Yes sustained for 20 consecutive minutes. It was coded negative when "
            "eArrest.12 contained No. Records containing both positive and negative codes, or only "
            "missing/not-applicable codes, were excluded from outcome-eligible cohorts (NEMSIS, 2024)."
        ),
        subsection("Response-time definition"),
        p(
            "EMS system response time is the interval from unit notification by dispatch (eTimes.03) "
            "to unit arrival on scene (eTimes.06). Zero-minute values were retained because they are "
            "permitted by the NEMSIS computed-variable range and may represent identical recorded "
            "timestamps. Three broad-cohort records exceeded 60 minutes (64.3, 69.0, and 153.02 "
            "minutes); they were retained because the values were internally computable and within "
            "the NEMSIS public-release bounds. The classic subgroup maximum was 55 minutes "
            "(NEMSIS, 2024)."
        ),
        PageBreak(),
    ]

    # Page 4: Variables and preprocessing
    story += [
        section("2. Variables and Preprocessing"),
        styled_table(
            [
                ["Role", "Variables", "Processing"],
                ["Outcome", "ROSC", "Binary 0/1 target from eArrest.12"],
                ["Numeric", "Age; EMS system response time", "Median imputation; standardized for logistic regression"],
                [
                    "Categorical",
                    "Urbanicity; Census region; etiology; witness; AED; rhythm",
                    "Explicit missing categories and one-hot encoding",
                ],
                [
                    "Cohort flags",
                    "Bystander witnessed; shockable rhythm; Utstein-style; classic Utstein",
                    "Rule-based indicators; not used as predictors",
                ],
            ],
            [0.9 * inch, 2.85 * inch, 2.9 * inch],
            font_size=6.6,
        ),
        Spacer(1, 6),
        p(
            "The local modeling file omitted PcrKey and contained only the 17,198 broad-cohort rows. "
            "The row-level CSV was excluded from Git because NEMSIS terms restrict redistribution. "
            "Reproducible preparation and modeling code, aggregate results, and figures were retained "
            "in the project repository."
        ),
        subsection("Initial rhythm"),
        p(
            "Initial rhythm showed the strongest descriptive separation among available variables. "
            "Asystole had a 17.34% ROSC rate, compared with 46.57% for ventricular fibrillation and "
            "57.34% for pulseless ventricular tachycardia. This justified including rhythm in the "
            "baseline model before testing response time's incremental value."
        ),
        report_image("rosc_by_initial_rhythm.png", 6.55 * inch, 3.35 * inch),
        p(
            "AED use also separated outcomes: pre-arrival AED defibrillation was associated with "
            "44.58% ROSC versus 29.17% where no AED was used. These are descriptive associations and "
            "may reflect underlying rhythm and witness differences.",
            "Caption",
        ),
        PageBreak(),
    ]

    # Page 5: Classic subgroup pattern
    story += [
        section("3. Response-Time Pattern in the Classic Utstein Subgroup"),
        p(
            "The classic subgroup provided a clinically familiar, more homogeneous comparison: "
            "presumed-cardiac, bystander-witnessed arrest with an initial shockable rhythm. This "
            "comparator follows the standardized Utstein reporting framework (Bray et al., 2024). "
            "Its 1,777 records were divided into equal-frequency response-time deciles."
        ),
        report_image("rosc_by_response_decile.png", 6.45 * inch, 3.35 * inch),
        styled_table(
            [
                ["Decile", "n", "Median min", "Max min", "ROSC"],
                ["1", "178", "2.06", "2.97", "62.92%"],
                ["2", "179", "3.40", "3.75", "62.01%"],
                ["3", "177", "4.02", "4.30", "57.06%"],
                ["4", "178", "4.73", "5.02", "55.62%"],
                ["5", "180", "5.42", "5.82", "53.89%"],
                ["6", "174", "6.03", "6.45", "48.28%"],
                ["7", "178", "6.98", "7.53", "47.75%"],
                ["8", "177", "8.32", "9.17", "55.37%"],
                ["9", "182", "10.23", "12.00", "52.20%"],
                ["10", "174", "14.66", "55.00", "43.68%"],
            ],
            [0.85 * inch, 0.75 * inch, 1.25 * inch, 1.15 * inch, 1.05 * inch],
            font_size=6.35,
            alignments=["CENTER"] * 5,
        ),
        Spacer(1, 4),
        p(
            "The overall gradient is downward but not perfectly monotonic. Deciles 8 and 9 rebound "
            "relative to deciles 6 and 7, reinforcing the decision to evaluate a nonlinear model and "
            "avoid interpreting the descriptive pattern as a dose-response causal effect.",
            "BodyTiny",
        ),
        PageBreak(),
    ]

    # Page 6: Modeling methods
    story += [
        section("4. Modeling Methods"),
        subsection("Algorithms"),
        bullet("Logistic regression served as the interpretable linear baseline."),
        bullet(
            "Random forest used 300 trees, maximum depth 12, minimum leaf size 10, square-root "
            "feature sampling, and balanced-subsample class weighting."
        ),
        subsection("Model comparison"),
        p(
            "For each algorithm and cohort, a baseline model used age, urbanicity, Census region, "
            "arrest etiology, witness category, pre-arrival AED use, and initial rhythm. The enhanced "
            "model added EMS system response time. Five-fold stratified cross-validation with a fixed "
            "random seed generated out-of-fold probabilities for every record."
        ),
        subsection("Evaluation Metrics Justification"),
        p(
            "<b>Task and model fit:</b> This project is a supervised binary classification task that predicts "
            "whether return of spontaneous circulation (ROSC) was documented for each NEMSIS cardiac-arrest "
            "record. Logistic regression and random forest both produce class probabilities, so discrimination "
            "and positive-case retrieval metrics are appropriate for comparing the two model types."
        ),
        p(
            "<b>ROC AUC:</b> ROC AUC measures how well each model ranks ROSC-positive records above "
            "ROSC-negative records across all possible thresholds instead of depending on one cutoff. This is "
            "appropriate for comparing logistic regression and random forest even though the models can produce "
            "differently distributed probabilities."
        ),
        p(
            "<b>Average precision and class imbalance:</b> The broad cohort contains 5,097 ROSC-positive "
            "records among 17,198 records, a positive rate of 29.64%. Because negative outcomes are the majority, "
            "ordinary accuracy can appear acceptable even when a model performs poorly on the ROSC-positive "
            "class. Average precision is therefore a primary metric because it summarizes precision-recall "
            "performance for the less common positive outcome and can be interpreted relative to the 0.2964 "
            "positive-class prevalence baseline (Saito &amp; Rehmsmeier, 2015)."
        ),
        p(
            "<b>Balanced accuracy and F1:</b> Balanced accuracy gives equal importance to sensitivity for "
            "ROSC-positive records and specificity for ROSC-negative records. F1 summarizes the balance between "
            "precision and recall at the fixed 0.50 threshold. This matters because false positives overstate "
            "ROSC likelihood while false negatives miss positive outcomes. These threshold-dependent metrics "
            "complement, rather than replace, threshold-independent ROC AUC and average precision."
        ),
        p(
            "<b>Validation design:</b> Five-fold stratified cross-validation preserves the ROSC class proportion "
            "within every fold and generates an out-of-fold prediction for every record. This provides a more "
            "stable comparison than one train-test split and reduces the risk that a favorable or unfavorable "
            "single split determines the reported performance."
        ),
        Spacer(1, 6),
        report_image("model_metric_comparison.png", 6.35 * inch, 3.6 * inch),
        PageBreak(),
    ]

    # Page 7: Results
    story += [
        section("5. Model Results"),
        styled_table(
            [
                ["Cohort", "Algorithm", "Response time", "ROC AUC", "Avg. precision", "Accuracy", "Bal. accuracy", "F1"],
                ["Broad", "Logistic", "No", "0.7215", "0.4946", "0.7193", "0.5891", "0.3624"],
                ["Broad", "Logistic", "Yes", "0.7241", "0.4979", "0.7218", "0.5959", "0.3793"],
                ["Broad", "Random forest", "No", "0.7289", "0.5088", "0.6554", "0.6787", "0.5587"],
                ["Broad", "Random forest", "Yes", "0.7321", "0.5160", "0.6591", "0.6805", "0.5604"],
                ["Classic", "Logistic", "No", "0.5947", "0.6129", "0.5774", "0.5682", "0.6363"],
                ["Classic", "Logistic", "Yes", "0.6049", "0.6154", "0.5853", "0.5758", "0.6441"],
                ["Classic", "Random forest", "No", "0.5933", "0.6199", "0.5689", "0.5691", "0.5864"],
                ["Classic", "Random forest", "Yes", "0.6095", "0.6328", "0.5937", "0.5921", "0.6192"],
            ],
            [
                0.57 * inch,
                0.86 * inch,
                0.78 * inch,
                0.68 * inch,
                0.82 * inch,
                0.68 * inch,
                0.78 * inch,
                0.55 * inch,
            ],
            font_size=5.8,
            alignments=["LEFT", "LEFT", "CENTER", "CENTER", "CENTER", "CENTER", "CENTER", "CENTER"],
        ),
        Spacer(1, 6),
        subsection("Broad cohort"),
        p(
            "Adding response time increased logistic ROC AUC by 0.0026 and random-forest ROC AUC by "
            "0.0032. The enhanced random forest achieved the strongest broad-cohort discrimination "
            "(ROC AUC 0.7321; average precision 0.5160). Its raw accuracy was lower than logistic "
            "accuracy because balanced-subsample weighting increased sensitivity to the minority "
            "ROSC-positive class. Its balanced accuracy (0.6805) and F1 (0.5604) were substantially "
            "higher than the enhanced logistic values."
        ),
        subsection("Classic Utstein subgroup"),
        p(
            "Response time produced a larger incremental gain in the standardized subgroup. Logistic "
            "ROC AUC increased by 0.0102, and random-forest ROC AUC increased by 0.0162. The enhanced "
            "random forest also improved average precision by 0.0129 and F1 by 0.0328 compared with "
            "the random-forest baseline. The enhanced logistic model retained the highest "
            "classic-subgroup F1 at the fixed 0.50 threshold, illustrating that model preference "
            "depends on the operational metric."
        ),
        callout(
            "Selection: the enhanced random forest was selected as the leading classifier based on "
            "ROC AUC and average precision. Logistic regression remained an important interpretability benchmark."
        ),
        PageBreak(),
    ]

    # Page 8: Interpretation and limitations
    story += [
        section("6. Interpretation and Operational Relevance"),
        p(
            "The findings align with the department's use of Utstein-style cardiac-arrest review. "
            "The standardized subgroup made the response-time gradient more visible and increased "
            "the incremental model value of response time. This does not mean the subgroup model was "
            "more accurate overall; its smaller sample and reduced case-mix variation limited "
            "discrimination. Instead, the subgroup is useful for comparing a more clinically consistent set of arrests."
        ),
        bullet("Use the broad model for general predictive benchmarking and feature comparison."),
        bullet("Use the classic Utstein analysis for a recognizable quality-review lens."),
        bullet(
            "Report response time as one factor among rhythm, witness status, AED use, etiology, age, and geography."
        ),
        bullet("Do not use this model for individual patient treatment, dispatch prioritization, or causal performance claims."),
        subsection("Bias and Responsible Use"),
        p(
            "<b>Potential sources of bias:</b> NEMSIS is a de-identified convenience sample rather than a "
            "nationally representative patient sample. Participation, case mix, response systems, and documentation "
            "practices can differ across states, agencies, Census regions, and urbanicity categories. Missing and "
            "not-recorded values may reflect agency workflow rather than the patient condition. These differences "
            "can introduce representation bias and measurement bias into both training and evaluation."
        ),
        p(
            "<b>Possible real-world impact:</b> The model may perform better for well-represented agencies or "
            "urban systems and may understate or overstate ROSC probability for rural, frontier, regional, or age "
            "subgroups. If such predictions were used for treatment or dispatch decisions, unequal error rates "
            "could reinforce existing disparities. ROSC is also only an intermediate outcome, so it must not be "
            "treated as a substitute for survival to discharge or favorable neurological outcome."
        ),
        p(
            "<b>Proposed mitigation step:</b> Before any operational use, the model should be externally validated "
            "with data from separate agencies and audited by urbanicity, Census region, and age band using ROC AUC, "
            "average precision, balanced accuracy, recall, and calibration. Material subgroup gaps should trigger "
            "investigation, collection of more representative data, and reweighting or retraining; use should be "
            "withheld for groups that do not demonstrate acceptable performance. Until those checks are completed, "
            "this model remains an educational quality-improvement prototype and must not be used for individual "
            "patient treatment or dispatch prioritization."
        ),
        subsection("Limitations"),
        bullet("NEMSIS is a convenience sample and is not nationally population-based (NEMSIS, 2026)."),
        bullet("Records are EMS activations, not unique patients or incidents; multiple agencies may submit records for one event."),
        bullet(
            "First EMS unit on scene refers to the reporting agency and may not always identify the "
            "first responder across agencies."
        ),
        bullet("Missing and not-recorded values can introduce information bias and may encode documentation practices."),
        bullet("The 50,000-record source sample is a subset of the full 2025 cardiac-arrest population."),
        bullet("ROSC is an intermediate outcome, not survival to discharge or favorable neurological survival."),
        bullet(
            "Unmeasured factors, including CPR quality, exact collapse-to-CPR time, comorbidities, "
            "and agency-level practices, may confound associations."
        ),
        bullet("Cross-validation estimates internal predictive performance within the sample; external validation was not performed."),
        bullet("Random-forest impurity importance is descriptive and can favor continuous or high-cardinality predictors."),
        subsection("Conclusion"),
        callout(
            "EMS system response time improved ROSC prediction in both the broad and classic "
            "Utstein-style cohorts. The incremental gain was most visible in the classic subgroup, "
            "where the slowest response-time decile also had a substantially lower ROSC rate than the "
            "fastest decile. The enhanced random forest offered the strongest threshold-independent "
            "performance, while logistic regression supplied a transparent comparison. These results "
            "support including response time in cardiac-arrest analytics while preserving careful "
            "language: the project demonstrates prediction and association, not causation."
        ),
        PageBreak(),
    ]

    # Page 9: Reproducibility, references, and appendix
    story += [
        section("7. Reproducibility and Data Governance"),
        bullet("Source archive remained outside Git and was never extracted in full."),
        bullet("Preparation scripts streamed selected tables and wrote bounded local CSV files."),
        bullet("The final modeling CSV omitted PcrKey and is ignored by Git."),
        bullet(
            "The executed notebook, preparation script, aggregate results, figures, and requirements "
            "file form the reproducible project record."
        ),
        bullet(
            "NEMSIS confirmed by email that sharing the derived row-level project data with the course "
            "evaluation cohort is permitted; the repository remains private to avoid broader redistribution."
        ),
        subsection("References"),
        p(
            "Bray, J. E., Gr&#228;sner, J.-T., Nolan, J. P., Iwami, T., Ong, M. E. H., Finn, J., "
            "McNally, B., Nehme, Z., Sasson, C., Tijssen, J., Lim, S. L., Tjelmeland, I., "
            "Wnent, J., Dicker, B., Nishiyama, C., Doherty, Z., Welsford, M., Perkins, G. D., "
            "&amp; International Liaison Committee on Resuscitation. "
            "(2024). Cardiac arrest and cardiopulmonary resuscitation outcome reports: 2024 update "
            "of the Utstein Out-of-Hospital Cardiac Arrest Registry template. <i>Circulation, "
            "150</i>(9), e203-e223. https://doi.org/10.1161/CIR.0000000000001243",
            "Reference",
        ),
        p(
            "National Emergency Medical Services Information System. (2024). <i>2024 NEMSIS "
            "Public-Release Research Dataset user manual</i>. National Highway Traffic Safety "
            "Administration. https://nemsis.org/using-ems-data/request-research-data/",
            "Reference",
        ),
        p(
            "National Emergency Medical Services Information System. (2026, May 6). <i>2025 "
            "NEMSIS Public-Release Research Dataset now available</i>. "
            "https://nemsis.org/2025-nemsis-public-release-research-dataset-now-available/",
            "Reference",
        ),
        p(
            "Saito, T., &amp; Rehmsmeier, M. (2015). The precision-recall plot is more informative "
            "than the ROC plot when evaluating binary classifiers on imbalanced datasets. "
            "<i>PLOS ONE, 10</i>(3), e0118432. https://doi.org/10.1371/journal.pone.0118432",
            "Reference",
        ),
        subsection("Appendix: Key NEMSIS code rules"),
        styled_table(
            [
                ["Concept", "Codes used"],
                ["Resuscitation attempted", "eArrest.03 contains 3003001, 3003003, or 3003005"],
                ["ROSC positive", "eArrest.12 contains 3012003, 3012005, or 3012007"],
                ["ROSC negative", "eArrest.12 contains 3012001 without a positive code"],
                ["Bystander witnessed", "eArrest.04 contains 3004003, 3004005, or 3004007 and not 3004001"],
                ["Shockable rhythm", "eArrest.11 contains 3011009, 3011011, or 3011013"],
                ["Presumed cardiac", "eArrest.02 = 3002001"],
                ["First EMS unit", "eScene.01 = 9923003"],
                ["Primary emergency response", "eResponse.05 = 2205001"],
            ],
            [1.55 * inch, 5.1 * inch],
            font_size=6.2,
        ),
    ]
    return story


def main():
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.62 * inch,
        title="Machine Learning Analysis Report: NEMSIS Cardiac-Arrest ROSC Prediction",
        author="Grant Collings",
        subject="Machine learning analysis of EMS response time and ROSC",
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="Report", frames=[frame], onPage=page_header_footer)])
    doc.build(build_story())
    print(f"Created PDF: {OUTPUT.name}")


if __name__ == "__main__":
    main()
