"""학급 경제 앱 연계 학생 활동지 HWPX 생성 스크립트.

사용법: python3 docs/make_worksheet.py docs/학급경제앱_활동지.hwpx
"""
import sys
from hwpx import HwpxDocument

OUT = sys.argv[1]
MM = 283.465  # 1mm in HWPUNIT

doc = HwpxDocument.new()
doc.page.setup(paper_size="A4", margin_left_mm=18, margin_right_mm=18,
               margin_top_mm=15, margin_bottom_mm=15,
               header_margin_mm=10, footer_margin_mm=10)
hdr = doc.parts.headers[0]

FONT = "함초롬돋움"
BLUE = "#1F3A93"
GRAY = "#7F7F7F"


def cs(size=10, bold=False, color=None):
    return doc.styles.ensure_run(font=FONT, size=size, bold=bold, color=color)


def ps(align="LEFT", hang_mm=0.0, line=150, before=0):
    margins = {}
    if hang_mm:
        margins = {"left": int(hang_mm * MM), "intent": int(-hang_mm * MM)}
    if before:
        margins["prev"] = int(before * 100)
    return hdr.ensure_paragraph_format(alignment=align, line_spacing_percent=line,
                                       margins=margins or None)


C_BODY = cs(10)
C_BOLD = cs(10, bold=True)
C_SMALL = cs(9)
C_HINT = cs(9, color=GRAY)
C_HEAD = cs(10, bold=True)
C_TITLE = cs(18, bold=True, color=BLUE)
C_SEC = cs(12, bold=True, color=BLUE)

P_LEFT = ps("LEFT")
P_CENTER = ps("CENTER")
P_RIGHT = ps("RIGHT")
P_HANG = ps("LEFT", hang_mm=3.5)
P_SEC = ps("LEFT", before=8)

BF_HEAD = doc.styles.ensure_border_fill(border_color="#000000", border_width="0.12 mm", fill_color="#DEEAF6")
BF_BODY = doc.styles.ensure_border_fill(border_color="#000000", border_width="0.12 mm")
BF_BOX = doc.styles.ensure_border_fill(border_color="#1F3A93", border_width="0.4 mm", fill_color="#F2F6FC")

TEXT_W = int((210 - 36) * MM)


def fill(cell, lines):
    """lines: list of (text | [(text, charPr)], charPr, paraPr)."""
    expanded = []
    for content, char_id, para_id in lines:
        if isinstance(content, str) and "\n" in content:
            expanded += [(part, char_id, para_id) for part in content.split("\n")]
        else:
            expanded.append((content, char_id, para_id))
    first = True
    for content, char_id, para_id in expanded:
        if first:
            para = cell.paragraphs[0]
            para.clear_text()
            for r in list(para.runs):
                r.element.getparent().remove(r.element)
            para.element.set("paraPrIDRef", str(para_id))
            first = False
        else:
            para = cell.add_paragraph(para_pr_id_ref=para_id, char_pr_id_ref=char_id)
            for r in list(para.runs):
                r.element.getparent().remove(r.element)
        if isinstance(content, str):
            content = [(content, char_id)]
        for text, cid in content:
            para.add_run(text, char_pr_id_ref=cid)


def c(text, char=C_BODY, para=P_LEFT):
    return (text, char, para)


def add_par(text, char=C_BODY, para=P_LEFT):
    p = doc.add_paragraph("", para_pr_id_ref=para, char_pr_id_ref=char, inherit_style=False)
    for r in list(p.runs):
        r.element.getparent().remove(r.element)
    if isinstance(text, str):
        text = [(text, char)]
    for t, cid in text:
        p.add_run(t, char_pr_id_ref=cid)
    return p


TABLES = []
HP = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"


def sync_table_heights():
    """표 전체 높이(hp:sz)를 각 행 높이의 합으로 맞춘다."""
    for t in TABLES:
        total = 0
        for tr in t.element.findall(f"{HP}tr"):
            total += max(int(sz.get("height", "0")) for sz in tr.iter(f"{HP}cellSz"))
        t.element.find(f"{HP}sz").set("height", str(total))


def table(rows, cols, widths, header=True, bf=BF_BODY):
    t = doc.add_table(rows, cols, width=TEXT_W, border_fill_id_ref=bf)
    t.set_column_widths(widths)
    for r in range(rows):
        for col in range(cols):
            t.set_cell_border_fill(r, col, BF_HEAD if header and r == 0 else bf)
    TABLES.append(t)
    return t


def head_row(t, labels):
    for col, text in enumerate(labels):
        fill(t.cell(0, col), [c(text, C_HEAD, P_CENTER)])


def row_height(t, r, mm):
    for col in range(t.column_count):
        t.cell(r, col).set_size(height=int(mm * MM))


def section(text):
    add_par(text, C_SEC, P_SEC)


# ───────────────── 제목 ─────────────────
first = doc.paragraphs[0]
first.element.set("paraPrIDRef", str(P_CENTER))
first.clear_text()  # 첫 run의 구역 설정(secPr)은 유지
first.add_run("우리 반 경제 활동지", char_pr_id_ref=C_TITLE)
add_par("- 학급 경제 체험 앱 「새롬초 6-2 은행」과 함께하는 합리적인 경제생활 -", C_BODY, P_CENTER)
add_par("", C_SMALL, P_LEFT)

info = table(1, 6, [12, 18, 12, 18, 12, 28], header=False)
for col, text in [(0, "학년"), (2, "반·번호"), (4, "이름")]:
    fill(info.cell(0, col), [c(text, C_HEAD, P_CENTER)])
    info.set_cell_border_fill(0, col, BF_HEAD)
row_height(info, 0, 9)

# ───────────────── 1. 개념 ─────────────────
section("1. 에듀넷 자료로 알아보기")
add_par("에듀넷 자료를 보고 경제 용어의 뜻을 쓰고, 우리 반 앱에서는 무엇에 해당하는지 찾아봅시다.", C_SMALL, P_LEFT)
t1 = table(4, 3, [16, 46, 38])
head_row(t1, ["용어", "뜻", "우리 반 앱에서는?"])
for r, (word, hint) in enumerate([("소득", "예) 직업 센터에서 얻은 직업의 일급"),
                                  ("저축", ""), ("소비", "")], start=1):
    fill(t1.cell(r, 0), [c(word, C_BOLD, P_CENTER)])
    if hint:
        fill(t1.cell(r, 2), [c(hint, C_HINT)])
    row_height(t1, r, 12)

# ───────────────── 2. 직업 ─────────────────
section("2. 나의 직업 정하기")
add_par("앱의 [직업 센터]에서 직업을 살펴보고 지원해 봅시다.", C_SMALL, P_LEFT)
t2 = table(3, 4, [20, 30, 20, 30], header=False)
for r, col, text in [(0, 0, "나의 직업"), (0, 2, "일급"), (1, 0, "하는 일"), (2, 0, "선택한 이유")]:
    fill(t2.cell(r, col), [c(text, C_HEAD, P_CENTER)])
    t2.set_cell_border_fill(r, col, BF_HEAD)
fill(t2.cell(0, 3), [c("새롬(₩)", C_BODY, P_RIGHT)])
t2.merge_cells(2, 1, 2, 3)
t2.merge_cells(1, 1, 1, 3)
row_height(t2, 0, 10)
row_height(t2, 1, 10)
row_height(t2, 2, 14)

# ───────────────── 3. 기록장 ─────────────────
section("3. 나의 경제 활동 기록장")
add_par("앱의 [내 지갑] 거래 내역을 보며 들어온 돈과 나간 돈을 기록해 봅시다.", C_SMALL, P_LEFT)
t3 = table(8, 5, [16, 36, 16, 16, 16])
head_row(t3, ["날짜", "내용", "들어온 돈", "나간 돈", "남은 돈"])
fill(t3.cell(1, 0), [c("예) 9/29", C_HINT, P_CENTER)])
fill(t3.cell(1, 1), [c("처음 받은 돈", C_HINT)])
fill(t3.cell(1, 2), [c("1,000", C_HINT, P_RIGHT)])
fill(t3.cell(1, 4), [c("1,000", C_HINT, P_RIGHT)])
for r in range(1, 8):
    row_height(t3, r, 8)

# ───────────────── 4. 이자 ─────────────────
section("4. 저축과 이자 계산해 보기")
box = table(1, 1, [100], header=False, bf=BF_BOX)
fill(box.cell(0, 0), [
    c("우리 반 은행의 예금 이자: 매주 원금의 2%", C_BOLD),
    c("- 1주 이자 = 원금 × 2 ÷ 100  (예: 1,000새롬 × 2 ÷ 100 = 20새롬)", C_SMALL, P_HANG),
    c("- 이자는 원금을 기준으로 매주 같은 금액이 지급되고, 몇 주 동안 받은 이자를 모두 더하면 누적 이자가 됩니다.", C_SMALL, P_HANG),
])
add_par("", C_SMALL, P_LEFT)
t4 = table(4, 5, [20, 20, 20, 20, 20])
head_row(t4, ["저축한 돈(원금)", "1주 뒤 이자", "2주 뒤 누적 이자", "4주 뒤 누적 이자", "4주 뒤 예금 잔액"])
fill(t4.cell(1, 0), [c("1,000새롬", C_BODY, P_CENTER)])
fill(t4.cell(1, 1), [c("20새롬", C_HINT, P_CENTER)])
fill(t4.cell(2, 0), [c("500새롬", C_BODY, P_CENTER)])
fill(t4.cell(3, 0), [c("내가 저축한 돈\n(          )새롬", C_BODY, P_CENTER)])
for r in range(1, 4):
    row_height(t4, r, 10)
add_par("", C_SMALL, P_LEFT)
add_par([("▶ 지금 바로 쓰는 것과 몇 주 동안 저축하는 것은 어떤 차이가 있을까요?", C_BOLD)], C_BOLD, P_LEFT)
add_par("  ____________________________________________________________________________________", C_BODY, P_LEFT)

# ───────────────── 5. 합리적 선택 ─────────────────
section("5. 합리적으로 선택하기")
add_par("[학급 상점]에서 사고 싶은 상품을 골라 기준에 따라 따져 보고 결정해 봅시다.", C_SMALL, P_LEFT)
t5 = table(4, 6, [22, 12, 17, 17, 16, 16])
head_row(t5, ["사고 싶은 상품", "가격", "꼭 필요한가?\n(○ / ×)", "지금 사야 하는가?\n(○ / ×)", "살 돈이\n충분한가?", "나의 결정\n(구매 / 저축)"])
fill(t5.cell(1, 0), [c("예) 음악 신청권", C_HINT, P_CENTER)])
fill(t5.cell(1, 1), [c("500", C_HINT, P_CENTER)])
for r in range(1, 4):
    row_height(t5, r, 10)
add_par("", C_SMALL, P_LEFT)
add_par([("▶ 내가 이렇게 결정한 까닭은? ", C_BOLD)], C_BOLD, P_LEFT)
add_par("  ____________________________________________________________________________________", C_BODY, P_LEFT)

# ───────────────── 6. 계획과 느낀 점 ─────────────────
section("6. 나의 저축·소비 계획과 느낀 점")
t6 = table(3, 2, [26, 74], header=False)
for r, text in enumerate(["나의 저축 목표", "나의 소비 약속", "활동을 하며\n느낀 점"]):
    fill(t6.cell(r, 0), [c(text, C_HEAD, P_CENTER)])
    t6.set_cell_border_fill(r, 0, BF_HEAD)
fill(t6.cell(0, 1), [c("나는 (          )주 동안 (          )새롬을 모아서 (                              )에 쓰겠다.", C_BODY)])
fill(t6.cell(1, 1), [c("물건을 사기 전에 나는 ", C_BODY)])
row_height(t6, 0, 12)
row_height(t6, 1, 12)
row_height(t6, 2, 22)

# ───────────────── 7. 자기 평가 ─────────────────
section("7. 스스로 평가하기")
t7 = table(4, 4, [64, 12, 12, 12])
head_row(t7, ["평가 내용 (알맞은 칸에 ○ 표시)", "잘함", "보통", "노력 필요"])
for r, text in enumerate(["소득, 저축, 소비의 뜻을 알고 설명할 수 있다.",
                          "앱에서 저축과 이자의 원리를 확인하고 계산할 수 있다.",
                          "기준을 세워 합리적으로 소비할지 저축할지 결정할 수 있다."], start=1):
    fill(t7.cell(r, 0), [c(text, C_BODY)])
    row_height(t7, r, 8)

sync_table_heights()
doc.save_to_path(OUT)
print("saved", OUT)
