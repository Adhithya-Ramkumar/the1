# Purpose Graph System

A lightweight system for mapping assets (physical objects, digital services, shared resources) to the purposes they serve, making functional overlap visible without focusing on cost or ownership.

## Overview

The Purpose Graph supports intentional decision-making by revealing how different assets—across physical, digital, and shared domains—serve the same purposes in daily life. Instead of tracking what you buy or own, it centers on **what you need your things to do**.

### Key Concepts

- **Assets**: Physical objects, digital services, subscriptions, or shared resources
- **Purposes**: Functions or needs in daily life (e.g., "remote work", "cooking basic meals", "entertainment")
- **Purpose Graph**: A mapping that links assets to purposes, revealing functional overlap
- **Functional Overlap**: When multiple assets serve the same purpose

### What Makes It Novel

- **Reframes redundancy as information** rather than waste or failure
- **Removes money from the center**, focusing on purpose and function instead
- **Treats overlap intentionally**, especially across physical/digital boundaries
- **Most useful during transitions**: moving, co-living, work mode changes, temporary communities

## Installation

No installation needed! This is a pure Python implementation with no external dependencies (uses only the standard library).

Requirements:
- Python 3.7 or higher

## Quick Start

### Running Examples

See the system in action with pre-built scenarios:

```bash
python3 examples.py
```

This demonstrates three scenarios:
1. **Relocation to Shared Housing**: What can I leave behind?
2. **Office to Remote Work Transition**: What office equipment is now redundant?
3. **Minimal Living Assessment**: Where do I have redundancy?

### Using the CLI

Create a new purpose graph and start adding your assets:

```bash
# Add a purpose
python3 cli.py add-purpose "remote work" --description "Video calls and document editing"

# Add assets
python3 cli.py add-asset laptop physical --description "Personal work computer"
python3 cli.py add-asset zoom subscription --description "Video conferencing"
python3 cli.py add-asset "office-desk-phone" physical --description "VoIP phone at office"

# Link assets to purposes
python3 cli.py link laptop "remote work"
python3 cli.py link zoom "remote work"
python3 cli.py link office-desk-phone "remote work"

# Analyze overlaps
python3 cli.py show-overlaps
```

## CLI Reference

### Asset Management

```bash
# Add an asset
python3 cli.py add-asset <name> <type> [--description TEXT]
# Types: physical, digital, shared, subscription

# Remove an asset
python3 cli.py remove-asset <name>

# List all assets
python3 cli.py list-assets [--type TYPE]
```

### Purpose Management

```bash
# Add a purpose
python3 cli.py add-purpose <name> [--description TEXT]

# Remove a purpose
python3 cli.py remove-purpose <name>

# List all purposes
python3 cli.py list-purposes
```

### Linking Assets to Purposes

```bash
# Link an asset to a purpose
python3 cli.py link <asset> <purpose>

# Unlink an asset from a purpose
python3 cli.py unlink <asset> <purpose>
```

### Analysis Commands

```bash
# Show functional overlaps (purposes served by multiple assets)
python3 cli.py show-overlaps

# Show cross-domain overlaps (purposes served across physical/digital/shared boundaries)
python3 cli.py show-cross-domain

# Show summary statistics
python3 cli.py summary
```

### Data Management

```bash
# Use a custom data file
python3 cli.py --file my_graph.json <command>
```

## Usage Scenarios

### Scenario 1: Moving to Shared Housing

**Question**: What can I leave behind?

1. Add purposes: "remote work", "cooking", "entertainment", "document scanning"
2. Add your personal assets
3. Add shared resources available at new location
4. Link assets to purposes
5. Run `show-overlaps` to see where shared resources cover your needs

**Insight**: Shared printer covers document scanning → can leave personal scanner behind

### Scenario 2: Changing Work Modes

**Question**: What's redundant after going remote?

1. Add work-related purposes
2. Add office equipment and digital tools
3. Link them to purposes
4. Run `show-cross-domain` to see physical/digital overlaps

**Insight**: Zoom covers video calls → office desk phone now redundant

### Scenario 3: Intentional Living

**Question**: Where do I have redundancy?

1. Add daily life purposes
2. Add all assets that serve each purpose
3. Run `show-overlaps` to reveal patterns

**Insight**: Not a prescription, but information for intentional decisions

## Python API

Use the purpose graph programmatically:

```python
from purpose_graph import PurposeGraph, Asset, Purpose, AssetType

# Create a graph
graph = PurposeGraph()

# Add purposes
work = Purpose("remote work", "Video calls and documents")
graph.add_purpose(work)

# Add assets
laptop = Asset("laptop", AssetType.PHYSICAL, "Work computer")
zoom = Asset("zoom", AssetType.SUBSCRIPTION, "Video platform")
graph.add_asset(laptop)
graph.add_asset(zoom)

# Link assets to purposes
graph.link_asset_to_purpose("laptop", "remote work")
graph.link_asset_to_purpose("zoom", "remote work")

# Analyze
overlaps = graph.find_overlapping_purposes()
cross_domain = graph.find_cross_domain_overlaps()
summary = graph.get_coverage_summary()

# Save/load
graph.save_to_file("my_graph.json")
loaded = PurposeGraph.load_from_file("my_graph.json")
```

## Core API Reference

### Classes

#### `Asset`
Represents an asset (object, service, or shared resource)

- `name: str` - Asset identifier
- `asset_type: AssetType` - Type (PHYSICAL, DIGITAL, SHARED, SUBSCRIPTION)
- `description: Optional[str]` - Optional description
- `metadata: Dict[str, Any]` - Optional metadata

#### `Purpose`
Represents a purpose or function

- `name: str` - Purpose identifier
- `description: Optional[str]` - Optional description

#### `PurposeGraph`
Core graph linking assets to purposes

**Methods**:
- `add_asset(asset)` - Add an asset
- `remove_asset(name)` - Remove an asset
- `add_purpose(purpose)` - Add a purpose
- `remove_purpose(name)` - Remove a purpose
- `link_asset_to_purpose(asset_name, purpose_name)` - Create a link
- `unlink_asset_from_purpose(asset_name, purpose_name)` - Remove a link
- `get_assets_for_purpose(purpose_name)` - Get assets serving a purpose
- `get_purposes_for_asset(asset_name)` - Get purposes served by an asset
- `find_overlapping_purposes()` - Find purposes with multiple assets
- `find_cross_domain_overlaps()` - Find overlaps across asset types
- `get_coverage_summary()` - Get statistical summary
- `save_to_file(filename)` - Save to JSON
- `load_from_file(filename)` - Load from JSON (class method)

## Testing

Run the test suite:

```bash
python3 test_purpose_graph.py
```

Or with verbose output:

```bash
python3 test_purpose_graph.py -v
```

## Design Philosophy

### Why Purpose-Centered?

Traditional tools focus on spending, ownership, or decluttering. The purpose graph shifts the lens to **function and access**:

- Not "how much did this cost?" but "what does this do?"
- Not "do I own it?" but "do I have access to this function?"
- Not "should I throw it away?" but "how is this purpose already served?"

### Assumption: Clarity from Imperfect Data

The system doesn't require complete or precise information. Partial input reveals patterns. Users can:

- Tag loosely without perfect categorization
- Add data incrementally
- Focus on areas of active decision-making

### When Transitions Matter

The purpose graph is designed for moments when decisions must be made:

- **Moving homes**: What to bring vs. leave
- **Shared housing**: What's redundant with shared resources
- **Work mode changes**: Remote vs. office needs
- **Temporary communities**: What to acquire vs. what's available
- **Intentional reduction**: Understanding current coverage

### Information, Not Prescription

The graph reveals overlap but doesn't dictate action. It supports:

- **Reflection** during transitions
- **Awareness** of functional redundancy
- **Intentional choices** about what to keep, share, or change

Some overlaps are useful (redundancy for reliability). Others signal opportunities. The user decides.

## Example Output

### Overlap Analysis
```
FUNCTIONAL OVERLAPS DETECTED

The following purposes are served by multiple assets:

📋 Purpose: document scanning
   Covered by 3 assets:
     • scanner (physical)
     • adobe-scan-app (digital)
     • shared-printer-scanner (shared)
```

### Cross-Domain Analysis
```
CROSS-DOMAIN OVERLAPS

Purposes served by different types of assets:

📋 Purpose: entertainment
   Served across 2 domains:

   SUBSCRIPTION:
     • netflix

   SHARED:
     • house-netflix
```

## Data Storage

Graphs are stored as JSON files:

```json
{
  "assets": {
    "laptop": {
      "name": "laptop",
      "asset_type": "physical",
      "description": "Work computer",
      "metadata": {}
    }
  },
  "purposes": {
    "remote work": {
      "name": "remote work",
      "description": "Video calls and documents"
    }
  },
  "links": {
    "remote work": ["laptop", "zoom"]
  }
}
```

## Contributing

This is a minimal implementation demonstrating the core concept. Potential extensions:

- Web interface
- Import from existing inventory systems
- Collaborative/shared graphs for communities
- Temporal tracking (coverage over time)
- Recommendation system for shared resources

## License

This is a demonstration implementation. Use and modify as needed.

## Acknowledgments

This implementation realizes the concept described in the problem statement: a purpose-centered approach to understanding functional overlap across physical, digital, and shared resources—designed for transitions and intentional decision-making.