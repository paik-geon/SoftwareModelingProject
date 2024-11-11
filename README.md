# SoftwareModelingProject

RSVP는 Rapid serial visual presentation의 약자로    
RSVP는 화면 한자리에서 연속적으로 그림 혹은 단어를 출력한다면   
일반적으로 평문을 읽을 경우보다 빨리 읽을 수 있는 현상임



![Rapid-serial-visual-presentation-RSVP-task-a-Experimental-procedure-The-160](https://github.com/user-attachments/assets/b48fbd17-fca9-4c81-8b97-bb4d6cb4a2ae)

최근 현대인들이 글을 읽는 속도가 감소하고 문해력이 감소하고 있는데,   
그 이유중 큰 비중을 차지하는 것이 글을 읽는데 시간이 오래 소비되어서임      

위와 같은 현상을 해결하기 위해 RSVP를 이용한 프로그램을 만들어 봄

***
### 필요한 라이브러리 설정
```python
import tkinter as tk
from tkinter import messagebox
import time
```

python에서 UI를 구현하기 위해 tkinter 라이브러리 호출
또한 시간에 따른 텍스트 변화를 위해서 Time 라이브러리 호출

### 메인 클래스 설정
    

```python
def __init__(self, root):
    self.root = root
    self.root.title("Rapid Serial Visual Presentation")
    self.root.geometry("800x600")
```

기본 창 구현을 위해 창 이름으로 _**Rapid Serial Visual Presentation**_ 지정
기본 창 사이즈는 800px X 600px로 지정

## Setup sector
```python
self.root.bind("<Configure>", self.resize_widgets)
```
창 사이즈에 맞추어 변화도록 설정
```python
# Text -1
self.text_label = tk.Label(root, text="Enter your text:", font=("Arial", 16))
self.text_label.pack(pady=10)

# Text -2 
self.text_input = tk.Text(root, height=10, font=("Arial", 14), wrap=tk.WORD)
self.text_input.pack(padx=20, pady=10)

# Text -3
self.start_button = tk.Button(root, text="Start", font=("Arial", 14), command=self.start_rsvp)
self.start_button.pack(pady=20)
```

Text-1에서 텍스트 입력 창 상단에 뜨는 텍스트를 폰트 Arial로 설정하고 크기는 16으로 설정
텍스트 상단과 하단에 10px의 여백 설정

Text-2에서는 텍스트 박스를 설정하고 폰트 Arial에 크기를 14로 설정
상하에 10px의 여백을 두고 좌우로 20px의 여백 설정

Text-3에서는 시작버튼을 설정하고 폰트는 Arial에 크기는 14로 설정

```python
self.speed_frame = tk.Frame(root)
self.speed_frame.pack(pady=10)

self.speed_label = tk.Label(self.speed_frame, text="Words per minute (WPM):", font=("Arial", 14))
self.speed_label.grid(row=0, column=0, padx=5)

self.speed_scale = tk.Scale(self.speed_frame, from_=300, to=700, orient='horizontal', length=300, command=self.update_wpm_from_scale)
self.speed_scale.set(300)  # 기본 속도 설정 (300 WPM)
self.speed_scale.grid(row=0, column=1, padx=5)

self.speed_entry = tk.Entry(self.speed_frame, font=("Arial", 14), width=5)
self.speed_entry.insert(0, "300")
self.speed_entry.grid(row=0, column=2, padx=5)
self.speed_entry.bind("<Return>", self.update_wpm_from_entry)
```
슬라이더 바를 생생하고 범위는 300에서부터 700으로 설정 - 단위는 WPM (Word per Minute)   
정해진 값이 아닌 너무 빠른 속도 혹은 너무 느린 속도는 에러메세지 출력

```python
def resize_widgets(self, event):
  self.text_input.config(width=int(self.root.winfo_width() / 10))
  self.start_button.config(width=int(self.root.winfo_width() / 25))
```

창의 크기에 따라 버튼 크기를 조절

```python
def update_wpm_from_scale(self, value):
  self.speed_entry.delete(0, tk.END)
  self.speed_entry.insert(0, value)
```
슬라이더 값을 변경할 경우 텍스트박스 업데이트
```python 
def update_wpm_from_entry(self, event):
  try:
    wpm = int(self.speed_entry.get())
    if 100 <= wpm <= 1000:
      self.speed_scale.set(wpm)
    else:
      raise ValueError
  except ValueError:
    messagebox.showwarning("Warning", "Please enter a valid WPM between 100 and 1000.")
```

텍스트박스에 값을 넣을경우 슬라이더 바에도 적용
하지만 적정값을 벗어난 수는 에러박스 출력

```python
def start_rsvp(self):
  text = self.text_input.get("1.0", tk.END).strip()
  if not text:
    messagebox.showwarning("Warning", "Please enter some text!")
    return

  try:
    wpm = int(self.speed_entry.get())
    if wpm <= 0:
      raise ValueError
  except ValueError:
    messagebox.showwarning("Warning", "Please enter a valid WPM!")
    return
```

텍스트와 속도 가져오기
만약 텍스트가 비어있을 경우 텍스트를 입력하라는 에러메세지 출력
속도가 이상할 경우에도 에러메세지 출력


```python
words = text.split()
delay = 60 / wpm
```
WPM을 시간단위로 변환 - 초단위


## Running Sector

```python
self.fullscreen_window = tk.Toplevel(self.root)
self.fullscreen_window.attributes("-fullscreen", True)
self.fullscreen_window.configure(bg='black')

self.word_label = tk.Label(self.fullscreen_window, text="", font=("Arial", 50), fg='white', bg='black')
self.word_label.pack(expand=True)
```
전체화면을 설정하고 배경은 검정, 폰트는 Arial 색상은 화이트, 크기는 50으로 설정

```python
self.fullscreen_window.bind("<Escape>", lambda e: self.fullscreen_window.destroy())
self.fullscreen_window.bind("<space>", lambda e: self.fullscreen_window.destroy())
```

종료를 위해서 ESC 버튼과 스페이스바를 설정

```python
self.show_words(words, delay)
```
RSVP 시작

```python
def show_words(self, words, delay):
  for word in words:
    self.word_label.config(text=word)
    self.root.update()
    time.sleep(delay)
        
  self.word_label.config(text="")
  self.fullscreen_window.focus_set()
```
텍스트를 순차적으로 보여주고 속도는 사전에 설정한 값으로 시작
모든 텍스트가 종료된 후에도 화면은 검정 전체화면으로 유지

## Starter
```python
if __name__ == "__main__":
    root = tk.Tk()
    app = RSVPApp(root)
    root.mainloop()
```
시작을 위해 위에서 설정한 값을 불러오고 프로그램을 실행
















