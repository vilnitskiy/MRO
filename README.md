# MRO #
Клонируем:
```
git clone https://github.com/vilnitskiy/MRO.git
cd MRO
```
Затем разворачиваем локально:
```
virtualenv .venv --no-site-packages
source .venv/bin/activate
pip install -r requirements.txt
cd mro
scrapy list
```
**
Все новые спайдеры должны быть в папке mro/spiders.
Все .csv файлы от заказчика должны быть в папке mro/spiders/csv_data.
Все .csv результаты сбора в mro/results.
**
TODO reminder:
1) Вынести прокси в отдельную стратегию
2) Навести порядок в utils
3) Создать отдельные стратегии для разной скорости краулинга
4) Создать отдельные стратегии с распространёнными юзерагентами