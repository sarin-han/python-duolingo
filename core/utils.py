import os
import re

def sanitize_filename(filename):
    """
    [함수 역할] 파일명으로 쓸 수 없는 특수문자(?, !, / 등)를 언더바(_)로 바꿉니다.
    [문법 설명] re.sub(패턴, 바꿀문자, 대상): 정규표현식을 사용하여 문자를 치환합니다.
    """
    # \w는 문자+숫자를 의미, \s는 공백을 의미. 이 외의 문자는 다 _로 바꿉니다.
    clean_name = re.sub(r'[^\w\s-]', '_', filename)
    return clean_name.strip().replace(' ', '_')

def create_practice_file(day, title, details):
    """
    [함수 역할] practice/ 폴더 안에 해당 날짜의 파이썬 파일을 생성합니다.
    """
    # 1. 폴더가 없으면 생성 (os.makedirs: 하위 폴더까지 한 번에 생성)
    folder_name = "practice"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"시스템: {folder_name} 폴더를 생성했습니다.")

    # 2. 파일명 결정 (예: day01_문법_기초.py)
    safe_title = sanitize_filename(title)
    file_name = f"day{day:02d}_{safe_title}.py"
    file_path = os.path.join(folder_name, file_name)

    # 3. 파일이 이미 존재하면 덮어쓰지 않음 (기존 코드 보호)
    if os.path.exists(file_path):
        return file_path, False 

    # 4. 파일 생성 및 기본 템플릿 작성
    template = f'''"""
Day {day:02d}: {title}
학습 내용: {details}
작성일: {os.popen('date /t').read().strip() if os.name == 'nt' else os.popen('date').read().strip()}
"""

# 아래에 코드를 작성하며 공부를 시작하세요!
print(f"--- Day {day:02d} {title} 학습 시작 ---")

'''
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(template)
    
    return file_path, True