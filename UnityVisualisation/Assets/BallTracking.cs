using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Text.RegularExpressions;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;

public class BallTracking : MonoBehaviour {
    
    public UDPReceive udpReceive;
    public GameObject Ball;

    public Vector3 BallPosition;
    public Vector3 BallScale;

    public Vector3 ScalingFactor;

    public GameObject VirtualGuideLine;

    private string pattern = @"[-+]?\d*\.\d+|\d+";
    public Vector3 initPosition = new Vector3(0,0,0);

    private bool dataSent;
    private UdpClient client;


    // Start is called before the first frame update
    void Start() {
        BallPosition = new Vector3(-0.4f,0, 0);
        ScalingFactor = new Vector3(-813.5485f,1857.837f,715.3846154f);
        BallScale = new Vector3(0.1f, 0.1f, 0.1f);

        dataSent = false;
        client = new UdpClient(15000);

        client.Connect("localhost", 17000);

    }

    void sendData(int intData) {
        if(!dataSent) {
            dataSent = true;
            
            // Print dataSent value in red
            // Debug.Log("<color=red>dataSent: " + dataSent + "</color>");
            // Debug.Log("<color=green>dataSent: " + intData + "</color>");
            string msg = ""+intData+"";
            byte[] data = Encoding.ASCII.GetBytes(msg);
            client.Send(data, data.Length);

            // Send data through UDP
            // client.
            // Debug.Log("<color=yellow>msg AFTER: " + msg + "</color>");
            // Debug.Log("<color=yellow>msg AFTER: " + msg.GetType() + "</color>");
            // Debug.Log("<color=red>dataSent AFTER: " + dataSent + "</color>");
            // Debug.Log("<color=green>dataSent AFTER: " + intData + "</color>");
        }
    }

    // Update is called once per frame
    void Update() {

        Ball.transform.localScale = BallScale;
        Ball.transform.localPosition = BallPosition;

        // ScalingFactor.x = 4164.521f;
        // ScalingFactor.y = 4164.521f;


        string data = udpReceive.data2;
        MatchCollection matches = Regex.Matches(data, pattern);
        if (matches.Count == 3)
        {
            float z = -float.Parse(matches[2].Value) / ScalingFactor.z + initPosition.z; // Scaling Factor = 715.3846154

            // Set the position of the sphere based on the extracted numbers
            // print(x,y,z);
            // Debug.Log(x);
            // Debug.Log(y);
            // Debug.Log(z);

            BallPosition.z = z;

            // Debug.Log("<color=red>dataSent AFTER: " + matches + "</color>");
            if(BallPosition.z > VirtualGuideLine.transform.localPosition.z) {
                // Debug.Log("WIDE");
                Debug.Log("<color=red>WIDE</color>");
                sendData(1);
            } else {
                // Debug.Log("NOT WIDE");
                Debug.Log("<color=green>NOT WIDE</color>");
                sendData(0);

                // Call sendData
                // sendData(0);
            }
        }

        
    }
}