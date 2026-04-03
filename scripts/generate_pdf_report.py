#!/usr/bin/env python3
"""
営業パイプライン PDF レポートジェネレーター — AI Sales Team for Claude Code

スコアゲージ・棒グラフ・見込み客カード・パイプラインサマリーテーブル・
優先アクションプランを含む、プロフェッショナルな複数ページのPDFを生成します。

使い方:
    python3 generate_pdf_report.py <json_data_file> [output_pdf_file]
    python3 generate_pdf_report.py  # デモモードでサンプルレポートを生成
"""

import json
import math
import sys
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Circle, String, Line, Rect, Wedge
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics

# --- 日本語フォントのセットアップ ---
JP_FONT = "Helvetica"
JP_FONT_BOLD = "Helvetica-Bold"


def setup_japanese_fonts():
    """日本語フォントを登録する。利用可能なフォントを自動検出する。"""
    global JP_FONT, JP_FONT_BOLD

    # 方法1: reportlab 内蔵の CID フォント（外部フォント不要）
    try:
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
        JP_FONT = 'HeiseiKakuGo-W5'
        JP_FONT_BOLD = 'HeiseiKakuGo-W5'
        return True
    except Exception:
        pass

    # 方法2: システムフォント（TTFont）を検索
    from reportlab.pdfbase.ttfonts import TTFont

    candidates = [
        # macOS
        ('/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc', '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
         'HiraginoBold', 'HiraginoRegular'),
        ('/Library/Fonts/NotoSansCJKjp-Regular.otf', '/Library/Fonts/NotoSansCJKjp-Bold.otf',
         'NotoSansJP', 'NotoSansJP-Bold'),
        # Homebrew / 一般的なパス
        ('/usr/local/share/fonts/NotoSansCJKjp-Regular.otf',
         '/usr/local/share/fonts/NotoSansCJKjp-Bold.otf',
         'NotoSansJP', 'NotoSansJP-Bold'),
        # Linux
        ('/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf',
         '/usr/share/fonts/opentype/noto/NotoSansCJKjp-Bold.otf',
         'NotoSansJP', 'NotoSansJP-Bold'),
        ('/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf',
         '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf',
         'IPAGothic', 'IPAGothic'),
        # Windows
        ('C:/Windows/Fonts/meiryo.ttc', 'C:/Windows/Fonts/meiryob.ttc',
         'Meiryo', 'Meiryo-Bold'),
        ('C:/Windows/Fonts/msgothic.ttc', 'C:/Windows/Fonts/msgothic.ttc',
         'MSGothic', 'MSGothic'),
    ]

    for regular_path, bold_path, regular_name, bold_name in candidates:
        if os.path.exists(regular_path):
            try:
                pdfmetrics.registerFont(TTFont(regular_name, regular_path))
                if os.path.exists(bold_path) and bold_path != regular_path:
                    try:
                        pdfmetrics.registerFont(TTFont(bold_name, bold_path))
                    except Exception:
                        bold_name = regular_name
                else:
                    bold_name = regular_name
                JP_FONT = regular_name
                JP_FONT_BOLD = bold_name
                return True
            except Exception:
                continue

    # フォントが見つからない場合の警告
    print("警告: 日本語フォントが見つかりませんでした。日本語テキストが正しく表示されない可能性があります。")
    print("  解決方法: 以下のいずれかをインストールしてください:")
    print("    macOS: brew install font-noto-sans-cjk-japanese")
    print("    Linux: sudo apt install fonts-noto-cjk")
    print("    Windows: Meiryo フォント（標準搭載）を確認してください")
    return False


# フォントを初期化
setup_japanese_fonts()

# --- カラーパレット ---
PRIMARY = colors.HexColor("#1B2A4A")       # ダークネイビー
ACCENT = colors.HexColor("#0EA5E9")        # セールスブルー
HIGHLIGHT = colors.HexColor("#F59E0B")     # アンバー/ゴールド
SUCCESS = colors.HexColor("#10B981")       # グリーン
WARNING = colors.HexColor("#F59E0B")       # アンバー
DANGER = colors.HexColor("#EF4444")        # レッド
LIGHT_BG = colors.HexColor("#F0F9FF")      # 薄いブルー
BODY_TEXT = colors.HexColor("#1E293B")
SECONDARY_TEXT = colors.HexColor("#64748B")
BORDER = colors.HexColor("#CBD5E1")
WHITE = colors.white
GRADE_A_BG = colors.HexColor("#ECFDF5")
GRADE_B_BG = colors.HexColor("#EFF6FF")
GRADE_C_BG = colors.HexColor("#FFFBEB")
GRADE_D_BG = colors.HexColor("#FEF2F2")


def score_color(score):
    """スコアに基づいて色を返す。"""
    if score >= 80:
        return SUCCESS
    elif score >= 60:
        return ACCENT
    elif score >= 40:
        return WARNING
    else:
        return DANGER


def grade_color(grade):
    """グレードに基づいて色を返す。"""
    grade_map = {"A": SUCCESS, "B": ACCENT, "C": WARNING, "D": DANGER}
    return grade_map.get(grade, SECONDARY_TEXT)


def grade_bg(grade):
    """グレードに基づいて背景色を返す。"""
    bg_map = {"A": GRADE_A_BG, "B": GRADE_B_BG, "C": GRADE_C_BG, "D": GRADE_D_BG}
    return bg_map.get(grade, LIGHT_BG)


def build_styles():
    """レポート用の全段落スタイルを構築する。"""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CoverTitle",
        fontName=JP_FONT_BOLD,
        fontSize=28,
        textColor=PRIMARY,
        alignment=TA_LEFT,
        spaceAfter=6,
        leading=34,
    ))
    styles.add(ParagraphStyle(
        name="CoverSubtitle",
        fontName=JP_FONT,
        fontSize=14,
        textColor=SECONDARY_TEXT,
        alignment=TA_LEFT,
        spaceAfter=4,
        leading=18,
    ))
    styles.add(ParagraphStyle(
        name="SectionTitle",
        fontName=JP_FONT_BOLD,
        fontSize=20,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=10,
        leading=26,
    ))
    styles.add(ParagraphStyle(
        name="SubSection",
        fontName=JP_FONT_BOLD,
        fontSize=13,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=6,
        leading=17,
    ))
    styles.add(ParagraphStyle(
        name="BodyText2",
        fontName=JP_FONT,
        fontSize=10,
        textColor=BODY_TEXT,
        spaceAfter=6,
        leading=16,
    ))
    styles.add(ParagraphStyle(
        name="SmallText",
        fontName=JP_FONT,
        fontSize=8,
        textColor=SECONDARY_TEXT,
        leading=11,
    ))
    styles.add(ParagraphStyle(
        name="TableCell",
        fontName=JP_FONT,
        fontSize=9,
        textColor=BODY_TEXT,
        leading=13,
    ))
    styles.add(ParagraphStyle(
        name="TableHeader",
        fontName=JP_FONT_BOLD,
        fontSize=9,
        textColor=WHITE,
        leading=12,
    ))
    styles.add(ParagraphStyle(
        name="ActionItem",
        fontName=JP_FONT,
        fontSize=10,
        textColor=BODY_TEXT,
        leftIndent=20,
        spaceAfter=4,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="ProspectName",
        fontName=JP_FONT_BOLD,
        fontSize=12,
        textColor=PRIMARY,
        spaceAfter=2,
        leading=16,
    ))
    styles.add(ParagraphStyle(
        name="ProspectDetail",
        fontName=JP_FONT,
        fontSize=9,
        textColor=BODY_TEXT,
        leading=13,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name="FooterText",
        fontName=JP_FONT,
        fontSize=7,
        textColor=SECONDARY_TEXT,
        alignment=TA_CENTER,
    ))
    return styles


def draw_score_gauge(score, size=180):
    """カラーリングと中央スコア数値を持つ円形スコアゲージを描画する。"""
    d = Drawing(size, size + 20)
    cx, cy = size / 2, size / 2 + 10
    radius = size / 2 - 10

    # 背景円（トラック）
    d.add(Circle(cx, cy, radius, fillColor=LIGHT_BG, strokeColor=BORDER, strokeWidth=2))

    # スコア弧
    col = score_color(score)
    angle_extent = (score / 100) * 360
    if angle_extent > 0:
        d.add(Wedge(cx, cy, radius, 90, 90 - angle_extent,
                     fillColor=col, strokeColor=col, strokeWidth=0))

    # 内側の白い円（ドーナツ効果）
    inner_r = radius * 0.65
    d.add(Circle(cx, cy, inner_r, fillColor=WHITE, strokeColor=WHITE, strokeWidth=0))

    # スコア数値
    d.add(String(cx, cy + 8, str(score),
                 fontSize=36, fontName=JP_FONT_BOLD,
                 fillColor=PRIMARY, textAnchor="middle"))
    d.add(String(cx, cy - 14, "パイプラインスコア",
                 fontSize=8, fontName=JP_FONT,
                 fillColor=SECONDARY_TEXT, textAnchor="middle"))

    # グレードラベル
    if score >= 75:
        grade = "A"
    elif score >= 50:
        grade = "B"
    elif score >= 25:
        grade = "C"
    else:
        grade = "D"

    d.add(String(cx, cy - 32, f"グレード: {grade}",
                 fontSize=12, fontName=JP_FONT_BOLD,
                 fillColor=col, textAnchor="middle"))

    return d


def create_bar_chart(categories, width=480, height=200):
    """カテゴリスコアの横棒グラフを描画する。"""
    d = Drawing(width, height)

    names = list(categories.keys())
    scores = [categories[n]["score"] for n in names]

    chart = HorizontalBarChart()
    chart.x = 160
    chart.y = 10
    chart.width = width - 180
    chart.height = height - 20
    chart.data = [scores]
    chart.categoryAxis.categoryNames = names
    chart.categoryAxis.labels.fontName = JP_FONT
    chart.categoryAxis.labels.fontSize = 8
    chart.categoryAxis.labels.fillColor = BODY_TEXT
    chart.categoryAxis.visibleGrid = False
    chart.categoryAxis.visibleAxis = False
    chart.categoryAxis.visibleTicks = False

    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 100
    chart.valueAxis.valueStep = 20
    chart.valueAxis.labels.fontName = JP_FONT
    chart.valueAxis.labels.fontSize = 7
    chart.valueAxis.labels.fillColor = SECONDARY_TEXT
    chart.valueAxis.visibleGrid = True
    chart.valueAxis.gridStrokeColor = BORDER
    chart.valueAxis.gridStrokeWidth = 0.5
    chart.valueAxis.visibleAxis = False
    chart.valueAxis.visibleTicks = False

    chart.bars[0].fillColor = ACCENT
    chart.barWidth = 14
    chart.barSpacing = 6

    # スコアに応じて各バーの色を設定
    bar_colors = [score_color(s) for s in scores]
    for i, col in enumerate(bar_colors):
        chart.bars[(0, i)].fillColor = col

    d.add(chart)

    # 各バーの末尾にスコアラベルを追加
    bar_total_height = len(names) * (chart.barWidth + chart.barSpacing)
    start_y = chart.y + (chart.height - bar_total_height) / 2
    for i, s in enumerate(scores):
        bar_y = start_y + i * (chart.barWidth + chart.barSpacing) + chart.barWidth / 2
        bar_end_x = chart.x + (s / 100) * chart.width + 4
        d.add(String(bar_end_x, bar_y - 3, str(s),
                     fontSize=8, fontName=JP_FONT_BOLD,
                     fillColor=score_color(s), textAnchor="start"))

    return d


def add_header_footer(canvas, doc, report_title=""):
    """各ページにヘッダーとフッターを追加する。"""
    canvas.saveState()
    # ヘッダーライン
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(2)
    canvas.line(54, letter[1] - 40, letter[0] - 54, letter[1] - 40)

    # ヘッダーテキスト
    canvas.setFont(JP_FONT_BOLD, 8)
    canvas.setFillColor(PRIMARY)
    canvas.drawString(54, letter[1] - 35, f"営業パイプラインレポート — {report_title}")

    canvas.setFont(JP_FONT, 8)
    canvas.setFillColor(SECONDARY_TEXT)
    canvas.drawRightString(letter[0] - 54, letter[1] - 35, f"{doc.page} ページ")

    # フッターライン
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(54, 40, letter[0] - 54, 40)

    # フッターテキスト
    canvas.setFont(JP_FONT, 7)
    canvas.setFillColor(SECONDARY_TEXT)
    canvas.drawCentredString(letter[0] / 2, 28,
                              "AI Sales Team for Claude Code による自動生成")
    canvas.restoreState()


def generate_report(data, output_path):
    """データ辞書から完全な PDF レポートを生成する。"""
    styles = build_styles()
    report_date = data.get("date", "")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    story = []

    # ==================== 1ページ目: 表紙 ====================
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("営業パイプラインレポート", styles["CoverTitle"]))
    story.append(Spacer(1, 40))
    story.append(Paragraph(f"<b>{report_date}</b>", styles["CoverSubtitle"]))

    pipeline_health = data.get("pipeline_health", {})
    total_prospects = pipeline_health.get("total_prospects", 0)
    if total_prospects:
        story.append(Spacer(1, 30))
        story.append(Paragraph(f"{total_prospects} 件の見込み客を分析", styles["CoverSubtitle"]))
    story.append(Spacer(1, 60))

    # 総合パイプラインスコアゲージ
    overall_score = data.get("overall_pipeline_score", 0)
    gauge = draw_score_gauge(overall_score)
    story.append(gauge)
    story.append(Spacer(1, 40))

    # エグゼクティブサマリー
    summary = data.get("executive_summary", "")
    if summary:
        story.append(Paragraph("エグゼクティブサマリー", styles["SubSection"]))
        story.append(Paragraph(summary, styles["BodyText2"]))

    story.append(PageBreak())

    # ==================== 2ページ目: スコア内訳 ====================
    story.append(Paragraph("スコア内訳", styles["SectionTitle"]))
    story.append(Spacer(1, 6))

    categories = data.get("categories", {})
    if categories:
        chart = create_bar_chart(categories)
        story.append(chart)
        story.append(Spacer(1, 16))

        # スコア比較テーブル
        header = [
            Paragraph("<b>カテゴリ</b>", styles["TableHeader"]),
            Paragraph("<b>スコア</b>", styles["TableHeader"]),
            Paragraph("<b>評価</b>", styles["TableHeader"]),
        ]
        table_data = [header]

        for cat_name, cat_info in categories.items():
            s = cat_info.get("score", 0)
            col = score_color(s)
            hex_col = col.hexval() if hasattr(col, 'hexval') else str(col)
            if s >= 80:
                label = "良好"
            elif s >= 60:
                label = "適切"
            elif s >= 40:
                label = "要改善"
            else:
                label = "要注意"

            table_data.append([
                Paragraph(cat_name, styles["TableCell"]),
                Paragraph(f"<b>{s}/100</b>", styles["TableCell"]),
                Paragraph(f'<font color="{hex_col}"><b>{label}</b></font>', styles["TableCell"]),
            ])

        # 総合行
        overall_col = score_color(overall_score)
        hex_overall = overall_col.hexval() if hasattr(overall_col, 'hexval') else str(overall_col)
        table_data.append([
            Paragraph("<b>パイプライン総合</b>", styles["TableCell"]),
            Paragraph(f"<b>{overall_score}/100</b>", styles["TableCell"]),
            Paragraph(f'<font color="{hex_overall}"><b>パイプラインスコア</b></font>', styles["TableCell"]),
        ])

        col_widths = [200, 100, 100]
        t = Table(table_data, colWidths=col_widths)
        t_style = [
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
            ("TOPPADDING", (0, 1), (-1, -1), 6),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("BACKGROUND", (0, -1), (-1, -1), LIGHT_BG),
        ]
        for i in range(1, len(table_data) - 1):
            if i % 2 == 0:
                t_style.append(("BACKGROUND", (0, i), (-1, i), LIGHT_BG))
        t.setStyle(TableStyle(t_style))
        story.append(t)

    story.append(PageBreak())

    # ==================== 3ページ目: トップ見込み客 ====================
    prospects = data.get("prospects", [])
    if prospects:
        story.append(Paragraph("トップ見込み客", styles["SectionTitle"]))
        story.append(Spacer(1, 6))

        # 上位5社を詳細カードで表示
        for i, prospect in enumerate(prospects[:5]):
            name = prospect.get("name", "不明")
            p_score = prospect.get("score", 0)
            p_grade = prospect.get("grade", "?")
            stage = prospect.get("stage", "不明")
            url = prospect.get("url", "")
            next_action = prospect.get("next_action", "")

            col = score_color(p_score)
            hex_col = col.hexval() if hasattr(col, 'hexval') else str(col)
            g_col = grade_color(p_grade)
            hex_g = g_col.hexval() if hasattr(g_col, 'hexval') else str(g_col)

            # 見込み客カード（ミニテーブル）
            card_data = [
                [
                    Paragraph(f'<b>{i+1}. {name}</b>', styles["ProspectName"]),
                    Paragraph(f'<font color="{hex_col}" size="14"><b>{p_score}</b></font>', styles["TableCell"]),
                    Paragraph(f'<font color="{hex_g}" size="12"><b>{p_grade}</b></font>', styles["TableCell"]),
                ],
                [
                    Paragraph(f'ステージ: <b>{stage}</b> &nbsp;&nbsp; {url}', styles["ProspectDetail"]),
                    Paragraph("スコア", styles["SmallText"]),
                    Paragraph("グレード", styles["SmallText"]),
                ],
            ]
            if next_action:
                card_data.append([
                    Paragraph(f'次のアクション: <i>{next_action}</i>', styles["ProspectDetail"]),
                    Paragraph("", styles["SmallText"]),
                    Paragraph("", styles["SmallText"]),
                ])

            card = Table(card_data, colWidths=[340, 50, 50])
            card_style = [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                ("SPAN", (0, -1), (-1, -1)) if next_action else ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOX", (0, 0), (-1, -1), 1, BORDER),
                ("BACKGROUND", (0, 0), (-1, -1), grade_bg(p_grade)),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
            card.setStyle(TableStyle(card_style))
            story.append(KeepTogether([card, Spacer(1, 8)]))

    story.append(PageBreak())

    # ==================== 4ページ目: パイプラインサマリー ====================
    if prospects:
        story.append(Paragraph("パイプラインサマリー", styles["SectionTitle"]))
        story.append(Spacer(1, 6))

        header = [
            Paragraph("<b>企業名</b>", styles["TableHeader"]),
            Paragraph("<b>スコア</b>", styles["TableHeader"]),
            Paragraph("<b>グレード</b>", styles["TableHeader"]),
            Paragraph("<b>ステージ</b>", styles["TableHeader"]),
            Paragraph("<b>次のアクション</b>", styles["TableHeader"]),
        ]
        table_data = [header]

        for prospect in prospects:
            p_score = prospect.get("score", 0)
            p_grade = prospect.get("grade", "?")
            col = score_color(p_score)
            hex_col = col.hexval() if hasattr(col, 'hexval') else str(col)
            g_col = grade_color(p_grade)
            hex_g = g_col.hexval() if hasattr(g_col, 'hexval') else str(g_col)

            table_data.append([
                Paragraph(prospect.get("name", ""), styles["TableCell"]),
                Paragraph(f'<font color="{hex_col}"><b>{p_score}</b></font>', styles["TableCell"]),
                Paragraph(f'<font color="{hex_g}"><b>{p_grade}</b></font>', styles["TableCell"]),
                Paragraph(prospect.get("stage", ""), styles["TableCell"]),
                Paragraph(prospect.get("next_action", ""), styles["TableCell"]),
            ])

        col_widths = [110, 45, 40, 80, 225]
        t = Table(table_data, colWidths=col_widths)
        t_style = [
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("ALIGN", (1, 0), (2, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
            ("TOPPADDING", (0, 1), (-1, -1), 5),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ]
        for i in range(1, len(table_data)):
            if i % 2 == 0:
                t_style.append(("BACKGROUND", (0, i), (-1, i), LIGHT_BG))
        t.setStyle(TableStyle(t_style))
        story.append(t)

        # パイプライン健全性サマリー
        if pipeline_health:
            story.append(Spacer(1, 16))
            story.append(Paragraph("パイプライン健全性", styles["SubSection"]))

            health_data = [
                [
                    Paragraph("<b>見込み客数</b>", styles["TableCell"]),
                    Paragraph("<b>平均スコア</b>", styles["TableCell"]),
                    Paragraph("<b>Aグレード</b>", styles["TableCell"]),
                    Paragraph("<b>Bグレード</b>", styles["TableCell"]),
                    Paragraph("<b>Cグレード</b>", styles["TableCell"]),
                    Paragraph("<b>Dグレード</b>", styles["TableCell"]),
                ],
                [
                    Paragraph(str(pipeline_health.get("total_prospects", 0)), styles["TableCell"]),
                    Paragraph(str(pipeline_health.get("avg_score", 0)), styles["TableCell"]),
                    Paragraph(str(pipeline_health.get("a_grade", 0)), styles["TableCell"]),
                    Paragraph(str(pipeline_health.get("b_grade", 0)), styles["TableCell"]),
                    Paragraph(str(pipeline_health.get("c_grade", 0)), styles["TableCell"]),
                    Paragraph(str(pipeline_health.get("d_grade", 0)), styles["TableCell"]),
                ],
            ]
            ht = Table(health_data, colWidths=[83, 83, 83, 83, 83, 83])
            ht_style = [
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
            ]
            ht.setStyle(TableStyle(ht_style))
            story.append(ht)

    story.append(PageBreak())

    # ==================== 5ページ目: アクションプラン ====================
    story.append(Paragraph("アクションプラン", styles["SectionTitle"]))
    story.append(Spacer(1, 8))

    action_items = data.get("action_items", {})

    # 即時対応
    quick_wins = action_items.get("quick_wins", [])
    if quick_wins:
        story.append(Paragraph("即時対応（クイックウィン）", styles["SubSection"]))
        for i, item in enumerate(quick_wins, 1):
            col_hex = SUCCESS.hexval() if hasattr(SUCCESS, 'hexval') else str(SUCCESS)
            story.append(Paragraph(
                f'<font color="{col_hex}"><b>{i}.</b></font> {item}', styles["ActionItem"]
            ))
        story.append(Spacer(1, 12))

    # 今週中
    this_week = action_items.get("this_week", [])
    if this_week:
        story.append(Paragraph("今週中", styles["SubSection"]))
        for i, item in enumerate(this_week, 1):
            col_hex = ACCENT.hexval() if hasattr(ACCENT, 'hexval') else str(ACCENT)
            story.append(Paragraph(
                f'<font color="{col_hex}"><b>{i}.</b></font> {item}', styles["ActionItem"]
            ))
        story.append(Spacer(1, 12))

    # 今月中
    this_month = action_items.get("this_month", [])
    if this_month:
        story.append(Paragraph("今月中", styles["SubSection"]))
        for i, item in enumerate(this_month, 1):
            col_hex = WARNING.hexval() if hasattr(WARNING, 'hexval') else str(WARNING)
            story.append(Paragraph(
                f'<font color="{col_hex}"><b>{i}.</b></font> {item}', styles["ActionItem"]
            ))

    story.append(PageBreak())

    # ==================== 6ページ目: スコアリング方法論 ====================
    story.append(Paragraph("スコアリング方法論", styles["SectionTitle"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "本営業パイプラインレポートは、BANT + MEDDIC スコアリングフレームワークを用いて見込み客を評価・ランク付けしています。"
        "各見込み客は、BANT の4つの評価軸（予算・権限・必要性・タイムライン）に基づいて0〜100点でスコアリングされます。"
        "また、日本市場向けに「稟議プロセス対応度」「上場区分・組織規模」を補助的な評価指標として考慮します。",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 10))

    # 方法論テーブル
    method_header = [
        Paragraph("<b>評価軸</b>", styles["TableHeader"]),
        Paragraph("<b>ウェイト</b>", styles["TableHeader"]),
        Paragraph("<b>計測シグナル</b>", styles["TableHeader"]),
    ]
    method_data = [method_header]

    method_rows = [
        ("予算 (Budget)", "25点",
         "資金調達額・従業員数・価格ページの公開有無・テック支出指標・エンタープライズツール利用状況・稟議での予算取得可能性"),
        ("権限 (Authority)", "25点",
         "意思決定者の特定・稟議フロー上の承認者確認・役員・部長・課長レベルのコンタクト取得状況"),
        ("必要性 (Need)", "25点",
         "課題の明確化・関連求人情報・レビューサイトの不満シグナル・競合他社への不満・業務上の痛点"),
        ("タイムライン (Timeline)", "25点",
         "関連ポジションの採用活動・最近の資金調達・決算期・契約更新時期・予算申請サイクル（10〜12月・3月末）"),
    ]

    for dim, weight, desc in method_rows:
        method_data.append([
            Paragraph(f"<b>{dim}</b>", styles["TableCell"]),
            Paragraph(weight, styles["TableCell"]),
            Paragraph(desc, styles["TableCell"]),
        ])

    t = Table(method_data, colWidths=[120, 55, 325])
    t_style = [
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
    ]
    for i in range(1, len(method_data)):
        if i % 2 == 0:
            t_style.append(("BACKGROUND", (0, i), (-1, i), LIGHT_BG))
    t.setStyle(TableStyle(t_style))
    story.append(t)

    story.append(Spacer(1, 16))

    # グレード基準
    story.append(Paragraph("グレード基準", styles["SubSection"]))

    grade_header = [
        Paragraph("<b>スコア範囲</b>", styles["TableHeader"]),
        Paragraph("<b>グレード</b>", styles["TableHeader"]),
        Paragraph("<b>評価</b>", styles["TableHeader"]),
        Paragraph("<b>推奨アクション</b>", styles["TableHeader"]),
    ]
    grade_data = [grade_header]
    grade_rows = [
        ("75-100", "A", "高優先度の見込み客", "即座にアプローチ・商談設定を進める"),
        ("50-74", "B", "有望な見込み客",     "継続的なナーチャリングと情報提供"),
        ("25-49", "C", "要育成の見込み客",   "リサーチを深め、複数の接点を構築する"),
        ("0-24",  "D", "低優先度",           "長期ナーチャリングリストに追加"),
    ]
    for score_range, grade, interp, action in grade_rows:
        g_col = grade_color(grade)
        hex_g = g_col.hexval() if hasattr(g_col, 'hexval') else str(g_col)
        grade_data.append([
            Paragraph(score_range, styles["TableCell"]),
            Paragraph(f'<font color="{hex_g}"><b>{grade}</b></font>', styles["TableCell"]),
            Paragraph(interp, styles["TableCell"]),
            Paragraph(action, styles["TableCell"]),
        ])

    t = Table(grade_data, colWidths=[80, 50, 140, 230])
    t_style = [
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ALIGN", (0, 0), (1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
    ]
    t.setStyle(TableStyle(t_style))
    story.append(t)

    # PDF ビルド
    doc.build(
        story,
        onFirstPage=lambda c, d: add_header_footer(c, d, report_date),
        onLaterPages=lambda c, d: add_header_footer(c, d, report_date),
    )

    return output_path


def main():
    if len(sys.argv) < 2:
        # デモモード — リアルなサンプルデータでレポートを生成
        sample_data = {
            "date": "2026年3月6日",
            "overall_pipeline_score": 72,
            "executive_summary": (
                "現在のパイプラインは12社の見込み客を抱え、複数のステージで順調に進捗しています。"
                "Aグレードの3社は即座にアプローチすべき高優先度案件であり、"
                "Bグレードの5社は継続的なナーチャリングで成約可能性が高い有望案件です。"
                "改善が必要な主な領域は、意思決定者へのアクセス強化と競合インテリジェンスの充実です。"
            ),
            "prospects": [
                {"name": "株式会社テックフロー", "url": "https://techflow.co.jp", "score": 92, "grade": "A",
                 "stage": "初回商談済み", "next_action": "エンジニアリング部長にデモを提案"},
                {"name": "データブリッジ株式会社", "url": "https://databridge.co.jp", "score": 85, "grade": "A",
                 "stage": "資格認定済み", "next_action": "3段階の価格プランを含む提案書を送付"},
                {"name": "クラウドスケール AI", "url": "https://cloudscale.ai", "score": 78, "grade": "A",
                 "stage": "商談中", "next_action": "紹介経由でCTOにコンタクト"},
                {"name": "ファイナンスハブ株式会社", "url": "https://financehub.co.jp", "score": 71, "grade": "B",
                 "stage": "リサーチ中", "next_action": "初回アウトリーチメールを送信"},
                {"name": "リテールエッジ", "url": "https://retailedge.co.jp", "score": 68, "grade": "B",
                 "stage": "ナーチャリング中", "next_action": "類似業界の導入事例を共有"},
                {"name": "セキュアネットラボ", "url": "https://securenet.co.jp", "score": 65, "grade": "B",
                 "stage": "資格認定済み", "next_action": "次回商談の準備ブリーフを作成"},
                {"name": "エデュプラットフォーム", "url": "https://eduplatform.co.jp", "score": 62, "grade": "B",
                 "stage": "商談中", "next_action": "価格提案についてフォローアップ"},
                {"name": "グリーンエナジー AI", "url": "https://greenenergy.co.jp", "score": 58, "grade": "B",
                 "stage": "リサーチ中", "next_action": "意思決定者を特定する"},
                {"name": "メディアスタック", "url": "https://mediastack.co.jp", "score": 45, "grade": "C",
                 "stage": "初期リサーチ", "next_action": "見込み客分析を完了する"},
                {"name": "ロジトラック", "url": "https://logitrack.co.jp", "score": 42, "grade": "C",
                 "stage": "コールド", "next_action": "企業リサーチとコンタクト特定"},
                {"name": "ヘルスファースト", "url": "https://healthfirst.co.jp", "score": 38, "grade": "C",
                 "stage": "コールド", "next_action": "ICP適合性を検証してからアプローチ"},
                {"name": "ビルドコーツールズ", "url": "https://buildco.co.jp", "score": 22, "grade": "D",
                 "stage": "不適格", "next_action": "長期ナーチャリングリストに追加"},
            ],
            "categories": {
                "企業適合度": {"score": 75},
                "コンタクトアクセス": {"score": 68},
                "ニーズ整合性": {"score": 82},
                "予算シグナル": {"score": 70},
                "タイムラインシグナル": {"score": 58},
                "競合ポジション": {"score": 63},
            },
            "action_items": {
                "quick_wins": [
                    "株式会社テックフロー エンジニアリング部長宛にパーソナライズされたアプローチメールを送信（Aグレード・デモ準備完了）",
                    "データブリッジ株式会社への3段階プロポーザルを作成・送付",
                    "クラウドスケール AI の CTO への紹介経由コンタクトを依頼",
                ],
                "this_week": [
                    "ファイナンスハブ株式会社向けアウトリーチシーケンスを開始",
                    "リテールエッジ向けに小売業界の導入事例を作成",
                    "セキュアネットラボの商談に向けた準備ブリーフを完成させる",
                    "エデュプラットフォームの稟議関与者をマッピングする",
                ],
                "this_month": [
                    "メディアスタック・ロジトラックの見込み客分析を実施",
                    "主要競合3社のバトルカードを作成",
                    "医療・教育業界向けの価値提案を開発",
                    "ICPをパイプラインの知見に基づいて見直し・更新",
                    "紹介経由のウォームイントロネットワークを構築",
                ],
            },
            "pipeline_health": {
                "total_prospects": 12,
                "avg_score": 65,
                "a_grade": 3,
                "b_grade": 5,
                "c_grade": 3,
                "d_grade": 1,
            },
        }
        output = "SALES-REPORT-sample.pdf"
        generate_report(sample_data, output)
        print(f"サンプルレポートを生成しました: {output}")
        return

    json_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "SALES-REPORT.pdf"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    generate_report(data, output_path)
    print(f"レポートを生成しました: {output_path}")


if __name__ == "__main__":
    main()
