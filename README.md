# KKU 360° Virtual Tour

A simple virtual tour project for Khon Kaen University's Department of Civil Engineering.

## About This Project

This is my attempt to create a virtual tour for KKU's Civil Engineering department. The tour allows visitors to navigate through different areas of our campus buildings using 360° panoramic images.

## Features

- **360° Panoramic Views**: Explore rooms and hallways in a complete 360° view
- **Simple Navigation**: Move between locations by clicking on hotspots
- **Basic Map**: A simple floor plan to help with orientation
- **Mobile Support**: Works on mobile devices, though the experience is better on desktop
- **Modest File Size**: Tried to keep image sizes reasonable for faster loading

## Live Demo

You can try out the tour here: [https://c-poramet.github.io/360KKU/index.html](https://c-poramet.github.io/360KKU/index.html)

## Project Structure

```
360KKU/
├── src/                      # Source files
│   ├── images/               # Panoramic images
│   │   ├── floor1/           # First floor images
│   │   └── floor2/           # Second floor images
│   ├── tour-config.json      # Tour configuration
│   ├── tour.html             # Tour viewer
│   ├── configurator.html     # Tour building tool
│   └── style.css             # CSS styles
├── analysis.py               # Analytics script
├── index.html                # Landing page
└── README.md                 # This file
```

## Tour Configurator Tool

I've also created a basic tool (`src/configurator.html`) to help build these kinds of tours:

- Upload floor plans to help with scene placement
- Add panoramic images by dragging and dropping
- Place navigation hotspots visually
- Generate the necessary configuration JSON

While it's still a work in progress with some bugs, it helps avoid editing JSON files manually. See the [configurator guide](configurator-guide.md) for more details.

## Known Issues

The tour has several limitations I'm still working on:

- Hotspots sometimes disappear when switching between scenes
- No minimap feature yet (planned for future updates)
- Scene transitions aren't very smooth
- Initial loading can be slow with many images

Check the [development roadmap](configurator-guide.md#development-roadmap) for planned improvements.

## Analytics Tool

The included Python script (`analysis.py`) provides some basic insights about the tour:

- Counts scenes and hotspots
- Shows connections between scenes
- Identifies navigation issues like dead-ends
- Creates simple visualizations of the tour structure

To run:
```bash
python3 analysis.py
```

Requirements: matplotlib, networkx, numpy, tabulate

## Getting Started with Development

1. Clone the repository
2. Open `index.html` in your browser to view the landing page
3. Click "Start Virtual Tour" to launch the tour
4. To modify the tour, edit `src/tour-config.json` or use the configurator

## Acknowledgements

- Tour viewer built with [Pannellum](https://pannellum.org/)
- Styling help from [Tailwind CSS](https://tailwindcss.com/)
- Icons from [Font Awesome](https://fontawesome.com/)
- Thanks to KKU Civil Engineering Department for access to the facilities

## Contact

Poramet Chomphoochit  
Computer Engineering, Khon Kaen University

This document provides detailed instructions for using the KKU 360° Tour Configurator, the specialized tool built to create and manage virtual tours with ease.

![Tour Configurator](src/images/configurator-screenshot.png)

## Getting Started

The Tour Configurator is a web-based application designed to provide a visual interface for building your 360° tour without editing JSON files manually.

### Opening the Configurator

1. Navigate to `src/configurator.html` in your web browser
2. The interface is divided into three main sections:
   - **Left Panel**: Floor plan and scene management
   - **Center Panel**: Panorama viewer and hotspot editing
   - **Bottom Panel**: JSON configuration output

## Step-by-Step Tour Creation

### 1. Upload a Floor Plan

The floor plan provides spatial context for positioning your scenes:

1. Click the "Upload Floor Plan" area in the left panel
2. Select an image file of your building layout
3. The floor plan will appear in the canvas area

### 2. Add Scenes to Your Tour

Each scene represents a viewpoint in your 360° tour:

1. Click anywhere on the floor plan to place a new scene
2. In the scene modal that appears:
   - Enter a unique Scene ID (or accept the auto-generated one)
   - Enter a descriptive Scene Title
   - Upload a panorama image or enter its path
3. Click "Save Scene" to create the scene

### 3. Add Navigation Hotspots

Hotspots connect scenes and allow users to navigate through your tour:

1. Select a scene from the scene list to load it in the panorama viewer
2. Click the "Add Hotspot" button (blue circle icon)
3. Click anywhere in the panorama view to place a hotspot
4. In the hotspot modal:
   - Select a destination scene from the dropdown
   - Enter descriptive text for the hotspot
5. Click "Save Hotspot"

### 4. Configure Tour Settings

Set up the overall tour behavior:

1. Select a starting scene from the "First Scene" dropdown
2. Adjust the transition duration using the slider
3. Set the default floor for new scenes (optional)

### 5. Export Your Configuration

When you're satisfied with your tour:

1. Review the JSON in the bottom panel
2. Click "Copy JSON" to copy the configuration to your clipboard
3. Paste into your project's `tour-config.json` file

## Advanced Features

### Auto-Save

The configurator automatically saves your work to the browser's local storage:

- Your work is saved as you make changes
- If you accidentally close the browser, you'll be prompted to restore your work
- Click "Clear Auto-Save" to delete the saved data

### Floor Detection

The system can automatically organize your images by floor:

- Filenames containing "floor1", "1st", "first", "ground", or "main" → Floor 1
- Filenames containing "floor2", "2nd", "second", "upper", or "top" → Floor 2

### Development Mode

When working with local images:

- Upload panoramic images to see them in the configurator
- The tool will generate the correct deployment paths automatically
- These paths will be included in the JSON output

## Tips & Tricks

1. **Consistent Naming**: Use consistent naming conventions for your panorama files to help with organization
2. **Test Navigation**: Always test navigation between scenes to ensure a smooth user experience
3. **Coordinate Spacing**: Avoid placing hotspots too close together
4. **Add Descriptions**: Always include clear descriptions for hotspots to guide users
5. **Use Auto-Detection**: Let the system auto-detect floors based on your filenames

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Panorama not displaying | Check file path and ensure image is a compatible equirectangular format |
| Hotspots not appearing | Try toggling hotspot mode off and on again |
| Floor plan not showing | Check if the image format is supported (JPG, PNG recommended) |
| Scenes not connecting | Verify that both scenes have hotspots pointing to each other |
| JSON not updating | Click inside the JSON display area to refresh |

## Keyboard Shortcuts

- **Esc**: Close any open modal
- **Ctrl+S**: Copy JSON configuration
- **Spacebar** (when viewing panorama): Toggle hotspot mode

## Development Roadmap

The Tour Configurator is continuously evolving. Here are the planned improvements for future releases:

### Known Issues to Address

- **Invisible Hotspots**: Hotspots can sometimes become invisible when switching between scenes. Workaround: Toggle hotspot mode off and on again to refresh the view.
- **Performance Concerns**: Loading large panoramas can cause slowdowns on some devices. Future optimizations will include image compression and lazy loading.
- **Scene Transitions**: The transitions between scenes are not as smooth as they could be, particularly on mobile devices.
- **Initial Load Time**: The initial loading of the tour can be slow, especially with many scenes.

### Planned Enhancements

1. **Interactive Minimap**: Adding a persistent minimap that shows current position during tour navigation
2. **Improved Hotspot Management**: Enhanced UI for editing existing hotspots
3. **Performance Optimizations**: Faster loading times and smoother transitions
4. **Mobile Experience**: Improved touch controls and responsive design for mobile devices
5. **Batch Operations**: Tools for managing multiple scenes and hotspots at once
6. **Advanced Floor Management**: Better support for multi-level buildings and complex layouts
7. **Export/Import Options**: More options for saving and sharing your tour configurations

We welcome contributions and feedback on these planned improvements! Visit our [live demo](https://c-poramet.github.io/360KKU/index.html) to see the current version in action.