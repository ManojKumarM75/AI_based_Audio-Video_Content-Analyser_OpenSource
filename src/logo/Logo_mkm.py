# 20241120 
"""
an excellent point about multiple static elements in TV broadcasts! Let's enhance the detection to specifically 
target logo regions while excluding other static elements:
Excludes known static regions:
News anchor area (center)
Clock region (top center)
Lower third graphics
Breaking news banners
Uses position-based scoring:
Favors typical logo locations
Weights corners higher than center
Considers aspect ratio
Implements size constraints:
Minimum size to avoid small artifacts
Maximum size to exclude backgrounds
Proper aspect ratio ranges

Here's how to use it:
"""
import cv2
import numpy as np

class SmartLogoDetector:
    def __init__(self):
        # Define typical logo positions (normalized coordinates)
        self.logo_positions = {
            'top_right': (0.8, 0.1),    # Most common
            'top_left': (0.1, 0.1),     # Second most common
            'bottom_right': (0.8, 0.9),  # Third most common
        }
        
    def filter_static_regions(self, frames, static_mask):
        height, width = static_mask.shape
        filtered_mask = static_mask.copy()
        
        # 1. Remove center region (news anchor area)
        center_y, center_x = height // 2, width // 2
        cv2.circle(filtered_mask, 
                  (center_x, center_y), 
                  int(height * 0.3), 
                  0, 
                  -1)
        
        # 2. Remove clock regions (typically top center)
        clock_width = int(width * 0.15)
        clock_height = int(height * 0.1)
        top_center_x = width // 2
        filtered_mask[0:clock_height, 
                     top_center_x-clock_width//2:top_center_x+clock_width//2] = 0
        
        # 3. Remove lower third (captions, tickers)
        lower_third_height = int(height * 0.2)
        filtered_mask[-lower_third_height:, :] = 0
        
        return filtered_mask

    def detect_logo(self, frames):
        # Stack frames and get standard deviation
        stacked = np.stack([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames])
        std_dev = np.std(stacked, axis=0)
        
        # Create static mask
        static_threshold = np.mean(std_dev) * 0.3
        static_mask = (std_dev < static_threshold).astype(np.uint8)
        
        # Filter out non-logo static regions
        filtered_mask = self.filter_static_regions(frames, static_mask)
        
        # Find connected components
        components = cv2.connectedComponentsWithStats(filtered_mask, 
                                                    connectivity=8)
        num_labels, labels, stats, centroids = components
        
        # Score each component based on position and size
        best_score = 0
        logo_region = None
        
        for i in range(1, num_labels):
            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]
            area = stats[i, cv2.CC_STAT_AREA]
            
            # Skip if size is not in logo range
            if not (1000 < area < 50000):
                continue
                
            # Calculate position score
            pos_score = self._calculate_position_score(x, y, frames[0].shape)
            size_score = self._calculate_size_score(w, h)
            
            total_score = pos_score * size_score
            
            if total_score > best_score:
                best_score = total_score
                logo_region = frames[0][y:y+h, x:x+w]
        
        return logo_region
    
    def _calculate_position_score(self, x, y, frame_shape):
        height, width = frame_shape[:2]
        normalized_x = x / width
        normalized_y = y / height
        
        # Calculate distance to known logo positions
        scores = []
        for pos_x, pos_y in self.logo_positions.values():
            distance = np.sqrt((normalized_x - pos_x)**2 + 
                             (normalized_y - pos_y)**2)
            scores.append(np.exp(-distance))
        
        return max(scores)
    
    def _calculate_size_score(self, width, height):
        aspect_ratio = width / height
        # Logos typically have aspect ratios between 1:1 and 3:1
        if 1.0 <= aspect_ratio <= 3.0:
            return 1.0
        return 0.5
