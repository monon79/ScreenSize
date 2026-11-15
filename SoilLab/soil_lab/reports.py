from io import BytesIO
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def build_excel_report(results, params, recovery):
    buffer = BytesIO()
    summary = pd.DataFrame([
        {"Parameter": key, "Value": value}
        for key, value in params.items()
    ] + [{"Parameter": "Mass recovery (%)", "Value": recovery}])

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        results.to_excel(writer, sheet_name="Sieve Analysis", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)
    return buffer.getvalue()


def build_pdf_report(results, params, recovery):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=36, leftMargin=36, topMargin=40, bottomMargin=36
    )
    styles = getSampleStyleSheet()
    story = [
        Paragraph("SoilLab – Sieve Analysis Report", styles["Title"]),
        Spacer(1, 8),
        Paragraph(
            "Particle-size distribution calculation report. "
            "Review sample identification, laboratory procedure and mass recovery "
            "before using the results for design.",
            styles["BodyText"],
        ),
        Spacer(1, 12),
        Paragraph(f"Mass recovery: {recovery:.2f}%", styles["Heading2"]),
        Spacer(1, 8),
        Paragraph("Characteristic particle sizes", styles["Heading2"]),
    ]

    summary_rows = [["Parameter", "Value"]]
    for key in ["D10", "D30", "D40", "D60", "D70", "Cu", "Cc"]:
        value = params.get(key)
        summary_rows.append([key, "Not bracketed" if value is None else f"{value:.5g}"])

    summary_table = Table(summary_rows, colWidths=[180, 180])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#173B56")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [summary_table, Spacer(1, 14),
              Paragraph("Sieve analysis table", styles["Heading2"])]

    table_data = [[
        "Sieve (mm)", "Retained (g)", "% Retained",
        "Cum. % Retained", "% Passing"
    ]]
    for _, row in results.iterrows():
        table_data.append([
            f'{row["sieve_mm"]:g}',
            f'{row["retained_g"]:.2f}',
            f'{row["percent_retained"]:.2f}',
            f'{row["cumulative_retained_pct"]:.2f}',
            f'{row["percent_passing"]:.2f}',
        ])

    data_table = Table(table_data, repeatRows=1, colWidths=[75, 85, 75, 95, 75])
    data_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#173B56")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    story += [data_table, Spacer(1, 14),
              Paragraph(
                  "Note: D-values are obtained by interpolation on the logarithmic "
                  "particle-size axis. This report does not certify the suitability "
                  "of a well screen or filter pack.",
                  styles["Italic"],
              )]
    doc.build(story)
    return buffer.getvalue()
