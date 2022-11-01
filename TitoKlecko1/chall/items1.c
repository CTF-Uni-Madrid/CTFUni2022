#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>

#define ITEM_NONE   0
#define ITEM_INT    1
#define ITEM_STRING 2
#define ITEM_WIN    3

struct item {
	int type;
	union {
		long n;
		char* s;
	} data;
};

#define N_ITEMS 4
#define STRING_SIZE 0x100

char name[32];
struct item items[N_ITEMS];

void error(const char* msg) {
	printf("error: %s\n", msg);
	exit(EXIT_FAILURE);
}

void win() {
	system("cat flag.txt");
	exit(EXIT_SUCCESS);
}

void print_menu() {
	printf("1. Add item\n");
	printf("2. Edit item\n");
	printf("3. Print item\n");
	printf("4. Edit name \n");
}

int read_number(const char* prompt) {
	char buf[10];
	printf("\n%s ", prompt);
	if (fgets(buf, sizeof(buf), stdin) == NULL)
		error("fgets EOF");
	return atoi(buf);
}

void add_item() {
	// Get index
	int idx = read_number("Index:");
	if (idx < 0 || idx > N_ITEMS-1) {
		printf("Invalid index\n");
		return;
	}

	// Check current type
	if (items[idx].type != ITEM_NONE) {
		printf("This item is already filled\n");
		return;
	}

	// Get type
	int type = read_number("Type (1 for int, 2 for string):");
	if (type != 1 && type != 2) {
		printf("Invalid type\n");
		return;
	}
	items[idx].type = type;

	// Get data
	if (type == 1) {
		// Int
		int n = read_number("Int:");
		items[idx].data.n = n;
	} else {
		// String
		char* s = malloc(STRING_SIZE);
		if (s == NULL)
			error("malloc failed");
		printf("String: ");
		fgets(s, STRING_SIZE, stdin);
		items[idx].data.s = s;
	}
}

void edit_item() {
	int idx = read_number("Index:");
	if (idx < 0 || idx > N_ITEMS-1) {
		printf("Invalid index\n");
		return;
	}

	switch (items[idx].type) {
		case ITEM_NONE:
			printf("This item is empty\n");
			break;
		case ITEM_INT: {
			int n = read_number("Int:");
			items[idx].data.n = n;
			break;
		}
		case ITEM_STRING:
			printf("String: ");
			fgets(items[idx].data.s, STRING_SIZE, stdin);
			break;
		case ITEM_WIN:
			win();
			break;
		default:
			printf("Unknown item type: %d\n", items[idx].type);
	}
}

void print_item() {
	// Get index
	int idx = read_number("Index:");
	if (idx < 0 || idx > N_ITEMS-1) {
		printf("Invalid index\n");
		return;
	}

	// Print data acording to type
	switch (items[idx].type) {
		case ITEM_NONE:
			printf("This item is empty\n");
			break;
		case ITEM_INT:
			printf("Data: %ld\n", items[idx].data.n);
			break;
		case ITEM_STRING:
			printf("Data: %s\n", items[idx].data.s);
			break;
		default:
			printf("Unknown item type: %d\n", items[idx].type);
	}
}

void edit_name() {
	printf("New name: ");
	fgets(name, 0x32, stdin);
}

int main(int argc, char** argv) {
	// Make I/O unbuffered (ignore).
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);

	printf("Tell me your name: ");
	fgets(name, 32, stdin);
	printf("Welcome, %s\n", name);

	while (1) {
		print_menu();
		int opt = read_number("> ");
		switch (opt) {
			case 1:
				add_item();
				break;
			case 2:
				edit_item();
				break;
			case 3:
				print_item();
				break;
			case 4:
				edit_name();
				break;
			default:
				printf("Invalid option\n");
		}
		printf("\n");
	}
}