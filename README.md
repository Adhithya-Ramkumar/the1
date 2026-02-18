# Purpose Graph System

A lightweight system for linking assets (physical objects, subscriptions, and shared tools) to the functions they serve in daily life. Surfaces functional overlap across different domains to support intentional decision-making.

## Overview

The Purpose Graph System reframes redundancy as information rather than waste or failure. Instead of tracking what people buy or own, it centers on **purpose**: what people actually need their things to do.

### Key Features

- **Purpose-Centered Tracking**: Link assets to the functions they serve, not just categories or spending
- **Cross-Domain Overlap Detection**: Surfaces redundancy across physical, digital, and shared resources
- **Transition Support**: Designed for moments of change (moving, co-living, work mode transitions)
- **Non-Prescriptive**: Reveals patterns without enforcing specific actions
- **Partial Input Friendly**: Useful insights emerge even with incomplete data

## Installation

No installation required. Simply clone this repository:

```bash
git clone https://github.com/Adhithya-Ramkumar/the1.git
cd the1
```

The system is implemented in pure Python with no external dependencies.

## Quick Start

### Interactive Mode (Recommended for Beginners)

```bash
python cli.py interactive
```

Follow the prompts to build your purpose graph step by step.

### Programmatic Use

```python
from purpose_graph import PurposeGraph, AssetType

# Create a purpose graph
graph = PurposeGraph()

# Define a purpose
graph.add_purpose("remote_work", "Remote Work", 
                 "Ability to work from home effectively")

# Add assets that serve this purpose
graph.add_asset("laptop", "Personal Laptop", AssetType.PHYSICAL)
graph.add_asset("desktop", "Desktop PC", AssetType.PHYSICAL)
graph.add_asset("shared_workspace", "Co-working Space", AssetType.SHARED)

# Link assets to purposes
graph.link_asset_to_purpose("laptop", "remote_work")
graph.link_asset_to_purpose("desktop", "remote_work")
graph.link_asset_to_purpose("shared_workspace", "remote_work")

# Detect overlap
overlap = graph.get_overlapping_purposes()
for info in overlap:
    purpose = info['purpose']
    assets = info['assets']
    print(f"{purpose.name}: {len(assets)} assets")
    for asset in assets:
        print(f"  - {asset.name} ({asset.asset_type.value})")
```

### Try the Examples

```bash
python cli.py examples
```

See complete scenarios: moving, co-living, and work transitions.

### Load Sample Data

```bash
python -c "from cli import load_graph_from_json; graph = load_graph_from_json('sample_data.json'); print([p.name for p in graph.get_all_purposes()])"
```

## Core Concepts

### Assets

Assets are things that serve purposes. They come in three types:

- **Physical**: Objects you own or could bring (laptop, cookware, furniture)
- **Digital**: Subscriptions, apps, online services (Netflix, cloud storage)
- **Shared**: Resources available through community or location (building gym, co-working printer)

### Purposes

Purposes are functional needs or use cases, such as:

- "Remote work"
- "Cooking basic meals"
- "Entertainment"
- "Document scanning"
- "Exercise"

Purposes should be framed around what you need to *do*, not what you need to *have*.

### The Purpose Graph

The graph maintains relationships between assets and purposes. When multiple assets map to the same purpose, **functional overlap** becomes visible.

## Use Cases

### 1. Moving to a New Place

```python
# See examples.py for full implementation
python examples.py
```

When relocating, the purpose graph helps you:
- Identify what's redundant with shared building resources
- Discover digital alternatives to physical items
- Make conscious decisions about what to bring

### 2. Co-Living Scenarios

When multiple people share a space:
- Reveals collective redundancy (3 coffee makers for 3 roommates)
- Shows what's already available vs. what each person might bring
- Facilitates group discussions without enforcing coordination

### 3. Work Mode Transitions

When shifting from office to remote work:
- Maps what was available at the office vs. what you need at home
- Identifies existing alternatives before purchasing new items
- Surfaces gaps vs. perceived needs

## API Reference

### PurposeGraph Class

#### Asset Management

```python
# Add an asset
asset = graph.add_asset(
    asset_id="unique_id",
    name="Human Readable Name",
    asset_type=AssetType.PHYSICAL,  # or DIGITAL or SHARED
    description="Optional description",
    metadata={"key": "value"}  # Optional metadata
)

# Remove an asset
graph.remove_asset("asset_id")

# Get assets
asset = graph.get_asset("asset_id")
all_assets = graph.get_all_assets()
physical_assets = graph.get_assets_by_type(AssetType.PHYSICAL)
```

#### Purpose Management

```python
# Add a purpose
purpose = graph.add_purpose(
    purpose_id="unique_id",
    name="Purpose Name",
    description="Optional description",
    category="Optional category"
)

# Remove a purpose
graph.remove_purpose("purpose_id")

# Get purposes
purpose = graph.get_purpose("purpose_id")
all_purposes = graph.get_all_purposes()
```

#### Linking Assets to Purposes

```python
# Create link
graph.link_asset_to_purpose("asset_id", "purpose_id")

# Remove link
graph.unlink_asset_from_purpose("asset_id", "purpose_id")

# Query relationships
assets = graph.get_assets_for_purpose("purpose_id")
purposes = graph.get_purposes_for_asset("asset_id")
```

#### Overlap Detection

```python
# Get all overlap information
overlap = graph.detect_overlap()

# Get only purposes with multiple assets
overlapping = graph.get_overlapping_purposes()

# Get purposes served by different asset types (physical + digital + shared)
cross_domain = graph.get_cross_domain_overlap()

# Get coverage summary
summary = graph.get_coverage_summary()
# Returns: {
#   'total_purposes': int,
#   'covered_purposes': int,
#   'uncovered_purposes': int,
#   'overlapping_purposes': int,
#   'cross_domain_purposes': int,
#   'total_assets': int,
#   'physical_assets': int,
#   'digital_assets': int,
#   'shared_assets': int
# }
```

#### Consolidation Suggestions

```python
# Get rule-based consolidation suggestions
suggestions = graph.suggest_consolidation_opportunities()

# Returns list of suggestions with types:
# - 'same_type_redundancy': Multiple physical/digital/shared assets for same purpose
# - 'digital_alternative': Digital options exist for physical assets
# - 'shared_alternative': Shared resources available for personal assets
```

## Testing

Run the comprehensive test suite:

```bash
python -m unittest test_purpose_graph.py -v
```

All 36 tests cover:
- Asset and purpose management
- Linking and unlinking
- Overlap detection
- Cross-domain analysis
- Consolidation suggestions
- Edge cases and error handling

## Design Philosophy

### What Makes This Novel

1. **Purpose Over Ownership**: Focuses on function rather than cost, spending, or possession
2. **Cross-Domain Visibility**: Surfaces overlap between physical, digital, and shared resources
3. **Non-Prescriptive**: Provides information, not judgments or mandatory actions
4. **Transition-Focused**: Most useful during moments of change and decision

### What This Is Not

- Not a spend tracker or budgeting tool
- Not a decluttering app with rules about what to keep
- Not an inventory system focused on cataloging possessions
- Not a recommendation engine telling you what to buy or discard

### Design Assumptions

- People are more open to reflection when decisions are framed around access and function rather than cost or guilt
- Clarity can emerge from imperfect, user-supplied information
- Overlap is information to be understood and acted upon intentionally
- Shared and digital resources are often overlooked when considering personal possessions

## Examples and Scenarios

See **[TUTORIAL.md](TUTORIAL.md)** for a comprehensive walkthrough.

See `examples.py` for three detailed scenarios:

1. **Moving to a New Apartment**: Individual decision-making during relocation
2. **Co-Living with Roommates**: Group-level redundancy and coordination
3. **Office to Remote Work Transition**: Replacing shared office resources

Run all examples:

```bash
python cli.py examples
# or
python examples.py
```

## Command-Line Interface

The CLI provides easy access to all features:

```bash
# Interactive mode - build your graph step by step
python cli.py interactive

# Run example scenarios
python cli.py examples

# Run test suite
python cli.py test
```

For programmatic use, you can also save and load graphs:

```python
from cli import save_graph_to_json, load_graph_from_json

# Save a graph
save_graph_to_json(graph, "my_graph.json")

# Load a graph
graph = load_graph_from_json("my_graph.json")
```

Sample data is provided in `sample_data.json`.

## Contributing

This is a novel concept implementation. Contributions, ideas, and feedback are welcome:

- Try the system in real scenarios
- Suggest new types of overlap detection
- Propose additional use cases
- Improve the API or add features

## License

This project is open source. See LICENSE for details.

## Future Directions

Potential extensions and experiments:

- Web interface for easier data entry and visualization
- Import/export to common formats (JSON, CSV)
- Community-level graphs for shared housing or neighborhoods
- Temporal tracking to see how purpose coverage changes over time
- Integration with existing inventory or asset management tools
- Visual graph representations of purpose networks

## Documentation

- **[README.md](README.md)** - This file, full documentation
- **[TUTORIAL.md](TUTORIAL.md)** - Step-by-step walkthrough with examples
- **[QUICKREF.md](QUICKREF.md)** - Quick reference for commands and API
- **[examples.py](examples.py)** - Three complete real-world scenarios
- **[sample_data.json](sample_data.json)** - Sample data to try the system

## Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.