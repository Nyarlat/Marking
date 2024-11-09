from shapely.geometry import box
from shapely.ops import unary_union
from Levenshtein import ratio
import pandas as pd
import numpy as np

# Функция для преобразования строки label в список bbox
def parse_label(label):
    try:
        boxes = []
        for item in label.split('\n'):
            if item:
                _, x_center, y_center, width, height = map(float, item.split())
                boxes.append([
                    x_center - width / 2, y_center - height / 2,
                    x_center + width / 2, y_center + height / 2
                ])
        return boxes
    except:
        raise Exception("Неправильный формат строки 'label'. Ожидается формат: '0 x_center y_center width height\\n...'")

# Функция для вычисления совокупного IoU для нескольких bbox
def calculate_total_iou(predicted_boxes, true_boxes):
    predicted_polygons = [box(*pred_box) for pred_box in predicted_boxes]
    true_polygons = [box(*true_box) for true_box in true_boxes]
    predicted_union = unary_union(predicted_polygons)
    true_union = unary_union(true_polygons)
    intersection_area = predicted_union.intersection(true_union).area
    union_area = predicted_union.union(true_union).area
    total_iou = intersection_area / union_area if union_area != 0 else 0
    return total_iou

# Основная функция для расчета метрик
def calc_metrics(ground_truth, submission):
    ious = []
    character_accuracies = []
    complete_matches = []

    ground_truth['text_is_notna'] = ground_truth['label_text'].notna()

    for _, row in ground_truth.iterrows():
        image_file = row['image_file']
        sub_row = submission[submission['image_file'] == image_file]

        if not sub_row.empty:
            gt_boxes = parse_label(row['label'])
            pred_boxes = parse_label(sub_row.iloc[0]['label'])
            iou = calculate_total_iou(pred_boxes, gt_boxes)
            ious.append(iou)

            if row['text_is_notna']:
                char_acc = ratio(row['label_text'], sub_row.iloc[0]['label_text'])
                character_accuracies.append(char_acc)
                complete_matches.append(row['label_text'] == sub_row.iloc[0]['label_text'])

    # Заполняем отсутствующие значения
    ious.extend([0] * (len(ground_truth) - len(ious)))
    character_accuracies.extend([0] * (ground_truth['text_is_notna'].sum() - len(character_accuracies)))
    complete_matches.extend([0] * (ground_truth['text_is_notna'].sum() - len(complete_matches)))

    mean_iou = np.mean(ious)
    mean_character_accuracy = np.mean(character_accuracies)
    accuracy = np.mean(complete_matches)

    return {
        "Средний IoU рамок": mean_iou,
        "Средняя посимвольная точность текста": mean_character_accuracy,
        "Точность абсолютно верного распознавания текста": accuracy
    }

# Расчет финального балла
def calc_score(metrics):
    score = (metrics["Средний IoU рамок"] * 0.05 +
             metrics["Средняя посимвольная точность текста"] * 0.65 +
             metrics["Точность абсолютно верного распознавания текста"] * 0.3)
    return score

if __name__ == '__main__':
    gt_path = 'grounded true train.csv'
    gt = pd.read_csv(gt_path, sep=',', encoding='utf-8')

    sub_path = 'submission.csv'
    sub = pd.read_csv(sub_path, sep=',', encoding='utf-8')

    metrics = calc_metrics(gt, sub)
    print(metrics)
    score = calc_score(metrics)
    print(score)