"""
Command-line interface for the Purpose Graph System

Provides an interactive way to build and query purpose graphs.
"""

import argparse
import json
from purpose_graph import PurposeGraph, AssetType


def save_graph_to_json(graph: PurposeGraph, filename: str) -> None:
    """
    Save a purpose graph to JSON file.
    
    Args:
        graph: The PurposeGraph to save
        filename: Path to the output JSON file
    """
    data = {
        'assets': [
            {
                'id': asset.id,
                'name': asset.name,
                'asset_type': asset.asset_type.value,
                'description': asset.description,
                'purposes': list(asset.purposes),
                'metadata': asset.metadata
            }
            for asset in graph.get_all_assets()
        ],
        'purposes': [
            {
                'id': purpose.id,
                'name': purpose.name,
                'description': purpose.description,
                'category': purpose.category
            }
            for purpose in graph.get_all_purposes()
        ]
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Graph saved to {filename}")


def load_graph_from_json(filename: str) -> PurposeGraph:
    """
    Load a purpose graph from JSON file.
    
    Args:
        filename: Path to the input JSON file
        
    Returns:
        Loaded PurposeGraph
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    
    graph = PurposeGraph()
    
    # Load purposes first
    for purpose_data in data.get('purposes', []):
        graph.add_purpose(
            purpose_id=purpose_data['id'],
            name=purpose_data['name'],
            description=purpose_data.get('description', ''),
            category=purpose_data.get('category', '')
        )
    
    # Load assets
    for asset_data in data.get('assets', []):
        asset_type = AssetType(asset_data['asset_type'])
        asset = graph.add_asset(
            asset_id=asset_data['id'],
            name=asset_data['name'],
            asset_type=asset_type,
            description=asset_data.get('description', ''),
            metadata=asset_data.get('metadata', {})
        )
        
        # Link to purposes
        for purpose_id in asset_data.get('purposes', []):
            if purpose_id in graph.purposes:
                graph.link_asset_to_purpose(asset_data['id'], purpose_id)
    
    print(f"Graph loaded from {filename}")
    return graph


def print_overlap_report(graph: PurposeGraph) -> None:
    """Print a formatted overlap report."""
    print("\n" + "=" * 70)
    print("OVERLAP REPORT")
    print("=" * 70)
    
    summary = graph.get_coverage_summary()
    print("\nCoverage Summary:")
    print("-" * 70)
    print(f"  Total Purposes: {summary['total_purposes']}")
    print(f"  Covered: {summary['covered_purposes']}")
    print(f"  Uncovered: {summary['uncovered_purposes']}")
    print(f"  With Overlap: {summary['overlapping_purposes']}")
    print(f"  Cross-Domain: {summary['cross_domain_purposes']}")
    print(f"\n  Total Assets: {summary['total_assets']}")
    print(f"  Physical: {summary['physical_assets']}")
    print(f"  Digital: {summary['digital_assets']}")
    print(f"  Shared: {summary['shared_assets']}")
    
    overlapping = graph.get_overlapping_purposes()
    if overlapping:
        print("\n\nPurposes with Functional Overlap:")
        print("-" * 70)
        for info in overlapping:
            purpose = info['purpose']
            assets = info['assets']
            print(f"\n  {purpose.name} ({len(assets)} assets):")
            for asset in assets:
                print(f"    - {asset.name} ({asset.asset_type.value})")
    
    cross_domain = graph.get_cross_domain_overlap()
    if cross_domain:
        print("\n\nCross-Domain Overlap:")
        print("-" * 70)
        for info in cross_domain:
            purpose = info['purpose']
            types = info['type_diversity']
            print(f"  {purpose.name}: {', '.join(t.value for t in types)}")
    
    uncovered = graph.get_uncovered_purposes()
    if uncovered:
        print("\n\nUncovered Purposes:")
        print("-" * 70)
        for purpose in uncovered:
            print(f"  - {purpose.name}")
    
    print("\n" + "=" * 70)


def print_suggestions(graph: PurposeGraph) -> None:
    """Print consolidation suggestions."""
    suggestions = graph.suggest_consolidation_opportunities()
    
    if not suggestions:
        print("\nNo consolidation suggestions at this time.")
        return
    
    print("\n" + "=" * 70)
    print("CONSOLIDATION SUGGESTIONS")
    print("=" * 70)
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n{i}. {suggestion['suggestion']}")
        
        if suggestion['type'] == 'same_type_redundancy':
            print(f"   Assets: {', '.join(suggestion['assets'])}")
        elif suggestion['type'] == 'digital_alternative':
            print(f"   Physical: {', '.join(suggestion['physical_assets'])}")
            print(f"   Digital: {', '.join(suggestion['digital_assets'])}")
        elif suggestion['type'] == 'shared_alternative':
            print(f"   Shared: {', '.join(suggestion['shared_assets'])}")
            print(f"   Personal: {', '.join(suggestion['personal_assets'])}")
    
    print("\n" + "=" * 70)


def interactive_mode():
    """Run interactive mode for building a purpose graph."""
    print("\n" + "=" * 70)
    print("Purpose Graph System - Interactive Mode")
    print("=" * 70)
    print("\nBuild your purpose graph step by step.")
    print("Type 'help' for commands or 'quit' to exit.\n")
    
    graph = PurposeGraph()
    
    commands = {
        'help': 'Show available commands',
        'add-purpose': 'Add a new purpose',
        'add-asset': 'Add a new asset',
        'link': 'Link an asset to a purpose',
        'list-purposes': 'List all purposes',
        'list-assets': 'List all assets',
        'overlap': 'Show overlap report',
        'suggestions': 'Show consolidation suggestions',
        'save': 'Save graph to JSON file',
        'load': 'Load graph from JSON file',
        'quit': 'Exit interactive mode'
    }
    
    while True:
        try:
            cmd = input("\n> ").strip().lower()
            
            if cmd == 'quit' or cmd == 'exit':
                print("Goodbye!")
                break
            
            elif cmd == 'help':
                print("\nAvailable commands:")
                for cmd_name, description in commands.items():
                    print(f"  {cmd_name:20} - {description}")
            
            elif cmd == 'add-purpose':
                purpose_id = input("  Purpose ID: ").strip()
                name = input("  Name: ").strip()
                description = input("  Description (optional): ").strip()
                category = input("  Category (optional): ").strip()
                
                try:
                    graph.add_purpose(purpose_id, name, description, category)
                    print(f"  ✓ Added purpose '{name}'")
                except ValueError as e:
                    print(f"  ✗ Error: {e}")
            
            elif cmd == 'add-asset':
                asset_id = input("  Asset ID: ").strip()
                name = input("  Name: ").strip()
                print("  Asset Type:")
                print("    1. Physical")
                print("    2. Digital")
                print("    3. Shared")
                type_choice = input("  Choice (1-3): ").strip()
                
                type_map = {'1': AssetType.PHYSICAL, '2': AssetType.DIGITAL, '3': AssetType.SHARED}
                if type_choice not in type_map:
                    print("  ✗ Invalid choice")
                    continue
                
                asset_type = type_map[type_choice]
                description = input("  Description (optional): ").strip()
                
                try:
                    graph.add_asset(asset_id, name, asset_type, description)
                    print(f"  ✓ Added asset '{name}' ({asset_type.value})")
                except ValueError as e:
                    print(f"  ✗ Error: {e}")
            
            elif cmd == 'link':
                asset_id = input("  Asset ID: ").strip()
                purpose_id = input("  Purpose ID: ").strip()
                
                try:
                    graph.link_asset_to_purpose(asset_id, purpose_id)
                    print(f"  ✓ Linked asset to purpose")
                except ValueError as e:
                    print(f"  ✗ Error: {e}")
            
            elif cmd == 'list-purposes':
                purposes = graph.get_all_purposes()
                if not purposes:
                    print("  No purposes defined yet.")
                else:
                    print(f"\n  {len(purposes)} purpose(s):")
                    for p in purposes:
                        print(f"    - {p.id}: {p.name}")
            
            elif cmd == 'list-assets':
                assets = graph.get_all_assets()
                if not assets:
                    print("  No assets defined yet.")
                else:
                    print(f"\n  {len(assets)} asset(s):")
                    for a in assets:
                        purposes_str = f" → {len(a.purposes)} purpose(s)" if a.purposes else ""
                        print(f"    - {a.id}: {a.name} ({a.asset_type.value}){purposes_str}")
            
            elif cmd == 'overlap':
                print_overlap_report(graph)
            
            elif cmd == 'suggestions':
                print_suggestions(graph)
            
            elif cmd == 'save':
                filename = input("  Filename: ").strip()
                if not filename.endswith('.json'):
                    filename += '.json'
                save_graph_to_json(graph, filename)
            
            elif cmd == 'load':
                filename = input("  Filename: ").strip()
                try:
                    graph = load_graph_from_json(filename)
                except Exception as e:
                    print(f"  ✗ Error loading file: {e}")
            
            elif cmd:
                print(f"  Unknown command: '{cmd}'. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Purpose Graph System - Link assets to purposes and detect overlap'
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        choices=['interactive', 'examples', 'test'],
        help='Command to run'
    )
    
    parser.add_argument(
        '--load',
        type=str,
        help='Load graph from JSON file'
    )
    
    parser.add_argument(
        '--save',
        type=str,
        help='Save graph to JSON file'
    )
    
    args = parser.parse_args()
    
    if args.command == 'interactive':
        interactive_mode()
    
    elif args.command == 'examples':
        import examples
        # examples.py runs when imported
    
    elif args.command == 'test':
        import subprocess
        subprocess.run(['python', '-m', 'unittest', 'test_purpose_graph.py', '-v'])
    
    else:
        # Default: show help
        parser.print_help()
        print("\nQuick start:")
        print("  python cli.py interactive   - Start interactive mode")
        print("  python cli.py examples      - Run example scenarios")
        print("  python cli.py test          - Run test suite")


if __name__ == "__main__":
    main()
