20241120
"""

The system effectively handles:

News anchors in fixed positions
Digital clocks and time displays
Live/Breaking news graphics
Scrolling tickers
Network watermarks
Sports scores
Weather graphics
This approach gives you clean logo extraction even with multiple static elements in the broadcast.
"""
def process_channel_stream(frame_paths):
    detector = SmartLogoDetector()
    
    # Read frames
    frames = []
    for path in frame_paths[:20]:  # Use 20 frames for analysis
        frame = cv2.imread(str(path))
        frames.append(frame)
    
    # Detect logo
    logo = detector.detect_logo(frames)
    
    return logo

# Additional validation
def validate_logo(logo_image):
    if logo_image is None:
        return False
        
    # Check color variance (logos typically have limited colors)
    colors = np.reshape(logo_image, (-1, 3))
    unique_colors = np.unique(colors, axis=0)
    
    return len(unique_colors) < 50  # Typical logos have limited color palette
