#define _POSIX_C_SOURCE 199309L 
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

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

    // Usar el mismo método de medición que el paralelo
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    // Procesar por filas para consistencia con la versión paralela
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int idx = y * width + x;
            int r = img[idx * 3 + 0];
            int g = img[idx * 3 + 1];
            int b = img[idx * 3 + 2];
            
            // Usar la misma aritmética entera
            gray_img[idx] = (unsigned char)((299 * r + 587 * g + 114 * b) / 1000);
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double tiempo_ms = (end.tv_sec - start.tv_sec) * 1000.0 + 
                       (end.tv_nsec - start.tv_nsec) / 1000000.0;

    if (!stbi_write_png(argv[2], width, height, 1, gray_img, width)) {
        fprintf(stderr, "Error al guardar la imagen.\n");
        free(gray_img);
        stbi_image_free(img);
        return 1;
    }

    printf("Conversión completada: %s\n", argv[2]);
    printf("Tiempo de ejecución: %.3f ms\n", tiempo_ms);
    printf("Imagen procesada: %dx%d (%zu píxeles)\n", width, height, img_size);

    free(gray_img);
    stbi_image_free(img);
    return 0;
}