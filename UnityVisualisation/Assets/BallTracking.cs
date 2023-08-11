using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Text.RegularExpressions;

public class BallTracking : MonoBehaviour {
    
    public UDPReceive udpReceive;
    public GameObject Ball;

    public Vector3 BallPosition;
    public Vector3 BallScale;

    public Vector3 ScalingFactor;

    public GameObject VirtualGuideLine;

    private string pattern = @"[-+]?\d*\.\d+|\d+";
    public Vector3 initPosition = new Vector3(0,0,0);


    // Start is called before the first frame update
    void Start() {
        BallPosition = new Vector3(-0.4f,0, 0);;
        ScalingFactor = new Vector3(-813.5485f,1857.837f,715.3846154f);
        BallScale = new Vector3(0.1f, 0.1f, 0.1f);
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
        }

        if(BallPosition.z > VirtualGuideLine.transform.localPosition.z) {
            Debug.Log("WIDE");
        } else {
            Debug.Log("NOT WIDE");
        }
    }
}