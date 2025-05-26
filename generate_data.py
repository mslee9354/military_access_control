import csv
import random

purposes = ["근무", "훈련", "휴가", "정비", "물자수송", "경계", "교육", "회의", "점검", "방문"]
destinations = ["본부", "생활관", "창고", "사무실", "훈련장", "정비소", "식당", "관리동"]
time_slots = ["오전", "오후", "야간"]

soldiers = []
for i in range(1000):  # 1000 unique soldier IDs if needed
    if i % 2 == 0:
        soldiers.append(f"24-76{i:04d}")
    else:
        soldiers.append(f"23-67{i:04d}")

with open('data/normal_access_logs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['soldier_id', 'purpose', 'destination', 'time_slot'])
    for _ in range(1000):
        sid = random.choice(soldiers)
        purpose = random.choice(purposes)
        dest = random.choice(destinations)
        time = random.choice(time_slots)
        writer.writerow([sid, purpose, dest, time])
