"""
Main script to run demographic analysis using EnhancedDeepFaceAnalyzer
"""

from enhanced_deepface_analysis import EnhancedDeepFaceAnalyzer
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Enhanced DeepFace Demographic Analysis')
    parser.add_argument('--image', type=str, required=True, help='Path to input image')
    parser.add_argument('--output', type=str, default='results', help='Output directory')
    parser.add_argument('--detector', type=str, default='opencv', 
                       choices=['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface'],
                       help='Face detector backend')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image):
        print(f"Error: Image file '{args.image}' not found.")
        return
    
    print(f"Starting analysis of {args.image}...")
    print(f"Using detector: {args.detector}")
    print(f"Output directory: {args.output}")
    
    # Initialize analyzer
    analyzer = EnhancedDeepFaceAnalyzer(detector_backend=args.detector)
    
    # Run analysis
    results = analyzer.analyze_image(args.image, args.output)
    
    # Print summary
    print(f"\nAnalysis Summary:")
    print(f"Faces detected: {len(results)}")
    for result in results:
        print(f"  Face {result['face_id']}: {result['age']}yo {result['gender']} ({result['emotion']})")

if __name__ == "__main__":
    main()