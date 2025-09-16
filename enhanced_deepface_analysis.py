import cv2
import numpy as np
from deepface import DeepFace
from deepface.modules import detection
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

class EnhancedDeepFaceAnalyzer:
    def __init__(self, detector_backend="opencv"):
        self.detector_backend = detector_backend
        print(f"Initialized analyzer with {detector_backend} detector")
        
    def analyze_image(self, img_path, output_dir="results"):
        """
        Enhanced analysis of age, gender, and emotion with visualization
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Read image
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Could not load image from {img_path}")
            
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_copy = img_rgb.copy()
        
        results = []
        
        try:
            # Detect faces using new detection API
            detected_faces = detection.detect_faces(
                detector_backend=self.detector_backend,
                img=img,
                align=True  
            )
            
            if not detected_faces:
                print("No faces detected in the image")
                return results
                
            print(f"Detected {len(detected_faces)} face(s)")
            
            for i, face_info in enumerate(detected_faces):
    # Extract face bounding box
                fa = face_info.facial_area
                x, y, w, h = fa.x, fa.y, fa.w, fa.h
                confidence = getattr(face_info, "confidence", 1.0)

                # Get cropped face
                face_img = face_info.img
                if face_img.size == 0:
                    continue

                # Save temp face image for DeepFace analysis
                temp_face_path = f"temp_face_{i}.jpg"
                cv2.imwrite(temp_face_path, face_img)

                # Analyze age, gender, emotion
                analysis = DeepFace.analyze(
                    img_path=temp_face_path,
                    actions=["age", "gender", "emotion"],
                    detector_backend=self.detector_backend,
                    enforce_detection=False,
                    silent=True
                )

                if isinstance(analysis, list):
                    analysis = analysis[0]

                # Store results
                result = {
                    "face_id": int(i),
                    "bbox": [int(x), int(y), int(w), int(h)],
                    "confidence": float(confidence),  # ensure float, not float32
                    "age": int(analysis.get("age", 0)),
                    "gender": analysis.get("dominant_gender", "unknown"),
                    "emotion": analysis.get("dominant_emotion", "unknown"),
                    "emotion_scores": {k: float(v) for k, v in analysis.get("emotion", {}).items()},
                    "gender_score": float(analysis.get("gender", {}).get(analysis.get("dominant_gender", ""), 0))
                }
                results.append(result)

                # Draw bounding box and labels
                self._draw_analysis(img_copy, result)

                # Remove temp file
                if os.path.exists(temp_face_path):
                    os.remove(temp_face_path)

            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(os.path.basename(img_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}_analysis_{timestamp}")
            
            # Save image with annotations
            plt.figure(figsize=(12, 8))
            plt.imshow(img_copy)
            plt.axis('off')
            plt.savefig(f"{output_path}.jpg", bbox_inches='tight', pad_inches=0.1, dpi=300)
            plt.close()
            
            # Save JSON results
            with open(f"{output_path}.json", 'w') as f:
                json.dump({
                    'image_path': img_path,
                    'analysis_date': timestamp,
                    'detector_backend': self.detector_backend,
                    'faces_detected': len(results),
                    'results': results
                }, f, indent=2)
            
            print(f"Analysis complete. Results saved to {output_path}.[jpg/json]")
            return results
            
        except Exception as e:
            print(f"Error analyzing image: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def _draw_analysis(self, img, result):
        """Draw bounding box and analysis results on image"""
        x, y, w, h = result['bbox']
        
        # Draw bounding box
        color = (0, 255, 0)  # Green
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        
        # Prepare text
        text = f"ID:{result['face_id']} Age:{result['age']} {result['gender']} {result['emotion']}"
        conf_text = f"Conf: {result['confidence']:.2f}"
        
        # Put text
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        
        # Text background for better visibility
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        cv2.rectangle(img, (x, y - text_size[1] - 5), (x + text_size[0], y), color, -1)
        
        # Put text on image
        cv2.putText(img, text, (x, y - 5), font, font_scale, (0, 0, 0), thickness)
        cv2.putText(img, conf_text, (x, y + h + 15), font, font_scale * 0.8, color, 1)

# Quick test function
def test_demo():
    """Quick demonstration function"""
    analyzer = EnhancedDeepFaceAnalyzer()
    
    test_image = "test_image.jpg"  # Change this to your image path
    
    if os.path.exists(test_image):
        results = analyzer.analyze_image(test_image)
        print("Demo results:", json.dumps(results, indent=2))
    else:
        print(f"Test image {test_image} not found. Please update the path.")

if __name__ == "__main__":
    test_demo()
