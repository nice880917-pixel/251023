"""학급 경제 시스템 앱 활용 교육 방법 소개 HWPX 생성 스크립트."""
import sys
from hwpx import HwpxDocument

OUT = sys.argv[1]
MM = 283.465  # 1mm in HWPUNIT

doc = HwpxDocument.new()
doc.set_page_setup(paper_size="A4", margin_left_mm=18, margin_right_mm=18,
                   margin_top_mm=15, margin_bottom_mm=15,
                   header_margin_mm=10, footer_margin_mm=10)
hdr = doc.parts.headers[0]

FONT = "함초롬돋움"
BLUE = "#1F3A93"
LINK = "#7030A0"


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


# 자주 쓰는 스타일
C_BODY = cs(10)
C_BOLD = cs(10, bold=True)
C_SMALL = cs(9)
C_SMALL_B = cs(9, bold=True)
C_LINK = cs(9, color=LINK)
C_HEAD = cs(10, bold=True)
C_TITLE = cs(16, bold=True, color=BLUE)
C_SUB = cs(11, bold=True)

P_LEFT = ps("LEFT")
P_CENTER = ps("CENTER")
P_HANG = ps("LEFT", hang_mm=3.5)   # "- " 목록
P_HANG2 = ps("LEFT", hang_mm=5.0)  # "1) " 목록

BF_HEAD = doc.styles.ensure_border_fill(border_color="#000000", border_width="0.12 mm", fill_color="#E7E6E6")
BF_BODY = doc.styles.ensure_border_fill(border_color="#000000", border_width="0.12 mm")


def fill(cell, lines):
    """lines: list of (text | [(text, charPr)], charPr, paraPr)."""
    expanded = []
    for content, char_id, para_id in lines:
        if isinstance(content, str) and "\n" in content:
            expanded += [(part, char_id, para_id) for part in content.split("\n")]
        else:
            expanded.append((content, char_id, para_id))
    first = True
    for spec in expanded:
        content, char_id, para_id = spec
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


def head_cell(tbl, r, col, text):
    fill(tbl.cell(r, col), [c(text, C_HEAD, P_CENTER)])
    tbl.set_cell_border_fill(r, col, BF_HEAD)


def style_all(tbl):
    for r in range(tbl.row_count):
        for col in range(tbl.column_count):
            try:
                tbl.set_cell_border_fill(r, col, BF_BODY)
            except Exception:
                pass


def add_par(text, char, para):
    p = doc.add_paragraph("", para_pr_id_ref=para, char_pr_id_ref=char, inherit_style=False)
    for r in list(p.runs):
        r.element.getparent().remove(r.element)
    p.add_run(text, char_pr_id_ref=char)
    return p


TEXT_W = int((210 - 36) * MM)

# ───────────────── 제목 ─────────────────
first_para = doc.paragraphs[0]
first_para.element.set("paraPrIDRef", str(P_CENTER))
first_para.clear_text()  # 첫 run에 들어 있는 구역 설정(secPr)은 유지
first_para.add_run("학급 경제 시스템 체험 앱 활용 교육 방법", char_pr_id_ref=C_TITLE)
add_par("- 에듀넷 경제·금융교육 자료 × 생성형 AI 제작 앱 「새롬초 6-2 은행」 -", C_BODY, P_CENTER)
add_par("", C_BODY, P_LEFT)

# ───────────────── 표 1: 콘텐츠 정보 ─────────────────
t1 = doc.add_table(8, 4, width=TEXT_W, border_fill_id_ref=BF_BODY)
t1.set_column_widths([24, 30, 20, 26])
style_all(t1)

head_cell(t1, 0, 0, "학교급(학년)")
fill(t1.cell(0, 1), [c("초등학교 (5~6학년)", C_BODY, P_CENTER)])
head_cell(t1, 0, 2, "관련 교과")
fill(t1.cell(0, 3), [c("사회, 실과, 창의적 체험활동", C_BODY, P_CENTER)])

head_cell(t1, 1, 0, "콘텐츠 내용")
fill(t1.cell(1, 1), [c("학급 경제 시스템(학급 은행) 체험 앱 제작")])

head_cell(t1, 2, 0, "키워드")
fill(t1.cell(2, 1), [c("경제 활동, 직업과 소득, 저축과 이자, 합리적 소비, 금융 교육")])

head_cell(t1, 3, 0, "에듀넷 자료 정보,\n콘텐츠 활용 방법/\n팁 등")

fill(t1.cell(3, 1), [
    c("•에듀넷 자료 검색 절차 (URL 포함)", C_BOLD),
    c("- 에듀넷 > 학습자료 > 주제별 학습자료 > ‘경제교육’, ‘금융교육’ 키워드 검색", C_BODY, P_HANG),
    c("- (검색한 에듀넷 자료 URL 입력)", C_LINK, P_HANG),
])
fill(t1.cell(4, 1), [
    c("•자료 활용 방법", C_BOLD),
    c("- 에듀넷 경제·금융교육 자료를 바탕으로 생성형 AI로 만든 학급 경제 앱을 학생들에게 제공하여 "
      "‘직업 → 소득 → 저축·송금 → 소비’로 이어지는 경제 활동의 원리와 합리적 선택 방법을 "
      "직접 체험하도록 함", C_BODY, P_HANG),
    c([("- 학급 경제 체험 앱 ", C_BODY), ("(앱 배포 URL 입력)", C_LINK)], C_BODY, P_HANG),
])
fill(t1.cell(5, 1), [
    c("•앱 주요 기능", C_BOLD),
    c("- [내 지갑] 사용 가능 잔액, 현재 직업(일급), 예금 잔액, 최근 거래 내역 확인", C_BODY, P_HANG),
    c("- [은행 업무] 친구에게 송금, 예금 입금·출금, 주 2% 이자 자동 지급 및 저축 내역·다음 이자 지급일 확인", C_BODY, P_HANG),
    c("- [직업 센터] 학급 직업(일급·정원·하는 일)을 보고 원하는 직업에 지원", C_BODY, P_HANG),
    c("- [학급 상점] 숙제 면제권, 짝꿍 선택권, 음악 신청권 등 학급 특권 상품 구매(재고 한정)", C_BODY, P_HANG),
    c("- [교사 관리] 학생 일괄 등록·비밀번호 초기화, 직업·상품 추가/수정/삭제, "
      "직무 수행 확인 후 급여 지급(개별·선택·전체, 1~7일치)", C_BODY, P_HANG),
])
fill(t1.cell(6, 1), [
    c("•콘텐츠 활용 방안", C_BOLD),
    c("1) 에듀넷 자료를 통해 ‘소득·저축·소비’ 개념 형성, 합리적 경제생활의 필요성 확인", C_BODY, P_HANG2),
    c("2) 학급 경제 앱을 학생들에게 제공하여 직업 선택, 급여 수령, 저축과 이자, 송금, "
      "상품 구매 등 경제 활동을 간접 체험하며 합리적 선택 방법 내재화", C_BODY, P_HANG2),
    c("3) 학급 경제 + 앱 활동과 연계되는 활동지 제공하여 후속 활동 및 정리", C_BODY, P_HANG2),
])
fill(t1.cell(7, 1), [
    c("•운영 팁", C_BOLD),
    c("- 수업 전 교사 계정으로 로그인하여 학생 명단(줄바꿈으로 여러 명 등록)과 초기 자산, "
      "우리 반 실정에 맞는 직업·상품을 먼저 설정함 (교사 계정 비밀번호는 사전에 변경)", C_BODY, P_HANG),
    c("- 학생은 첫 접속 시 이름 입력 후 비밀번호를 직접 설정하며, 분실 시 교사가 [비번 초기화]로 재설정 가능", C_BODY, P_HANG),
    c("- 앱 데이터는 접속한 기기(브라우저)에 저장되므로 교실 공용 기기(교사 PC·전자칠판)에서 운영하는 것을 권장하며, "
      "Google Apps Script 웹앱 URL을 연결하면 거래 내역이 구글 스프레드시트에 자동 기록됨", C_BODY, P_HANG),
    c("- 예금은 매주 2% 이자가 자동 지급되므로, 몇 주 뒤 ‘저축한 학생’과 ‘바로 소비한 학생’의 자산 변화를 비교하며 저축의 가치를 이야기 나눔", C_BODY, P_HANG),
])

# 병합 (아래쪽 → 위쪽 순서로 처리)
for r in range(7, 0, -1):
    t1.merge_cells(r, 1, r, 3)
t1.merge_cells(3, 0, 7, 0)

add_par("", C_BODY, P_LEFT)
add_par("◦ 교수학습 과정안(약안)", C_SUB, P_LEFT)

# ───────────────── 표 2: 교수학습 과정안 ─────────────────
t2 = doc.add_table(7, 5, width=TEXT_W, border_fill_id_ref=BF_BODY)
t2.set_column_widths([9, 11, 52, 8, 20])
style_all(t2)

head_cell(t2, 0, 0, "활동\n단계")
head_cell(t2, 0, 1, "활동\n요소")
head_cell(t2, 0, 2, "교수·학습 활동")
head_cell(t2, 0, 3, "시간\n(분)")
head_cell(t2, 0, 4, "자료 ▣ /\n유의점 ※")

# 도입
fill(t2.cell(1, 0), [c("도입", C_BOLD, P_CENTER)])
fill(t2.cell(1, 1), [c("동기\n유발", C_BODY, P_CENTER)])
fill(t2.cell(1, 2), [
    c("학급 경제 관련 영상 제공 및 발문", C_BOLD),
    c("- “우리 반에서 직접 돈을 벌고, 모으고, 쓸 수 있다면 어떻게 하고 싶나요?”", C_BODY, P_HANG),
    c("- 용돈을 받자마자 다 써 버린 경험, 모아서 원하는 것을 산 경험 나누기", C_BODY, P_HANG),
])
fill(t2.cell(1, 3), [c("5", C_BODY, P_CENTER)])
fill(t2.cell(1, 4), [c("▣ 경제·용돈 관리 관련 영상", C_SMALL), c("(영상 URL 입력)", C_LINK)])

# 전개
fill(t2.cell(2, 0), [c("전개", C_BOLD, P_CENTER)])
fill(t2.cell(2, 1), [c("자료\n제공", C_BODY, P_CENTER)])
fill(t2.cell(2, 2), [
    c("경제·금융교육 에듀넷 자료 확인", C_BOLD),
    c("- 자료 탐색 > 소득·저축·소비 개념 이해 > 합리적 선택 기준 모색", C_BODY, P_HANG),
])
fill(t2.cell(2, 3), [c("25", C_BODY, P_CENTER)])
fill(t2.cell(2, 4), [c("▣ 에듀넷 자료", C_SMALL), c("(에듀넷 자료 URL 입력)", C_LINK)])

fill(t2.cell(3, 1), [c("앱\n제공", C_BODY, P_CENTER)])
fill(t2.cell(3, 2), [
    c("교사가 제작한 학급 경제 앱 링크 학생들에게 제공", C_BOLD),
    c("- 로그인 및 비밀번호 설정 → [직업 센터]에서 직업 지원 → 급여 받기 → "
      "[은행 업무]에서 저축(주 2% 이자)·송금 → [학급 상점]에서 상품 구매 순으로 "
      "조작해 보며 소득·저축·소비의 원리와 합리적 선택 방법을 간접 체험", C_BODY, P_HANG),
])
fill(t2.cell(3, 4), [
    c("▣ 학급 경제 체험 앱", C_SMALL), c("(앱 배포 URL 입력)", C_LINK),
    c("※ 첫 접속 시 비밀번호 설정 방법을 안내하고, 친구 비밀번호를 묻지 않도록 지도", C_SMALL),
])

fill(t2.cell(4, 1), [c("활동지\n입력", C_BODY, P_CENTER)])
fill(t2.cell(4, 2), [
    c("학급 경제, 앱 활동과 연계되는 후속 활동지 제공", C_BOLD),
    c("- 나의 소득·지출·저축 기록하기, 예금 이자 계산해 보기(원금 × 2% × 주 수), "
      "상품 구매 전 ‘꼭 필요한가? 지금 사야 하는가?’ 합리적 선택 기준 적어 보기", C_BODY, P_HANG),
])
fill(t2.cell(4, 4), [c("▣ 후속 활동지", C_SMALL), c("(활동지 URL 입력)", C_LINK)])

# 정리
fill(t2.cell(5, 0), [c("정리", C_BOLD, P_CENTER)])
fill(t2.cell(5, 1), [c("발표", C_BODY, P_CENTER)])
fill(t2.cell(5, 2), [c("나의 경제 활동 결과와 저축·소비 계획 발표", C_BOLD)])
fill(t2.cell(6, 2), [c("학생 간 합리적 소비 방법 및 저축 계획 공유", C_BOLD)])
fill(t2.cell(5, 3), [c("10", C_BODY, P_CENTER)])
fill(t2.cell(5, 4), [
    c("※ (유)공유 게시판에 나의 저축·소비 계획을 게시하고 서로에게 댓글을 남기도록 함", C_SMALL),
    c("※ 잔액 순위 비교보다 ‘선택의 이유’에 초점을 두어 피드백", C_SMALL),
])

t2.merge_cells(5, 4, 6, 4)
t2.merge_cells(5, 3, 6, 3)
t2.merge_cells(5, 1, 6, 1)
t2.merge_cells(5, 0, 6, 0)
t2.merge_cells(2, 3, 4, 3)
t2.merge_cells(2, 0, 4, 0)

doc.save_to_path(OUT)
print("saved", OUT)
