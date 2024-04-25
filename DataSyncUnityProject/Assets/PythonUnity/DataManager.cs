using System;
using System.Collections;
using System.IO;
using System.Net.Sockets;
using UnityEngine;

public class DataManager : MonoBehaviour
{
	[Range(1, 100)] public int numToSend = 0;
	
	private TcpClient _client;
	private NetworkStream _stream;
	private StreamReader _reader;
	private void Start()
	{
		ConnectToServer();
		StartCoroutine(SendingIntDataRoutine());
		StartCoroutine(ReceivingFloatDataRoutine());
	}

	void ConnectToServer()
	{
		try
		{
			_client = new TcpClient("localhost", 55555);
			_stream = _client.GetStream();
			_reader = new StreamReader(_stream);
			Debug.Log($"Connected to server.");
			
			
		}
		catch (Exception e)
		{
			Debug.LogError($"Socket Error : {e.Message}");
			throw;
		}
	}

	IEnumerator SendingIntDataRoutine()
	{
		while (true)
		{
			if (_client != null && _stream != null && _stream.CanWrite)
			{
				try
				{
					// 정수형 데이터 보내기(쓰기)
					byte[] data = BitConverter.GetBytes(numToSend);
					_stream.Write(data, 0, data.Length);
					Debug.Log($"Data sent : {numToSend}");
				}
				catch (Exception e)
				{
					Debug.LogError($"Error sending data : {e.Message}");
					break;
				}
			}

			yield return null; // new WaitForSeconds(1f);
		}
	}

	IEnumerator ReceivingFloatDataRoutine()
	{
		while (true)
		{
			if (_client != null && _stream != null && _stream.CanRead)
			{
				try
				{
					// 데이터 읽기
					if (!_reader.EndOfStream) // 데이터에 줄 끝 표시가 없으면 EndOfStream이 true가 된다.
					{
						string message = _reader.ReadLine();
						Debug.Log($"Received data : {message}");
					}
				}
				catch (Exception e)
				{
					Debug.LogError($"Error receiving data : {e.Message}");
					break;
				}
			}
			yield return null;
		}
	}

	private void OnDestroy()
	{
		// 자원 정리
		if(_reader != null) _reader.Close();
		if(_stream != null) _stream.Close();
		if(_client != null) _client.Close();
	}
}
