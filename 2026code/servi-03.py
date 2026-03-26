from gpiozero import AngularServo

# 서보 설정 (핀 번호 18)
servo = AngularServo(18, min_angle=-90, max_angle=90, 
                     min_pulse_width=0.0005, max_pulse_width=0.0025)

print("--- MG996R 각도 제어 프로그램 ---")
print("범위: -90 (최저) ~ 90 (최고)")
print("종료하려면 'q'를 입력하세요.")

while True:
    user_input = input("이동할 각도를 입력하세요 (-90 ~ 90): ")
    
    if user_input.lower() == 'q':
        break
        
    try:
        angle = float(user_input)
        if -90 <= angle <= 90:
            servo.angle = angle
            print(f"현재 각도: {angle}도")
        else:
            print("범위를 벗어났습니다! -90에서 90 사이를 입력하세요.")
            
    except ValueError:
        print("유효한 숫자를 입력해 주세요.")

print("프로그램을 종료합니다.")