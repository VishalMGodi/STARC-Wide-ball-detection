using UnityEngine;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class UDPReceive : MonoBehaviour
{
    Thread receiveThread;
    Thread receiveThread2;
    bool startReceiving = true;
    public bool printToConsole = false;
    public string data;
    public string data2;

    public int port = 10000;
    public int port2 = 11001;

    public void Start()
    {
        receiveThread = new Thread(() => ReceiveData(port));
        receiveThread.IsBackground = true;
        receiveThread.Start();

        receiveThread2 = new Thread(() => ReceiveData(port2));
        receiveThread2.IsBackground = true;
        receiveThread2.Start();
    }

    // receive thread
    private void ReceiveData(int port)
    {
        UdpClient client = new UdpClient(port);
        while (startReceiving)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] dataByte = client.Receive(ref anyIP);
                if (port == 10000) {
                    data = Encoding.UTF8.GetString(dataByte);
                } else if (port == 11001) {
                    data2 = Encoding.UTF8.GetString(dataByte);
                }

                if (printToConsole)
                {
                    // Debug.Log($"Received {data2} on port {port} with a type of {data.GetType()}");
                    // Debug.Log($"Received {data} on port {port}");

                    // Debug.Log("DATA: ");
                    // Debug.Log(port);
                }
            }
            catch (Exception err)
            {
                Debug.Log(err.ToString());
            }
        }
    }
}