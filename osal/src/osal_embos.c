/*******************************************************************************
  embOS OSAL compatibility layer

  Company:
    SEGGER Microcontroller GmbH & Co. KG

  File Name:
    osal_embOS.c

  Summary:
    Provide OSAL mappings for embOS Real-time operating system

  Description:
    This file contains functional implementations of the OSAL for embOS.

*******************************************************************************/

// DOM-IGNORE-BEGIN
/*******************************************************************************
* Copyright (C) 2018 Microchip Technology Inc. and its subsidiaries.
*
* Subject to your compliance with these terms, you may use Microchip software
* and any derivatives exclusively with Microchip products. It is your
* responsibility to comply with third party license terms applicable to your
* use of third party software (including open source software) that may
* accompany Microchip software.
*
* THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
* EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
* WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
* PARTICULAR PURPOSE.
*
* IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
* INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND
* WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS
* BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
* FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
* ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
* THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
*******************************************************************************/
// DOM-IGNORE-END

/*********************************************************************
*
*       Include files
*
**********************************************************************
*/
#include "RTOS.h"
#include "osal/osal_embos.h"

/*********************************************************************
*
*       Semaphore functions
*
**********************************************************************
*/
static OS_UINT CSema_maxCount;

/*********************************************************************
*
*       OSAL_SEM_Create()
*
* Function description
*   Creates an OSAL semaphore
*
* Parameters
*   semID        - Pointer to the Semaphore ID
*   type         - OSAL_SEM_TYPE_BINARY, create a binary semaphore
*                - OSAL_SEM_TYPE_COUNTING, create a counting semaphore with the specified
*                  count values.
*   maxCount     - Maximum value for a counting semaphore. Ignored for a BINARY semaphore.
*   initialCount - Starting count value for the semaphore.
*                  For a BINARY semaphore if initialCount = 0 then Binary Semaphore is
*                  created in a state such semaphore must call 'OSAL_SEM_Post' before it
*                  can call 'OSAL_SEM_Pend' whereas if the initialCount = 1 then the first
*                  call to 'OSAL_SEM_Pend' would pass.
*
* Return value
*   OSAL_RESULT_SUCCESS    - Semaphore created
*   OSAL_RESULT_FAIL   - Semaphore creation failed
*
* Notes
*   Semaphore must have been declared using: OSAL_SEM_DECLARE(semID)
*
* Example
*   OSAL_SEM_Create(&mySemID, OSAL_SEM_TYPE_COUNTING, 10, 5);
*/
OSAL_RESULT OSAL_SEM_Create(OSAL_SEM_HANDLE_TYPE* semID, OSAL_SEM_TYPE type, uint8_t maxCount, uint8_t initialCount)
{
  switch (type)
  {
    case OSAL_SEM_TYPE_BINARY:
      if ( initialCount <= 1)
      {
        if (initialCount == 1)
        {
          OS_CreateCSema(semID, 1);
        }
        else // initialCount = 0
        {
          /* Macro that creates a semaphore with an initial count value of zero. */
          OS_SEMAPHORE_CREATE(semID);
        }
      }
      else // Binary Semaphore initialCount must be either "0" or "1"
      {
        return OSAL_RESULT_FAIL;
      }

      CSema_maxCount = 1;

      return OSAL_RESULT_SUCCESS;

    case OSAL_SEM_TYPE_COUNTING:
      OS_CreateCSema(semID, (OS_UINT)initialCount);
      CSema_maxCount = maxCount;

      return OSAL_RESULT_SUCCESS;

    default:
      return OSAL_RESULT_NOT_IMPLEMENTED;
  }
}

/*********************************************************************
*
*       OSAL_SEM_Delete()
*
* Function description
*   Deletes an OSAL semaphore
*
* Parameters
*   semID        - Pointer to the Semaphore ID
*
* Return value
*   OSAL_RESULT_SUCCESS    - Semaphore deleted
*   OSAL_RESULT_FAIL   - Semaphore deletion failed
*
* Notes
*   Semaphore must have been declared using: OSAL_SEM_DECLARE(semID)
*
* Example
*   OSAL_SEM_Delete(&mySemID);
*
*/
OSAL_RESULT OSAL_SEM_Delete(OSAL_SEM_HANDLE_TYPE* semID)
{
  if (semID == NULL)
  {
    return OSAL_RESULT_FAIL;
  }
  else
  {
    OS_DeleteCSema(semID);
    return OSAL_RESULT_SUCCESS;
  }
}

/*********************************************************************
*
*       OSAL_SEM_Pend()
*
* Function description
*   Waits for a semaphore and obtains it if it is available within
*   a specified time.
*
* Parameters
*   semID        - Semaphore ID
*   waitMS       - Time limit to wait in milliseconds.
*                  0 - do not wait
*                  OSAL_WAIT_FOREVER - return only when semaphore is obtained
*                  Other values - timeout delay
*
* Return value
*   OSAL_RESULT_SUCCESS    - Semaphore obtained
*   OSAL_RESULT_FAIL   - Semaphore obtaining failed
*
* Notes
*   Semaphore must have been declared using: OSAL_SEM_DECLARE(semID)
*
* Example
*   OSAL_SEM_Pend(&mySemID, 50);
*
*/
OSAL_RESULT OSAL_SEM_Pend(OSAL_SEM_HANDLE_TYPE* semID, uint16_t waitMS)
{
  if (waitMS == OSAL_WAIT_FOREVER)
  {
    OS_WaitCSema(semID);
    return OSAL_RESULT_SUCCESS;
  }
  else
  {
    if (OS_WaitCSemaTimed(semID, waitMS) == 1)
    {
      return OSAL_RESULT_SUCCESS;
    }
    else
    {
      return OSAL_RESULT_FAIL;
    }
  }
}

/*********************************************************************
*
*       OSAL_SEM_Post()
*
* Function description
*   Increments the counter of a semaphore. The waiting task with the highest
*   priority will become the running task.
*
* Parameters
*   semID        - Semaphore ID
*
* Return value
*   OSAL_RESULT_SUCCESS    - Semaphore signaled
*
* Notes
*   Semaphore must have been declared using: OSAL_SEM_DECLARE(semID)
*
* Example
*   OSAL_SEM_Post(&mySemID);
*
*/
OSAL_RESULT OSAL_SEM_Post(OSAL_SEM_HANDLE_TYPE* semID)
{
  OS_SignalCSemaMax(semID, CSema_maxCount);
  return OSAL_RESULT_SUCCESS;
}

/*********************************************************************
*
*       OSAL_SEM_PostISR()
*
* Function description
*   Increments the counter of a semaphore from within an ISR. The waiting task with the highest
*   priority will become the running task.
*
* Parameters
*   semID        - Semaphore ID
*
* Return value
*   OSAL_RESULT_SUCCESS    - Semaphore signaled
*
* Notes
*   Semaphore must have been declared using: OSAL_SEM_DECLARE(semID)
*
* Example
*   OSAL_SEM_PostISR(&mySemID);
*
*/
OSAL_RESULT OSAL_SEM_PostISR(OSAL_SEM_HANDLE_TYPE* semID)
{
  OS_SignalCSemaMax(semID, CSema_maxCount);
  return OSAL_RESULT_SUCCESS;
}

/*********************************************************************
*
*       OSAL_SEM_GetCount()
*
* Function description
*   Returns the counter value of a specified semaphore.
*
* Parameters
*   semID        - Semaphore ID
*
* Return value
*   OSAL_RESULT_SUCCESS    - Semaphore signaled
*
* Notes
*   Semaphore must have been declared using: OSAL_SEM_DECLARE(semID)
*
* Example
*   OSAL_SEM_GetCount(&mySemID);
*
*/
uint8_t OSAL_SEM_GetCount(OSAL_SEM_HANDLE_TYPE* semID)
{
  return OS_GetCSemaValue(semID);
}

/*********************************************************************
*
*       Critical region functions
*
**********************************************************************
*/
/*********************************************************************
*
*       OSAL_CRIT_Enter()
*
* Function description
*   Enters a critical region with the specified severity level.
*
* Parameters
*   severity      - OSAL_CRIT_TYPE_LOW, task switchs will be disabled but
*                   interrupts still occure
*                 - OSAL_CRIT_TYPE_HIGH, also interrupts will be disabled
*
* Example
*   OSAL_CRIT_Enter(OSAL_CRIT_TYPE_LOW);
*   OSAL_CRIT_Enter(OSAL_CRIT_TYPE_HIGH);
*
*/
OSAL_CRITSECT_DATA_TYPE OSAL_CRIT_Enter(OSAL_CRIT_TYPE severity)
{
  switch (severity)
  {
    case OSAL_CRIT_TYPE_LOW:
      /* LOW priority critical sections just disable the scheduler */
      OS_EnterRegion();
    break;

    case OSAL_CRIT_TYPE_HIGH:
      /* HIGH priority critical sections disable interrupts */
      OS_IncDI();
      OS_EnterRegion();
    break;
  }
  return(0);//not used with embOS
}

/*********************************************************************
*
*       OSAL_CRIT_Leave()
*
* Function description
*   Leaves a critical region with the specified severity level.
*
* Parameters
*   severity      - OSAL_CRIT_TYPE_LOW, task switchs disabled by OSAL_CRIT_Enter
*                   will be enabled again.
*                 - OSAL_CRIT_TYPE_HIGH, also interrupts will be enabled
*
* Example
*   OSAL_CRIT_Leave(OSAL_CRIT_TYPE_LOW);
*   OSAL_CRIT_Leave(OSAL_CRIT_TYPE_HIGH);
*
*/
void OSAL_CRIT_Leave(OSAL_CRIT_TYPE severity, OSAL_CRITSECT_DATA_TYPE status)
{
  switch (severity)
  {
    case OSAL_CRIT_TYPE_LOW:
      // LOW priority resumes scheduler
      OS_LeaveRegion();
    break;

    case OSAL_CRIT_TYPE_HIGH:
      // HIGH priority renables interrupts
      OS_LeaveRegion();
      OS_DecRI();
    break;
  }
}

/*********************************************************************
*
*       Mutex functions
*
**********************************************************************
*/
/*********************************************************************
*
*       OSAL_MUTEX_Create()
*
* Function description
*   Creates a mutex
*
* Parameters
*   mutexID        - Pointer to the mutex handle
*
* Return value
*   OSAL_RESULT_SUCCESS    - Mutex created
*
* Notes
*   A Mutex must have been declared using: OSAL_MUTEX_DECLARE(mutexID)
*
* Example
*   OSAL_MUTEX_Create(&mutexID)
*
*/
OSAL_RESULT OSAL_MUTEX_Create(OSAL_MUTEX_HANDLE_TYPE* mutexID)
{
  OS_CREATERSEMA(mutexID);
  return OSAL_RESULT_SUCCESS;
}

/*********************************************************************
*
*       OSAL_MUTEX_Delete()
*
* Function description
*   Deletes a mutex
*
* Parameters
*   mutexID        - Pointer to the mutex handle
*
* Return value
*   OSAL_RESULT_SUCCESS    - Mutex deleted
*   OSAL_RESULT_FAIL   - Mutex not deleted
*
* Notes
*   A Mutex must have been declared using: OSAL_MUTEX_DECLARE(mutexID)
*
* Example
*   OSAL_MUTEX_Delete(&mutexID)
*
*/
OSAL_RESULT OSAL_MUTEX_Delete(OSAL_MUTEX_HANDLE_TYPE* mutexID)
{
  if(OS_GetSemaValue(mutexID) != 0)
  {
    return OSAL_RESULT_FAIL;
  }
  else
  {
    OS_DeleteRSema(mutexID);
    return OSAL_RESULT_SUCCESS;
  }
}

/*********************************************************************
*
*       OSAL_MUTEX_Lock()
*
* Function description
*   Locks a mutex and waiting for the time out. If locking was not successful
*   in the specified timeout it returns false.
*
* Parameters
*   mutexID        - Pointer to the mutex handle
*   waitMS         - Timeout value in milliseconds
*                    0 - not timeout, return immediately
*
* Return value
*   OSAL_RESULT_SUCCESS    - Mutex locked
*   OSAL_RESULT_FAIL   - Mutex not locked
*
* Notes
*   A Mutex must have been declared using: OSAL_MUTEX_DECLARE(mutexID)
*
* Example
*   OSAL_MUTEX_DECLARE(mutexID);
*
*   OSAL_MUTEX_Create(&mutexID);
*    ...
*    if (OSAL_MUTEX_Lock(&mutexID, 1000) == OSAL_RESULT_SUCCESS) {
*       // Do something
*       ...
*       // unlock the mutex
*       OSAL_MUTEX_Unlock(&mutexID);
*    }
*
*/
OSAL_RESULT OSAL_MUTEX_Lock(OSAL_MUTEX_HANDLE_TYPE* mutexID, uint16_t waitMS)
{
  if (waitMS != OSAL_WAIT_FOREVER)
  {
    if (OS_UseTimed(mutexID, (OS_TIME)waitMS))
    {
      return OSAL_RESULT_SUCCESS;
    }
    else
    {
      return OSAL_RESULT_FAIL;
    }
  }
  else
  {
    if (OS_Use(mutexID))
    {
      return OSAL_RESULT_SUCCESS;
    }
    else
    {
      return OSAL_RESULT_FAIL;
    }
  }
}

/*********************************************************************
*
*       OSAL_MUTEX_Unlock()
*
* Function description
*   Unlocks a mutex.
*
* Parameters
*   mutexID        - Pointer to the mutex handle
*
* Return value
*   OSAL_RESULT_SUCCESS    - Mutex unlocked
*   OSAL_RESULT_FAIL   - Mutex not unlocked
*
* Notes
*   A Mutex must have been declared using: OSAL_MUTEX_DECLARE(mutexID)
*
* Example
*   OSAL_MUTEX_DECLARE(mutexID);
*
*   OSAL_MUTEX_Create(&mutexID);
*    ...
*    if (OSAL_MUTEX_Lock(&mutexID, 1000) == OSAL_RESULT_SUCCESS) {
*       // Do something
*       ...
*       // unlock the mutex
*       OSAL_MUTEX_Unlock(&mutexID);
*    }
*
*/
OSAL_RESULT OSAL_MUTEX_Unlock(OSAL_MUTEX_HANDLE_TYPE* mutexID)
{
  if (mutexID->UseCnt)
  {
    OS_Unuse(mutexID);
    return OSAL_RESULT_SUCCESS;
  }
  else
  {
    return OSAL_RESULT_FAIL;
  }
}

/*********************************************************************
*
*       Osal control functions
*
**********************************************************************
*/
/*********************************************************************
*
*       OSAL_Name()
*
* Function description
*   Returns the name of the OS.
*
* Return value
*   const char* - Name of the OS
*
* Example
*   ...
*   const char* OS_Name;
*   OS_Name = OSAL_Name();
*   ...
*
*/
const char* OSAL_Name()
{
  return "embOS";
}

/*********************************************************************
*
*       OSAL_Initialize()
*
* Function description
*   Initialize the underlying RTOS.
*
* Return value
*   OSAL_RESULT_SUCCESS  - Initialization completed successfully.
*
* Example
*   int main(void) {
*     OSAL_Initialize();
*     return 0;
*   }
*
*/
OSAL_RESULT OSAL_Initialize(void)
{
  return OSAL_RESULT_SUCCESS;
}

/*******************************************************************************
 End of File
*/
