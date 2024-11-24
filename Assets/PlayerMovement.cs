using UnityEngine;

public class PlayerMovement : MonoBehaviour 
{   
    public Animator animator;
    public ProjectileBehaviour ProjectilePrefab;
    public Transform LaunchOffset;
    public float groundSpeed;
    public float jumpSpeed;
    public float deadZone = -20;

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
        FaceInput();
        Shoot();
<<<<<<< HEAD
        CheckGround();
        if(transform.position.x<deadZone){
          Debug.Log("Pipe deleted");
          Destroy(gameObject); 
        }
=======
        // if(transform.position.x<deadZone){
        //     Debug.Log("Pipe deleted");
        //     Destroy(gameObject); 
        // }
>>>>>>> 9d4f35d30da3dbd14c97157b373c245298829fa7
    }

    void MoveWithInput() {
        if (Input.GetKeyDown(KeyCode.A)) {
            body.linearVelocity = Vector2.left*groundSpeed;
        }
        else if(Input.GetKeyDown(KeyCode.D)){
            body.linearVelocity = Vector2.right*groundSpeed;
        }

        if (Input.GetKeyDown(KeyCode.W)) {
            body.linearVelocity = Vector2.up*jumpSpeed;
        }
    
    }

    void FaceInput() {
        // float direction = Mathf.Sign(xInput);
        // transform.localScale = new Vector3(direction, 1, 1);
    }

    void CheckGround() {
        grounded = Physics2D.OverlapAreaAll(groundCheck.bounds.min, groundCheck.bounds.max, groundMask).Length > 0;
    }

    private float ShootCooldown = 50;
    void Shoot() {
        if (Input.GetKey(KeyCode.E)) {
            if (ShootCooldown == 50) {
                Instantiate(ProjectilePrefab, LaunchOffset.position, transform.rotation);
            }
        ShootCooldown -= 1;
        if (ShootCooldown <= 0) {
                ShootCooldown = 50;
            }
        }
    }
}