import customtkinter as ctk
from ui.styles import *
import re

class DayCard(ctk.CTkFrame):
    def __init__(self, master, day_data, on_complete_callback, on_start_callback):
        super().__init__(master, corner_radius=CARD_CORNER)
        
        self.day_data = day_data
        self.is_expanded = False
        self.checkboxes = []
        
        # 전체 카드 배경 설정
        self.refresh_bg()

        # [핵심 수정] 1. 헤더 프레임 (클릭 영역)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", cursor="hand2")
        self.header_frame.pack(fill="x", padx=15, pady=10)
        
        # [Day 번호]
        self.lbl_day = ctk.CTkLabel(self.header_frame, text=f"Day {day_data['day']:02d}", 
                                    font=FONT_DAY_NUM, text_color=COLOR_MAIN_GREEN[0])
        self.lbl_day.pack(side="left", padx=(0, 15))

        # [제목]
        self.lbl_title = ctk.CTkLabel(self.header_frame, text=day_data["title"], 
                                      font=FONT_CONTENT, text_color=COLOR_TEXT_MAIN[0])
        self.lbl_title.pack(side="left")

        # ---------------------------------------------------------
        # [강력 조치] 모든 요소에 클릭 이벤트 바인딩 (글자를 눌러도 실행되게)
        # ---------------------------------------------------------
        click_func = lambda e: self.toggle_expand(on_start_callback)
        
        self.bind("<Button-1>", click_func)             # 카드 몸체 클릭
        self.header_frame.bind("<Button-1>", click_func) # 헤더 영역 클릭
        self.lbl_day.bind("<Button-1>", click_func)      # Day 숫자 클릭
        self.lbl_title.bind("<Button-1>", click_func)    # 제목 텍스트 클릭

        # 2. 상세 영역 (초기 숨김)
        self.detail_frame = ctk.CTkFrame(self, fg_color="transparent")

        # 3. 체크박스 동적 생성
        # [수정된 로직] 괄호 안의 콤마는 보호하고 바깥의 콤마/마침표로만 분리
        raw_detail = day_data.get("detail", "")
        
        # 정규표현식 설명: 
        # [.,] : 마침표나 콤마를 찾는데,
        # (?![^(]*\)) : 뒤에 닫는 괄호 ')'는 있고 여는 괄호 '('는 없는 상황(즉, 괄호 안)이 아닐 때만!
        items = re.split(r'[.,](?![^(]*\))', raw_detail)
        
        items = [i.strip() for i in items if i.strip()]
        for item_text in items:
            cb = ctk.CTkCheckBox(
                self.detail_frame, text=item_text, font=FONT_DETAIL,
                checkmark_color="white", fg_color=COLOR_CHECKBOX[0],
                command=self.check_all_done
            )
            cb.pack(fill="x", padx=40, pady=5, anchor="w")
            self.checkboxes.append(cb)

        # 4. 완료 버튼
        self.btn_complete = ctk.CTkButton(
            self.detail_frame, text="오늘의 챌린지 완료!", font=FONT_CONTENT,
            fg_color=COLOR_MAIN_GREEN[0], state="disabled",
            command=lambda: on_complete_callback(day_data["day"])
        )
        self.btn_complete.pack(pady=(15, 15), padx=40, fill="x")

        # 완료 상태 처리
        if day_data["status"] == "Completed":
            for cb in self.checkboxes:
                cb.select()
                cb.configure(state="disabled")
            self.btn_complete.configure(state="disabled", text="완료된 챌린지")

    def toggle_expand(self, on_start_callback):
        """디버깅 메시지를 포함한 토글 함수"""
        print(f"DEBUG: Day {self.day_data['day']} 카드 클릭됨!") # 클릭 확인용
        
        if self.is_expanded:
            self.detail_frame.pack_forget()
        else:
            # header_frame 아래에 배치
            self.detail_frame.pack(fill="x", padx=20, pady=(0, 10))
            on_start_callback(self.day_data["day"])
        
        self.is_expanded = not self.is_expanded

    def check_all_done(self):
        all_checked = all(cb.get() for cb in self.checkboxes)
        if all_checked and self.day_data["status"] != "Completed":
            self.btn_complete.configure(state="normal")
        else:
            self.btn_complete.configure(state="disabled")

    def refresh_bg(self):
        bg = COLOR_CARD_COMPLETE if self.day_data["status"] == "Completed" else COLOR_CARD_PENDING
        self.configure(fg_color=bg)

class PhaseHeader(ctk.CTkFrame):
    """[신규] 주차 구분을 위한 헤더 컴포넌트"""
    def __init__(self, master, phase_name):
        super().__init__(master, fg_color=COLOR_PHASE_BG, corner_radius=8)
        self.lbl = ctk.CTkLabel(self, text=f"📂 {phase_name}", font=FONT_PHASE, text_color=COLOR_TEXT_MAIN[0])
        self.lbl.pack(pady=8)
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