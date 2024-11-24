using UnityEngine;

public class PlayerMovement : MonoBehaviour 
{

    public ProjectileBehaviour ProjectilePrefab;
    public Transform LaunchOffset;
    public float groundSpeed;
    public float jumpSpeed;

    [Range(0f, 1f)]
    public float groundDecay;
    public Rigidbody2D body;
    public BoxCollider2D groundCheck;
    public LayerMask groundMask;

    public bool grounded;

    float xInput;
    float yInput;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        //GetInput();
        MoveWithInput();
        Shoot();
    }

    void FixedUpdate() {
        CheckGround();
        ApplyFriction();
    }

    // void GetInput() {
    //     xInput = Input.GetAxis("Horizontal");
    //     yInput = Input.GetAxis("Vertical");
    // }

    void MoveWithInput() {
        if (Input.GetKeyDown(KeyCode.A)||Input.GetKeyDown(KeyCode.D)) {
            body.linearVelocity = new Vector2(xInput * groundSpeed, body.linearVelocity.y);
        }

        if (Input.GetKeyDown(KeyCode.W) && grounded) {
            body.linearVelocity = new Vector2(body.linearVelocity.x, yInput * jumpSpeed);
        }
        transform.Rotate(0f, 180f, 0f);
    }

    void ApplyFriction() {
        if (grounded && xInput == 0 && yInput == 0) {
            body.linearVelocity *= groundDecay;
        }
    }

    void CheckGround() {
        grounded = Physics2D.OverlapAreaAll(groundCheck.bounds.min, groundCheck.bounds.max, groundMask).Length > 0;
    }

    void Shoot() {
        if (Input.GetButtonDown("Fire1")) {
            Instantiate(ProjectilePrefab, LaunchOffset.position, transform.rotation);
        }
    }
}