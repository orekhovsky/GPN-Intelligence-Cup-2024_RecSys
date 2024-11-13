import pandas as pd

# Функция для подбора кандидатов по задаче с учетом доступности героев
def recommend_candidates(task_group, hero_marks_mean, hero_abilities, availability, task_date):
    group_actions = {
        0: ['разжечь костёр', 'залечить раны', 'выследить цель'],
        1: ['найти пропажу', 'отыскать заказчика'],
        2: ['выследить цель'],
        3: ['разжечь костёр', 'залечить раны'],
        4: ['разжечь костёр', 'выследить цель']
    }
    
    target_actions = group_actions.get(task_group, [])
    available_heroes = availability[
        (availability['Доступен'].isnull()) | (availability['Доступен'] < task_date)
    ]['Герой'].tolist()
    filtered_final_table = hero_abilities[hero_abilities['Герой'].isin(available_heroes)]
    relevant_heroes = filtered_final_table[['Герой'] + target_actions].copy()
    avg_action_scores = relevant_heroes[target_actions].mean()
    relevant_heroes['Skill Score'] = relevant_heroes[target_actions].mean(axis=1)

    unique_hero_data = hero_marks_mean.groupby('Герой').agg({
        'Оценка за качество': 'mean',
        'Оценка по срокам': 'mean',
        'Оценка за вежливость': 'mean',
        'Затрачено дней': 'mean'
    }).reset_index()

    candidate_data = pd.merge(relevant_heroes, unique_hero_data, on='Герой')
    candidate_data['Normalized Time'] = 1 / (candidate_data['Затрачено дней'] + 1e-5)
    candidate_data['Final Score'] = (
        candidate_data['Skill Score'] * 5 +
        candidate_data['Оценка за качество'] * 2 +
        candidate_data['Оценка по срокам'] * 3 +
        candidate_data['Оценка за вежливость'] * 1 +
        candidate_data['Normalized Time'] * 3
    )

    sorted_candidates = candidate_data.sort_values(by='Final Score', ascending=False)
    recommended_candidates = sorted_candidates[['Герой', 'Final Score']].copy()

    combinations = []
    added_combinations = set()
    used_heroes = set()
    
    for _, hero in sorted_candidates.iterrows():
        covers_all_actions = all(hero[action] >= avg_action_scores[action] for action in target_actions)
        
        if covers_all_actions and hero['Герой'] not in used_heroes:
            combinations.append({
                'Герой': hero['Герой'],
                'Final Score': hero['Final Score']
            })
            used_heroes.add(hero['Герой'])
        else:
            for _, additional_hero in sorted_candidates.iterrows():
                if additional_hero['Герой'] != hero['Герой'] and additional_hero['Герой'] not in used_heroes:
                    hero_pair = tuple(sorted([hero['Герой'], additional_hero['Герой']]))
                    if hero_pair not in added_combinations:
                        covers_missing_actions = all(
                            (hero[action] >= avg_action_scores[action] or additional_hero[action] > 0)
                            for action in target_actions
                        )
                        if covers_missing_actions:
                            combined_score = (hero['Final Score'] + additional_hero['Final Score']) / 2
                            combinations.append({
                                'Герой': f"{hero['Герой']} & {additional_hero['Герой']}",
                                'Final Score': combined_score
                            })
                            added_combinations.add(hero_pair)
                            used_heroes.update([hero['Герой'], additional_hero['Герой']])
                            break

    combined_df = pd.DataFrame(combinations)
    full_recommendations = pd.concat([recommended_candidates, combined_df], ignore_index=True)
    full_recommendations = full_recommendations.sort_values(by='Final Score', ascending=False).reset_index(drop=True)
    full_recommendations = full_recommendations.drop_duplicates(subset=['Герой'], keep='first')
    
    return full_recommendations
