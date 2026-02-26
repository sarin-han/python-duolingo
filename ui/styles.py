import customtkinter as ctk

# ==========================================
# 1. 컬러 팔레트 (Color Palette)
# ==========================================
# 듀오링고의 아이덴티티를 살린 색상 조합입니다.
# (라이트 모드 색상, 다크 모드 색상) 튜플 형태로 정의하여 자동 대응하게 합니다.

COLOR_MAIN_GREEN = ("#58CC02", "#58CC02")      # 듀오링고 시그니처 그린
COLOR_DARK_GREEN = ("#46A302", "#46A302")      # 버튼 클릭 시나 강조용 진한 그린
COLOR_FINISH_GOLD = ("#FFD700", "#FFD700")     # 완주 시 사용할 골드 포인트

# 배경 및 카드 색상
COLOR_BG = ("#FFFFFF", "#111214")              # 전체 창 배경 (흰색 / 아주 어두운 회색)
COLOR_CARD_PENDING = ("#F7F7F7", "#1E1F22")    # 아직 완료하지 않은 카드 배경
COLOR_CARD_COMPLETE = ("#E5FFD1", "#1B2E10")   # 완료된 카드의 은은한 녹색 배경

# 텍스트 색상
COLOR_TEXT_MAIN = ("#4B4B4B", "#E3E5E8")       # 메인 본문 글자색
COLOR_TEXT_SUB = ("#AFAFAF", "#8E9297")        # 부가 설명 글자색 (옅은 회색)

# ==========================================
# 2. 타이포그래피 (Typography)
# ==========================================
# 폰트의 종류와 크기를 정의합니다. (시스템 폰트 사용)

def get_font(size, weight="normal"):
    """
    [함수 역할] 일관된 폰트 설정을 위해 폰트 이름과 크기, 굵기를 반환합니다.
    [문법] 튜플 형태로 (폰트명, 크기, 굵기)를 반환하여 ctk에서 바로 쓰게 합니다.
    """
    return ("Malgun Gothic", size, weight)

FONT_TITLE = get_font(24, "bold")      # 앱 상단 제목용
FONT_DAY_NUM = get_font(18, "bold")    # 'Day 01' 표시용
FONT_CONTENT = get_font(14, "normal")  # 챌린지 제목용
FONT_DETAIL = get_font(12, "normal")   # 세부 설명용 (작은 글씨)

# ==========================================
# 3. 컴포넌트 규격 (Geometry & Layout)
# ==========================================
# UI 요소들의 모양과 간격을 정의합니다.

CARD_CORNER = 15      # 카드의 모서리를 얼마나 둥글게 할지 (라운드 값)
BUTTON_CORNER = 10    # 버튼의 모서리 라운드 값
PADDING_MAIN = 20     # 전체적인 여백 값