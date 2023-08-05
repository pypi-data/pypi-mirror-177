/*
 * LIBOIL - Library of Optimized Inner Loops
 * Copyright (c) 2003,2004 David A. Schleef <ds@schleef.org>
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
 * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
 * IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <liboil/liboilprofile.h>

#include <sys/time.h>
#include <time.h>
#include <string.h>
#include <math.h>

unsigned long oil_profile_stamp_gtod (void)
{
#ifdef HAVE_GETTIMEOFDAY
  struct timeval tv;
  gettimeofday(&tv,NULL);
  return 1000000*(unsigned long)tv.tv_sec + (unsigned long)tv.tv_usec;
#else
  return 0;
#endif
}

void
oil_profile_init (OilProfile *prof)
{
  memset(prof, 0, sizeof(OilProfile));

  prof->min = -1;

}

void
oil_profile_stop_handle (OilProfile *prof)
{
  int i;

  prof->last = prof->stop - prof->start;

  prof->total += prof->last;
  prof->n++;

  if (prof->last < prof->min) prof->min = prof->last;
  
  for(i=0;i<prof->hist_n;i++) {
    if (prof->last == prof->hist_time[i]) {
      prof->hist_count[i]++;
      break;
    }
  }
  if (i == prof->hist_n && prof->hist_n < OIL_PROFILE_HIST_LENGTH) {
    prof->hist_time[prof->hist_n] = prof->last;
    prof->hist_count[prof->hist_n] = 1;
    prof->hist_n++;
  }
}

void
oil_profile_get_ave_std (OilProfile *prof, double *ave_p, double *std_p)
{
  double ave;
  double std;
  int max_i;
  double off;
  double s;
  double s2;
  int i;
  int n;
  double x;

  do {
    s = s2 = 0;
    n = 0;
    max_i = -1;
    for(i=0;i<10;i++){
      x = prof->hist_time[i];
      s2 += x * x * prof->hist_count[i];
      s += x * prof->hist_count[i];
      n += prof->hist_count[i];
      if (prof->hist_count[i] > 0) {
        if (max_i == -1 || prof->hist_time[i] > prof->hist_time[max_i]) {
          max_i = i;
        }
      }
    }

    ave = s / n;
    std = sqrt (s2 - s * s / n + n*n) / (n-1);
    off = (prof->hist_time[max_i] - ave)/std;

    if (off > 4.0) {
      prof->hist_count[max_i] = 0;
    }
  } while (off > 4.0);

  if (ave_p) *ave_p = ave;
  if (std_p) *std_p = std;
}


