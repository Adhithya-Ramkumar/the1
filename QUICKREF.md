# Quick Reference Guide

## Essential Commands

### Python API

```python
from purpose_graph import PurposeGraph, AssetType

# Create graph
graph = PurposeGraph()

# Add purpose
graph.add_purpose("purpose_id", "Purpose Name", "Description")

# Add asset
graph.add_asset("asset_id", "Asset Name", AssetType.PHYSICAL)
# AssetType: PHYSICAL, DIGITAL, or SHARED

# Link asset to purpose
graph.link_asset_to_purpose("asset_id", "purpose_id")

# Get overlap
overlap = graph.get_overlapping_purposes()

# Get coverage
summary = graph.get_coverage_summary()

# Get suggestions
suggestions = graph.suggest_consolidation_opportunities()
```

### Command Line

```bash
# Interactive mode
python cli.py interactive

# Run examples
python cli.py examples

# Run tests
python cli.py test
```

### Interactive Mode Commands

```
add-purpose     - Add a new purpose
add-asset       - Add a new asset
link            - Link asset to purpose
list-purposes   - Show all purposes
list-assets     - Show all assets
overlap         - Show overlap report
suggestions     - Show consolidation ideas
save            - Save to JSON
load            - Load from JSON
help            - Show all commands
quit            - Exit
```

## Common Queries

### Find Overlap

```python
# All purposes with multiple assets
overlapping = graph.get_overlapping_purposes()

# Cross-domain overlap (physical + digital + shared)
cross_domain = graph.get_cross_domain_overlap()

# Purposes with no assets
uncovered = graph.get_uncovered_purposes()
```

### Get Assets/Purposes

```python
# All assets for a purpose
assets = graph.get_assets_for_purpose("purpose_id")

# All purposes for an asset
purposes = graph.get_purposes_for_asset("asset_id")

# All assets of a type
physical = graph.get_assets_by_type(AssetType.PHYSICAL)
```

### Coverage Analysis

```python
summary = graph.get_coverage_summary()
# Returns:
# {
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

## JSON Format

```json
{
  "assets": [
    {
      "id": "unique_id",
      "name": "Asset Name",
      "asset_type": "physical",  // or "digital" or "shared"
      "description": "Optional description",
      "purposes": ["purpose_id1", "purpose_id2"],
      "metadata": {"key": "value"}
    }
  ],
  "purposes": [
    {
      "id": "unique_id",
      "name": "Purpose Name",
      "description": "Optional description",
      "category": "Optional category"
    }
  ]
}
```

## Asset Types

- **PHYSICAL**: Things you own or could bring
  - Examples: Laptop, cookware, furniture, books
  
- **DIGITAL**: Subscriptions, apps, online services
  - Examples: Netflix, Spotify, cloud storage, Zoom
  
- **SHARED**: Community or location-based resources
  - Examples: Building gym, shared printer, co-working space

## Purpose Framing

✓ **Good** (action-oriented):
- "Participate in video calls"
- "Prepare healthy meals"
- "Stay physically active"
- "Access important documents"

✗ **Avoid** (ownership/possession):
- "Have a laptop"
- "Own kitchen tools"
- "Possess exercise equipment"

## Use Cases

1. **Moving**: Compare assets to bring vs. shared resources at new location
2. **Co-Living**: Reveal collective redundancy among roommates
3. **Work Transition**: Map office resources vs. home needs
4. **Decluttering**: See what serves the same purpose
5. **Purchasing Decisions**: Check if purpose already covered

## Tips

- Start small (3-5 purposes, 5-10 assets)
- Include shared and digital, not just physical
- Frame purposes as actions, not possessions
- Use during transitions for best results
- Results are reflection points, not prescriptions

## Files

- `purpose_graph.py` - Core library
- `cli.py` - Command-line interface
- `examples.py` - Real-world scenarios
- `test_purpose_graph.py` - Test suite
- `sample_data.json` - Example data
- `README.md` - Full documentation
- `TUTORIAL.md` - Step-by-step guide
- `QUICKREF.md` - This file
