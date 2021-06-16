# GoogleMeet-Attendance-Bot
>구글Meet에서 학생들의 출석을 자동으로 수집하는 툴

구글 Meet, Google Classroom 에서 화상강의에 참여한 학생들의 명단을 자동으로 수집합니다.

![](../header.png)

## 설치 방법

python
```sh
pip install selenium
pip install playsound
```
```sh
python MeetBot.py "Google ID" "Google PW" "Google Meet Link"
```

## 실행방법

```sh
python MeetBot.py "Google ID" "Google PW" "Google Meet Link"
```
이후 채팅에서 "!출석" 을 학생이 입력하면, 출석 로그에 기록됨.

## 업데이트 내역

* 0.1.0
    * 첫 출시
* 0.0.1
    * 작업 진행 중

## 정보

배서연 – talk@kakao.one

GPL 3.0 라이센스를 준수하며 ``LICENSE``에서 자세한 정보를 확인할 수 있습니다.
[https://opensource.org/licenses/gpl-3.0.html]

## 기여 방법

1. (<https://github.com/bsy0317/GoogleMeet-Attendance-Bot/fork>)을 포크합니다.
2. (`git checkout -b feature/fooBar`) 명령어로 새 브랜치를 만드세요.
3. (`git commit -am 'Add some fooBar'`) 명령어로 커밋하세요.
4. (`git push origin feature/fooBar`) 명령어로 브랜치에 푸시하세요. 
5. 풀리퀘스트를 보내주세요.
