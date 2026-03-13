#!/usr/bin/env python3
"""
Claude Code 시작하기 - Markdown to PDF converter
Converts all book chapters (markdown) into a single professional PDF with Korean support.
"""

import os
import re
import markdown
from io import BytesIO
from PIL import Image as PILImage

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether, HRFlowable,
    ListFlowable, ListItem, Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tableofcontents import TableOfContents

# ─── Configuration ───
BOOK_DIR = "/Users/robin/Downloads/claude-code-starter/book"
IMAGES_DIR = os.path.join(BOOK_DIR, "images")
OUTPUT_PDF = os.path.join(BOOK_DIR, "Claude_Code_시작하기.pdf")

FONT_PATH = "/Users/robin/Library/Fonts/NotoSansKR-VariableFont_wght.ttf"

# Colors
PRIMARY = HexColor("#4A6CF7")      # Blue
SECONDARY = HexColor("#6366F1")    # Indigo
ACCENT = HexColor("#8B5CF6")       # Purple
DARK = HexColor("#1E293B")         # Dark slate
MEDIUM = HexColor("#475569")       # Slate
LIGHT_BG = HexColor("#F8FAFC")     # Light background
CODE_BG = HexColor("#F1F5F9")      # Code background
TIP_BG = HexColor("#EFF6FF")       # Tip background
WARN_BG = HexColor("#FFF7ED")      # Warning background
BORDER = HexColor("#E2E8F0")       # Border
TIP_BORDER = HexColor("#3B82F6")   # Tip border blue
WARN_BORDER = HexColor("#F59E0B")  # Warning border amber

# Chapter files in order
CHAPTER_FILES = [
    "00_목차.md",
    "01_claude_code란_무엇인가.md",
    "02_설치와_첫_실행.md",
    "03_첫_번째_대화.md",
    "04_터미널_인터페이스.md",
    "05_코드_읽기와_검색.md",
    "06_코드_수정과_생성.md",
    "07_터미널_명령과_테스트.md",
    "08_git_워크플로우.md",
    "09_claude_md.md",
    "10_권한과_보안.md",
    "11_모델과_비용.md",
    "12_컨텍스트_관리.md",
    "13_커맨드와_스킬.md",
    "14_mcp_서버.md",
    "15_훅과_에이전트.md",
    "16_프롬프트_작성법.md",
    "17_실전_워크플로우.md",
    "18_부록.md",
]

# ─── Font Registration ───
def register_fonts():
    pdfmetrics.registerFont(TTFont("NotoSansKR", FONT_PATH))
    pdfmetrics.registerFont(TTFont("NotoSansKR-Bold", FONT_PATH))
    pdfmetrics.registerFontFamily(
        "NotoSansKR",
        normal="NotoSansKR",
        bold="NotoSansKR-Bold",
    )

# ─── Styles ───
def create_styles():
    styles = {}

    styles["title"] = ParagraphStyle(
        "BookTitle",
        fontName="NotoSansKR-Bold",
        fontSize=32,
        leading=42,
        textColor=DARK,
        alignment=TA_CENTER,
        spaceAfter=10 * mm,
    )
    styles["subtitle"] = ParagraphStyle(
        "BookSubtitle",
        fontName="NotoSansKR",
        fontSize=16,
        leading=22,
        textColor=MEDIUM,
        alignment=TA_CENTER,
        spaceAfter=20 * mm,
    )
    styles["h1"] = ParagraphStyle(
        "Heading1",
        fontName="NotoSansKR-Bold",
        fontSize=22,
        leading=30,
        textColor=DARK,
        spaceBefore=12 * mm,
        spaceAfter=6 * mm,
        borderPadding=(0, 0, 2 * mm, 0),
    )
    styles["h2"] = ParagraphStyle(
        "Heading2",
        fontName="NotoSansKR-Bold",
        fontSize=16,
        leading=22,
        textColor=PRIMARY,
        spaceBefore=8 * mm,
        spaceAfter=4 * mm,
    )
    styles["h3"] = ParagraphStyle(
        "Heading3",
        fontName="NotoSansKR-Bold",
        fontSize=13,
        leading=18,
        textColor=SECONDARY,
        spaceBefore=5 * mm,
        spaceAfter=3 * mm,
    )
    styles["h4"] = ParagraphStyle(
        "Heading4",
        fontName="NotoSansKR-Bold",
        fontSize=11,
        leading=15,
        textColor=ACCENT,
        spaceBefore=4 * mm,
        spaceAfter=2 * mm,
    )
    styles["body"] = ParagraphStyle(
        "BodyText",
        fontName="NotoSansKR",
        fontSize=10,
        leading=16,
        textColor=DARK,
        spaceBefore=1 * mm,
        spaceAfter=2 * mm,
        alignment=TA_JUSTIFY,
    )
    styles["code"] = ParagraphStyle(
        "CodeBlock",
        fontName="Courier",
        fontSize=8.5,
        leading=12,
        textColor=DARK,
        spaceBefore=2 * mm,
        spaceAfter=2 * mm,
        leftIndent=5 * mm,
        backColor=CODE_BG,
        borderPadding=6,
    )
    styles["inline_code"] = ParagraphStyle(
        "InlineCode",
        fontName="Courier",
        fontSize=9,
        textColor=HexColor("#C7254E"),
    )
    styles["tip"] = ParagraphStyle(
        "TipBlock",
        fontName="NotoSansKR",
        fontSize=9.5,
        leading=14,
        textColor=HexColor("#1E40AF"),
        spaceBefore=3 * mm,
        spaceAfter=3 * mm,
        leftIndent=8 * mm,
        borderPadding=8,
        backColor=TIP_BG,
    )
    styles["warning"] = ParagraphStyle(
        "WarningBlock",
        fontName="NotoSansKR",
        fontSize=9.5,
        leading=14,
        textColor=HexColor("#92400E"),
        spaceBefore=3 * mm,
        spaceAfter=3 * mm,
        leftIndent=8 * mm,
        borderPadding=8,
        backColor=WARN_BG,
    )
    styles["blockquote"] = ParagraphStyle(
        "Blockquote",
        fontName="NotoSansKR",
        fontSize=10,
        leading=15,
        textColor=MEDIUM,
        spaceBefore=3 * mm,
        spaceAfter=3 * mm,
        leftIndent=8 * mm,
        borderPadding=6,
    )
    styles["table_header"] = ParagraphStyle(
        "TableHeader",
        fontName="NotoSansKR-Bold",
        fontSize=9,
        leading=12,
        textColor=white,
        alignment=TA_CENTER,
    )
    styles["table_cell"] = ParagraphStyle(
        "TableCell",
        fontName="NotoSansKR",
        fontSize=8.5,
        leading=12,
        textColor=DARK,
        alignment=TA_LEFT,
    )
    styles["part_title"] = ParagraphStyle(
        "PartTitle",
        fontName="NotoSansKR-Bold",
        fontSize=26,
        leading=34,
        textColor=PRIMARY,
        alignment=TA_CENTER,
        spaceBefore=40 * mm,
        spaceAfter=10 * mm,
    )
    styles["toc_entry"] = ParagraphStyle(
        "TOCEntry",
        fontName="NotoSansKR",
        fontSize=11,
        leading=18,
        textColor=DARK,
        leftIndent=5 * mm,
    )
    styles["footer"] = ParagraphStyle(
        "Footer",
        fontName="NotoSansKR",
        fontSize=8,
        textColor=MEDIUM,
        alignment=TA_CENTER,
    )
    return styles

# ─── Custom Flowables ───

class ColoredBox(Flowable):
    """A colored box with left border for tips/warnings."""
    def __init__(self, text, style, border_color, bg_color, width=None):
        Flowable.__init__(self)
        self.text = text
        self.style = style
        self.border_color = border_color
        self.bg_color = bg_color
        self._width = width or 160 * mm

    def wrap(self, availWidth, availHeight):
        self._width = availWidth
        p = Paragraph(self.text, self.style)
        pw, ph = p.wrap(availWidth - 12 * mm, availHeight)
        self.para = p
        self.para_height = ph
        return (availWidth, ph + 8 * mm)

    def draw(self):
        canvas = self.canv
        h = self.para_height + 8 * mm
        # Background
        canvas.setFillColor(self.bg_color)
        canvas.roundRect(0, 0, self._width, h, 3, fill=1, stroke=0)
        # Left border
        canvas.setFillColor(self.border_color)
        canvas.roundRect(0, 0, 3 * mm, h, 2, fill=1, stroke=0)
        # Text
        self.para.drawOn(canvas, 6 * mm, 4 * mm)

class CodeBlock(Flowable):
    """A styled code block with background."""
    def __init__(self, code_text, lang="", width=None):
        Flowable.__init__(self)
        self.code_text = code_text
        self.lang = lang
        self._width = width or 160 * mm

    def wrap(self, availWidth, availHeight):
        self._width = availWidth
        lines = self.code_text.split("\n")
        self.lines = lines
        line_height = 11
        self.total_height = len(lines) * line_height + 12 * mm
        return (availWidth, self.total_height)

    def draw(self):
        canvas = self.canv
        h = self.total_height
        w = self._width

        # Background
        canvas.setFillColor(CODE_BG)
        canvas.roundRect(0, 0, w, h, 4, fill=1, stroke=0)

        # Border
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.5)
        canvas.roundRect(0, 0, w, h, 4, fill=0, stroke=1)

        # Language label
        if self.lang:
            canvas.setFillColor(PRIMARY)
            canvas.setFont("NotoSansKR", 7)
            canvas.drawString(8, h - 10, self.lang)

        # Code text
        canvas.setFillColor(DARK)
        canvas.setFont("Courier", 8)
        y = h - (14 if self.lang else 10)
        for line in self.lines:
            if y < 4:
                break
            # Truncate long lines
            display_line = line[:120] if len(line) > 120 else line
            canvas.drawString(8, y, display_line)
            y -= 11


# ─── Markdown Parser ───

class MarkdownToPDF:
    def __init__(self, styles):
        self.styles = styles
        self.story = []

    def parse_file(self, filepath, is_first=False):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if not is_first:
            self.story.append(PageBreak())

        self._parse_content(content)

    def _parse_content(self, content):
        lines = content.split("\n")
        i = 0
        in_code_block = False
        code_lines = []
        code_lang = ""
        in_table = False
        table_rows = []

        while i < len(lines):
            line = lines[i]

            # Code block start/end
            if line.strip().startswith("```"):
                if in_code_block:
                    # End code block
                    code_text = "\n".join(code_lines)
                    if code_text.strip():
                        self.story.append(Spacer(1, 2 * mm))
                        self.story.append(CodeBlock(code_text, code_lang))
                        self.story.append(Spacer(1, 2 * mm))
                    in_code_block = False
                    code_lines = []
                    code_lang = ""
                else:
                    # Flush table if active
                    if in_table:
                        self._flush_table(table_rows)
                        table_rows = []
                        in_table = False
                    # Start code block
                    in_code_block = True
                    code_lang = line.strip()[3:].strip()
                i += 1
                continue

            if in_code_block:
                code_lines.append(line)
                i += 1
                continue

            # Table detection
            if "|" in line and line.strip().startswith("|"):
                # Check if it's a separator row
                stripped = line.strip()
                if re.match(r"^\|[\s\-:|]+\|$", stripped):
                    i += 1
                    continue
                # Parse table row
                cells = [c.strip() for c in stripped.split("|")[1:-1]]
                if cells:
                    if not in_table:
                        in_table = True
                    table_rows.append(cells)
                i += 1
                continue
            else:
                if in_table:
                    self._flush_table(table_rows)
                    table_rows = []
                    in_table = False

            # Empty line
            if not line.strip():
                i += 1
                continue

            # Horizontal rule
            if re.match(r"^---+$", line.strip()):
                self.story.append(Spacer(1, 2 * mm))
                self.story.append(HRFlowable(
                    width="100%", thickness=0.5,
                    color=BORDER, spaceBefore=2*mm, spaceAfter=2*mm
                ))
                i += 1
                continue

            # Image
            img_match = re.match(r"^!\[(.*?)\]\((.*?)\)", line.strip())
            if img_match:
                alt_text = img_match.group(1)
                img_path = img_match.group(2)
                self._add_image(img_path, alt_text)
                i += 1
                continue

            # Headers
            if line.startswith("# "):
                text = self._process_inline(line[2:].strip())
                self.story.append(Paragraph(text, self.styles["h1"]))
                # Add underline
                self.story.append(HRFlowable(
                    width="100%", thickness=1.5,
                    color=PRIMARY, spaceBefore=0, spaceAfter=3*mm
                ))
                i += 1
                continue
            if line.startswith("## "):
                text = self._process_inline(line[3:].strip())
                self.story.append(Paragraph(text, self.styles["h2"]))
                i += 1
                continue
            if line.startswith("### "):
                text = self._process_inline(line[4:].strip())
                self.story.append(Paragraph(text, self.styles["h3"]))
                i += 1
                continue
            if line.startswith("#### "):
                text = self._process_inline(line[5:].strip())
                self.story.append(Paragraph(text, self.styles["h4"]))
                i += 1
                continue

            # Blockquote (tip/warning/note)
            if line.strip().startswith(">"):
                quote_lines = []
                while i < len(lines) and lines[i].strip().startswith(">"):
                    quote_text = lines[i].strip()[1:].strip()
                    quote_lines.append(quote_text)
                    i += 1
                full_quote = " ".join(quote_lines)
                full_quote = self._process_inline(full_quote)

                if "**팁**" in full_quote or "**Tip**" in full_quote.lower():
                    self.story.append(ColoredBox(
                        full_quote, self.styles["tip"],
                        TIP_BORDER, TIP_BG
                    ))
                elif "**주의**" in full_quote or "**Warning**" in full_quote:
                    self.story.append(ColoredBox(
                        full_quote, self.styles["warning"],
                        WARN_BORDER, WARN_BG
                    ))
                elif "**핵심 정리**" in full_quote or "**핵심**" in full_quote:
                    self.story.append(ColoredBox(
                        full_quote, self.styles["tip"],
                        ACCENT, HexColor("#F5F3FF")
                    ))
                else:
                    self.story.append(ColoredBox(
                        full_quote, self.styles["blockquote"],
                        BORDER, LIGHT_BG
                    ))
                continue

            # List items
            if re.match(r"^(\s*)[-*]\s", line):
                list_items = []
                while i < len(lines) and re.match(r"^(\s*)[-*]\s", lines[i]):
                    item_text = re.sub(r"^(\s*)[-*]\s", "", lines[i]).strip()
                    item_text = self._process_inline(item_text)
                    list_items.append(item_text)
                    i += 1
                for item in list_items:
                    bullet_text = f"  \u2022  {item}"
                    self.story.append(Paragraph(bullet_text, self.styles["body"]))
                continue

            # Numbered list
            if re.match(r"^(\s*)\d+\.\s", line):
                while i < len(lines) and re.match(r"^(\s*)\d+\.\s", lines[i]):
                    num_match = re.match(r"^(\s*)(\d+)\.\s(.*)", lines[i])
                    if num_match:
                        num = num_match.group(2)
                        item_text = self._process_inline(num_match.group(3).strip())
                        self.story.append(Paragraph(
                            f"  {num}.  {item_text}", self.styles["body"]
                        ))
                    i += 1
                continue

            # Regular paragraph
            para_lines = []
            while i < len(lines) and lines[i].strip() and \
                  not lines[i].startswith("#") and \
                  not lines[i].startswith(">") and \
                  not lines[i].strip().startswith("```") and \
                  not lines[i].strip().startswith("|") and \
                  not re.match(r"^---+$", lines[i].strip()) and \
                  not re.match(r"^!\[", lines[i].strip()) and \
                  not re.match(r"^(\s*)[-*]\s", lines[i]) and \
                  not re.match(r"^(\s*)\d+\.\s", lines[i]):
                para_lines.append(lines[i].strip())
                i += 1

            if para_lines:
                text = " ".join(para_lines)
                text = self._process_inline(text)
                self.story.append(Paragraph(text, self.styles["body"]))
                continue

            i += 1

        # Flush remaining table
        if in_table:
            self._flush_table(table_rows)

    def _process_inline(self, text):
        """Process inline markdown formatting."""
        # Escape XML special chars first
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")

        # 1. Extract inline code FIRST to protect from further processing
        code_placeholders = {}
        counter = [0]
        def replace_code(m):
            key = f"\x00CODE{counter[0]}\x00"
            code_placeholders[key] = f'<font face="Courier" size="8" color="#C7254E">{m.group(1)}</font>'
            counter[0] += 1
            return key
        text = re.sub(r"`([^`]+)`", replace_code, text)

        # 2. Bold + italic
        text = re.sub(r"\*\*\*(.*?)\*\*\*", r'<b><i>\1</i></b>', text)
        # 3. Bold
        text = re.sub(r"\*\*(.*?)\*\*", r'<b>\1</b>', text)
        # 4. Italic (only match single * pairs that don't look like wildcards)
        text = re.sub(r"(?<!\w)\*([^\*\n]+?)\*(?!\w)", r'<i>\1</i>', text)
        # 5. Links - just show text
        text = re.sub(r"\[(.*?)\]\(.*?\)", r'<u>\1</u>', text)
        # 6. Strikethrough
        text = re.sub(r"~~(.*?)~~", r'<strike>\1</strike>', text)
        # 7. Checkbox
        text = text.replace("- [ ]", "\u2610")
        text = text.replace("- [x]", "\u2611")

        # 8. Restore inline code
        for key, val in code_placeholders.items():
            text = text.replace(key, val)

        return text

    def _add_image(self, img_path, alt_text):
        """Add image to story."""
        full_path = os.path.join(BOOK_DIR, img_path)
        if not os.path.exists(full_path):
            self.story.append(Paragraph(
                f"[Image not found: {img_path}]", self.styles["body"]
            ))
            return

        try:
            pil_img = PILImage.open(full_path)
            img_w, img_h = pil_img.size

            # Scale to fit page width (max 150mm) while maintaining aspect ratio
            max_width = 150 * mm
            max_height = 180 * mm
            aspect = img_h / img_w

            width = min(max_width, img_w * 0.264)  # px to mm approx
            height = width * aspect

            if height > max_height:
                height = max_height
                width = height / aspect

            self.story.append(Spacer(1, 3 * mm))
            img = Image(full_path, width=width, height=height)
            self.story.append(img)

            # Caption
            if alt_text:
                caption_style = ParagraphStyle(
                    "ImageCaption",
                    fontName="NotoSansKR",
                    fontSize=8,
                    leading=12,
                    textColor=MEDIUM,
                    alignment=TA_CENTER,
                    spaceBefore=1 * mm,
                    spaceAfter=3 * mm,
                )
                self.story.append(Paragraph(alt_text, caption_style))
            self.story.append(Spacer(1, 2 * mm))
        except Exception as e:
            self.story.append(Paragraph(
                f"[Image error: {img_path} - {e}]", self.styles["body"]
            ))

    def _flush_table(self, rows):
        """Convert table rows to a ReportLab Table."""
        if not rows:
            return

        # Normalize column count
        max_cols = max(len(r) for r in rows)
        for r in rows:
            while len(r) < max_cols:
                r.append("")

        # First row is header
        header = rows[0]
        data_rows = rows[1:] if len(rows) > 1 else []

        # Build table data with Paragraphs
        table_data = []

        # Header row
        header_cells = []
        for cell in header:
            cell = self._process_inline(cell)
            header_cells.append(Paragraph(cell, self.styles["table_header"]))
        table_data.append(header_cells)

        # Data rows
        for row in data_rows:
            row_cells = []
            for cell in row:
                cell = self._process_inline(cell)
                row_cells.append(Paragraph(cell, self.styles["table_cell"]))
            table_data.append(row_cells)

        if not table_data:
            return

        # Calculate column widths
        avail_width = 165 * mm
        col_width = avail_width / max_cols

        try:
            table = Table(table_data, colWidths=[col_width] * max_cols)
            table.setStyle(TableStyle([
                # Header
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("FONTNAME", (0, 0), (-1, 0), "NotoSansKR-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("TOPPADDING", (0, 0), (-1, 0), 6),
                # Body
                ("FONTNAME", (0, 1), (-1, -1), "NotoSansKR"),
                ("FONTSIZE", (0, 1), (-1, -1), 8.5),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
                ("TOPPADDING", (0, 1), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                # Grid
                ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                # Alternating rows
                *[("BACKGROUND", (0, i), (-1, i), LIGHT_BG)
                  for i in range(2, len(table_data), 2)],
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))

            self.story.append(Spacer(1, 2 * mm))
            self.story.append(table)
            self.story.append(Spacer(1, 2 * mm))
        except Exception as e:
            self.story.append(Paragraph(f"[Table error: {e}]", self.styles["body"]))


# ─── Page Template ───

def add_page_number(canvas, doc):
    """Add page numbers and header/footer."""
    canvas.saveState()
    page_num = doc.page

    # Footer line
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, 15 * mm, 190 * mm, 15 * mm)

    # Page number
    canvas.setFont("NotoSansKR", 8)
    canvas.setFillColor(MEDIUM)
    canvas.drawCentredString(105 * mm, 10 * mm, f"— {page_num} —")

    # Header line (after first page)
    if page_num > 1:
        canvas.setStrokeColor(BORDER)
        canvas.line(20 * mm, 282 * mm, 190 * mm, 282 * mm)
        canvas.setFont("NotoSansKR", 7)
        canvas.setFillColor(MEDIUM)
        canvas.drawString(20 * mm, 284 * mm, "Claude Code 시작하기")

    canvas.restoreState()


# ─── Cover Page ───

def create_cover_page(story, styles):
    """Create the book cover page."""
    story.append(Spacer(1, 50 * mm))

    # Title
    story.append(Paragraph("Claude Code 시작하기", styles["title"]))
    story.append(Spacer(1, 5 * mm))

    # Subtitle
    story.append(Paragraph("AI와 함께 코딩하는 새로운 방법", styles["subtitle"]))

    # Decorative line
    story.append(HRFlowable(
        width="40%", thickness=2, color=PRIMARY,
        spaceBefore=10*mm, spaceAfter=10*mm, hAlign="CENTER"
    ))

    # Description
    desc_style = ParagraphStyle(
        "CoverDesc",
        fontName="NotoSansKR",
        fontSize=11,
        leading=18,
        textColor=MEDIUM,
        alignment=TA_CENTER,
    )
    story.append(Paragraph(
        "설치부터 고급 기능까지, 단계별로 Claude Code의 모든 것을 다룹니다.",
        desc_style
    ))
    story.append(Spacer(1, 30 * mm))

    # Date
    story.append(Paragraph("2026년 3월", desc_style))

    story.append(PageBreak())


# ─── Main Build ───

def build_pdf():
    print("📖 PDF 빌드를 시작합니다...")

    # Register fonts
    register_fonts()
    print("  ✓ 한글 폰트 등록 완료 (NotoSansKR)")

    # Create styles
    styles = create_styles()

    # Create document
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        topMargin=22 * mm,
        bottomMargin=20 * mm,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        title="Claude Code 시작하기",
        author="Claude Code Book Project",
        subject="AI와 함께 코딩하는 새로운 방법",
    )

    # Parser
    parser = MarkdownToPDF(styles)

    # Cover page
    create_cover_page(parser.story, styles)

    # Process each chapter
    for idx, filename in enumerate(CHAPTER_FILES):
        filepath = os.path.join(BOOK_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  ⚠ 파일 없음: {filename}")
            continue

        print(f"  ✓ 처리 중: {filename}")
        parser.parse_file(filepath, is_first=False)

    print(f"  ✓ 총 {len(parser.story)} 개의 요소 생성")

    # Build
    print("  ✓ PDF 렌더링 중...")
    doc.build(parser.story, onFirstPage=add_page_number, onLaterPages=add_page_number)

    # File size
    size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
    print(f"\n✅ PDF 생성 완료!")
    print(f"   📄 {OUTPUT_PDF}")
    print(f"   📏 {size_mb:.1f} MB")


if __name__ == "__main__":
    build_pdf()
