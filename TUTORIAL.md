# Getting Started with the Purpose Graph System

This guide will walk you through using the Purpose Graph System to map your assets to purposes and discover functional overlap.

## Table of Contents

1. [Understanding the Basics](#understanding-the-basics)
2. [Your First Purpose Graph](#your-first-purpose-graph)
3. [Interpreting Results](#interpreting-results)
4. [Real-World Scenarios](#real-world-scenarios)
5. [Interactive Mode](#interactive-mode)
6. [Saving and Loading](#saving-and-loading)

## Understanding the Basics

### What is a Purpose?

A purpose is a functional need or use case. Think about what you need to **do**, not what you need to **have**. Examples:

- ✓ "Stay informed about news"
- ✓ "Prepare healthy meals"
- ✓ "Participate in video meetings"
- ✗ "Have a smartphone" (this is an asset, not a purpose)
- ✗ "Own kitchen tools" (this is ownership, not a purpose)

### What is an Asset?

An asset is anything that helps you accomplish a purpose. Assets come in three types:

1. **Physical**: Things you own or could bring (laptop, cookware, furniture)
2. **Digital**: Subscriptions, apps, online services (Netflix, Dropbox, Spotify)
3. **Shared**: Resources available through community or location (building gym, shared printer, co-working space)

### What is Functional Overlap?

When multiple assets serve the same purpose, that's functional overlap. For example:

- Purpose: "Stay entertained"
  - Smart TV (physical)
  - Netflix subscription (digital)
  - Laptop (physical)
  - YouTube (digital)

This isn't necessarily bad! But it's information you might want to know when making decisions.

## Your First Purpose Graph

Let's build a simple graph step by step.

### Step 1: Import the Library

```python
from purpose_graph import PurposeGraph, AssetType

# Create a new graph
graph = PurposeGraph()
```

### Step 2: Define Your Purposes

Start with 2-3 purposes from your daily life:

```python
# Add purposes
graph.add_purpose(
    purpose_id="coffee",
    name="Make Morning Coffee",
    description="Have good coffee to start the day"
)

graph.add_purpose(
    purpose_id="video_calls",
    name="Video Calls",
    description="Professional video conferencing"
)

graph.add_purpose(
    purpose_id="exercise",
    name="Stay Active",
    description="Regular physical activity"
)
```

### Step 3: Add Your Assets

List things you have or have access to:

```python
# Physical assets you own
graph.add_asset("french_press", "French Press", AssetType.PHYSICAL)
graph.add_asset("espresso_machine", "Espresso Machine", AssetType.PHYSICAL)
graph.add_asset("yoga_mat", "Yoga Mat", AssetType.PHYSICAL)

# Digital assets (subscriptions/apps)
graph.add_asset("zoom", "Zoom Account", AssetType.DIGITAL)
graph.add_asset("peloton_app", "Peloton App", AssetType.DIGITAL)

# Shared resources
graph.add_asset("office_conference_room", "Office Conference Rooms", AssetType.SHARED)
graph.add_asset("building_gym", "Building Gym", AssetType.SHARED)
```

### Step 4: Link Assets to Purposes

Connect what you have to what it helps you do:

```python
# Coffee making
graph.link_asset_to_purpose("french_press", "coffee")
graph.link_asset_to_purpose("espresso_machine", "coffee")

# Video calls
graph.link_asset_to_purpose("zoom", "video_calls")
graph.link_asset_to_purpose("office_conference_room", "video_calls")

# Exercise
graph.link_asset_to_purpose("yoga_mat", "exercise")
graph.link_asset_to_purpose("peloton_app", "exercise")
graph.link_asset_to_purpose("building_gym", "exercise")
```

### Step 5: Discover Overlap

```python
# Get purposes with multiple assets
overlapping = graph.get_overlapping_purposes()

for info in overlapping:
    purpose = info['purpose']
    assets = info['assets']
    print(f"\n{purpose.name}:")
    for asset in assets:
        print(f"  - {asset.name} ({asset.asset_type.value})")
```

Output:
```
Make Morning Coffee:
  - French Press (physical)
  - Espresso Machine (physical)

Stay Active:
  - Yoga Mat (physical)
  - Peloton App (digital)
  - Building Gym (shared)

Video Calls:
  - Zoom Account (digital)
  - Office Conference Rooms (shared)
```

## Interpreting Results

### Coverage Summary

```python
summary = graph.get_coverage_summary()
print(f"Total purposes: {summary['total_purposes']}")
print(f"Overlapping purposes: {summary['overlapping_purposes']}")
```

This tells you:
- How many purposes you've defined
- How many have multiple assets (overlap)
- How many have zero assets (gaps)

### Cross-Domain Overlap

This is especially valuable:

```python
cross_domain = graph.get_cross_domain_overlap()
```

Cross-domain overlap means a purpose is served by assets from different types (physical + digital, or digital + shared, etc.).

Example: "Stay Active" is served by:
- Physical: Yoga Mat
- Digital: Peloton App  
- Shared: Building Gym

This reveals that you have access through multiple channels, which might not be obvious when looking at your physical possessions alone.

### Consolidation Suggestions

```python
suggestions = graph.suggest_consolidation_opportunities()

for suggestion in suggestions:
    print(suggestion['suggestion'])
```

The system generates suggestions like:
- "Consider consolidating 2 physical assets serving 'Make Morning Coffee'"
- "Shared resources available for 'Stay Active' - consider if personal assets are needed"
- "Digital alternatives exist for physical assets serving 'Video Calls'"

**Remember**: These are reflection points, not prescriptions. You decide what makes sense.

## Real-World Scenarios

### Scenario 1: Moving to a Smaller Apartment

You're downsizing and need to decide what to bring.

```python
# Add both current assets and what's available at new place
graph.add_asset("my_printer", "My Printer", AssetType.PHYSICAL)
graph.add_asset("new_building_printer", "Building Office Printer", AssetType.SHARED)

graph.add_purpose("printing", "Print Documents")

graph.link_asset_to_purpose("my_printer", "printing")
graph.link_asset_to_purpose("new_building_printer", "printing")

# Check overlap
overlapping = graph.get_overlapping_purposes()
# Shows that printing is covered by both personal and shared
```

**Insight**: The shared printer at your new building might eliminate the need to move your personal printer.

### Scenario 2: Joining a Co-Living Space

Three roommates each have coffee makers:

```python
# Person A's assets
graph.add_asset("coffee_maker_a", "Coffee Maker (Person A)", AssetType.PHYSICAL,
               metadata={"owner": "Person A"})

# Person B's assets
graph.add_asset("espresso_b", "Espresso Machine (Person B)", AssetType.PHYSICAL,
               metadata={"owner": "Person B"})

# Person C's assets  
graph.add_asset("french_press_c", "French Press (Person C)", AssetType.PHYSICAL,
               metadata={"owner": "Person C"})

# Link all to coffee purpose
for asset_id in ["coffee_maker_a", "espresso_b", "french_press_c"]:
    graph.link_asset_to_purpose(asset_id, "coffee")

# Check collective overlap
assets = graph.get_assets_for_purpose("coffee")
print(f"{len(assets)} coffee makers for {len(assets)} people")
```

**Insight**: Makes collective redundancy visible so the group can discuss.

### Scenario 3: Transitioning to Remote Work

Map what was at the office vs. what you need at home:

```python
# What you had at office (shared)
graph.add_asset("office_desk", "Office Desk", AssetType.SHARED)
graph.add_asset("office_printer", "Office Printer", AssetType.SHARED)

# What you already have at home
graph.add_asset("dining_table", "Dining Table", AssetType.PHYSICAL)

# What you're considering buying
graph.add_asset("standing_desk", "Standing Desk (considering)", AssetType.PHYSICAL)
graph.add_asset("home_printer", "Home Printer (considering)", AssetType.PHYSICAL)

# Map to purposes
graph.add_purpose("workspace", "Ergonomic Workspace")
graph.add_purpose("printing", "Print Documents")

graph.link_asset_to_purpose("office_desk", "workspace")
graph.link_asset_to_purpose("dining_table", "workspace")
graph.link_asset_to_purpose("standing_desk", "workspace")

graph.link_asset_to_purpose("office_printer", "printing")
graph.link_asset_to_purpose("home_printer", "printing")
```

**Insight**: You already have the dining table for workspace. Try it before buying a standing desk. For printing, you might not print as often as you think.

## Interactive Mode

For a guided experience, use the CLI:

```bash
python cli.py interactive
```

Commands:
- `add-purpose` - Add a new purpose
- `add-asset` - Add a new asset
- `link` - Link an asset to a purpose
- `list-purposes` - See all purposes
- `list-assets` - See all assets
- `overlap` - View overlap report
- `suggestions` - Get consolidation suggestions
- `save` - Save to JSON file
- `load` - Load from JSON file
- `help` - Show all commands
- `quit` - Exit

## Saving and Loading

### Save Your Graph

```python
from cli import save_graph_to_json

save_graph_to_json(graph, "my_graph.json")
```

### Load a Graph

```python
from cli import load_graph_from_json

graph = load_graph_from_json("my_graph.json")
```

### Use Sample Data

Try the included sample:

```bash
python -c "
from cli import load_graph_from_json
graph = load_graph_from_json('sample_data.json')

overlap = graph.get_overlapping_purposes()
for info in overlap:
    print(f\"{info['purpose'].name}: {info['asset_count']} assets\")
"
```

## Tips for Effective Use

### 1. Start Small

Don't try to map everything at once. Start with:
- 3-5 purposes
- 5-10 assets
- Focus on one area of life (e.g., work, exercise, entertainment)

### 2. Frame Purposes Around Actions

Good purposes are action-oriented:
- ✓ "Participate in video calls"
- ✓ "Prepare healthy meals"
- ✗ "Have technology"
- ✗ "Be organized"

### 3. Include Shared and Digital Assets

Don't just list what you own. Include:
- What's available where you live (building gym, shared tools)
- Digital subscriptions and apps
- What's available at work or school

### 4. Use During Transitions

The graph is most valuable when you're:
- Moving
- Changing living situations
- Starting/stopping remote work
- Joining shared housing
- Decluttering

### 5. Treat Results as Reflection Points

The graph shows patterns. You decide:
- Which overlaps to keep (maybe you love both coffee makers)
- Which to consolidate (shared printer replaces personal)
- What gaps to fill (or leave unfilled)

## Next Steps

- Try `python cli.py examples` to see complete scenarios
- Run `python cli.py test` to see how it all works
- Build your own graph for an upcoming decision
- Share insights with roommates or family

Remember: This tool doesn't tell you what to do. It shows you what access you already have, so you can make intentional decisions.
