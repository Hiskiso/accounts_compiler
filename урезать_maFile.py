import os
import json

def process_mafiles():
    # Создаем папки input и output, если они не существуют
    input_dir = "input_obrez"
    output_dir = "output_obrez"
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Перебираем все файлы в папке input
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        
        # Проверяем, что это файл и имеет правильное расширение
        if os.path.isfile(input_path) and filename.endswith('.maFile'):
            try:
                # Читаем содержимое файла
                with open(input_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # Проверяем необходимые поля
                required_fields = ['shared_secret', 'account_name', 'Session']
                for field in required_fields:
                    if field not in data:
                        raise ValueError(f"Отсутствует обязательное поле: {field}")
                
                if 'SteamID' not in data['Session']:
                    raise ValueError("Отсутствует поле Session.SteamID")

                # Создаем урезанную версию данных
                new_data = {
                    "shared_secret": data["shared_secret"],
                    "account_name": data["account_name"],
                    "Session": {
                        "SteamID": data["Session"]["SteamID"]
                    }
                }

                output_path = os.path.join(output_dir, filename)
                
                # Сохраняем урезанный файл
                with open(output_path, 'w', encoding='utf-8') as file:
                    json.dump(new_data, file, indent=4)  # Добавляем форматирование для читаемости
                
                print(f"Файл {filename} успешно обработан и сохранен как {filename}")
                    
            except json.JSONDecodeError:
                print(f"Ошибка: файл {filename} содержит некорректный JSON")
            except ValueError as ve:
                print(f"Ошибка в файле {filename}: {str(ve)}")
            except Exception as e:
                print(f"Произошла непредвиденная ошибка при обработке файла {filename}: {str(e)}")

if __name__ == "__main__":
    process_mafiles()