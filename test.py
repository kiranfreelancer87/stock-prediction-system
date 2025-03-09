import numpy as np
import time

# Function to run the computation on CPU for 10 seconds
def run_on_cpu(duration=10):
    # Allocate memory for arrays on the CPU
    host_data = np.random.randn(10000000).astype(np.float32)

    start_time = time.time()
    elapsed_time = 0
    iterations = 0

    # Run the operation continuously for 'duration' seconds
    while elapsed_time < duration:
        # Complex operation on CPU (square, then take square root)
        host_data = np.sqrt(np.square(host_data) + 1.0)  # Square, then sqrt with a constant
        iterations += 1
        elapsed_time = time.time() - start_time

    cpu_time = elapsed_time
    return cpu_time, iterations

# Function to run the computation on GPU using CUDA for 10 seconds
import pycuda.driver as cuda
from pycuda.compiler import SourceModule

def run_on_gpu(duration=10):
    # Allocate memory for arrays on the host (CPU)
    host_data = np.random.randn(10000000).astype(np.float32)

    # Initialize CUDA
    cuda.init()

    # Select the first CUDA device (GPU)
    device = cuda.Device(0)
    context = device.make_context()

    # Allocate memory for arrays on the device (GPU)
    device_data = cuda.mem_alloc(host_data.nbytes)

    # Copy the data from host to device
    cuda.memcpy_htod(device_data, host_data)

    # Define a complex CUDA kernel that squares the elements and adds 1, then takes the square root
    kernel_code = """
    __global__ void complex_operation(float *a)
    {
        int idx = threadIdx.x + blockIdx.x * blockDim.x;
        a[idx] = sqrtf(a[idx] * a[idx] + 1.0f);  // Squared element plus 1, then sqrt
    }
    """

    # Compile the CUDA kernel
    mod = SourceModule(kernel_code)

    # Get the kernel function
    complex_operation_kernel = mod.get_function("complex_operation")

    start_time = time.time()
    elapsed_time = 0
    iterations = 0

    # Run the operation continuously for 'duration' seconds
    while elapsed_time < duration:
        # Launch the kernel (1 block, 1024 threads per block)
        complex_operation_kernel(device_data, block=(1024, 1, 1), grid=(int(host_data.size / 1024), 1))
        iterations += 1
        elapsed_time = time.time() - start_time

    gpu_time = elapsed_time

    # Copy the result back from device to host
    cuda.memcpy_dtoh(host_data, device_data)

    # Clean up the context
    context.pop()

    return gpu_time, iterations

# Run CPU test for 10 seconds
cpu_time, cpu_iterations = run_on_cpu(duration=10)
print(f"CPU time: {cpu_time:.6f} seconds, Iterations: {cpu_iterations}")

# Run GPU test for 10 seconds
gpu_time, gpu_iterations = run_on_gpu(duration=10)
print(f"GPU time: {gpu_time:.6f} seconds, Iterations: {gpu_iterations}")

# Compare the results
speedup = cpu_time / gpu_time if gpu_time != 0 else float('inf')
print(f"Speedup (CPU/GPU): {speedup:.2f}")
