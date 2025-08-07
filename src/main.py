from utils import create_xlsx_and_move_to_files
from chat_generator import generate_chats


def main():
    generate_chats()
    create_xlsx_and_move_to_files()

if __name__ == "__main__":
    main()