using UnityEngine;

public class ProjectileBehaviour : MonoBehaviour
{
    public float Speed = 0.5f;
    float timer = 0;
    static public int jakeHealth = 3;

    private void Update()
    {
        transform.position += transform.right * Time.deltaTime * Speed;
        if (transform.position.x<-20 || 20 < transform.position.x){
            Debug.Log("Pipe deleted");
            Destroy(gameObject); 
        }
    }
    private void OnCollisionEnter2D(Collision2D collision) {
        if(timer>0){
         Destroy(gameObject); 
         timer=0;
         jakeHealth--;
        }
        else{
            timer++;
        }

    }    
}
