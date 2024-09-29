#include<stdio.h>
#include<conio.h>
#include<string.h>

int readRandom() {
    int randNum;

    FILE *imageSrv = fopen("image-service.txt", "r");
    fscanf(imageSrv, "%d", &randNum);
    fclose(imageSrv);
    return randNum;
}

char* generateImagePath(int randomNumber) {
    char *imageSet[6] = {
        "C:\\Users\\Derek\\Desktop\\CS361\\Assignment 1\\images\\image1.jpg",
        "C:\\Users\\Derek\\Desktop\\CS361\\Assignment 1\\images\\image2.jpg", 
        "C:\\Users\\Derek\\Desktop\\CS361\\Assignment 1\\images\\image3.jpg",
        "C:\\Users\\Derek\\Desktop\\CS361\\Assignment 1\\images\\image4.jpg",
        "C:\\Users\\Derek\\Desktop\\CS361\\Assignment 1\\images\\image5.jpg",
        "C:\\Users\\Derek\\Desktop\\CS361\\Assignment 1\\images\\image6.jpg"
        };

    char imagePath[50];

    if (randomNumber >= 5) {
        randomNumber = randomNumber % 5;
    }
    return imageSet[randomNumber];
}

int main() {
    char buffer[2];

    while (1) {
        FILE *imageSrv = fopen("image-service.txt", "r");
        fgets(buffer, sizeof(buffer), imageSrv);
        fclose(imageSrv);

        if (strcmp(buffer, "0") == 0  || strcmp(buffer, "1") == 0 ||
            strcmp(buffer, "2") == 0 || strcmp(buffer, "3") == 0 ||
            strcmp(buffer, "4") == 0 || strcmp(buffer, "5") == 0) {

            int randomNumber = readRandom();
            char *imagePath = generateImagePath(randomNumber);   

            sleep(1);
            FILE *imageSrv = fopen("image-service.txt", "w");
            fputs(imagePath, imageSrv);
            fclose(imageSrv);
           continue;
        }
    }
}