/* $Cambridge: exim/src/src/auths/get_no64_data.c,v 1.5 2007/01/08 10:50:19 ph10 Exp $ */

/*************************************************
*     Exim - an Internet mail transport agent    *
*************************************************/

/* Copyright (c) University of Cambridge 1995 - 2007 */
/* See the file NOTICE for conditions of use and distribution. */

#include "../exim.h"


/*************************************************
*  Issue a non-b64 challenge and get a response  *
*************************************************/

/* This function is used by authentication drivers to output a challenge
to the SMTP client and read the response line. This version does not use base
64 encoding for the text on the 334 line. It is used by the SPA and dovecot
authenticators.

Arguments:
   aptr       set to point to the response (which is in big_buffer)
   challenge  the challenge text (unencoded)

Returns:      OK on success
              BAD64 if response too large for buffer
              CANCELLED if response is "*"
*/

int
auth_get_no64_data(uschar **aptr, uschar *challenge)
{
int c;
int p = 0;
smtp_printf("334 %s\r\n", challenge);
while ((c = receive_getc()) != '\n' && c != EOF)
  {
  if (p >= big_buffer_size - 1) return BAD64;
  big_buffer[p++] = c;
  }
if (p > 0 && big_buffer[p-1] == '\r') p--;
big_buffer[p] = 0;
if (Ustrcmp(big_buffer, "*") == 0) return CANCELLED;
*aptr = big_buffer;
return OK;
}

/* End of get_no64_data.c */
