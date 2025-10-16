#!/usr/bin/env python3
"""
Tour Analysis Script for KKU 360° Virtual Tour
----------------------------------------------
This script analyzes the tour-config.json file and displays statistics and insights
about the virtual tour configuration, including scene counts, connections,
hotspot analytics, and visualization of the tour structure.
"""

import json
import os
import sys
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import networkx as nx
from tabulate import tabulate
import math

class TourAnalyzer:
    """Analyzes a 360° tour configuration file and provides statistics and visualizations."""
    
    def __init__(self, config_path):
        """Initialize the analyzer with the path to the tour config JSON file."""
        self.config_path = config_path
        self.config = self._load_config()
        self.scenes = self.config.get("scenes", {})
        self.default = self.config.get("default", {})
        
        # Extract first scene
        self.first_scene = self.default.get("firstScene", "")
        
        # Scene organization by floor
        self.scenes_by_floor = self._organize_by_floor()

    def _load_config(self):
        """Load the tour configuration from the JSON file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Config file not found at {self.config_path}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in config file {self.config_path}")
            sys.exit(1)
    
    def _organize_by_floor(self):
        """Group scenes by floor based on their panorama path."""
        floor_scenes = defaultdict(list)
        
        for scene_id, scene in self.scenes.items():
            panorama = scene.get("panorama", "")
            if "floor1" in panorama:
                floor_scenes["Floor 1"].append(scene_id)
            elif "floor2" in panorama:
                floor_scenes["Floor 2"].append(scene_id)
            else:
                floor_scenes["Other"].append(scene_id)
                
        return floor_scenes

    def get_basic_stats(self):
        """Return basic statistics about the tour configuration."""
        total_scenes = len(self.scenes)
        
        # Count hotspots
        hotspot_counts = []
        scene_hotspots = {}
        total_hotspots = 0
        scene_connections = 0
        
        for scene_id, scene in self.scenes.items():
            hotspots = scene.get("hotSpots", [])
            count = len(hotspots)
            hotspot_counts.append(count)
            scene_hotspots[scene_id] = count
            total_hotspots += count
            
            # Count scene connections
            for hotspot in hotspots:
                if hotspot.get("type") == "scene":
                    scene_connections += 1
        
        # Find scenes with most and least hotspots
        if total_scenes > 0:
            most_hotspots = max(scene_hotspots.items(), key=lambda x: x[1]) if scene_hotspots else None
            least_hotspots = min(scene_hotspots.items(), key=lambda x: x[1]) if scene_hotspots else None
            avg_hotspots = sum(hotspot_counts) / total_scenes if total_scenes > 0 else 0
        else:
            most_hotspots = None
            least_hotspots = None
            avg_hotspots = 0
            
        # Count hotspot types
        hotspot_types = Counter()
        for scene in self.scenes.values():
            for hotspot in scene.get("hotSpots", []):
                hotspot_types[hotspot.get("type", "unknown")] += 1
        
        return {
            "total_scenes": total_scenes,
            "total_hotspots": total_hotspots,
            "scene_connections": scene_connections,
            "avg_hotspots_per_scene": avg_hotspots,
            "most_connected_scene": most_hotspots,
            "least_connected_scene": least_hotspots,
            "hotspot_types": dict(hotspot_types),
            "scenes_by_floor": {floor: len(scenes) for floor, scenes in self.scenes_by_floor.items()},
        }
    
    def find_isolated_scenes(self):
        """Find scenes that have no connections to or from other scenes."""
        incoming_connections = defaultdict(list)
        outgoing_connections = defaultdict(list)
        
        # Map connections
        for scene_id, scene in self.scenes.items():
            # Track outgoing connections
            for hotspot in scene.get("hotSpots", []):
                if hotspot.get("type") == "scene":
                    target_scene = hotspot.get("sceneId")
                    if target_scene:
                        outgoing_connections[scene_id].append(target_scene)
                        incoming_connections[target_scene].append(scene_id)
        
        # Find isolated scenes
        isolated_scenes = []
        for scene_id in self.scenes:
            if not incoming_connections[scene_id] and not outgoing_connections[scene_id]:
                isolated_scenes.append(scene_id)
                
        # Find one-way connections (can go to but not return)
        one_way_connections = []
        for scene_id in self.scenes:
            for target in outgoing_connections[scene_id]:
                if scene_id not in outgoing_connections[target]:
                    one_way_connections.append((scene_id, target))
        
        return {
            "isolated_scenes": isolated_scenes,
            "one_way_connections": one_way_connections
        }

    def print_tour_summary(self):
        """Print a comprehensive summary of the tour configuration."""
        stats = self.get_basic_stats()
        isolation_data = self.find_isolated_scenes()
        
        print("\n" + "="*80)
        print(f"🌟 KKU 360° VIRTUAL TOUR ANALYSIS 🌟".center(80))
        print("="*80)
        
        # Basic Tour Information
        print("\n📊 TOUR OVERVIEW:")
        print(f"  • Configuration File: {os.path.basename(self.config_path)}")
        print(f"  • First Scene: {self.first_scene if self.first_scene else 'Not specified'}")
        print(f"  • Scene Transition Duration: {self.default.get('sceneFadeDuration', 'Not specified')} ms")
        
        # Scene Distribution
        print("\n📍 SCENE DISTRIBUTION:")
        total_scenes = stats["total_scenes"]
        for floor, count in stats["scenes_by_floor"].items():
            percentage = (count / total_scenes * 100) if total_scenes > 0 else 0
            print(f"  • {floor}: {count} scenes ({percentage:.1f}%)")
        
        # Hotspot Statistics
        print("\n🔍 HOTSPOT STATISTICS:")
        print(f"  • Total Hotspots: {stats['total_hotspots']}")
        
        # Hotspot Types
        print("\n🏷️  HOTSPOT TYPES:")
        for hotspot_type, count in stats["hotspot_types"].items():
            percentage = (count / stats["total_hotspots"] * 100) if stats["total_hotspots"] > 0 else 0
            print(f"  • {hotspot_type}: {count} ({percentage:.1f}%)")
        
        # Connectivity Statistics
        print("\n🔗 CONNECTIVITY STATISTICS:")
        print(f"  • Average Hotspots per Scene: {stats['avg_hotspots_per_scene']:.2f}")
        if stats["most_connected_scene"]:
            scene_id, count = stats["most_connected_scene"]
            scene_title = self.scenes[scene_id].get("title", "Unnamed")
            print(f"  • Most Connected Scene: {scene_title} (ID: {scene_id}) with {count} hotspots")
        
        if stats["least_connected_scene"]:
            scene_id, count = stats["least_connected_scene"]
            scene_title = self.scenes[scene_id].get("title", "Unnamed")
            print(f"  • Least Connected Scene: {scene_title} (ID: {scene_id}) with {count} hotspots")
        
        # Isolated Scenes
        if isolation_data["isolated_scenes"]:
            print("\n⚠️  ISOLATED SCENES (not connected to any other scenes):")
            for scene_id in isolation_data["isolated_scenes"]:
                scene_title = self.scenes.get(scene_id, {}).get("title", "Unnamed")
                print(f"  • {scene_title} (ID: {scene_id})")
        else:
            print("\n✅ No isolated scenes detected - all scenes are connected!")
        
        # One-way Connections
        if isolation_data["one_way_connections"]:
            print("\n⚠️  ONE-WAY CONNECTIONS (no return path):")
            for source, target in isolation_data["one_way_connections"][:5]:  # Show first 5
                source_title = self.scenes.get(source, {}).get("title", "Unnamed")
                target_title = self.scenes.get(target, {}).get("title", "Unnamed")
                print(f"  • {source_title} → {target_title}")
            
            if len(isolation_data["one_way_connections"]) > 5:
                print(f"    ... and {len(isolation_data['one_way_connections'])-5} more")
        
        print("\n" + "="*80)

    def visualize_tour_graph(self):
        """Create a visualization of the tour scene connections as a graph."""
        try:
            # Create a directed graph
            G = nx.DiGraph()
            
            # Add nodes for each scene
            for scene_id, scene in self.scenes.items():
                title = scene.get("title", f"Scene {scene_id}")
                G.add_node(scene_id, title=title)
                
                # Add edges for scene connections
                for hotspot in scene.get("hotSpots", []):
                    if hotspot.get("type") == "scene":
                        target_scene = hotspot.get("sceneId")
                        if target_scene:
                            G.add_edge(scene_id, target_scene)
            
            # Use a larger figure size
            plt.figure(figsize=(12, 8))
            
            # Color nodes by floor
            node_colors = []
            for node in G.nodes():
                panorama = self.scenes.get(node, {}).get("panorama", "")
                if "floor1" in panorama:
                    node_colors.append("skyblue")
                elif "floor2" in panorama:
                    node_colors.append("lightcoral")
                else:
                    node_colors.append("lightgray")
            
            # Set node sizes based on number of connections
            node_sizes = []
            for node in G.nodes():
                scene_data = self.scenes.get(node, {})
                if isinstance(scene_data, dict):
                    hotspots = scene_data.get("hotSpots", [])
                    node_sizes.append(300 + 50 * len(hotspots))
                else:
                    node_sizes.append(300)  # Default size if scene data is not a dictionary
            
            # Highlight first scene
            if self.first_scene and self.first_scene in G.nodes():
                node_colors[list(G.nodes()).index(self.first_scene)] = "gold"
            
            # Position nodes using a force-directed layout
            pos = nx.spring_layout(G, k=0.3, iterations=50, seed=42)
            
            # Draw the graph
            nx.draw(
                G, pos,
                node_color=node_colors,
                node_size=node_sizes,
                with_labels=False,
                arrows=True,
                arrowsize=15,
                edge_color="gray",
                alpha=0.8,
                width=1.5
            )
            
            # Add node labels with smaller font
            labels = {}
            for node, data in nx.get_node_attributes(G, 'title').items():
                if isinstance(data, str):
                    labels[node] = data
                else:
                    labels[node] = str(node)
            nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_family="sans-serif")
            
            # Add legend
            legend_elements = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='skyblue', markersize=10, label='Floor 1'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightcoral', markersize=10, label='Floor 2'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gold', markersize=10, label='First Scene')
            ]
            plt.legend(handles=legend_elements, loc='upper right')
            
            # Add title
            plt.title("KKU 360° Virtual Tour - Scene Connection Map", size=16)
            
            # Add custom information
            plt.figtext(0.5, 0.02, 
                     f"Total: {len(G.nodes())} scenes, {len(G.edges())} connections\nNode size represents number of hotspots",
                     ha="center", fontsize=10)
            
            # Save the visualization
            plt.tight_layout()
            plt.savefig("tour_graph.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"\n📊 Graph visualization saved as 'tour_graph.png'")
        except Exception as e:
            print(f"\n⚠️ Could not create visualization: {e}")
            print("Install matplotlib and networkx packages to enable visualizations.")

    def create_hotspot_heatmap(self):
        """Create a heatmap showing hotspot distribution across scenes."""
        try:
            # Collect pitch and yaw data from all hotspots
            pitch_yaw_data = []
            
            for scene in self.scenes.values():
                for hotspot in scene.get("hotSpots", []):
                    pitch = hotspot.get("pitch")
                    yaw = hotspot.get("yaw")
                    if pitch is not None and yaw is not None:
                        pitch_yaw_data.append((pitch, yaw))
            
            if not pitch_yaw_data:
                print("\n⚠️ No hotspot position data available for heatmap.")
                return
            
            # Convert to numpy array
            data = np.array(pitch_yaw_data)
            
            # Create figure
            plt.figure(figsize=(10, 5))
            
            # Create scatter plot with density
            plt.hexbin(
                data[:, 1],   # yaw
                data[:, 0],   # pitch
                gridsize=20, 
                cmap='viridis', 
                mincnt=1,
                bins='log'
            )
            
            # Add colorbar
            cbar = plt.colorbar()
            cbar.set_label('Hotspot Density')
            
            # Set limits and labels
            plt.xlim(-180, 180)
            plt.ylim(-90, 90)
            plt.xlabel('Yaw (degrees)')
            plt.ylabel('Pitch (degrees)')
            plt.title('Hotspot Position Distribution in 360° Space', size=14)
            
            # Add equator and poles reference lines
            plt.axhline(y=0, color='white', linestyle='--', alpha=0.5)
            plt.axhline(y=90, color='white', linestyle=':', alpha=0.3)
            plt.axhline(y=-90, color='white', linestyle=':', alpha=0.3)
            
            # Add text labels
            plt.text(175, 0, 'Equator', color='white', alpha=0.7, ha='right')
            plt.text(175, 85, 'Zenith', color='white', alpha=0.7, ha='right')
            plt.text(175, -85, 'Nadir', color='white', alpha=0.7, ha='right')
            
            # Save the heatmap
            plt.tight_layout()
            plt.savefig("hotspot_heatmap.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            print("🔥 Hotspot heatmap saved as 'hotspot_heatmap.png'")
        except Exception as e:
            print(f"\n⚠️ Could not create heatmap: {e}")

def main():
    """Main function to run the analysis."""
    # Get path to tour configuration
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "src", "tour-config.json")
    
    # If we're already in src directory, adjust path
    if not os.path.exists(config_path) and os.path.exists(os.path.join(script_dir, "tour-config.json")):
        config_path = os.path.join(script_dir, "tour-config.json")
    
    # Create analyzer and run analysis
    analyzer = TourAnalyzer(config_path)
    
    # Print text summary
    analyzer.print_tour_summary()
    
    # Create visualizations if matplotlib is available
    try:
        # matplotlib should already be imported at the top
        analyzer.visualize_tour_graph()
        analyzer.create_hotspot_heatmap()
    except ImportError:
        print("\n📊 Visualizations skipped: matplotlib or networkx package not installed.")
        print("To enable visualizations, run: pip install matplotlib networkx")

if __name__ == "__main__":
    main()
