using System;
using System.Collections;
using System.IO;
using System.Net.Sockets;
using UnityEngine;
using UnityEngine.UI;

public class WebcamReceiver : MonoBehaviour
{
    public string serverIP = "127.0.0.1";   // 서버 IP 주소
    public int serverPort = 55555;          // 연결할 서버의 포트 번호
    private TcpClient _client;              // TCP 클라이언트 인스턴스
    private NetworkStream _stream;          // 네트워크 스트림

    public Texture2D texture;
    public Material rawImageMaterial;
    public RawImage rawImage;
    private void Start()
    {
        InitializeSocket();
        StartCoroutine(ReceiveData());
    }

    void InitializeSocket()
    {
        _client = new TcpClient(serverIP, serverPort);  // IP 주소와 포트로 TCP 클라이언트 초기화
        _stream = _client.GetStream();                  // 클라이언트의 데이터 스트림을 가져옴
        texture = new Texture2D(0, 0);
    }

    private IEnumerator ReceiveData()
    {
        while (true)
        {
            if (_stream.DataAvailable)          // 데이터가 스트림에 있는지 확인
            {
                byte[] sizeInfo = new byte[4];  // 파이썬에서 4바이트 빅엔디언 포맷으로 패킹해서 전송함.
                if (ReadFull(_stream, sizeInfo, sizeInfo.Length)) // 스트림에서 데이터 하나를 모두 읽음
                {
                    Array.Reverse(sizeInfo);
                    int webcamDataSize = BitConverter.ToInt32(sizeInfo, 0); // sizeInfo 바이트 배열엔 웹캠 데이터의 크기가 바이트 배열로 담겨있음.
                    Debug.Log(webcamDataSize);
                    byte[] data = new byte[webcamDataSize];     // 데이터를 저장할 바이트 배열
                    if (ReadFull(_stream, data, webcamDataSize)) // 스트림에서 데이터를 읽음
                    {
                        // 이제 이미지를 텍스처로 로드
                        if (texture.LoadImage(data)) // JPEG 이미지 데이터를 Texture2D로 직접 로드
                        {
                            // rawImageMaterial.mainTexture = texture; // 텍스처를 머티리얼에 적용
                            rawImage.texture = texture;
                        }
                        else
                        {
                            Debug.LogError("Failed to load texture from received data");
                        }
                    }
                    else
                    {
                        Debug.LogError("Incomplete data received");
                    }
                }
                else
                {
                    Debug.LogError("Failed to read size information");
                }
            }
            yield return null; // 대기 없이 계속 루프를 돌게 하여 응답을 빠르게 처리
        }
    }
    private bool ReadFull(Stream stream, byte[] buffer, int size)
    {
        int index = 0;
        while (index < size)
        {
            int bytesRead = stream.Read(buffer, index, size - index);
            if (bytesRead == 0)
            {
                return false; // 스트림의 끝에 도달하거나 읽을 데이터가 없음
            }
            index += bytesRead;
        }
        return true;
    }
    private void OnApplicationQuit()
    {
        _stream.Close();
        _client.Close();
    }
}
