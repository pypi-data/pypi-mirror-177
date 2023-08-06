import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime
from typing import List, Dict, Any
from .utils import get_content_duration

# ground truth intersection thresholds for evaluating at different detection strictness degrees
GT_INTER_TH = [0.5, 0.75, 0.9]


def __evaluate_file_predictions(
    gt_times: List[List[int]],
    pred_times: List[List[int]],
    file_path: str,
    data_type: str,
) -> Dict[str, Any]:
    """Evaluates file predictions using provided annotations

    Args:
        gt_times (List[List[int]]): list of ground truth activity time intervals
        pred_times (List[List[int]]): list of predicted activity time intervals
        file_path (str): path to file sample used for evaluation
        data_type (str): what type of data is being evaluated

    Returns:
        Dict[str, Any]: a dictionary with evaluation metrics
    """
    # fetch sample duration, in seconds
    clip_duration = get_content_duration(file_path, data_type)
    # for every ground truth intersection interval, count predicted activities
    activity_captured = {thr: 0 for thr in GT_INTER_TH}
    matched_gt = 0
    for pred_interval in pred_times:
        matched_time = 0
        pred_min = min(pred_interval)
        pred_max = max(pred_interval)
        for gt_interval in gt_times:
            # time intervals don't overlap
            if max(gt_interval) <= pred_min or min(gt_interval) >= pred_max:
                continue
            else:
                # intersection corresponds to range between second and third highest times
                sorted_times = gt_interval + pred_interval
                sorted_times.sort()
                intersection = sorted_times[2] - sorted_times[1]
                matched_time += intersection
                # evaluate intersection against each threshold (Intersection over Ground Truth)
                for thr in GT_INTER_TH:
                    if intersection / (max(gt_interval) - min(gt_interval)) >= thr:
                        activity_captured[thr] += 1
        matched_gt += matched_time
    # the total time corresponding to the activity in this sample
    total_gt = sum([gt_interval[1] - gt_interval[0] for gt_interval in gt_times])
    # the total time predicted as an activity in this sample
    total_pred = sum(
        [pred_interval[1] - pred_interval[0] for pred_interval in pred_times]
    )
    tp = matched_gt
    fn = total_gt - matched_gt
    fp = total_pred - matched_gt
    tn = clip_duration * 1000 - total_gt - fp
    # here we evaluate precision, accuracy and recall based on total matched time intervals
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    accuracy = (tp + tn) / (tp + fn + fp + tn)
    output_dict = {
        "file_path": file_path,
        "clip_duration": int(clip_duration * 1000),
        "gt_time": total_gt,
        "matched_gt_time": tp,
        "unmatched_gt_time": fn,
        "noise_detected_time": fp,
        "noise_undetected_time": tn,
        "time_AP": precision,
        "time_AR": recall,
        "time_Acc": accuracy,
    }
    # here we are evaluating, for each detection strictness, the average recall
    total_gt_count = len(gt_times)
    for threshold, detection_count in activity_captured.items():
        output_dict[f"count_AR{threshold}"] = detection_count / total_gt_count
    return output_dict


# TODO: implement multi-class evaluation
def __compute_dataset_stats(
    annotations: Dict[str, List[Dict]],
    predictions: Dict[str, List[List[int]]],
    files_dir: str,
    data_type: str,
) -> pd.DataFrame:
    """Generate evaluation metrics for a certain dataset, given its annotations and predictions

    Args:
        annotations (Dict[str, List[Dict]]): dictionary with annotations for each file
        predictions (Dict[str, List[List[int]]]): dictionary with predictions for each file
        files_dir (str): path to directory containing file samples
        data_type (str): type of data being evaluated

    Returns:
        pd.DataFrame: dataframe with evaluation metrics, where each row contains metrics for a single file
    """
    files = list(annotations.keys())
    stats = []
    for file in files:
        filepath = os.path.join(files_dir, file)
        file_anns = [
            [annotation["s_time"], annotation["e_time"]]
            for annotation in annotations[file]
        ]
        file_pred = predictions[file]
        file_stats = __evaluate_file_predictions(
            file_anns, file_pred, filepath, data_type
        )
        stats.append(file_stats)
    return pd.DataFrame(stats)


def evaluate(
    annotations: Dict[str, List[Dict]],
    predictions: Dict[str, List[List[int]]],
    data_dir: str,
    data_type: str,
    results_path: str = None,
    verbose=1,
) -> Dict[str, float]:
    """Computes evaluation metrics for a certain activity detection dataset, given annotations and predictions.
    Metrics are aggregated and returned. If desired, user can also print metrics to console or
    save them to disk

    Args:
        annotations (Dict[str, List[Dict]]): dictionary with annotations in the format defined by the library
        predictions (Dict[str, List[List[int]]]): dictionary with predictions in the format defined by the library
        data_dir (str): path to directory with file samples over which detections were made
        data_type (str): type of data used
        results_path (str, optional): path in disk to save results to. Defaults to None.
        verbose (int, optional): verbosity level. Higher is more. Defaults to 1.

    Returns:
        Dict[str, float]: a dictionary with aggregated evaluation metrics
    """
    assert (
        data_type == "audio" or data_type == "video"
    ), f"Unrecognized data type provided {data_type}"
    # compute evaluation statistics for each file
    eval_stats = __compute_dataset_stats(annotations, predictions, data_dir, data_type)
    eval_stats = eval_stats.fillna(0)

    # these stats reflect activity matching performance over dataset as a whole, summing
    # all ground truth and predicted data
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

    # these stats are more sensible to individual file and activity performances. If a certain
    # activity was not well predicted, it will have a greater impact in the overall metric computed here
    time_m_AP = eval_stats["time_AP"].mean()
    time_m_AR = eval_stats["time_AR"].mean()
    time_m_Acc = eval_stats["time_Acc"].mean()

    results = {
        "matched_gt_ratio": matched_gt_percent,
        "undetected_noise_ratio": 1 - noise_detection_percent,
        "hmean_gt_noise": hmean_gt_noise,
        "time_mAP": time_m_AP,
        "time_mAR": time_m_AR,
        "time_mAcc": time_m_Acc,
    }
    for threshold in GT_INTER_TH:
        results[f"count_mAR{threshold}"] = eval_stats[f"count_AR{threshold}"].mean()

    # print evaluation metrics to console
    if verbose > 1:
        print("### EVALUATION RESULTS ###\n")
        for metric_name, metric_value in results.items():
            print(f"{metric_name}: {metric_value}")

    # plot evaluation metrics of total predicted time
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

    # save results to disk
    if results_path != None and os.path.isdir("/".join(results_path.split("/")[:-1])):
        pd.to_csv(eval_stats, index=False)

    return results
