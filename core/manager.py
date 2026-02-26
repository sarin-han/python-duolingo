import json
import os
from datetime import datetime, date
from core.utils import create_practice_file  # [1단계 추가] 파일 생성 도구 가져오기

class ChallengeManager:
    def __init__(self, file_path="data/challenge.json"):
        self.file_path = file_path
        self.data = {}
        self.load_data()

    def load_data(self):
        """JSON 데이터를 읽어오는 기존 함수"""
        if not os.path.exists(self.file_path):
            print(f"Error: {self.file_path}를 찾을 수 없습니다.")
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            actual_length = len(self.data.get("curriculum", []))
            if self.data.get("total_days") != actual_length:
                self.data["total_days"] = actual_length
        except json.JSONDecodeError:
            print("Error: JSON 형식이 올바르지 않습니다.")

    def save_data(self):
        """변경된 데이터를 저장하는 기존 함수"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    # --- [1단계 신규 기능 1] 주차 구분 데이터 가공 ---
    def get_curriculum_with_phase_info(self):
        """
        UI에서 1주차, 2주차 구분선을 그릴 수 있도록
        데이터에 'is_header' 플래그를 추가해서 리스트를 반환합니다.
        """
        curriculum = self.data.get("curriculum", [])
        processed_list = []
        last_phase = None

        for item in curriculum:
            temp_item = item.copy()
            # 이전 아이템과 phase(주차)가 다르면 헤더로 표시
            if item.get("phase") != last_phase:
                temp_item["is_header"] = True
                last_phase = item.get("phase")
            else:
                temp_item["is_header"] = False
            processed_list.append(temp_item)
            
        return processed_list

    # --- [1단계 신규 기능 2] 공부 시작 (파일 생성) ---
    def start_day_study(self, day_num):
        """
        카드를 클릭했을 때 실행됩니다. 
        해당 날짜의 정보를 찾아 실습용 파이썬 파일을 만듭니다.
        """
        curriculum = self.data.get("curriculum", [])
        for item in curriculum:
            if item["day"] == day_num:
                # utils.py의 함수를 호출해 파일을 생성합니다.
                path, created = create_practice_file(
                    item["day"], 
                    item["title"], 
                    item["detail"]
                )
                return path, created
        return None, False

    def update_status(self, day, status="Completed"):
        """상태 업데이트 로직 (기존과 동일)"""
        curriculum = self.data.get("curriculum", [])
        for item in curriculum:
            if item["day"] == day:
                if item["status"] != status:
                    item["status"] = status
                    if status == "Completed":
                        self._update_streak()
                    self.save_data()
                break

    def _update_streak(self):
        """스트릭 계산 로직 (기존과 동일)"""
        today = date.today()
        streak_info = self.data.get("streak_info", {"count": 0, "last_date": ""})
        last_date_str = streak_info.get("last_date")
        
        if last_date_str:
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
            delta = (today - last_date).days
            if delta == 1:
                streak_info["count"] += 1
            elif delta > 1:
                streak_info["count"] = 1
        else:
            streak_info["count"] = 1
            
        streak_info["last_date"] = today.strftime("%Y-%m-%d")
        self.data["streak_info"] = streak_info

    def get_progress_stats(self):
        """통계 계산 로직 (기존과 동일)"""
        total = self.data.get("total_days", 0)
        curriculum = self.data.get("curriculum", [])
        completed = sum(1 for item in curriculum if item["status"] == "Completed")
        ratio = completed / total if total > 0 else 0
        return ratio, completed, total

    def get_streak_count(self):
        return self.data.get("streak_info", {}).get("count", 0)