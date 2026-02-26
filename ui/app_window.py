import customtkinter as ctk
from core.manager import ChallengeManager
from ui.styles import *
from ui.components import DayCard, TopDashboard

class AppWindow(ctk.CTk):
    """
    [클래스 역할] 앱의 메인 창입니다. 
    모든 컴포넌트를 배치하고 사용자와의 상호작용을 관리합니다.
    """
    def __init__(self):
        super().__init__()

        # 1. 매니저 초기화 (데이터 로드)
        self.manager = ChallengeManager()
        
        # 2. 기본 윈도우 설정
        self.title("파이썬 마스터 30일 챌린지")
        self.geometry("600x800")
        self.configure(fg_color=COLOR_BG)

        # 3. 상단 대시보드 배치
        # 챌린지 제목과 스트릭 정보를 매니저에서 가져와 전달합니다.
        self.dashboard = TopDashboard(
            self, 
            title=self.manager.data.get("challenge_title", "Challenge"),
            streak_count=self.manager.get_streak_count()
        )
        self.dashboard.pack(fill="x", padx=PADDING_MAIN, pady=PADDING_MAIN)
        
        # 진행률 초기 업데이트
        ratio, _, _ = self.manager.get_progress_stats()
        self.dashboard.update_progress(ratio)

        # 4. 스크롤 가능한 메인 영역 (30일치 카드가 들어갈 곳)
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            label_text="Daily Curriculum",
            label_font=FONT_CONTENT
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=PADDING_MAIN, pady=(0, PADDING_MAIN))

        # 5. 카드 리스트 생성 (붕어빵 찍어내기)
        self.render_cards()

    def render_cards(self):
        """[함수 역할] 매니저의 데이터를 바탕으로 DayCard들을 화면에 그립니다."""
        # 기존에 그려진 카드들을 싹 지웁니다 (새로고침 기능 대비)
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # 데이터 매니저에서 전체 커리큘럼 리스트를 가져와 하나씩 카드로 만듭니다.
        curriculum = self.manager.data.get("curriculum", [])
        for day_data in curriculum:
            card = DayCard(
                self.scroll_frame, 
                day_data=day_data, 
                on_click_callback=self.handle_complete
            )
            card.pack(fill="x", pady=10, padx=5)

    def handle_complete(self, day_num):
        """
        [함수 역할] 카드에서 '완료' 버튼을 눌렀을 때 실행되는 핵심 로직입니다.
        """
        # 1. 데이터 업데이트 (매니저가 JSON 수정 및 스트릭 계산 수행)
        self.manager.update_status(day_num, "Completed")
        
        # 2. UI 새로고침 (진행률 바 업데이트)
        ratio, _, _ = self.manager.get_progress_stats()
        self.dashboard.update_progress(ratio)
        
        # 3. 스트릭 텍스트 업데이트
        new_streak = self.manager.get_streak_count()
        self.dashboard.lbl_streak.configure(text=f"🔥 {new_streak}일째 열공 중!")
        
        # 4. 카드 상태 다시 그리기 (완료된 카드의 색상을 바꾸기 위함)
        self.render_cards()