#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Uso: %s <imagen_entrada> <imagen_salida>\n", argv[0]);
        return 1;
    }

    int width, height, channels;
    unsigned char *img = stbi_load(argv[1], &width, &height, &channels, 3);
    if (!img) {
        fprintf(stderr, "Error al cargar la imagen.\n");
        return 1;
    }

    size_t img_size = width * height;
    unsigned char *gray_img = malloc(img_size);
    if (!gray_img) {
        fprintf(stderr, "Error al asignar memoria.\n");
        stbi_image_free(img);
        return 1;
    }

    // Configurar número de hilos según el hardware
    int num_threads = omp_get_max_threads();
    printf("Usando %d hilos\n", num_threads);

    double start = omp_get_wtime();

    // Paralelizar por filas en lugar de píxeles individuales
    #pragma omp parallel for schedule(static) num_threads(num_threads)
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int idx = y * width + x;
            int r = img[idx * 3 + 0];
            int g = img[idx * 3 + 1];
            int b = img[idx * 3 + 2];
            
            // Usar enteros para evitar operaciones en punto flotante
            gray_img[idx] = (unsigned char)((299 * r + 587 * g + 114 * b) / 1000);
        }
    }

    double end = omp_get_wtime();

    if (!stbi_write_png(argv[2], width, height, 1, gray_img, width)) {
        fprintf(stderr, "Error al guardar la imagen.\n");
        free(gray_img);
        stbi_image_free(img);
        return 1;
    }

    printf("Conversión completada: %s\n", argv[2]);
    printf("Tiempo de ejecución: %.3f ms\n", (end - start) * 1000);
    printf("Imagen procesada: %dx%d (%zu píxeles)\n", width, height, img_size);

    free(gray_img);
    stbi_image_free(img);
    return 0;
}