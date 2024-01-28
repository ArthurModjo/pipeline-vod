import cv2
import numpy as np
import tensorflow as tf
from keras_cv.models.yolo import YOLOV8Backbone, yolo_post_process, draw_boxes
from keras_cv.losses import binary_crossentropy, yolo_loss

# Charger la vidéo
video_path = "../demo.mp4"
video = cv2.VideoCapture(video_path)

# Créer le modèle YOLOv8
model = YOLOV8Backbone.from_preset("yolo_v8_xl_backbone_coco")

# Créer un fichier texte pour écrire les résultats
output_file_path = "results.txt"
output_file = open(output_file_path, "w")

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Prétraitement de l'image pour YOLOv8
    input_data = cv2.resize(frame, (640, 640))  # Ajustez la taille selon votre modèle
    input_data = np.expand_dims(input_data, axis=0)

    # Prédiction avec le modèle YOLOv8
    predictions = model(input_data)

    # Post-traitement des prédictions
    boxes, confidences, class_ids = yolo_post_process(predictions, score_threshold=0.5)

    # Dessiner les boîtes sur l'image
    frame_with_boxes = draw_boxes(frame, boxes, confidences, class_ids)

    # Enregistrement de l'image avec les boîtes dessinées
    cv2.imwrite("output_frame.jpg", frame_with_boxes)

    # Écrire les résultats dans le fichier texte
    for box, confidence, class_id in zip(boxes, confidences, class_ids):
        x, y, w, h = box
        line = f"{video_path} {x} {y} {x+w} {y+h} {confidence} {class_id}\n"
        output_file.write(line)

    # Affichage de la vidéo avec les boîtes
    cv2.imshow("Video", frame_with_boxes)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fermeture du fichier de sortie
output_file.close()

# Fermeture de la vidéo
video.release()
cv2.destroyAllWindows()
