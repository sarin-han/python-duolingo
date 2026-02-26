import customtkinter as ctk
from ui.app_window import AppWindow

def main():
    """
    [함수 역할] 프로그램의 시작점(Entry Point)입니다.
    테마를 설정하고 메인 윈도우를 실행합니다.
    """
    # 1. 앱 테마 설정 (시스템 설정을 따르거나 다크/라이트로 고정 가능)
    ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
    ctk.set_default_color_theme("blue") 

    # 2. 앱 실행
    app = AppWindow()
    
    # 3. 메인 루프 시작 (창이 닫힐 때까지 대기)
    app.mainloop()

if __name__ == "__main__":
    main()