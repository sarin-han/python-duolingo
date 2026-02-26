from rich import print
from rich.panel import Panel

# 그냥 print 대신 rich의 print를 쓰면?
print("[bold red]안녕![/bold red] [green]Rich[/green]의 세계에 오신 걸 환영합니다. 🚀")

# 박스 안에 텍스트 넣기
print(Panel("이건 패널 안에 들어있는 텍스트예요!", title="알림", subtitle="하단 설명"))