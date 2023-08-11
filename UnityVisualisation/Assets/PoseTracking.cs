using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NewBehaviourScript : MonoBehaviour {
    // Start is called before the first frame update
    public UDPReceive udpReceive;
    public GameObject[] posePoints;
    public GameObject Pose;
    public Vector3 PosePosition;
    public Vector3 PoseScale;
    public Vector3 PoseRotation;

    void Start() {
        PoseScale = new Vector3(0.67f, 1f, 1f);
        PosePosition = new Vector3(-2.41f, -0.6f, 0.06f);
        // Pose.transform.localEulerAngles = new Vector3(6.77f,0f,0f);
    }

    // Update is called once per frame
    void Update() {

        Pose.transform.localScale = PoseScale;
        Pose.transform.localPosition = PosePosition;
        

        string data = udpReceive.data;
        // if data is empty return
        if (data == "") {
            return;
        }

        if(udpReceive.port == 11001) {
            return;
        }
        data = data.Remove(0,1);
        data = data.Remove(data.Length-1,1);

        string[] points = data.Split(',');

        // print("Pose Position: " + Pose.transform.position.x + " " + Pose.transform.position.y + " " + Pose.transform.position.z);

        // x0,y0,z0,x1,y1,z1,x2,y2,z2,x3,y3,z3
        // Debug.Log(points)
        // 0

        for(int i=11;i<33;i++){
            float x = float.Parse(points[i * 3])     / 170;  // 170
            float y = float.Parse(points[i * 3 + 1]) / 215;  // 215
            float z = float.Parse(points[i * 3 + 2]) / 200;  // 700

            // if(i == 32){
            //     print("RightFoot: " + x + " " + y + " " + z);
            // }

            posePoints[i-11].transform.localPosition = new Vector3(x, y, z);
        }
    }
}


//  + offsetPosition.x - originalPosePosition.x
//  + offsetPosition.y - originalPosePosition.y
//  + offsetPosition.z - originalPosePosition.z