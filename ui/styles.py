import customtkinter as ctk

# ==========================================
# 1. 컬러 팔레트 (Color Palette)
# ==========================================
COLOR_MAIN_GREEN = ("#58CC02", "#58CC02")      # 듀오링고 그린
COLOR_DARK_GREEN = ("#46A302", "#46A302")      # 강조 및 완료 버튼용
COLOR_FINISH_GOLD = ("#FFD700", "#FFD700")     # 완주 포인트

# [2단계 추가] 주차(Phase) 헤더 배경색
# 1주차, 2주차를 구분하는 바(Bar)의 색상입니다.
COLOR_PHASE_BG = ("#EBEBEB", "#2A2D31")        # 연한 회색 / 다크그레이

# [2단계 추가] 체크박스 포인트 컬러
COLOR_CHECKBOX = ("#1CB0F6", "#1CB0F6")        # 듀오링고 블루 (체크 시 색상)

# 배경 및 카드 색상
COLOR_BG = ("#FFFFFF", "#111214")
COLOR_CARD_PENDING = ("#F7F7F7", "#1E1F22")
COLOR_CARD_COMPLETE = ("#E5FFD1", "#1B2E10")

# 텍스트 색상
COLOR_TEXT_MAIN = ("#4B4B4B", "#E3E5E8")
COLOR_TEXT_SUB = ("#AFAFAF", "#8E9297")

# ==========================================
# 2. 타이포그래피 (Typography)
# ==========================================
def get_font(size, weight="normal"):
    return ("Malgun Gothic", size, weight)

FONT_TITLE = get_font(24, "bold")
# [2단계 추가] 주차 제목용 폰트
FONT_PHASE = get_font(18, "bold")      
FONT_DAY_NUM = get_font(16, "bold")    
FONT_CONTENT = get_font(15, "bold")    # 카드가 닫혔을 때 보여줄 제목 폰트
FONT_DETAIL = get_font(13, "normal")   # 체크박스 옆에 붙을 설명 폰트

# ==========================================
# 3. 컴포넌트 규격 (Geometry & Layout)
# ==========================================
CARD_CORNER = 15
BUTTON_CORNER = 12
# [2단계 추가] 체크박스 사이의 간격
CHECK_SPACING = 8      
PADDING_MAIN = 20