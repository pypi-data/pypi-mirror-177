import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime
from typing import List
from .utils import get_content_duration

GT_INTER_TH = [0.5, 0.75, 0.9]


def __evaluate_file_predictions(
    gt_times: List[List[int]],
    pred_times: List[List[int]],
    file_path: str,
    data_type: str,
) -> float:

    clip_duration = get_content_duration(file_path, data_type)
    matched_gt = 0
    activity_captured = {thr: 0 for thr in GT_INTER_TH}
    for pred_interval in pred_times:
        matched_time = 0
        pred_min = min(pred_interval)
        pred_max = max(pred_interval)
        for gt_interval in gt_times:
            if max(gt_interval) <= pred_min or min(gt_interval) >= pred_max:
                continue
            else:
                sorted_times = gt_interval + pred_interval
                sorted_times.sort()
                intersection = sorted_times[2] - sorted_times[1]
                matched_time += intersection
                for thr in GT_INTER_TH:
                    if intersection / (max(gt_interval) - min(gt_interval)) >= thr:
                        activity_captured[thr] += 1
        matched_gt += matched_time
    total_gt = sum([gt_interval[1] - gt_interval[0] for gt_interval in gt_times])
    total_pred = sum(
        [pred_interval[1] - pred_interval[0] for pred_interval in pred_times]
    )
    unmatched_gt = total_gt - matched_gt
    unmatched_pred = total_pred - matched_gt
    undetected_bg = clip_duration * 1000 - total_gt - unmatched_pred
    output_dict = {
        "file_path": file_path,
        "clip_duration": int(clip_duration * 1000),
        "gt_time": total_gt,
        "matched_gt_time": matched_gt,
        "unmatched_gt_time": unmatched_gt,
        "noise_detected_time": unmatched_pred,
        "noise_undetected_time": undetected_bg,
    }
    total_gt_count = len(gt_times)
    for threshold, detection_count in activity_captured.items():
        output_dict[f"gt_detection_ratio_{threshold}"] = (
            detection_count / total_gt_count
        )
    return output_dict


def __compute_dataset_stats(annotations: dict, predictions, files_dir):
    files = list(annotations.keys())
    stats = []
    for file in files:
        filepath = os.path.join(files_dir, file)
        file_anns = [
            [annotation["s_time"], annotation["e_time"]]
            for annotation in annotations[file]
        ]
        file_pred = predictions[file]
        file_stats = __evaluate_file_predictions(file_anns, file_pred, filepath)
        stats.append(file_stats)

    return pd.DataFrame(stats)


def evaluate(annotations, predictions, data_dir, results_path: str = None, verbose=3):
    eval_stats = __compute_dataset_stats(annotations, predictions, data_dir)
    eval_stats = eval_stats.fillna(0)
    stats_sum = eval_stats[
        [
            "noise_undetected_time",
            "matched_gt_time",
            "unmatched_gt_time",
            "noise_detected_time",
        ]
    ].sum()
    total_gt_time = stats_sum["matched_gt_time"] + stats_sum["unmatched_gt_time"]
    total_noise_time = (
        stats_sum["noise_detected_time"] + stats_sum["noise_undetected_time"]
    )
    matched_gt_percent = stats_sum["matched_gt_time"] / total_gt_time
    noise_detection_percent = stats_sum["noise_detected_time"] / total_noise_time
    hmean_gt_noise = 2 / (1 / matched_gt_percent + 1 / (1 - noise_detection_percent))

    if verbose > 1:
        print("### EVALUATION RESULTS ###\n")
        print(f"Matched gt percent: {matched_gt_percent*100}")
        print(f"False positive percent: {noise_detection_percent*100}\n")

    if verbose > 2:
        gt_time_str = str(datetime.timedelta(seconds=int(total_gt_time / 1000)))
        noise_time_str = str(datetime.timedelta(seconds=int(total_noise_time / 1000)))
        fig1, axs = plt.subplots(1, 2, figsize=(12, 8))
        axs[0].pie(
            [matched_gt_percent, 1 - matched_gt_percent],
            labels=["Detected gt", "Undetected gt"],
            autopct="%1.1f%%",
            shadow=True,
            startangle=90,
        )
        axs[0].set_title(f"Ground truth detections - all audio [{gt_time_str}]")
        axs[1].pie(
            [noise_detection_percent, 1 - noise_detection_percent],
            labels=["Detected noise", "Undetected noise"],
            autopct="%1.1f%%",
            shadow=True,
            startangle=90,
        )
        axs[1].set_title(
            f"Noise detection (non gt label) - all audio [{noise_time_str}]"
        )
        plt.show()

    if results_path != None and os.path.isdir("/".join(results_path.split("/")[:-1])):
        pd.to_csv(eval_stats, index=False)

    return {
        "matched_gt_ratio": matched_gt_percent,
        "undetected_noise_ratio": 1 - noise_detection_percent,
        "hmean_gt_noise": hmean_gt_noise,
    }
