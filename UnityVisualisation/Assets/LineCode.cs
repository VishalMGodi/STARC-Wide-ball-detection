using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LineCode : MonoBehaviour {

    LineRenderer lineRenderer;

    public Transform origin;
    public Transform destination;
    public Vector3 originPosition;
    public Vector3 destinationPosition;
    
    
    // Start is called before the first frame update
    void Start() {
        lineRenderer = GetComponent<LineRenderer>();
        lineRenderer.startWidth = 0.01f;
        lineRenderer.endWidth = 0.01f;
    }

    // Update is called once per frame
    void Update() {

        originPosition = origin.position;
        destinationPosition = destination.position;


        lineRenderer.SetPosition(0, originPosition);
        lineRenderer.SetPosition(1, destinationPosition);
        lineRenderer.transform.position = new Vector3(0, 0, 0);

        // Debug.Log("Rendered Pos: " + lineRenderer.GetPosition(0) + ": Actual Pos: " + originPosition);
    }
}