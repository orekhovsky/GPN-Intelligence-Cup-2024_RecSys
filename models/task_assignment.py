import pandas as pd
from datetime import datetime, timedelta
from models.recommendation import recommend_candidates  # Импортируем функцию
# Проверка и преобразование даты в нужный формат
def convert_to_date(date):
    if isinstance(date, str):
        try:
            return datetime.strptime(date, '%d.%m.%Y')
        except ValueError:
            print(f"Некорректный формат даты: {date}")
            return None
    return date

# Алгоритм последовательного выполнения задач
def assign_tasks(tasks_table, availability, average_duration, hero_marks_mean, hero_abilities, rest_days):
    for index, task in tasks_table.iterrows():
        task_group = task['group']
        task_date = convert_to_date(task['Дата поручения'])
        
        if task_date is None:
            print(f"Некорректная дата поручения в строке {index}, пропуск задания.")
            continue

        for hero in availability['Герой']:
            hero_tasks = tasks_table[(tasks_table['Исполнитель'] == hero) & (tasks_table['Предполагаемая дата выполнения'].notnull())]
            if not hero_tasks.empty:
                last_end_date = hero_tasks['Предполагаемая дата выполнения'].max()
                availability.loc[availability['Герой'] == hero, 'Доступен'] = last_end_date + timedelta(days=rest_days)
            else:
                availability.loc[availability['Герой'] == hero, 'Доступен'] = None

        recommended_candidates = recommend_candidates(task_group, hero_marks_mean, hero_abilities, availability, task_date)
        if recommended_candidates.empty:
            print(f"Нет доступных кандидатов для задачи в строке {index}")
            continue

        best_candidate = recommended_candidates.iloc[0]
        hero_name = best_candidate['Герой']
        availability.loc[availability['Герой'] == hero_name, 'Доступен'] = task_date + timedelta(days=1)
        tasks_table.at[index, 'Исполнитель'] = hero_name

        hero_duration = average_duration[(average_duration['Герой'] == hero_name) & (average_duration['group'] == task_group)]
        days_required = hero_duration['Затрачено дней'].values[0] if not hero_duration.empty else 1
        tasks_table.at[index, 'Затрачено дней'] = days_required
        tasks_table.at[index, 'Предполагаемая дата выполнения'] = task_date + timedelta(days=days_required)

    return tasks_table
