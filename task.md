1) Реализовать следующее решение на языке Python - «Нейроcказка про погоду в городе N»
Входные данные с консоли:
⁃ Город - на Русском или Английском языках
⁃ Жанр - один из вариантов Drama, Comedy, Musical, Detective, Action, Horror
⁃ Длина в символах
По вводным данным программа должна:
- найти геолокацию указанного города (используйте открытые API)
- по геолокации узнать прогноз погоды на завтра (используйте открытые API)
- составить промпт к нейросети с задачей придумать сказку в заданном жанре про погоду на завтра в заданном городе, не больше указанной длины
- в параллельном режиме сделать запрос промпта в двух нейросетях - YandexGPT (https://yandex.cloud/ru/docs/foundation-models/concepts/yandexgpt/) и GigaChat (https://developers.sber.ru/docs/ru/gigachat/api/overview)
⁃ засечь время от запроса до ответа каждой модели
⁃ ответ каждой нейросети записать в файл
- в консоль вывести название модели, длительность запроса и название файла

2) Снабдить код комментариями / документацией
3) Выложить решение на GitHub
4) Прислать нам ссылку на репозиторий
