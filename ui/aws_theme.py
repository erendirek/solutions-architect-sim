"""
AWS theme module with color palettes and styling constants.
"""

class AWSColors:
    """AWS color palette constants."""
    
    # Primary colors
    SQUID_INK = (25, 35, 50)      # Daha koyu bir mavi/siyah
    ANCHOR = (58, 58, 58)         # Daha koyu gri
    SMILE_ORANGE = (255, 153, 0)  # #FF9900 - AWS Orange
    
    # Secondary colors
    RIND = (255, 215, 0)          # #FFD700 - Gold
    LIME = (53, 172, 75)          # #35AC4B - Green
    POWDER_BLUE = (51, 153, 204)  # #3399CC - Blue
    RUST = (204, 102, 0)          # #CC6600 - Dark orange
    MERLOT = (153, 0, 51)         # #990033 - Red
    
    # Neutral colors
    WHITE = (255, 255, 255)       # #FFFFFF
    LIGHT_GRAY = (240, 240, 240)  # #F0F0F0
    MEDIUM_GRAY = (204, 204, 204) # #CCCCCC
    DARK_GRAY = (102, 102, 102)   # #666666
    
    # UI State colors
    SUCCESS = (53, 172, 75)       # #35AC4B - Green
    WARNING = (255, 153, 0)       # #FF9900 - Orange
    ERROR = (204, 51, 51)         # #CC3333 - Red
    INFO = (51, 153, 204)         # #3399CC - Blue
    
    # Background colors
    BACKGROUND_LIGHT = (240, 240, 240)  # Biraz daha koyu
    BACKGROUND_DARK = (25, 35, 50)      # Daha koyu mavi/siyah
    PANEL_LIGHT = (230, 230, 230)       # Biraz daha koyu
    PANEL_DARK = (40, 50, 60)           # Daha koyu panel
    
    # Button states
    BUTTON_PRIMARY = (255, 153, 0)      # #FF9900 - AWS Orange
    BUTTON_PRIMARY_HOVER = (230, 138, 0) # #E68A00 - Darker orange
    BUTTON_SECONDARY = (51, 153, 204)   # #3399CC - Blue
    BUTTON_SECONDARY_HOVER = (46, 138, 184) # #2E8AB8 - Darker blue
    BUTTON_DISABLED = (180, 180, 180)   # Daha koyu gri


class AWSStyling:
    """AWS styling constants."""
    
    # Font families
    FONT_FAMILY = "Arial"
    
    # Font sizes
    FONT_SIZE_SMALL = 12
    FONT_SIZE_NORMAL = 14
    FONT_SIZE_MEDIUM = 16
    FONT_SIZE_LARGE = 18
    FONT_SIZE_XLARGE = 24
    FONT_SIZE_XXLARGE = 32
    
    # Padding and margins
    PADDING_SMALL = 5
    PADDING_MEDIUM = 10
    PADDING_LARGE = 15
    PADDING_XLARGE = 20
    
    # Border radius
    BORDER_RADIUS_SMALL = 2
    BORDER_RADIUS_MEDIUM = 4
    BORDER_RADIUS_LARGE = 8
    
    # Button sizes
    BUTTON_HEIGHT_SMALL = 30
    BUTTON_HEIGHT_MEDIUM = 40
    BUTTON_HEIGHT_LARGE = 50
    
    # Icon sizes
    ICON_SIZE_SMALL = 16
    ICON_SIZE_MEDIUM = 24
    ICON_SIZE_LARGE = 32
    ICON_SIZE_XLARGE = 48
    ICON_SIZE_XXLARGE = 64