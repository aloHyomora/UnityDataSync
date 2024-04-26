import socket
import time
import cv2
import struct


def DataReadIntValueWriteFloatValue():
    # 소켓 객체 생성
    with socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    ) as so:  # 네트워크 리소스 사용 후 자동으로 정리, 소켓 사용이 끝나면 자동으로 소켓을 닫음.
        so.bind((host, port))  # 소켓에 주소 할당
        so.listen()  # 클라이언트의 연결을 기다림
        print("Server started. Waiting for connection...")
        conn, addr = so.accept()  # 연결 수락

        with conn:
            print("Connected by", addr)
            while True:
                try:
                    print("Read....")
                    data = conn.recv(
                        1024
                    )  # 한 번에 최대 1024 바이트의 데이터를 수신한다.
                    if not data:
                        print("No data received, attempting to reconnect...")
                        break
                    receivedNumber = int.from_bytes(
                        data, byteorder="little", signed=True
                    )
                    float_number = float(receivedNumber)  # 정수를 실수로 변환
                    print(
                        "Received int : ",
                        receivedNumber,
                        "-> Conver to float : ",
                        float_number,
                    )

                    modified_number = float_number * 2
                    print("Send float value * 2 = ", modified_number)

                    float_data = (
                        str(modified_number).encode("utf-8") + b"\n"
                    )  # 실수를 문자열로 변환 후 바이트로 인코딩하여 전송
                    # bytearray(str(float_number * 2), 'utf-8') # 실수를 문자열로 변환 후 바이트 배열로 변환
                    conn.sendall(float_data)
                except Exception as e:
                    print(f"Error during data processing : {e}. Retrying...")
                    time.sleep(1)

        print("Connection Closed")


def open_local_webCam():
    cv2.namedWindow("first Frame")
    vc = cv2.VideoCapture(0)

    if vc.isOpened:  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("Video Capture Real-time", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

    vc.release()
    cv2.destroyAllWindows()


def send_webcam_data(connection):
    """웹캠 데이터를 소켓을 통해 전송"""
    vc = cv2.VideoCapture(0)  # 웹캠 초기화

    try:
        while vc.isOpened():
            isFrameCaptured, frame = vc.read()
            if not isFrameCaptured:
                break

            # 프레임을 JPEG 포맷으로 압축
            ret, buffer = cv2.imencode(".jpg", frame)
            if not ret:
                continue

            data = buffer.tobytes()  # buffer를 바이트로 변환
            size = struct.pack(
                ">L", len(data)
            )  # 포맷 (">L")에 따라 객체를 패키징하여 바이트 객체로 변환, 빅 엔디언 바이트 순서의 unsigned long(4바이트) 정수를 나타냄
            connection.sendall(size + data)
    finally:
        connection.close()


def initialize_socket(host, port):
    """소켓 초기화 및 클라이언트 연결 대기"""
    with socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    ) as so:  # 네트워크 리소스 사용 후 자동으로 정리, 소켓 사용이 끝나면 자동으로 소켓을 닫음.
        so.bind((host, port))  # 소켓에 주소 할당
        so.listen()  # 클라이언트의 연결을 기다림
        print("Server started. Waiting for connection...")
        conn, addr = so.accept()  # 연결 수락
        print("Connected to:", addr)
        return conn


if __name__ == "__main__":
    # start_server()
    # open_local_webCam()

    print("Server is starting...")
    host = "127.0.0.1"  # 로컬 호스트
    port = 55555

    connection = initialize_socket(host, port)
    if connection:
        send_webcam_data(connection)
