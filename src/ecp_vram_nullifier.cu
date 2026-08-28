#include <cuda_runtime.h>
#include <iostream>
#include <cstring>
#include <openssl/sha.h>

extern "C" {

uint8_t* ecp_allocate_vram_shadow_buffer(size_t size) {
    uint8_t* d_vram_ptr = nullptr;
    cudaError_t err = cudaMalloc((void**)&d_vram_ptr, size);
    if (err != cudaSuccess) return nullptr;
    cudaMemset(d_vram_ptr, 0, size);
    return d_vram_ptr;
}

bool ecp_zeroize_and_free_vram(uint8_t* d_vram_ptr, size_t size) {
    if (!d_vram_ptr) return false;
    cudaMemset(d_vram_ptr, 0xFF, size);
    cudaDeviceSynchronize();
    cudaMemset(d_vram_ptr, 0x00, size);
    cudaDeviceSynchronize();
    cudaFree(d_vram_ptr);
    return true;
}

void ecp_generate_deletion_hash(const uint8_t* d_vram_ptr, size_t size, unsigned char* hash_output) {
    uint8_t* h_buffer = (uint8_t*)malloc(size);
    cudaMemcpy(h_buffer, d_vram_ptr, size, cudaMemcpyDeviceToHost);
    SHA256(h_buffer, size, hash_output);
    memset(h_buffer, 0, size);
    free(h_buffer);
}

}
