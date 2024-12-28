
# flutter_translator.py
# This script is an advanced Flutter translation tool designed for Flutter projects. It extracts strings from Dart files, translates them using Google Translate, and generates ARB files for localization.
# Modules:
#     os: Provides a way of using operating system dependent functionality.
#     re: Provides regular expression matching operations.
#     json: Provides functions for working with JSON data.
#     logging: Provides a way to configure and use loggers.
#     googletrans: Provides a way to use Google Translate API.
#     datetime: Supplies classes for manipulating dates and times.
# Classes:
#     bcolors: Contains ANSI escape sequences for colored terminal text.
# Functions:
#     generate_key(text): Generates a key for a given text string.
#     get_language_input(prompt, default=None): Prompts the user for a language input.
#     process_file(file_path, translator, target_language, source_data, translated_data): Processes a Dart file, extracts strings, translates them, and updates the source and translated data dictionaries.
#     extract_and_translate_strings(directory, source_json_file, translated_json_file): Extracts strings from Dart files in a directory, translates them, and saves the source and translated data to JSON files.
#     generate_arb_files(source_data, translated_data, l10n_directory, source_lang_code="en", target_lang_code="ar"): Generates ARB files from the source and translated data.
# Usage:
#     Run the script directly behind Main.dart In Lib Forlder to start the translation process. The script will prompt for the target language and process all Dart files in the current directory, excluding certain files and directories. The results will be saved in the specified output files and directories.

import os
import re
import json
import logging
from googletrans import Translator
from datetime import datetime

# Configure logging
new_folder = "output_files"
os.makedirs(new_folder, exist_ok=True)
log_file = os.path.join(new_folder, "flutter_translate_log.txt")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file, mode='w', encoding='utf-8'), logging.StreamHandler()]
)

# ASCII Art For Me Mostafa Sensei106
ASCII_ART = """
    ╔═══════════════════════════════════════════════════════════╗
    ║       Sensei's Advanced Flutter Translator Tool v1.1      ║
    ║             for Professional Flutter Projects             ║
    ╠═══════════════════════════════════════════════════════════╣
    ║              Developed by: Mostafa Sensei106              ║
    ╚═══════════════════════════════════════════════════════════╝
"""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def generate_key(text):
    key = text.strip().lower().replace(" ", "_").replace(".", "").replace("!", "").replace("?", "")
    return f"key_{key[:30]}"


def get_language_input(prompt, default=None):
    language = input(prompt).strip()
    return language if language else default


def process_file(file_path, translator, target_language, source_data, translated_data):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        content_no_comments = re.sub(r'//.*?$|/\*.*?\*/', '', content, flags=re.DOTALL | re.MULTILINE)
        content_no_imports = re.sub(r'import.*?;', '', content_no_comments)

        matches = re.findall(r'["\'](.*?)["\']', content_no_imports)
        for match in matches:
            if len(match.strip()) > 1:
                key = generate_key(match)
                if key not in source_data:
                    source_data[key] = match
                if key not in translated_data:
                    translated_text = translator.translate(match, dest=target_language).text
                    translated_data[key] = translated_text

                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"{bcolors.OKGREEN}[{timestamp}] Original: '{match}' -> Translated: '{translated_text}'{bcolors.ENDC}")

                content = content.replace(f'"{match}"', f"S.of(context).{key}")
                content = content.replace(f"'{match}'", f"S.of(context).{key}")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    except Exception as e:
        logging.error(f"Error processing file {file_path}: {str(e)}")
        print(f"{bcolors.FAIL}Error processing file {file_path}: {str(e)}{bcolors.ENDC}")


def extract_and_translate_strings(directory, source_json_file, translated_json_file):
    source_data = {}
    translated_data = {}
    translator = Translator()

    target_language = get_language_input(f"{bcolors.OKBLUE}Enter the target language ('ar' for Arabic): {bcolors.ENDC}")

    for subdir, _, files in os.walk(directory):
        if 'generated' in subdir:
            continue
        for file in files:
            if file.endswith(".dart") and "params" not in file and "model" not in file:
                file_path = os.path.join(subdir, file)
                logging.info(f"Processing file: {file_path}")
                process_file(file_path, translator, target_language, source_data, translated_data)

    os.makedirs(os.path.dirname(source_json_file), exist_ok=True)

    try:
        with open(source_json_file, "w", encoding="utf-8") as f:
            json.dump(source_data, f, ensure_ascii=False, indent=4)
        logging.info(f"Source language file saved at: {source_json_file}")
        print(f"{bcolors.OKGREEN}Source language file saved at: {source_json_file}{bcolors.ENDC}")

        with open(translated_json_file, "w", encoding="utf-8") as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=4)
        logging.info(f"Translated language file saved at: {translated_json_file}")
        print(f"{bcolors.OKGREEN}Translated language file saved at: {translated_json_file}{bcolors.ENDC}")
    except Exception as e:
        logging.error(f"Error saving translation files: {str(e)}")
        print(f"{bcolors.FAIL}Error saving translation files: {str(e)}{bcolors.ENDC}")

    return source_data, translated_data


def generate_arb_files(source_data, translated_data, l10n_directory, source_lang_code="en", target_lang_code="ar"):
    source_arb_file = os.path.join(l10n_directory, f"intl_{source_lang_code}.arb")
    translated_arb_file = os.path.join(l10n_directory, f"intl_{target_lang_code}.arb")

    try:
        with open(source_arb_file, "w", encoding="utf-8") as f:
            json.dump(source_data, f, ensure_ascii=False, indent=4)
        logging.info(f"Source ARB file saved at: {source_arb_file}")
        print(f"{bcolors.OKGREEN}Source ARB file saved at: {source_arb_file}{bcolors.ENDC}")

        with open(translated_arb_file, "w", encoding="utf-8") as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=4)
        logging.info(f"Translated ARB file saved at: {translated_arb_file}")
        print(f"{bcolors.OKGREEN}Translated ARB file saved at: {translated_arb_file}{bcolors.ENDC}")
    except Exception as e:
        logging.error(f"Error saving ARB files: {str(e)}")
        print(f"{bcolors.FAIL}Error saving ARB files: {str(e)}{bcolors.ENDC}")


if __name__ == "__main__":
    print(ASCII_ART)
    directory = os.path.dirname(os.path.abspath(__file__))
    l10n_directory = os.path.join(new_folder, "l10n")
    os.makedirs(l10n_directory, exist_ok=True)
    source_json_file = os.path.join(l10n_directory, "intl_en.arb")
    translated_json_file = os.path.join(l10n_directory, "intl_ar.arb")

    logging.info(f"Processing started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{bcolors.HEADER}Processing started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{bcolors.ENDC}")

    source_data, translated_data = extract_and_translate_strings(directory, source_json_file, translated_json_file)

    (source_data, translated_data, l10n_directory)

    logging.info(f"Processing completed - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{bcolors.HEADER}Processing completed - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{bcolors.ENDC}")