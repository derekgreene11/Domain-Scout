#include<stdio.h>
#include<stdlib.h>
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

void viewImage() {
    char imagePath[100];

    FILE *imageSrv = fopen("image-service.txt", "r");
    fgets(imagePath, sizeof(imagePath), imageSrv);
    fclose(imageSrv);

    HINSTANCE result = ShellExecute(0, "open", imagePath, NULL, NULL, 1);
}

int main() {
    while (1) {
        printf("Press any key to view a random image...\n");
        getch();

        system("cls");
        printf("Loading....");
        FILE *randFile = fopen("pseudoRandom.txt", "w");
        fprintf(randFile, "%s", "run");
        fclose(randFile);
        sleep(1);

        readWriteRandom();
        sleep(1);

        system("cls");
        viewImage();
    }
}