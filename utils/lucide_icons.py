"""
Utility functions for using Lucide icons in Streamlit
"""

import base64

def lucide_icon_svg(icon_name, size=24, color="currentColor", stroke_width=2):
    """
    Returns SVG markup for the specified Lucide icon
    
    Args:
        icon_name: Name of the Lucide icon
        size: Size of the icon (width and height)
        color: Color of the icon
        stroke_width: Stroke width of the icon
    
    Returns:
        SVG markup for the icon
    """
    icons = {
        "alert-triangle": """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path><path d="M12 9v4"></path><path d="M12 17h.01"></path></svg>""",
        "info": """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg>""",
        "check-circle": """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path><path d="m9 12 2 2 4-4"></path></svg>""",
        "x": """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>""",
        "chevron-right": """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"></path></svg>""",
        "chevron-left": """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"></path></svg>"""
    }
    
    if icon_name not in icons:
        return ""
        
    svg = icons[icon_name].format(size=size, color=color, stroke_width=stroke_width)
    return svg

def get_risk_icon(risk_level, size=16):
    """
    Returns the appropriate risk icon for a given risk level
    
    Args:
        risk_level: Risk level (high, medium, low)
        size: Size of the icon
    
    Returns:
        SVG markup for the icon
    """
    if risk_level == "high":
        return lucide_icon_svg("alert-triangle", size=size, color="#ef4444")
    elif risk_level == "medium":
        return lucide_icon_svg("info", size=size, color="#f59e0b")
    else:  # low
        return lucide_icon_svg("check-circle", size=size, color="#10b981")

def get_safe_icon(risk_level, size=16):
    """
    Returns the appropriate risk icon for a given risk level as a base64 encoded image
    that can be safely used in Streamlit buttons without unsafe_allow_html
    
    Args:
        risk_level: Risk level (high, medium, low)
        size: Size of the icon
    
    Returns:
        Base64 encoded image for the icon
    """
    svg = ""
    if risk_level == "high":
        svg = lucide_icon_svg("alert-triangle", size=size, color="#ef4444")
    elif risk_level == "medium":
        svg = lucide_icon_svg("info", size=size, color="#f59e0b") 
    else:  # low
        svg = lucide_icon_svg("check-circle", size=size, color="#10b981")
    
    # Convert SVG to base64
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{b64}"