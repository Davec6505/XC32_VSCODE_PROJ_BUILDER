/*******************************************************************************
  Main Source File

  Company:
    Your Company Name

  File Name:
    main.c

  Summary:
    This file contains the "main" function for TestProject.

  Description:
    This file contains the "main" function for the project.
    Simple bare-metal main function without system initialization dependencies.
 *******************************************************************************/

// *****************************************************************************
// *****************************************************************************
// Section: Included Files
// *****************************************************************************
// *****************************************************************************

#include <stddef.h>                     // Defines NULL
#include <stdbool.h>                    // Defines true
#include <stdlib.h>                     // Defines EXIT_FAILURE
#include <stdint.h>                     // Defines uint32_t, uintptr_t

// *****************************************************************************
// *****************************************************************************
// Variables 
// *****************************************************************************
// *****************************************************************************

// *****************************************************************************
// *****************************************************************************
// Section: Main Entry Point
// *****************************************************************************
// *****************************************************************************

int main ( void )
{
    // Initialize your hardware/peripherals here
    // Example: GPIO configuration, clock setup, etc.
    
    while ( true )
    {
        // Your main application code here
        // Example: toggle LED, read sensors, communicate, etc.
    }

    /* Execution should not come here during normal operation */
    return ( EXIT_FAILURE );
}

/*******************************************************************************
 End of File
*/
