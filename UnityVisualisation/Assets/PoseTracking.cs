using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NewBehaviourScript : MonoBehaviour {
    // Start is called before the first frame update
    public UDPReceive udpReceive;
    public GameObject[] posePoints;
    public GameObject Pose;
    public GameObject PosePointsGroup;
    public Vector3 PosePosition;
    public Vector3 PoseScale;
    public Vector3 PoseRotation;
    public Vector3 PoseDiv;

    void Start() {
        PosePosition = new Vector3(4.04f, -2.44f, -0.8f);
        PoseScale = new Vector3(1f, 1f, 1f);
        PoseRotation = new Vector3(0,180,0);
        PoseDiv = new Vector3(122,114.7f,234);
    }

    // Update is called once per frame
    void Update() {

        Pose.transform.localScale = PoseScale;
        Pose.transform.localPosition = PosePosition;
        PosePointsGroup.transform.rotation = Quaternion.Euler(PoseRotation.x, PoseRotation.y, PoseRotation.z);
        

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

        float groundOffset = 0.0f;

        // float y30 = float.Parse(points[30 * 3 + 1]) / PoseDiv.y; // Left Heel
        // float y31 = float.Parse(points[31 * 3 + 1]) / PoseDiv.y; // Left Toe
        float y30 = float.Parse(points[30 * 3 + 1]) / PoseDiv.y; // Left Heel
        float y31 = float.Parse(points[31 * 3 + 1]) / PoseDiv.y; // Left Toe

        if (y30 < 0.0f){
            groundOffset = -1 * y30;
        }else{
            groundOffset = 0.0f;
        }

        for(int i=11;i<33;i++){
            float x = float.Parse(points[i * 3])     / PoseDiv.x;  // 170
            float y = float.Parse(points[i * 3 + 1]) / PoseDiv.y + groundOffset;  // 215
            float z = float.Parse(points[i * 3 + 2]) / PoseDiv.z;  // 700

            if(i >= 30 && y < 0.0f){
                y = 0.0f;
            }

            posePoints[i-11].transform.localPosition = new Vector3(x, y, z);
        }

        Debug.Log($"groundOffset: {groundOffset}, Left Heel (y): {y30}, Left Toe (y): {y31}");
        Debug.Log($"Left Heel (y): {posePoints[30-11].transform.position}, Left Toe (y): {y31}");
        //! Pose Calibration
        // // Left Sholder Coords
        // float x11 = float.Parse(points[11 * 3])     / PoseDiv.x;
        // float y11 = float.Parse(points[11 * 3 + 1]) / PoseDiv.y;
        // float z11 = float.Parse(points[11 * 3 + 2]) / PoseDiv.z;

        // // Right Sholder Coords
        // float x12 = float.Parse(points[12 * 3])     / PoseDiv.x;
        // float y12 = float.Parse(points[12 * 3 + 1]) / PoseDiv.y;
        // float z12 = float.Parse(points[12 * 3 + 2]) / PoseDiv.z;

        // // Right Foot Toe
        // float x32 = float.Parse(points[32 * 3])     / PoseDiv.x;
        // float y32 = float.Parse(points[32 * 3 + 1]) / PoseDiv.y;
        // float z32 = float.Parse(points[32 * 3 + 2]) / PoseDiv.z;

        // // Right Foot Heel
        // float x30 = float.Parse(points[30 * 3])     / PoseDiv.x;
        // // float y30 = float.Parse(points[30 * 3 + 1]) / PoseDiv.y;
        // float z30 = float.Parse(points[30 * 3 + 2]) / PoseDiv.z;


        // float shoulderWidth = Mathf.Sqrt(Mathf.Pow(x11-x12,2)+Mathf.Pow(y11-y12,2)+Mathf.Pow(z11-z12,2));
        // float footLength = Mathf.Sqrt(Mathf.Pow(x32-x30,2)+Mathf.Pow(y32-y30,2)+Mathf.Pow(z32-z30,2));
        // Debug.Log($"shoulderWidth: {shoulderWidth}, footLength: {footLength}");
    }
}


//  + offsetPosition.x - originalPosePosition.x
//  + offsetPosition.y - originalPosePosition.y
//  + offsetPosition.z - originalPosePosition.z