/* C kernels for Lab 14-09 (compiled with clang -O2 for RV32IM by cache.py). */

int sum_rows(int *a, int n) {
  int s = 0;
  for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++) s += a[i * n + j];
  return s;
}

int sum_cols(int *a, int n) {
  int s = 0;
  for (int j = 0; j < n; j++)
    for (int i = 0; i < n; i++) s += a[i * n + j];
  return s;
}

void hist(unsigned char *x, int n, int *h) {
  for (int i = 0; i < n; i++) h[x[i] & 15]++;
}

void copy(int *dst, int *src, int n) {
  for (int i = 0; i < n; i++) dst[i] = src[i];
}

int count(int *p) {            /* length of a linked list whose first word is the next pointer */
  int n = 0;
  while (p) {
    p = (int *)*p;
    n++;
  }
  return n;
}

void transpose(int *b, int *a, int n) {
  for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++) b[j * n + i] = a[i * n + j];
}

void transpose_tiled(int *b, int *a, int n, int t) {
  for (int ii = 0; ii < n; ii += t)
    for (int jj = 0; jj < n; jj += t)
      for (int i = ii; i < ii + t; i++)
        for (int j = jj; j < jj + t; j++) b[j * n + i] = a[i * n + j];
}

void mm_ijk(int *a, int *b, int *c, int n) {
  for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++) {
      int s = 0;
      for (int k = 0; k < n; k++) s += a[i * n + k] * b[k * n + j];
      c[i * n + j] = s;
    }
}

void mm_ikj(int *a, int *b, int *c, int n) {
  for (int i = 0; i < n * n; i++) c[i] = 0;
  for (int i = 0; i < n; i++)
    for (int k = 0; k < n; k++) {
      int r = a[i * n + k];
      for (int j = 0; j < n; j++) c[i * n + j] += r * b[k * n + j];
    }
}

void mm_tiled(int *a, int *b, int *c, int n, int t) {
  for (int i = 0; i < n * n; i++) c[i] = 0;
  for (int kk = 0; kk < n; kk += t)
    for (int jj = 0; jj < n; jj += t)
      for (int i = 0; i < n; i++)
        for (int k = kk; k < kk + t; k++) {
          int r = a[i * n + k];
          for (int j = jj; j < jj + t; j++) c[i * n + j] += r * b[k * n + j];
        }
}
