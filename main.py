import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

import numpy

a = numpy.random.randn(4, 4)  # create 4x4 vector data
a = a.astype(numpy.float32)  # change data format to single precision numbers
a_gpu = cuda.mem_alloc(a.nbytes)  # allocate memory for sizeof(a)
cuda.memcpy_htod(a_gpu, a)  # copy a data into a_gpu allocated memory

mod = SourceModule("""
  __global__ void doublify(float *a)
  {
    int idx = threadIdx.x + threadIdx.y*4;
    a[idx] = a[idx] * 2;
  }
  """)

func = mod.get_function("doublify")
func(a_gpu, block=(4, 4, 1))  # (arguments, size oh threads)

a_doubled = numpy.empty_like(a)  # create similar structure to a but empty
cuda.memcpy_dtoh(a_doubled, a_gpu)  # copy the content of a_gpu into a_doubled
print a
print "\n"
print a_doubled