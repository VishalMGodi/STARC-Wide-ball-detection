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
    public float groundOffset;

    void Start() {
        PosePosition = new Vector3(-4.1f, -1.75f, 0.79f);
        PoseScale = new Vector3(1f, 1f, 1f);
        PoseRotation = new Vector3(0,180,0);
        PoseDiv = new Vector3(122,114.7f,234);
        groundOffset = 0.0f;
    }

    // Update is called once per frame
    void Update() {

        // Pose.transform.localScale = PoseScale;
        // Pose.transform.localPosition = PosePosition;
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

        // float y30 = float.Parse(points[30 * 3 + 1]) / PoseDiv.y; // Right Heel
        // float y31 = float.Parse(points[31 * 3 + 1]) / PoseDiv.y; // Left Toe
        float y30 = posePoints[30-11].transform.position.y; // Right Heel
        float y31 = posePoints[31-11].transform.position.y; // Left Toe
        bool onGround = true;

        for(int i=29;i<33;i++){
            float x = float.Parse(points[i * 3])     / PoseDiv.x + PosePosition.x;  // 170
            float y = float.Parse(points[i * 3 + 1]) / PoseDiv.y + PosePosition.y;  // 215
            float z = float.Parse(points[i * 3 + 2]) / PoseDiv.z + PosePosition.z;  // 700

            posePoints[i-11].transform.localPosition = new Vector3(x, y, z);

            if(posePoints[i-11].transform.position.y < 0.0f){
                groundOffset = -1 * posePoints[i-11].transform.position.y;
                Debug.Log($"{i}: {x} {y} {z} : GroundOffset:{groundOffset}");
                posePoints[i-11].transform.position = new Vector3(posePoints[i-11].transform.position.x, 0.0f, posePoints[i-11].transform.position.z);
            }else{
                groundOffset = 0;
                onGround = false;
            }
        }

        for(int i=11;i<29;i++){
            float x = float.Parse(points[i * 3])     / PoseDiv.x + PosePosition.x;  // 170
            float y = float.Parse(points[i * 3 + 1]) / PoseDiv.y + PosePosition.y;  // 215
            float z = float.Parse(points[i * 3 + 2]) / PoseDiv.z + PosePosition.z;  // 700

            posePoints[i-11].transform.localPosition = new Vector3(x, y, z);
            
            // if(i >= 29 && posePoints[i-11].transform.position.y < 0.0f){
            //     groundOffset = -1 * posePoints[i-11].transform.position.y;
            //     Debug.Log($"{i}: {x} {y} {z} : GroundOffset:{groundOffset}");
            //     posePoints[i-11].transform.position = new Vector3(posePoints[i-11].transform.position.x, 0.0f, posePoints[i-11].transform.position.z);
            // }else{
            //     groundOffset = 0;
            // }    
        }

        if(onGround){
            Pose.transform.localPosition = new Vector3(Pose.transform.localPosition.x, 
                                                       Pose.transform.localPosition.y + groundOffset,
                                                       Pose.transform.localPosition.z);
        }

        // Debug.Log($"RightHeel(y)[loc]: {y30}, groundOffset: {groundOffset}, Left Toe (y): {y31}");
        // Debug.Log($"RightHeel(y)[abs]: {posePoints[30-11].transform.position}");

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