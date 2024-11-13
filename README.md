# GPN-Intelligence-Cup-2024

Основное полное решение находится в ноутбуке =solution.ipynb=
В папке src находятся исходные данные кейса. 

В папке additional tables находятся необходимые для решения таблицы:
- всё что начинается на hero - это таблицы с профилями героев
- tasks_table - таблица с невыполненными поручениями, которая используется для формирования команд и туда же впоследствии вписываются выбранные кандидаты и другие данные

В папке additional_data находятся описания поручений, разбитые по кластерам

В папке compare suggestions находятся две таблицы:
- tasks_table_with_RecSys - таблица с выбранными героями посредством разработанной в ходе решения кейса рекомендательной системой 
- tasks_table_with_random_heroes_1 - таблица случайного распределения героев по задачам. Таблица для наглядности всего одна. В ноутбуке показано сравнение разработанной системы с 1000 аналогичными решениями рандомной системы.

В папке models находится два скрипта для оптимального подбора кандидата(ов) в команду для выполнения поручения

short_example.ipynb - показательное короткое решение, которое выводит итоговую таблицу выбранных Аркашей команд, используя скрипты из папки models. 

MindMap.png - карта для идей в ходе решения и общей картины

trash.ipynb - мусорный код
