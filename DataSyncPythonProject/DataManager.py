import socket
import time


def DataReadIntValueWriteFloatValue(conn):
    while True:
        try:
            print("Read....")
            data = conn.recv(1024)  # 한 번에 최대 1024 바이트의 데이터를 수신한다.
            if not data:
                print("No data received, attempting to reconnect...")
                break
            receivedNumber = int.from_bytes(data, byteorder="little", signed=True)
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


def start_server():
    print("Server is starting...")
    host = "127.0.0.1"  # 로컬 호스트
    port = 55555

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
            DataReadIntValueWriteFloatValue(conn)

        print("Connection Closed")


if __name__ == "__main__":
    start_server()
