import tqdm
import os
import cv2
import torch
import numpy as np
import pandas as pd
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import pose as mp_pose
from helper.bootstrap import BootstrapHelper
from pose.embedder import FullBodyPoseEmbedder
from pose.classifier import PoseClassifier

bootstrap_images_in_folder = '../data'
bootstrap_images_out_folder = './images'
bootstrap_csvs_out_folder = './csvs'


def bootstrap():
    # Find Outliers
    pose_embedder = FullBodyPoseEmbedder()
    pose_classifier = PoseClassifier(
        pose_samples_folder=bootstrap_csvs_out_folder,
        pose_embedder=pose_embedder,
        top_n_by_max_distance=30,
        top_n_by_mean_distance=10)
    outliers = pose_classifier.find_pose_sample_outliers()
    print('Number of outliers: ', len(outliers))

    # Bootstraping
    bootstrap_helper = BootstrapHelper(
        images_in_folder=bootstrap_images_in_folder,
        images_out_folder=bootstrap_images_out_folder,
        csvs_out_folder=bootstrap_csvs_out_folder,
    )
    bootstrap_helper.bootstrap(per_pose_class_limit=None)
    bootstrap_helper.align_images_and_csvs(print_removed_items=False)
    bootstrap_helper.remove_outliers(outliers)
    bootstrap_helper.print_images_out_statistics()


def get_pose():
    # Initialize model.
    pose_tracker = mp_pose.Pose(upper_body_only=False)
    pose_embedder = FullBodyPoseEmbedder()
    pose_classifier = PoseClassifier(
        pose_samples_folder=bootstrap_csvs_out_folder,
        pose_embedder=pose_embedder,
        top_n_by_max_distance=30,
        top_n_by_mean_distance=10)
    return pose_tracker, pose_embedder, pose_classifier


def get_yolo():
    # Get Yolo model.
    return torch.hub.load('ultralytics/yolov5', 'yolov5n6')
