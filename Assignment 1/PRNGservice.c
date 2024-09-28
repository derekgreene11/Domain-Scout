#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<string.h>

void pseudoRandom() {
    int randNum;
    srand (time(NULL));
    randNum = rand() % 5;

    FILE *randFile = fopen("pseudoRandom.txt", "w");
    fprintf(randFile, "%d", randNum);
    fclose(randFile);
}

int main() {
    char buffer[4];
    
    while (1) {
        FILE *randFile = fopen("pseudoRandom.txt", "r");
        fgets(buffer, sizeof(buffer), randFile);
        fclose(randFile);

        if (strcmp(buffer, "run") == 0) {
            sleep(1);
            pseudoRandom();
        }
    }
}