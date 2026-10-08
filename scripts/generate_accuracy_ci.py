"""Regenerate Figure 4 from the per-seed percentage-point differences."""

from pathlib import Path

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor


seeds = [42, 123, 456, 789, 1024, 2048, 4096]
values = [2.00, 0.00, 0.48, -6.98, 4.60, 0.51, 6.00]
mean, ci_low, ci_high = 0.94, -2.91, 4.80

width, height = 446, 226
left, right, bottom, top = 55, 426, 42, 205
y_min, y_max = -8.0, 7.0


def y(value: float) -> float:
    return bottom + (value - y_min) / (y_max - y_min) * (top - bottom)


output = Path(__file__).resolve().parents[1] / "figures" / "fig_accuracy_ci.pdf"
c = canvas.Canvas(str(output), pagesize=(width, height))

# Horizontal grid and y-axis labels.
c.setFont("Helvetica", 8)
for tick in [-8, -6, -4, -2, 0, 2, 4, 6]:
    c.setStrokeColor(HexColor("#E6E6E6") if tick else HexColor("#666666"))
    c.setLineWidth(0.5 if tick else 0.8)
    c.line(left, y(tick), right, y(tick))
    c.setFillColor(HexColor("#333333"))
    c.drawRightString(left - 6, y(tick) - 2.5, str(tick))

# Four-percentage-point non-inferiority margin.
mean_x = right - 22
c.setStrokeColor(HexColor("#C0392B"))
c.setLineWidth(0.9)
c.setDash(4, 3)
c.line(left, y(4), right, y(4))
c.setDash()
c.setFillColor(HexColor("#C0392B"))
c.drawRightString(mean_x - 10, y(4) + 4, "4 pp margin")

# Seed points.
step = 39
x_positions = [left + 23 + i * step for i in range(len(seeds))]
c.setFillColor(HexColor("#2E86AB"))
c.setStrokeColor(HexColor("#111111"))
c.setLineWidth(0.45)
for x_pos, value, seed in zip(x_positions, values, seeds):
    c.circle(x_pos, y(value), 3.2, fill=1, stroke=1)
    c.setFillColor(HexColor("#222222"))
    c.drawCentredString(x_pos, bottom - 14, str(seed))
    c.setFillColor(HexColor("#2E86AB"))

# Mean and confidence interval.
c.setStrokeColor(HexColor("#27AE60"))
c.setFillColor(HexColor("#27AE60"))
c.setLineWidth(1.3)
c.line(mean_x, y(ci_low), mean_x, y(ci_high))
c.line(mean_x - 5, y(ci_low), mean_x + 5, y(ci_low))
c.line(mean_x - 5, y(ci_high), mean_x + 5, y(ci_high))
c.setStrokeColor(HexColor("#111111"))
c.circle(mean_x, y(mean), 3.5, fill=1, stroke=1)
c.setFillColor(HexColor("#27AE60"))
c.drawCentredString(mean_x - 5, top - 2, "+0.94 pp")
c.drawCentredString(mean_x - 5, top - 12, "CI [-2.91, +4.80]")
c.setFillColor(HexColor("#222222"))
c.drawCentredString(mean_x, bottom - 13, "mean")
c.drawCentredString(mean_x, bottom - 23, "(95% CI)")
c.setFillColor(HexColor("#555555"))
c.drawString(left + 5, y(0) + 4, "no difference")

# Axes and labels.
c.setStrokeColor(HexColor("#222222"))
c.setLineWidth(0.8)
c.line(left, bottom, left, top)
c.line(left, bottom, right, bottom)
c.saveState()
c.translate(15, (bottom + top) / 2)
c.rotate(90)
c.setFillColor(HexColor("#222222"))
c.setFont("Helvetica", 9)
c.drawCentredString(0, 0, "Final accuracy delta (Grad - Rand), pp")
c.restoreState()
c.save()
