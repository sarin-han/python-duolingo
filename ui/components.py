import customtkinter as ctk
from ui.styles import * # 우리가 만든 디자인 가이드를 가져옵니다.

class DayCard(ctk.CTkFrame):
    """
    [클래스 역할] 30일 중 '하루'를 나타내는 개별 카드 컴포넌트입니다.
    이 클래스는 붕어빵 틀처럼 작동하여, 데이터만 주면 카드를 찍어냅니다.
    """
    def __init__(self, master, day_data, on_click_callback):
        # master: 이 카드가 놓일 부모 위젯(스크롤 프레임)입니다.
        # day_data: JSON에서 가져온 해당 날짜의 정보(딕셔너리)입니다.
        # on_click_callback: 완료 버튼을 눌렀을 때 실행할 함수(manager와 연결됨)입니다.
        
        # 1. 프레임 초기화 (카드 테두리와 배경 설정)
        # ctk.CTkFrame 상속: 이 클래스 자체가 하나의 프레임(상자)이 됩니다.
        super().__init__(
            master, 
            corner_radius=CARD_CORNER,  # styles.py에서 정의한 둥근 모서리
            fg_color=COLOR_CARD_COMPLETE if day_data["status"] == "Completed" else COLOR_CARD_PENDING
        )
        
        self.day_data = day_data
        self.day_num = day_data["day"]

        # 2. 내부 레이아웃 설정 (그리드 방식)
        self.grid_columnconfigure(1, weight=1)  # 중앙 제목 영역이 넓게 퍼지도록 설정

        # [Day 번호 표시] - 왼쪽
        self.lbl_day = ctk.CTkLabel(
            self, 
            text=f"Day {self.day_num:02d}", 
            font=FONT_DAY_NUM,
            text_color=COLOR_MAIN_GREEN[0] if day_data["status"] == "Completed" else COLOR_TEXT_SUB[0]
        )
        self.lbl_day.grid(row=0, column=0, padx=20, pady=20)

        # [제목 및 상세 설명] - 중앙
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.grid(row=0, column=1, sticky="w")

        self.lbl_title = ctk.CTkLabel(
            self.info_frame, 
            text=day_data["title"], 
            font=FONT_CONTENT,
            text_color=COLOR_TEXT_MAIN[0]
        )
        self.lbl_title.pack(anchor="w")

        self.lbl_detail = ctk.CTkLabel(
            self.info_frame, 
            text=day_data["detail"], 
            font=FONT_DETAIL,
            text_color=COLOR_TEXT_SUB[0],
            wraplength=300  # 글자가 길어지면 자동으로 줄바꿈
        )
        self.lbl_detail.pack(anchor="w")

        # [완료 버튼] - 오른쪽
        btn_text = "완료됨" if day_data["status"] == "Completed" else "완료하기"
        btn_state = "disabled" if day_data["status"] == "Completed" else "normal"
        btn_color = COLOR_DARK_GREEN if day_data["status"] == "Completed" else COLOR_MAIN_GREEN

        self.btn_clear = ctk.CTkButton(
            self, 
            text=btn_text,
            width=80,
            height=32,
            corner_radius=BUTTON_CORNER,
            fg_color=btn_color,
            state=btn_state,
            command=lambda: on_click_callback(self.day_num) # 버튼 클릭 시 실행될 함수
        )
        self.btn_clear.grid(row=0, column=2, padx=20)

class TopDashboard(ctk.CTkFrame):
    """
    [클래스 역할] 앱 상단에 고정되어 전체 진척도와 스트릭을 보여주는 대시보드입니다.
    """
    def __init__(self, master, title, streak_count):
        super().__init__(master, fg_color="transparent")
        
        # 챌린지 제목
        self.lbl_title = ctk.CTkLabel(self, text=title, font=FONT_TITLE)
        self.lbl_title.pack(pady=(10, 0))

        # 스트릭 표시 (불꽃 아이콘 대신 이모지 활용)
        self.lbl_streak = ctk.CTkLabel(
            self, 
            text=f"🔥 {streak_count}일째 열공 중!", 
            font=FONT_CONTENT,
            text_color="#FF4500"
        )
        self.lbl_streak.pack(pady=(0, 10))

        # 프로그레스 바 (진행 상태 게이지)
        self.progress_bar = ctk.CTkProgressBar(
            self, 
            width=400, 
            height=15, 
            progress_color=COLOR_MAIN_GREEN[0],
            corner_radius=10
        )
        self.progress_bar.pack(padx=20, pady=10)
        self.progress_bar.set(0) # 초기값 0%

    def update_progress(self, ratio):
        """[함수 역할] 게이지 바의 수치를 실시간으로 업데이트합니다."""
        self.progress_bar.set(ratio)