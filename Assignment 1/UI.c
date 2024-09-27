#include<stdio.h>
#include<conio.h>
#include<windows.h>

void readWriteRandom() {
    char randNum[2];

    FILE *randFile = fopen("pseudoRandom.txt", "r");
    fgets(randNum, sizeof(randNum), randFile);
    fclose(randFile);

    FILE *imageSrv = fopen("image-service.txt", "w");
    fputs(randNum, imageSrv);
    fclose(imageSrv);
}

void printPath() {
    char imagePath[50];

    FILE *imageSrv = fopen("image-service.txt", "r");
    fgets(imagePath, sizeof(imagePath), imageSrv);
    fclose(imageSrv);

    printf("Image Path: %s\n\n", imagePath);
}

int main() {
    while (1) {
        printf("Press any key to generate path to a random image...\n");
        getch();

        FILE *randFile = fopen("pseudoRandom.txt", "w");
        fprintf(randFile, "%s", "run");
        fclose(randFile);
        sleep(2);

        readWriteRandom();
        sleep(1);

        printPath();
    }
}