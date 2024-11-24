using UnityEngine;

public class Projectile : MonoBehaviour
{
    public GameObject projectilePrefab;  // Reference to the projectile prefab
    public Transform firePoint;          // Location where the projectile will spawn
    public float projectileSpeed = 10f;  // Speed of the projectile
    private PlayerMovement playerMovement; // Reference to PlayerMovement script

    void Start()
    {
        // Ensure PlayerMovement is assigned if not already
        if (playerMovement == null)
        {
            playerMovement = FindObjectOfType<PlayerMovement>();
        }
    }

    void Update()
    {
        // Fire the projectile when the player presses the Fire button (e.g., E key)
        if (Input.GetKeyDown(KeyCode.E))
        {
            FireProjectile();
        }
    }

    void FireProjectile()
    {
        // Check if PlayerMovement and firePoint are assigned
        if (playerMovement != null && firePoint != null)
        {
            // Instantiate the projectile at the fire point's position and rotation
            GameObject projectile = Instantiate(projectilePrefab, firePoint.position, firePoint.rotation);

            // Get the Rigidbody2D component of the projectile
            Rigidbody2D rb = projectile.GetComponent<Rigidbody2D>();

            // Apply velocity to the projectile in the direction the fire point is facing
            if (rb != null)
            {
                rb.velocity = firePoint.right * projectileSpeed; // firePoint.right points in the direction of the firePoint's rotation
            }
        } 
            Debug.LogWarning("PlayerMovement or firePoint is not set up.");
        }
    }

    // This method is for detecting collision with the projectile (optional)
    private void OnCollisionEnter2D(Collision2D collision)
    {
        // Handle collision logic here
        // For example, destroy the projectile when it collides with something
        Destroy(gameObject);
    }
}