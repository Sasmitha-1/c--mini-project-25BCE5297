#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FILE_NAME "data.txt"
#define MAX 100

struct Student {
    int regNo;
    char name[50];
    int total;
    int present;
};

struct Student s[MAX];
int count = 0;

/* ===== LOAD DATA ===== */
void load() {
    FILE *fp = fopen(FILE_NAME, "r");
    if (!fp) return;

    count = 0;

    while (fscanf(fp, "%d %49s %d %d",
                  &s[count].regNo,
                  s[count].name,
                  &s[count].total,
                  &s[count].present) == 4) {
        count++;
    }

    fclose(fp);
}

/* ===== SAVE DATA ===== */
void save() {
    FILE *fp = fopen(FILE_NAME, "w");
    if (!fp) return;

    for (int i = 0; i < count; i++) {
        fprintf(fp, "%d %s %d %d\n",
                s[i].regNo,
                s[i].name,
                s[i].total,
                s[i].present);
    }

    fclose(fp);
}

/* ===== ADD ===== */
void addStudent(int reg, char name[]) {
    for (int i = 0; i < count; i++) {
        if (s[i].regNo == reg) {
            printf("RegNo already exists\n");
            return;
        }
    }

    if (count >= MAX) {
        printf("Limit reached\n");
        return;
    }

    s[count].regNo = reg;
    strcpy(s[count].name, name);
    s[count].total = 0;
    s[count].present = 0;
    count++;

    save();
    printf("Student added\n");
}

/* ===== REMOVE ===== */
void removeStudent(int reg) {
    int found = -1;

    for (int i = 0; i < count; i++) {
        if (s[i].regNo == reg) {
            found = i;
            break;
        }
    }

    if (found == -1) {
        printf("Student not found\n");
        return;
    }

    for (int i = found; i < count - 1; i++) {
        s[i] = s[i + 1];
    }

    count--;

    save();
    printf("Student removed\n");
}

/* ===== MARK ===== */
void markAttendance(int reg, char status) {
    for (int i = 0; i < count; i++) {
        if (s[i].regNo == reg) {
            s[i].total++;

            if (status == 'P' || status == 'p')
                s[i].present++;

            save();
            printf("Attendance marked\n");
            return;
        }
    }

    printf("Student not found\n");
}

/* ===== DISPLAY ===== */
void display() {
    printf("RegNo Name Total Present\n");

    for (int i = 0; i < count; i++) {
        printf("%d %s %d %d\n",
               s[i].regNo,
               s[i].name,
               s[i].total,
               s[i].present);
    }
}

/* ===== ATTENDANCE % ===== */
void attendance() {
    printf("RegNo Name Percentage\n");

    for (int i = 0; i < count; i++) {
        float p = 0;

        if (s[i].total != 0)
            p = (float)s[i].present / s[i].total * 100;

        printf("%d %s %.2f\n",
               s[i].regNo,
               s[i].name,
               p);
    }
}

/* ===== SHORTAGE ===== */
void shortage() {
    printf("RegNo Name Percentage\n");

    for (int i = 0; i < count; i++) {
        float p = 0;

        if (s[i].total != 0)
            p = (float)s[i].present / s[i].total * 100;

        if (p < 75) {
            printf("%d %s %.2f\n",
                   s[i].regNo,
                   s[i].name,
                   p);
        }
    }
}

/* ===== SUMMARY ===== */
void summary() {
    float total = 0;

    for (int i = 0; i < count; i++) {
        if (s[i].total != 0)
            total += (float)s[i].present / s[i].total * 100;
    }

    if (count == 0) {
        printf("No students\n");
    } else {
        printf("Class Average: %.2f\n", total / count);
    }
}

/* ===== MAIN ===== */
int main(int argc, char *argv[]) {
    load();

    /* ===== WEB MODE ===== */
    if (argc > 1) {

        if (strcmp(argv[1], "add") == 0) {
            int reg = atoi(argv[2]);
            char name[100] = "";

            for (int i = 3; i < argc; i++) {
                strcat(name, argv[i]);
                if (i < argc - 1) strcat(name, " ");
            }

            addStudent(reg, name);
        }

        else if (strcmp(argv[1], "remove") == 0) {
            removeStudent(atoi(argv[2]));
        }

        else if (strcmp(argv[1], "mark") == 0) {
            markAttendance(atoi(argv[2]), argv[3][0]);
        }

        else if (strcmp(argv[1], "display") == 0) {
            display();
        }

        else if (strcmp(argv[1], "attendance") == 0) {
            attendance();
        }

        else if (strcmp(argv[1], "shortage") == 0) {
            shortage();
        }

        else if (strcmp(argv[1], "summary") == 0) {
            summary();
        }

        return 0;
    }

    /* ===== TERMINAL MODE ===== */
    int choice, reg;
    char name[50], status;

    while (1) {
        printf("\n--- Attendance Manager ---\n");
        printf("1 Add\n2 Remove\n3 Mark\n4 Display\n5 Attendance\n6 Shortage\n7 Summary\n8 Exit\n");
        printf("Choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("RegNo: ");
                scanf("%d", &reg);
                printf("Name: ");
                scanf("%49s", name);
                addStudent(reg, name);
                break;

            case 2:
                printf("RegNo: ");
                scanf("%d", &reg);
                removeStudent(reg);
                break;

            case 3:
                printf("RegNo: ");
                scanf("%d", &reg);
                printf("P/A: ");
                scanf(" %c", &status);
                markAttendance(reg, status);
                break;

            case 4: display(); break;
            case 5: attendance(); break;
            case 6: shortage(); break;
            case 7: summary(); break;
            case 8: exit(0);
            default: printf("Invalid\n");
        }
    }
}