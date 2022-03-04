#!/usr/bin/env python3
import json
import os

project_path = os.path.dirname(os.path.abspath(__file__))
print(project_path)
today_weather = []

with open(project_path + '/weather.json', encoding="utf-8") as f:
    data = json.load(f)
    taipei_weather = data['records']['location'][0]
    location = taipei_weather['locationName']
    element = taipei_weather['weatherElement']
    n = [0, 1]
    for i in n:
        date = element[0]['time'][i]['startTime'][0:10]
        start_time = element[0]['time'][i]['startTime'][11:13]
        end_time = element[0]['time'][i]['endTime'][11:13]
        weather = element[0]['time'][i]['parameter']['parameterName']
        weather_no = element[0]['time'][i]['parameter']['parameterValue']
        chance_of_rain = element[1]['time'][i]['parameter']['parameterName']
        min_temp = element[2]['time'][i]['parameter']['parameterName']
        max_temp = element[4]['time'][i]['parameter']['parameterName']

        today_weather.append({
            'location': location,
            'date': date,
            'start_time': start_time,
            'end_time': end_time,
            'weather': weather,
            'weather_no': weather_no,
            'chance_of_rain': int(chance_of_rain),
            'min_temp': int(min_temp),
            'max_temp': int(max_temp)
        })

w_morning = today_weather[0]
w_afternoon = today_weather[1]
today_max_temp = max(w_morning['max_temp'], w_afternoon['max_temp'])
today_min_temp = min(w_morning['min_temp'], w_afternoon['min_temp'])

path = project_path + '/linehistory/' + date + '.txt'

f = open(path, 'w', encoding="utf-8")
f.writelines(['位置 : ', w_morning['location'], '\n'])
f.writelines(['日期 : ', w_morning['date'], '\n'])
f.writelines(['時間 : ', w_morning['start_time'], ' ~ ',
             w_morning['end_time'], ' ~ ', w_afternoon['end_time'], '\n'])
write_weather = ['天氣 : ', w_morning['weather'], '\n'] if w_morning['weather_no'] == w_afternoon['weather_no'] else [
    '天氣 : ', w_morning['weather'], ' ~ ', w_afternoon['weather'], '\n']
f.writelines(write_weather)
f.writelines(['降雨機率 : ', str(w_morning['chance_of_rain']), ' ~ ',
             str(w_afternoon['chance_of_rain']), ' %', '\n'])
f.writelines(['最高溫度 : ', str(today_max_temp), ' °C', '\n'])
f.writelines(['最低溫度 : ', str(today_min_temp), ' °C', '\n'])
f.writelines(['最大溫差 : ', str(abs(today_max_temp-today_min_temp)), ' °C', '\n'])


path = project_path+'/today-line-message.txt'
f = open(path, 'w', encoding="utf-8")
score = 0
if w_morning['weather'].find('雨') > 0 or w_afternoon['weather'].find('雨') > 0:
    score += 1
if today_min_temp < 22:
    score += 2

template_files = ['nothing.txt', 'rain.txt',
                  'temperature.txt', 'rain-and-temperature.txt']
banner_file = project_path + "/linebot/%s" % (template_files[score])
with open(banner_file, 'rb') as warning_f:
    warning = warning_f.read()
    warning = warning.decode("utf-16")
f.writelines([warning, '\n'])

if score == 1 or score == 3:
    f.writelines(write_weather)
    f.writelines(['降雨機率 : ', str(w_morning['chance_of_rain']), ' ~ ',
                  str(w_afternoon['chance_of_rain']), ' %', '\n'])
if score == 2 or score == 3:
    f.writelines(['最低溫度 : ', str(today_min_temp), ' °C', '\n'])
    
f.writelines([str(score)])
