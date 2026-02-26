import customtkinter as ctk
from core.manager import ChallengeManager
from ui.styles import *
from ui.components import DayCard, PhaseHeader  # PhaseHeader 추가됨

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. 매니저 초기화
        self.manager = ChallengeManager()
        
        # 2. 기본 윈도우 설정
        self.title("30일 챌린지 마스터")
        self.geometry("650x850")
        self.configure(fg_color=COLOR_BG)

        # 3. 상단 대시보드 (기존과 동일하지만 UI 연결을 위해 유지)
        from ui.components import TopDashboard
        self.dashboard = TopDashboard(
            self, 
            title=self.manager.data.get("challenge_title", "Challenge"),
            streak_count=self.manager.get_streak_count()
        )
        self.dashboard.pack(fill="x", padx=PADDING_MAIN, pady=PADDING_MAIN)
        
        # 진행률 업데이트
        self.refresh_stats()

        # 4. 스크롤 영역
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=PADDING_MAIN, pady=(0, PADDING_MAIN))

        # 5. 카드 리스트 렌더링 시작
        self.render_cards()

    def render_cards(self):
        """[핵심] 주차 구분선을 포함하여 카드들을 화면에 배치합니다."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # 매니저에게 '주차 정보가 포함된' 가공 데이터를 요청합니다.
        curriculum = self.manager.get_curriculum_with_phase_info()

        for day_data in curriculum:
            # [수정] 주차가 시작되는 지점이라면 헤더(구분선)를 먼저 그립니다.
            if day_data.get("is_header"):
                header = PhaseHeader(self.scroll_frame, day_data["phase"])
                header.pack(fill="x", pady=(20, 10), padx=10)

            # [수정] 카드 생성 시 두 가지 콜백(함수)을 전달합니다.
            card = DayCard(
                self.scroll_frame, 
                day_data=day_data, 
                on_start_callback=self.handle_start_study,   # 파일 생성용
                on_complete_callback=self.handle_complete     # 완료 처리용
            )
            card.pack(fill="x", pady=5, padx=10)

    def handle_start_study(self, day_num):
        """카드를 클릭(펼치기)했을 때 실행되는 로직"""
        path, created = self.manager.start_day_study(day_num)
        if created:
            print(f"알림: 새로운 연습 파일이 생성되었습니다 -> {path}")
        # 이미 파일이 있다면 별도 메시지 없이 공부를 시작하면 됩니다.

    def handle_complete(self, day_num):
        """최종 완료 버튼을 눌렀을 때 실행되는 로직"""
        # 1. 데이터 업데이트
        self.manager.update_status(day_num, "Completed")
        
        # 2. 상단 수치들 갱신
        self.refresh_stats()
        
        # 3. 화면 다시 그리기 (카드 색상 반영)
        self.render_cards()
        print(f"축하합니다! Day {day_num} 챌린지를 완료했습니다!")

    def refresh_stats(self):
        """상단 대시보드의 진행률과 스트릭을 최신화합니다."""
        ratio, _, _ = self.manager.get_progress_stats()
        self.dashboard.update_progress(ratio)
        
        new_streak = self.manager.get_streak_count()
        self.dashboard.lbl_streak.configure(text=f"🔥 {new_streak}일째 열공 중!")