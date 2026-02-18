# Quick Start Guide

## Installation

No installation needed! Just Python 3.7+

## Try It Now

### 1. Run the Examples

See the purpose graph in action with pre-built scenarios:

```bash
python3 examples.py
```

This shows three real-world scenarios:
- Moving to shared housing
- Transitioning to remote work
- Minimal living assessment

### 2. Create Your Own Graph

Start tracking your own assets and purposes:

```bash
# Add a purpose
python3 cli.py add-purpose "remote work" --description "Video calls and docs"

# Add some assets
python3 cli.py add-asset laptop physical --description "Work computer"
python3 cli.py add-asset zoom subscription --description "Video platform"
python3 cli.py add-asset "office-phone" physical --description "Desk phone"

# Link them
python3 cli.py link laptop "remote work"
python3 cli.py link zoom "remote work"
python3 cli.py link office-phone "remote work"

# See the overlap
python3 cli.py show-overlaps
```

### 3. Run Tests

Verify everything works:

```bash
python3 test_purpose_graph.py
```

## Common Use Cases

### Moving to Shared Housing

```bash
# Create purposes for daily needs
python3 cli.py add-purpose "cooking"
python3 cli.py add-purpose "document scanning"
python3 cli.py add-purpose "entertainment"

# Add your personal items
python3 cli.py add-asset microwave physical
python3 cli.py add-asset scanner physical
python3 cli.py add-asset netflix subscription

# Add shared resources at new place
python3 cli.py add-asset "shared-kitchen" shared
python3 cli.py add-asset "shared-printer" shared
python3 cli.py add-asset "house-netflix" shared

# Link everything
python3 cli.py link microwave cooking
python3 cli.py link "shared-kitchen" cooking
python3 cli.py link scanner "document scanning"
python3 cli.py link "shared-printer" "document scanning"
python3 cli.py link netflix entertainment
python3 cli.py link "house-netflix" entertainment

# Analyze what you can leave behind
python3 cli.py show-overlaps
```

### Work Mode Change

```bash
# Track work-related purposes
python3 cli.py add-purpose "video calls"
python3 cli.py add-purpose "file storage"

# Add office and remote tools
python3 cli.py add-asset "desk-phone" physical
python3 cli.py add-asset zoom subscription
python3 cli.py add-asset "office-drive" shared
python3 cli.py add-asset dropbox subscription

# Link them
python3 cli.py link "desk-phone" "video calls"
python3 cli.py link zoom "video calls"
python3 cli.py link "office-drive" "file storage"
python3 cli.py link dropbox "file storage"

# See cross-domain overlaps
python3 cli.py show-cross-domain
```

## Tips

1. **Start small** - Focus on one area (work, kitchen, entertainment)
2. **Tag loosely** - Don't overthink categories
3. **Use during transitions** - Moving, changing jobs, joining communities
4. **Review overlaps** - Let the graph show you patterns
5. **Make your own decisions** - The graph informs, doesn't prescribe

## Commands Reference

```bash
# Asset management
python3 cli.py add-asset <name> <type> [--description TEXT]
python3 cli.py remove-asset <name>
python3 cli.py list-assets [--type TYPE]

# Purpose management
python3 cli.py add-purpose <name> [--description TEXT]
python3 cli.py remove-purpose <name>
python3 cli.py list-purposes

# Linking
python3 cli.py link <asset> <purpose>
python3 cli.py unlink <asset> <purpose>

# Analysis
python3 cli.py show-overlaps
python3 cli.py show-cross-domain
python3 cli.py summary

# Use custom data file
python3 cli.py --file my_graph.json <command>
```

## Next Steps

Read the full [README.md](README.md) for:
- Python API documentation
- Design philosophy
- Advanced use cases
- Contributing guidelines
