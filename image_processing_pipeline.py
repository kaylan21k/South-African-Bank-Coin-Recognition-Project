import cv2
import numpy as np
from skimage.feature import local_binary_pattern, hog

def preprocess_denoise_normalize(image):
    """Denoising with normalization"""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    resized = cv2.resize(gray, (300, 300), interpolation=cv2.INTER_AREA)
    denoised = cv2.fastNlMeansDenoising(resized, None, h=10, searchWindowSize=21, templateWindowSize=7)
    normalized = cv2.normalize(denoised, None, 0, 255, cv2.NORM_MINMAX)
    return normalized

def segment_hough_circle(image):
    """Hough Circle Transform that also returns the circle data for visualization."""
    if image is None: return None, None, None
    blurred = cv2.GaussianBlur(image, (9, 9), 2)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100,
                               param1=50, param2=30, minRadius=50, maxRadius=150)
    mask = np.zeros_like(image)
    if circles is not None:
        circles_uint = np.uint16(np.around(circles))
        x, y, r = circles_uint[0, 0]
        cv2.circle(mask, (x, y), r, 255, -1)
    
    segmented = cv2.bitwise_and(image, image, mask=mask)
    return segmented, mask, circles

def extract_shape_features(image_context, mask):
    """Extract shape features from segmented coin."""
    features = {}
    if mask is None or np.sum(mask) == 0:
        return {name: 0.0 for name in ['area', 'perimeter', 'circularity', 'aspect_ratio', 'extent', 'solidity']}

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        features['area'] = float(area)
        perimeter = cv2.arcLength(largest_contour, True)
        features['perimeter'] = float(perimeter)
        features['circularity'] = (4 * np.pi * area / (perimeter * perimeter)) if perimeter > 0 else 0.0
        x, y, w, h = cv2.boundingRect(largest_contour)
        features['aspect_ratio'] = float(w) / h if h > 0 else 0.0
        features['extent'] = float(area) / (w * h) if (w * h) > 0 else 0.0
        hull = cv2.convexHull(largest_contour)
        hull_area = cv2.contourArea(hull)
        features['solidity'] = float(area) / hull_area if hull_area > 0 else 0.0
    else:
        features = {name: 0.0 for name in ['area', 'perimeter', 'circularity', 'aspect_ratio', 'extent', 'solidity']}
    return features

def extract_hu_moments(gray_image, mask):
    """Extract Hu moments from segmented coin"""
    features = {}
    if gray_image is None or mask is None or np.sum(mask) == 0:
        return {f'hu_moment_{i+1}': 0.0 for i in range(7)}
    moments = cv2.moments(mask)
    hu_moments_array = cv2.HuMoments(moments)
    for i in range(7):
        val = hu_moments_array[i][0]
        features[f'hu_moment_{i+1}'] = float(-1 * np.sign(val) * np.log10(abs(val))) if val != 0 else 0.0
    return features

def extract_lbp_features(gray_image, mask):
    """Extract Local Binary Pattern features from segmented coin"""
    features = {}
    num_expected_lbp_bins = 10
    if gray_image is None or mask is None or np.sum(mask) == 0:
        return {f'lbp_bin_{i+1}': 0.0 for i in range(num_expected_lbp_bins)}
    masked_image = cv2.bitwise_and(gray_image, gray_image, mask=mask)
    radius = 3; n_points = 8 * radius
    lbp = local_binary_pattern(masked_image, n_points, radius, method='uniform')
    lbp_values_in_mask = lbp[mask > 0]
    if len(lbp_values_in_mask) > 0:
        n_bins = int(lbp_values_in_mask.max() + 1)
        hist, _ = np.histogram(lbp_values_in_mask, bins=n_bins, range=(0, n_bins), density=True)
        for i in range(min(num_expected_lbp_bins, len(hist))): features[f'lbp_bin_{i+1}'] = float(hist[i])
        for i in range(len(hist), num_expected_lbp_bins): features[f'lbp_bin_{i+1}'] = 0.0
    else:
        for i in range(num_expected_lbp_bins): features[f'lbp_bin_{i+1}'] = 0.0
    return features

def extract_hog_features(gray_image, mask):
    """Extract Histogram of Oriented Gradients features from segmented coin."""
    features_dict = {}
    num_expected_hog_features = 20
    if gray_image is None or mask is None or np.sum(mask) == 0:
        return {f'hog_{i+1}': 0.0 for i in range(num_expected_hog_features)}
    masked_image = cv2.bitwise_and(gray_image, gray_image, mask=mask)
    resized = cv2.resize(masked_image, (64, 64))
    hog_feature_vector, _ = hog(resized, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm='L2-Hys', visualize=True)
    if hog_feature_vector is not None and len(hog_feature_vector) > 0:
        step = max(1, len(hog_feature_vector) // num_expected_hog_features)
        selected_hog_features = hog_feature_vector[::step][:num_expected_hog_features]
        for i, value in enumerate(selected_hog_features): features_dict[f'hog_{i+1}'] = float(value)
        for i in range(len(selected_hog_features), num_expected_hog_features): features_dict[f'hog_{i+1}'] = 0.0
    else:
        for i in range(num_expected_hog_features): features_dict[f'hog_{i+1}'] = 0.0
    return features_dict

def extract_color_features(bgr_image_input, mask):
    """Extract color features from segmented coin using a BGR image."""
    features = {}
    default_features = {f'hist_b_{i+1}': 0.0 for i in range(5)}
    default_features.update({f'hist_g_{i+1}': 0.0 for i in range(5)})
    default_features.update({f'hist_r_{i+1}': 0.0 for i in range(5)})
    default_features.update({f'mean_{c}': 0.0 for c in 'bgr'})
    default_features.update({f'std_{c}': 0.0 for c in 'bgr'})
    default_features.update({f'skewness_{c}': 0.0 for c in 'bgr'})
    if bgr_image_input is None or mask is None or np.sum(mask) == 0: return default_features
    masked_color_image = cv2.bitwise_and(bgr_image_input, bgr_image_input, mask=mask)
    b, g, r = cv2.split(masked_color_image)
    for channel_pixels, name in [(b, 'b'), (g, 'g'), (r, 'r')]:
        channel_values_in_mask = channel_pixels[mask > 0]
        if len(channel_values_in_mask) > 0:
            hist, _ = np.histogram(channel_values_in_mask, bins=5, range=(0, 256), density=True)
            for i, value in enumerate(hist): features[f'hist_{name}_{i+1}'] = float(value)
            mean_val = np.mean(channel_values_in_mask)
            std_val = np.std(channel_values_in_mask)
            features[f'mean_{name}'] = float(mean_val)
            features[f'std_{name}'] = float(std_val)
            features[f'skewness_{name}'] = float(np.mean(((channel_values_in_mask - mean_val) / std_val) ** 3)) if std_val > 0 else 0.0
    return features

def extract_all_features(segmented_gray_image, mask, feature_names_list_from_json, original_bgr_frame):
    """Combines all feature types."""
    all_features = {name: 0.0 for name in feature_names_list_from_json}
    if segmented_gray_image is None or mask is None or np.sum(mask) == 0:
        return all_features
    
    #Temporary dictionary to hold extracted features
    temp_features = {}
    temp_features.update(extract_shape_features(segmented_gray_image, mask))
    temp_features.update(extract_hu_moments(segmented_gray_image, mask))
    temp_features.update(extract_lbp_features(segmented_gray_image, mask))
    temp_features.update(extract_hog_features(segmented_gray_image, mask))
    temp_features.update(extract_color_features(original_bgr_frame, mask))

    #Populate the final dictionary in the correct order
    for key in all_features:
        if key in temp_features:
            all_features[key] = temp_features[key]
            
    return all_features

def run_recognition_pipeline(frame_bgr, scaler, type_clf, side_clf, feature_names_from_json):
    """
    Takes a raw BGR frame, runs the full pipeline, and returns prediction results
    and a visualized frame for display.
    """
    if frame_bgr is None:
        return {'error': "Input frame is None."}, None

    frame_bgr = cv2.resize(frame_bgr, (300, 300), interpolation=cv2.INTER_AREA)

    visualized_frame = frame_bgr.copy()
    error_result = {'error': "Pipeline error", 'coin_type': "N/A", 'coin_side': "N/A", 'type_confidence': 0.0, 'side_confidence': 0.0}

    preprocessed_gray = preprocess_denoise_normalize(frame_bgr)
    if preprocessed_gray is None:
        error_result['error'] = "Preprocessing failed."
        return error_result, visualized_frame

    #Segmentation
    segmented_gray, mask, detected_circles = segment_hough_circle(preprocessed_gray)
    if segmented_gray is None or mask is None:
        error_result['error'] = "Segmentation failed."
        return error_result, visualized_frame

    #Visualizations
    if detected_circles is not None:
        circles_uint = np.uint16(np.around(detected_circles))
        for i in circles_uint[0, :]:
            cv2.circle(visualized_frame, (i[0], i[1]), i[2], (0, 255, 0), 3) # Outer circle
            cv2.circle(visualized_frame, (i[0], i[1]), 2, (0, 0, 255), 3)     # Center dot

    if np.sum(mask) == 0:
        return {'error': "No coin detected"}, visualized_frame

    #Feature Extraction
    current_features_dict = extract_all_features(segmented_gray, mask, feature_names_from_json, original_bgr_frame=frame_bgr)

    #Create Feature Vector
    feature_vector = np.array([current_features_dict.get(name, 0.0) for name in feature_names_from_json]).reshape(1, -1)

    if feature_vector.shape[1] != scaler.n_features_in_:
        error_result['error'] = f"Feature shape mismatch. Expected {scaler.n_features_in_}."
        return error_result, visualized_frame

    #Scale and Predict
    try:
        scaled_features = scaler.transform(feature_vector)
        pred_type = type_clf.predict(scaled_features)[0]
        type_proba = np.max(type_clf.predict_proba(scaled_features)) * 100
        pred_side = side_clf.predict(scaled_features)[0]
        side_proba = np.max(side_clf.predict_proba(scaled_features)) * 100
    except Exception as e:
        error_result['error'] = f"Prediction failed: {e}"
        return error_result, visualized_frame

    #Final results
    final_results = {'coin_type': str(pred_type), 'coin_side': str(pred_side), 'type_confidence': float(type_proba), 'side_confidence': float(side_proba), 'error': None}
    return final_results, visualized_frame
