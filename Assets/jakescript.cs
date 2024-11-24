using UnityEngine;

public class jakescript : MonoBehaviour 
{   
    public Animator animator;
    public ProjectileBehaviour ProjectilePrefab;
    public float groundSpeed;
    public float jumpSpeed;
    [Range(0f, 1f)]
    public float groundDecay;
    public Rigidbody2D body;
    public BoxCollider2D groundCheck;
    public LayerMask groundMask;


    public bool grounded;

    // Update is called once per frame
    void Update()
    {
        //GetInput();
        MoveWithInput();
        // FaceInput();
        CheckGround();

    }

    void MoveWithInput() {
        if (Input.GetKeyDown(KeyCode.LeftArrow)) {
            body.linearVelocity = Vector2.left*groundSpeed;

        }
        else if(Input.GetKeyDown(KeyCode.RightArrow)){
            body.linearVelocity = Vector2.right*groundSpeed;
        }

        if (Input.GetKeyDown(KeyCode.UpArrow) && grounded) {
            body.linearVelocity = Vector2.up*jumpSpeed;
        }
        float direction = Mathf.Sign(body.linearVelocity.x);
        transform.localScale = new Vector3(direction, 1, 1);
    
    }


    void CheckGround() {
        grounded = Physics2D.OverlapAreaAll(groundCheck.bounds.min, groundCheck.bounds.max, groundMask).Length > 0;
    }
}