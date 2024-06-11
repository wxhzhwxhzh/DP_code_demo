import autoit
import time

# 打开记事本
autoit.run("notepad.exe")

# 等待记事本窗口打开
autoit.win_wait_active("[CLASS:Notepad]")

# 获取当前时间
current_time = time.strftime("%Y-%m-%d %H:%M:%S")
print(current_time)

# 输入当前时间到记事本
autoit.send(current_time)

# 等待一段时间，以便查看结果
time.sleep(20)

# 关闭记事本
autoit.win_close("[CLASS:Notepad]")
