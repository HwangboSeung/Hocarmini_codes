import cv2

def main():
    video_in = cv2.VideoCapture(1) 
    
    waitTime = 1
    while(1):
        ret, frame = video_in.read()
        if not ret :
            break
        else:
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    video_in.release()
    cv2.destroyAllWindows()

if __name__ =='__main__':
    main()

