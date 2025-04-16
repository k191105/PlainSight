"""
Legal Text Analyzer for Streamlit Applications

This module provides utilities to identify and highlight problematic segments in legal text,
with different severity levels, detailed annotations, and interactive navigation.
"""

import streamlit as st
import html
import re
from typing import List, Dict, Any, Optional, Tuple
import uuid
import json


class LegalTextAnalyzer:
    """
    A class that analyzes legal text and highlights problematic segments
    with annotations and severity indicators.
    """

    SEVERITY_COLORS = {
        "high": {"bg": "rgba(255, 0, 0, 0.15)", "border": "rgba(255, 0, 0, 0.6)", "text": "#990000"},
        "medium": {"bg": "rgba(255, 153, 0, 0.15)", "border": "rgba(255, 153, 0, 0.6)", "text": "#b36b00"},
        "low": {"bg": "rgba(255, 204, 0, 0.15)", "border": "rgba(255, 204, 0, 0.6)", "text": "#806600"},
    }

    def __init__(self):
        """Initialize the LegalTextAnalyzer."""
        self.unique_id = str(uuid.uuid4()).replace("-", "")[:8]
        
    def _generate_css(self) -> str:
        """
        Generate the CSS for styling the highlighted text and annotations with a dark theme.
        
        Returns:
            str: CSS styles for the component
        """
        css = f"""
        <style>
            .legal-clause-{self.unique_id} {{
                position: relative;
                padding: 1.5rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                margin-bottom: 1.25rem;
                font-size: 1rem;
                line-height: 1.6;
                color: rgba(255, 255, 255, 0.87);
                background-color: rgba(30, 30, 35, 0.7);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
                font-family: "Inter", "Georgia", serif;
            }}
            
            .legal-clause-{self.unique_id}::before,
            .legal-clause-{self.unique_id}::after {{
                content: "⋯";
                display: block;
                color: rgba(255, 255, 255, 0.5);
                font-size: 1.5rem;
                margin: 0.5rem 0;
                text-align: center;
            }}
            
            .highlight-{self.unique_id} {{
                cursor: pointer;
                border-bottom-width: 2px;
                border-bottom-style: solid;
                padding: 0 2px;
                position: relative;
                transition: all 0.2s ease;
                border-radius: 3px;
            }}
            
            .highlight-{self.unique_id}:hover {{
                filter: brightness(1.2);
            }}
            
            .highlight-{self.unique_id}.active {{
                filter: brightness(1.5);
                box-shadow: 0 0 8px rgba(255, 255, 255, 0.3);
            }}
            
            .annotation-ref-{self.unique_id} {{
                font-size: 0.65rem;
                vertical-align: super;
                font-weight: 600;
                margin-left: 1px;
                margin-right: 1px;
                opacity: 0.9;
            }}
            
            .annotations-section-{self.unique_id} {{
                margin-top: 2rem;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                padding-top: 1.5rem;
            }}
            
            .annotations-section-{self.unique_id} h3 {{
                color: rgba(255, 255, 255, 0.87);
                margin-bottom: 1rem;
                font-weight: 500;
                font-family: "Inter", "Georgia", serif;
            }}
            
            .annotation-item-{self.unique_id} {{
                margin-bottom: 1.25rem;
                padding: 1rem;
                border-left: 3px solid rgba(255, 255, 255, 0.2);
                background-color: rgba(40, 40, 45, 0.6);
                border-radius: 0 6px 6px 0;
                transition: all 0.2s ease;
            }}
            
            .annotation-item-{self.unique_id}:hover {{
                background-color: rgba(50, 50, 55, 0.7);
            }}
            
            .annotation-item-{self.unique_id}.high {{
                border-left-color: rgba(255, 70, 70, 0.9);
            }}
            
            .annotation-item-{self.unique_id}.medium {{
                border-left-color: rgba(255, 153, 0, 0.9);
            }}
            
            .annotation-item-{self.unique_id}.low {{
                border-left-color: rgba(255, 204, 0, 0.9);
            }}
            
            .annotation-header-{self.unique_id} {{
                font-weight: 600;
                margin-bottom: 0.5rem;
                cursor: pointer;
                color: rgba(255, 255, 255, 0.9);
                display: flex;
                align-items: center;
                justify-content: space-between;
            }}
            
            .annotation-header-{self.unique_id}::after {{
                content: "▼";
                font-size: 0.75rem;
                opacity: 0.7;
                transition: transform 0.2s ease;
            }}
            
            .annotation-header-{self.unique_id}.collapsed::after {{
                transform: rotate(-90deg);
            }}
            
            .annotation-body-{self.unique_id} {{
                font-size: 0.9rem;
                color: rgba(255, 255, 255, 0.8);
                line-height: 1.5;
            }}
            
            .legal-reference-{self.unique_id} {{
                font-style: italic;
                margin-top: 0.5rem;
                font-size: 0.8rem;
                color: rgba(180, 180, 200, 0.7);
            }}
            
            .severity-legend-{self.unique_id} {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.75rem;
                margin: 1.25rem 0;
                padding: 0.75rem 1rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                background-color: rgba(35, 35, 40, 0.7);
                color: rgba(255, 255, 255, 0.87);
            }}
            
            .legend-item-{self.unique_id} {{
                display: flex;
                align-items: center;
                margin-right: 1rem;
                padding: 0.25rem 0;
            }}
            
            .legend-color-{self.unique_id} {{
                display: inline-block;
                width: 1.25rem;
                height: 0.9rem;
                margin-right: 0.5rem;
                border-radius: 3px;
                border-bottom-width: 2px;
                border-bottom-style: solid;
            }}
            
            .legend-label-{self.unique_id} {{
                font-size: 0.85rem;
            }}

            @media (max-width: 768px) {{
                .legal-clause-{self.unique_id} {{
                    padding: 1rem;
                    font-size: 0.9rem;
                }}
                
                .annotation-item-{self.unique_id} {{
                    padding: 0.75rem;
                }}
                
                .severity-legend-{self.unique_id} {{
                    flex-direction: column;
                    gap: 0.5rem;
                }}
            }}
        </style>
        """
        return css

    def _generate_js(self) -> str:
        """
        Generate the JavaScript code for enabling interactive features with improved animations.
        
        Returns:
            str: JavaScript code for the component
        """
        js = f"""
        <script>
            // Initialize collapsed state for annotations
            document.addEventListener('DOMContentLoaded', () => {{
                // Set all annotation bodies to be visible by default
                document.querySelectorAll('.annotation-body-{self.unique_id}').forEach(el => {{
                    el.style.display = 'block';
                }});
            }});
            
            function highlightClick_{self.unique_id}(refId) {{
                // Remove active class from all highlights
                document.querySelectorAll('.highlight-{self.unique_id}').forEach(el => {{
                    el.classList.remove('active');
                }});
                
                // Add active class to clicked highlight
                document.querySelectorAll(`.highlight-{self.unique_id}[data-ref-ids*="${{refId}}"]`).forEach(el => {{
                    el.classList.add('active');
                }});
                
                // Scroll to annotation
                const annotation = document.getElementById(`annotation-${{refId}}-{self.unique_id}`);
                if (annotation) {{
                    // Ensure the annotation body is visible
                    const body = document.getElementById(`annotation-body-${{refId}}-{self.unique_id}`);
                    if (body) {{
                        body.style.display = 'block';
                    }}
                    
                    // Remove collapsed class from header
                    const header = annotation.querySelector(`.annotation-header-{self.unique_id}`);
                    if (header) {{
                        header.classList.remove('collapsed');
                    }}
                    
                    // Smooth scroll to the annotation
                    annotation.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    
                    // Pulse animation effect
                    annotation.style.transition = 'background-color 0.3s ease';
                    annotation.style.backgroundColor = 'rgba(80, 80, 100, 0.5)';
                    setTimeout(() => {{
                        annotation.style.backgroundColor = '';
                    }}, 800);
                }}
            }}
            
            function annotationClick_{self.unique_id}(refId) {{
                // Toggle the body visibility
                toggleAnnotation_{self.unique_id}(refId);
                
                // Remove active class from all highlights first
                document.querySelectorAll('.highlight-{self.unique_id}').forEach(el => {{
                    el.classList.remove('active');
                }});
                
                // Find all corresponding highlights
                const highlights = document.querySelectorAll(`.highlight-{self.unique_id}[data-ref-ids*="${{refId}}"]`);
                
                // If there are no active highlights, activate and scroll to the first one
                if (highlights.length > 0) {{
                    // Add active class to all corresponding highlights
                    highlights.forEach(el => {{
                        el.classList.add('active');
                    }});
                    
                    // Scroll to the first highlight
                    highlights[0].scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    
                    // Pulse animation effect
                    highlights.forEach(el => {{
                        el.style.transition = 'all 0.3s ease';
                        const originalBackground = el.style.backgroundColor;
                        el.style.backgroundColor = 'rgba(100, 100, 140, 0.3)';
                        setTimeout(() => {{
                            el.style.backgroundColor = originalBackground;
                        }}, 800);
                    }});
                }}
            }}
            
            function toggleAnnotation_{self.unique_id}(refId) {{
                const body = document.getElementById(`annotation-body-${{refId}}-{self.unique_id}`);
                const header = document.querySelector(`#annotation-${{refId}}-{self.unique_id} .annotation-header-{self.unique_id}`);
                
                if (body && header) {{
                    // Toggle body visibility with a smooth animation
                    if (body.style.display === 'none') {{
                        // Show the body
                        body.style.display = 'block';
                        body.style.maxHeight = '0';
                        body.style.overflow = 'hidden';
                        body.style.transition = 'max-height 0.3s ease';
                        
                        // Use setTimeout to allow the transition to work
                        setTimeout(() => {{
                            body.style.maxHeight = body.scrollHeight + 'px';
                        }}, 10);
                        
                        // After transition completes, remove the constraints
                        setTimeout(() => {{
                            body.style.maxHeight = '';
                            body.style.overflow = '';
                            body.style.transition = '';
                        }}, 300);
                        
                        // Update header state
                        header.classList.remove('collapsed');
                    }} else {{
                        // Hide the body with animation
                        body.style.maxHeight = body.scrollHeight + 'px';
                        body.style.overflow = 'hidden';
                        body.style.transition = 'max-height 0.3s ease';
                        
                        // Use setTimeout to allow the transition to work
                        setTimeout(() => {{
                            body.style.maxHeight = '0';
                        }}, 10);
                        
                        // After transition completes, actually hide it
                        setTimeout(() => {{
                            body.style.display = 'none';
                            body.style.maxHeight = '';
                            body.style.overflow = '';
                            body.style.transition = '';
                        }}, 300);
                        
                        // Update header state
                        header.classList.add('collapsed');
                    }}
                }}
            }}
        </script>
        """
        return js
    
    def _escape_text(self, text: str) -> str:
        """
        Escape HTML special characters to prevent XSS attacks.
        
        Args:
            text (str): The text to escape
            
        Returns:
            str: HTML-escaped text
        """
        return html.escape(text)
    
    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace in text to handle flexible matching.
        
        Args:
            text (str): The text to normalize
            
        Returns:
            str: Text with normalized whitespace
        """
        # Replace multiple whitespace characters with a single space
        return re.sub(r'\s+', ' ', text.strip())
    
    def _find_text_positions(self, clause_text: str, problematic_text: str) -> List[Tuple[int, int]]:
        """
        Find all occurrences of problematic_text in clause_text with flexible whitespace matching.
        
        Args:
            clause_text (str): The full legal clause text
            problematic_text (str): The problematic text segment to find
            
        Returns:
            List[Tuple[int, int]]: List of (start, end) positions for all occurrences
        """
        # Normalize both texts for comparison
        normalized_clause = self._normalize_whitespace(clause_text)
        normalized_problematic = self._normalize_whitespace(problematic_text)
        
        # Create a regex pattern that matches the problematic text with flexible whitespace
        # Convert spaces to \s+ in the regex pattern
        pattern = re.escape(normalized_problematic).replace('\\ ', '\\s+')
        
        # Find all matches in the normalized clause
        matches = list(re.finditer(pattern, normalized_clause))
        
        # Return all start and end positions
        return [(m.start(), m.end()) for m in matches]
    
    def highlight_problematic_texts(self, clause_text: str, problematic_segments: List[Dict[str, Any]]) -> str:
        """
        Transform legal text into HTML with highlighting for problematic segments.
        
        Args:
            clause_text (str): The full legal clause text
            problematic_segments (List[Dict]): List of dictionaries containing problematic text segments
                Each dict must have 'problematic_text' and 'explanation' keys
                Optional keys: 'severity' (default: 'medium') and 'legal_reference'
                
        Returns:
            str: HTML string with highlighted problematic segments
        """
        # Normalize the clause text
        normalized_clause = self._normalize_whitespace(clause_text)
        
        # Create a list to track all segment positions with their annotations
        segments = []
        
        # Generate unique reference IDs for each problematic segment
        for i, segment in enumerate(problematic_segments):
            ref_id = f"ref{i+1}"
            problematic_text = segment.get('problematic_text', '')
            positions = self._find_text_positions(normalized_clause, problematic_text)
            
            severity = segment.get('severity', 'medium').lower()
            # Ensure severity is one of the supported levels
            if severity not in self.SEVERITY_COLORS:
                severity = 'medium'
            
            # Add all positions with this reference ID and severity
            for start, end in positions:
                segments.append({
                    'start': start,
                    'end': end,
                    'ref_id': ref_id,
                    'severity': severity
                })
        
        # Sort segments by start position to process them in order
        segments.sort(key=lambda x: x['start'])
        
        # Merge overlapping segments
        merged_segments = []
        if segments:
            current = segments[0].copy()
            for segment in segments[1:]:
                if segment['start'] <= current['end']:
                    # Overlapping segments - extend the end if needed
                    current['end'] = max(current['end'], segment['end'])
                    # Combine reference IDs for annotations
                    if segment['ref_id'] not in current['ref_id']:
                        current['ref_id'] = f"{current['ref_id']},{segment['ref_id']}"
                    # Use the highest severity among overlapping segments
                    severities = ['low', 'medium', 'high']
                    current_severity_idx = severities.index(current['severity'])
                    segment_severity_idx = severities.index(segment['severity'])
                    if segment_severity_idx > current_severity_idx:
                        current['severity'] = segment['severity']
                else:
                    # Non-overlapping - add the current segment and start a new one
                    merged_segments.append(current)
                    current = segment.copy()
            
            # Add the last segment
            merged_segments.append(current)
        
        # Prepare for building the highlighted HTML
        result = []
        last_end = 0
        
        # Apply highlights to the original text
        for segment in merged_segments:
            # Add text before this segment
            result.append(self._escape_text(normalized_clause[last_end:segment['start']]))
            
            # Add the highlighted segment
            severity = segment['severity']
            colors = self.SEVERITY_COLORS[severity]
            
            # Extract multiple reference IDs if present
            ref_ids = segment['ref_id'].split(',')
            ref_badges = ''.join([
                f'<sup class="annotation-ref-{self.unique_id}">{ref_id[3:]}</sup>' 
                for ref_id in ref_ids
            ])
            
            # Create the highlighted text with all annotation references
            highlighted_text = self._escape_text(normalized_clause[segment['start']:segment['end']])
            
            result.append(
                f'<span class="highlight-{self.unique_id}" '
                f'style="background-color: {colors["bg"]}; border-bottom-color: {colors["border"]};" '
                f'data-ref-ids="{segment["ref_id"]}" '
                f'onclick="highlightClick_{self.unique_id}(\'{ref_ids[0]}\')">'
                f'{highlighted_text}{ref_badges}</span>'
            )
            
            last_end = segment['end']
        
        # Add any remaining text
        result.append(self._escape_text(normalized_clause[last_end:]))
        
        # Wrap in a div with the document context indicators
        html_result = (
            f'<div class="legal-clause-{self.unique_id}">'
            f'{"".join(result)}'
            f'</div>'
        )
        
        return html_result
    
    def _generate_annotations_html(self, problematic_segments: List[Dict[str, Any]]) -> str:
        """
        Generate HTML for displaying annotations.
        
        Args:
            problematic_segments (List[Dict]): List of dictionaries with problematic segments
            
        Returns:
            str: HTML string with annotations
        """
        annotations_html = f'<div class="annotations-section-{self.unique_id}">'
        annotations_html += f'<h3>Annotations</h3>'
        
        for i, segment in enumerate(problematic_segments):
            ref_id = f"ref{i+1}"
            severity = segment.get('severity', 'medium').lower()
            if severity not in self.SEVERITY_COLORS:
                severity = 'medium'
            
            explanation = self._escape_text(segment.get('explanation', ''))
            legal_reference = segment.get('legal_reference', '')
            
            annotations_html += f"""
            <div id="annotation-{ref_id}-{self.unique_id}" 
                 class="annotation-item-{self.unique_id} {severity}">
                <div class="annotation-header-{self.unique_id}" 
                     onclick="toggleAnnotation_{self.unique_id}('{ref_id}')">
                    <span onclick="annotationClick_{self.unique_id}('{ref_id}')"
                          style="cursor: pointer;">
                        Issue {i+1}: {self._escape_text(segment.get('problematic_text', '')[:50])}
                        {' [...]' if len(segment.get('problematic_text', '')) > 50 else ''}
                    </span>
                </div>
                <div id="annotation-body-{ref_id}-{self.unique_id}" 
                     class="annotation-body-{self.unique_id}">
                    <p>{explanation}</p>
                    {f'<p class="legal-reference-{self.unique_id}">{self._escape_text(legal_reference)}</p>' 
                      if legal_reference else ''}
                </div>
            </div>
            """
        
        annotations_html += '</div>'
        return annotations_html
    
    def _generate_severity_legend(self) -> str:
        """
        Generate HTML for the severity level legend.
        
        Returns:
            str: HTML string for the severity legend
        """
        legend_html = f'<div class="severity-legend-{self.unique_id}">'
        
        # Add a title for the legend
        legend_html += '<div style="width: 100%; margin-bottom: 8px;"><strong>Risk Severity Levels:</strong></div>'
        
        # Add legend items for each severity level
        for severity, colors in self.SEVERITY_COLORS.items():
            legend_html += f"""
            <div class="legend-item-{self.unique_id}">
                <span class="legend-color-{self.unique_id}" 
                      style="background-color: {colors['bg']}; border-bottom-color: {colors['border']};"></span>
                <span class="legend-label-{self.unique_id}">{severity.capitalize()}</span>
            </div>
            """
        
        legend_html += '</div>'
        return legend_html
    
    def display_highlighted_clause(self, clause_text: str, problematic_segments: List[Dict[str, Any]]) -> None:
        """
        Display the highlighted clause in Streamlit.
        
        Args:
            clause_text (str): The full legal clause text
            problematic_segments (List[Dict]): List of dictionaries containing problematic text segments
        """
        # Generate all necessary HTML components
        css = self._generate_css()
        js = self._generate_js()
        highlighted_html = self.highlight_problematic_texts(clause_text, problematic_segments)
        
        # Combine into a single HTML string
        full_html = f"{css}{js}{highlighted_html}"
        
        # Display in Streamlit
        st.components.v1.html(full_html, height=400, scrolling=True)
    
    def annotate_clause_risks(self, clause_text: str, problematic_segments: List[Dict[str, Any]]) -> None:
        """
        Comprehensive display with highlighted text, annotations, and legend.
        
        Args:
            clause_text (str): The full legal clause text
            problematic_segments (List[Dict]): List of dictionaries containing problematic text segments
        """
        # Generate all necessary HTML components
        css = self._generate_css()
        js = self._generate_js()
        highlighted_html = self.highlight_problematic_texts(clause_text, problematic_segments)
        annotations_html = self._generate_annotations_html(problematic_segments)
        legend_html = self._generate_severity_legend()
        
        # Add heading above text
        heading_html = f'<h3 style="color: rgba(255, 255, 255, 0.87); margin-bottom: 15px; font-family: \\"Inter\\", \\"Georgia\\", serif; font-weight: 500;">Clause Text With Annotations</h3>'
        
        # Combine into a single HTML string - heading first, then text, legend, and annotations
        full_html = f"{css}{js}{heading_html}{highlighted_html}{legend_html}{annotations_html}"
        
        # Calculate appropriate height based on content
        content_height = 500 + (len(problematic_segments) * 50)
        
        # Display in Streamlit
        st.components.v1.html(full_html, height=content_height, scrolling=True)


# Create a wrapper function to maintain backward compatibility
def annotate_clause_risks(clause_text: str, problematic_segments: List[Dict[str, Any]]) -> None:
    """
    Wrapper function to maintain backward compatibility with existing code.
    Creates an instance of LegalTextAnalyzer and calls the annotate_clause_risks method.
    
    Args:
        clause_text (str): The full legal clause text
        problematic_segments (List[Dict]): List of dictionaries containing problematic text segments
    """
    # Convert string segments to dictionary format if needed
    if problematic_segments and isinstance(problematic_segments[0], str):
        problematic_segments = [
            {
                'problematic_text': segment,
                'explanation': segment,
                'severity': 'medium'
            }
            for segment in problematic_segments
        ]
    
    analyzer = LegalTextAnalyzer()
    analyzer.annotate_clause_risks(clause_text, problematic_segments)


def highlight_problematic_texts(clause_text: str, problematic_segments: List[Dict[str, Any]]) -> str:
    """
    Wrapper function for highlight_problematic_texts method.
    
    Args:
        clause_text (str): The full legal clause text
        problematic_segments (List[Dict]): List of dictionaries containing problematic text segments
            
    Returns:
        str: HTML string with highlighted problematic segments
    """
    # Convert string segments to dictionary format if needed
    if problematic_segments and isinstance(problematic_segments[0], str):
        problematic_segments = [
            {
                'problematic_text': segment,
                'explanation': segment,
                'severity': 'medium'
            }
            for segment in problematic_segments
        ]
    
    analyzer = LegalTextAnalyzer()
    return analyzer.highlight_problematic_texts(clause_text, problematic_segments)


def display_highlighted_clause(clause_text: str, problematic_segments: List[Dict[str, Any]]) -> None:
    """
    Wrapper function for display_highlighted_clause method.
    
    Args:
        clause_text (str): The full legal clause text
        problematic_segments (List[Dict]): List of dictionaries containing problematic text segments
    """
    # Convert string segments to dictionary format if needed
    if problematic_segments and isinstance(problematic_segments[0], str):
        problematic_segments = [
            {
                'problematic_text': segment,
                'explanation': segment,
                'severity': 'medium'
            }
            for segment in problematic_segments
        ]
    
    analyzer = LegalTextAnalyzer()
    analyzer.display_highlighted_clause(clause_text, problematic_segments)