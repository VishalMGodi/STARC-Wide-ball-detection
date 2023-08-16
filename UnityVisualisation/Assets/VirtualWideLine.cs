using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VirtualWideLine : MonoBehaviour
{

    public GameObject VirtualWideLineObject;
    public GameObject BatsmanFoot;
    public GameObject ReturnCreaseObject;
    public GameObject OffsideWicketObject; // Wicket Width = 0.2667 m
    public GameObject TestSphere;
    public Vector3 FootTestPosition;

    private float initialZPosition = 0.0f;
    public float maxShiftZ = 0.0f;
    public bool flag = true;
    // Start is called before the first frame update
    void Start()
    {

        FootTestPosition = BatsmanFoot.transform.position;
        initialZPosition = VirtualWideLineObject.transform.position.z;

    }

    // Update is called once per frame
    void Update()
    {

        float OffstumpZ = (float)(OffsideWicketObject.transform.position.z + 0.2667 / 2);
        float BatsmanFootZ = BatsmanFoot.transform.position.z;
        float WideLineDistanceShift = BatsmanFootZ - OffstumpZ;

        Debug.Log("WidelineShift: " + WideLineDistanceShift);
        Debug.Log("Max_Shift:" + maxShiftZ);
        Debug.Log("Flag: " + flag);

        if (WideLineDistanceShift > maxShiftZ && flag == true)
        {
            if (WideLineDistanceShift >= 0.43)
            {
                VirtualWideLineObject.transform.position = new Vector3(
                    VirtualWideLineObject.transform.position.x, // SAME POSITION
                    VirtualWideLineObject.transform.position.y, // SAME POSITION
                    ReturnCreaseObject.transform.position.z // MOVE VIRTUAL GUIDE LINE TO RETURN CREASE
                );
                flag = false;
            }
            else if (WideLineDistanceShift >= 0f && WideLineDistanceShift < 0.43)
            {
                VirtualWideLineObject.transform.position = new Vector3(
                    VirtualWideLineObject.transform.position.x, // SAME POSITION
                    VirtualWideLineObject.transform.position.y, // SAME POSITION
                    initialZPosition + WideLineDistanceShift
                );
            }
            maxShiftZ = WideLineDistanceShift;
        }
        
    }
}