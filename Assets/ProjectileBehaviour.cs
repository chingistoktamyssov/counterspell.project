using UnityEngine;

public class ProjectileBehaviour : MonoBehaviour
{
    public float Speed = 0.5f;

    private void Update()
    {
        transform.position += -transform.right * Time.deltaTime * Speed;
        if (transform.position.x<-20 || 20 < transform.position.x){
            Debug.Log("Pipe deleted");
            Destroy(gameObject); 
        }
    }
    private void OnCollisionEnter2D(Collision2D collision) {
        Destroy(gameObject); 
    }

    // private void OnCollisionEnter2D(Collision2D collision) {
    //     Destroy(gameObject);
    // }        
}
