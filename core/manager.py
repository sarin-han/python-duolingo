import json  # JSON 파일을 읽고 쓰기 위한 모듈입니다.
import os    # 파일 경로가 실제로 존재하는지 확인하기 위해 사용합니다.
from datetime import datetime, date  # 날짜 계산(스트릭 확인)을 위한 모듈입니다.

class ChallengeManager:
    """
    이 클래스는 챌린지의 '두뇌' 역할을 합니다. 
    데이터를 로드하고, 저장하고, 학습 진도를 계산하는 모든 로직이 담겨 있습니다.
    """
    
    def __init__(self, file_path="data/challenge.json"):
        # self.file_path: 파일 위치를 저장합니다. 나중에 다른 파일을 불러올 때 유연하게 대처하기 위함입니다.
        self.file_path = file_path
        # self.data: JSON에서 읽어온 실제 데이터가 담길 딕셔너리 변수입니다.
        self.data = {}
        # 객체가 생성되자마자 데이터를 불러오도록 설정합니다.
        self.load_data()

    def load_data(self):
        """
        [함수 역할] 하드디스크에 있는 JSON 파일을 파이썬 메모리로 가져옵니다.
        [주요 문법] os.path.exists() - 파일이 없는데 읽으려 하면 에러가 나므로 미리 체크하는 안전장치입니다.
        """
        if not os.path.exists(self.file_path):
            print(f"경고: {self.file_path} 파일이 없습니다.")
            return

        try:
            # 'with' 문법: 파일을 열고 작업이 끝나면 자동으로 닫아줍니다. (메모리 누수 방지)
            with open(self.file_path, "r", encoding="utf-8") as f:
                # json.load: 텍스트 형태의 JSON을 파이썬의 '딕셔너리' 구조로 변환합니다.
                self.data = json.load(f)
            
            # [확장성 로직] 실제 커리큘럼 리스트의 개수를 세서 total_days와 맞지 않으면 자동 보정합니다.
            # .get("key", default): 해당 키가 없으면 에러 대신 기본값(0 혹은 [])을 반환하게 합니다.
            actual_length = len(self.data.get("curriculum", []))
            if self.data.get("total_days") != actual_length:
                self.data["total_days"] = actual_length
                
        except json.JSONDecodeError:
            print("에러: JSON 파일의 형식이 잘못되어 읽을 수 없습니다.")

    def save_data(self):
        """
        [함수 역할] 메모리상의 변경사항(예: 완료 체크)을 다시 JSON 파일에 기록합니다.
        [주요 문법] json.dump - 파이썬 객체를 JSON 텍스트로 변환하여 파일에 씁니다.
        """
        with open(self.file_path, "w", encoding="utf-8") as f:
            # indent=4: 사람이 읽기 좋게 들여쓰기를 적용합니다.
            # ensure_ascii=False: 한글이 '\u1234'처럼 깨지지 않고 정상적으로 저장되게 합니다.
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def update_status(self, day, status="Completed"):
        """
        [함수 역할] 특정 일차의 상태를 변경하고, 스트릭(연속 기록)을 갱신한 뒤 저장합니다.
        """
        curriculum = self.data.get("curriculum", [])
        for item in curriculum:
            # 리스트 안을 돌면서 내가 바꾸고자 하는 'day' 번호를 찾습니다.
            if item["day"] == day:
                # 중복 클릭 시 중복 계산을 막기 위해 상태가 다를 때만 실행합니다.
                if item["status"] != status:
                    item["status"] = status
                    # 만약 상태가 'Completed'로 바뀌는 것이라면 스트릭 계산 함수를 실행합니다.
                    if status == "Completed":
                        self._update_streak()
                    # 변경된 내용을 파일에 즉시 저장합니다.
                    self.save_data()
                break

    def _update_streak(self):
        """
        [함수 역할] 마지막으로 공부한 날짜와 오늘을 비교해 스트릭(연속 일수)을 계산합니다.
        [주요 문법] 함수명 앞의 '_' : 클래스 내부에서만 쓰는 '프라이빗' 함수임을 뜻하는 관례입니다.
        """
        today = date.today() # 오늘 날짜를 가져옵니다.
        
        # streak_info가 데이터에 없으면 기본 구조(0일, 날짜없음)를 생성합니다.
        streak_info = self.data.get("streak_info", {"count": 0, "last_date": ""})
        last_date_str = streak_info.get("last_date")
        
        if last_date_str:
            # strptime: "2026-02-26" 같은 '글자'를 계산 가능한 '날짜 객체'로 변환합니다.
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
            # 오늘 날짜에서 마지막 완료 날짜를 빼서 며칠 차이인지 계산합니다.
            delta = (today - last_date).days
            
            if delta == 1:
                # 어제 공부했고 오늘 또 완료한 경우: 스트릭 숫자를 1 올립니다.
                streak_info["count"] += 1
            elif delta > 1:
                # 하루 이상 건너뛰고 오늘 다시 시작한 경우: 스트릭을 1로 초기화합니다.
                streak_info["count"] = 1
            # delta == 0 (오늘 이미 완료함)인 경우는 숫자를 올리지 않고 유지합니다.
        else:
            # 생애 첫 완료인 경우 스트릭을 1로 시작합니다.
            streak_info["count"] = 1
            
        # 마지막 완료 날짜를 오늘 날짜로 기록합니다. (strftime: 날짜 객체를 다시 글자로 변환)
        streak_info["last_date"] = today.strftime("%Y-%m-%d")
        self.data["streak_info"] = streak_info

    def get_progress_stats(self):
        """
        [함수 역할] 진행률 바(Progress Bar)를 그리기 위한 데이터를 가공해서 반환합니다.
        [주요 문법] Generator Expression - 리스트 컴프리헨션과 비슷하지만 메모리를 아끼며 개수를 셀 때 유리합니다.
        """
        total = self.data.get("total_days", 0)
        curriculum = self.data.get("curriculum", [])
        
        # 상태가 'Completed'인 아이템들만 골라내어 그 개수를 합산(sum)합니다.
        completed = sum(1 for item in curriculum if item["status"] == "Completed")
        
        # 0으로 나누는 에러(ZeroDivisionError)를 방지하기 위한 조건문입니다.
        ratio = completed / total if total > 0 else 0
        return ratio, completed, total

    def get_streak_count(self):
        """[함수 역할] 현재 나의 연속 학습 일수를 외부(UI)에 알려줍니다."""
        return self.data.get("streak_info", {}).get("count", 0)