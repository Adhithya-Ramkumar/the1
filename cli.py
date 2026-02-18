#!/usr/bin/env python3
"""
Purpose Graph CLI

A command-line interface for managing assets, purposes, and discovering functional overlaps.
"""

import argparse
import sys
import os
from typing import Optional
from purpose_graph import PurposeGraph, Asset, Purpose, AssetType


class PurposeGraphCLI:
    """CLI for the purpose graph system"""
    
    def __init__(self, data_file: str = "purpose_graph.json"):
        self.data_file = data_file
        self.graph = self._load_graph()
    
    def _load_graph(self) -> PurposeGraph:
        """Load the graph from file or create a new one"""
        if os.path.exists(self.data_file):
            try:
                return PurposeGraph.load_from_file(self.data_file)
            except Exception as e:
                print(f"Warning: Could not load {self.data_file}: {e}")
                print("Starting with a new graph.")
        return PurposeGraph()
    
    def _save_graph(self) -> None:
        """Save the graph to file"""
        try:
            self.graph.save_to_file(self.data_file)
            print(f"✓ Saved to {self.data_file}")
        except Exception as e:
            print(f"Error saving graph: {e}", file=sys.stderr)
    
    def add_asset(self, name: str, asset_type: str, description: Optional[str] = None) -> None:
        """Add a new asset"""
        try:
            asset_type_enum = AssetType(asset_type.lower())
            asset = Asset(name=name, asset_type=asset_type_enum, description=description)
            self.graph.add_asset(asset)
            print(f"✓ Added {asset_type} asset: {name}")
            self._save_graph()
        except ValueError as e:
            print(f"Error: Invalid asset type '{asset_type}'. "
                  f"Must be one of: {', '.join([t.value for t in AssetType])}", file=sys.stderr)
    
    def remove_asset(self, name: str) -> None:
        """Remove an asset"""
        if name not in self.graph.assets:
            print(f"Error: Asset '{name}' not found", file=sys.stderr)
            return
        self.graph.remove_asset(name)
        print(f"✓ Removed asset: {name}")
        self._save_graph()
    
    def list_assets(self, asset_type: Optional[str] = None) -> None:
        """List all assets or filter by type"""
        assets = list(self.graph.assets.values())
        
        if asset_type:
            try:
                type_enum = AssetType(asset_type.lower())
                assets = [a for a in assets if a.asset_type == type_enum]
            except ValueError:
                print(f"Error: Invalid asset type '{asset_type}'", file=sys.stderr)
                return
        
        if not assets:
            print("No assets found.")
            return
        
        print(f"\n{'Asset':<30} {'Type':<15} {'Purposes':<20} {'Description':<40}")
        print("-" * 105)
        
        for asset in sorted(assets, key=lambda a: a.name):
            purposes = self.graph.get_purposes_for_asset(asset.name)
            purpose_names = ", ".join([p.name for p in purposes]) if purposes else "none"
            desc = asset.description or ""
            print(f"{asset.name:<30} {asset.asset_type.value:<15} {purpose_names:<20} {desc:<40}")
    
    def add_purpose(self, name: str, description: Optional[str] = None) -> None:
        """Add a new purpose"""
        purpose = Purpose(name=name, description=description)
        self.graph.add_purpose(purpose)
        print(f"✓ Added purpose: {name}")
        self._save_graph()
    
    def remove_purpose(self, name: str) -> None:
        """Remove a purpose"""
        if name not in self.graph.purposes:
            print(f"Error: Purpose '{name}' not found", file=sys.stderr)
            return
        self.graph.remove_purpose(name)
        print(f"✓ Removed purpose: {name}")
        self._save_graph()
    
    def list_purposes(self) -> None:
        """List all purposes"""
        if not self.graph.purposes:
            print("No purposes defined.")
            return
        
        print(f"\n{'Purpose':<30} {'Assets':<10} {'Description':<50}")
        print("-" * 90)
        
        for purpose in sorted(self.graph.purposes.values(), key=lambda p: p.name):
            assets = self.graph.get_assets_for_purpose(purpose.name)
            asset_count = len(assets)
            desc = purpose.description or ""
            print(f"{purpose.name:<30} {asset_count:<10} {desc:<50}")
    
    def link(self, asset_name: str, purpose_name: str) -> None:
        """Link an asset to a purpose"""
        try:
            self.graph.link_asset_to_purpose(asset_name, purpose_name)
            print(f"✓ Linked '{asset_name}' to '{purpose_name}'")
            self._save_graph()
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
    
    def unlink(self, asset_name: str, purpose_name: str) -> None:
        """Unlink an asset from a purpose"""
        self.graph.unlink_asset_from_purpose(asset_name, purpose_name)
        print(f"✓ Unlinked '{asset_name}' from '{purpose_name}'")
        self._save_graph()
    
    def show_overlaps(self) -> None:
        """Show purposes with functional overlap"""
        overlaps = self.graph.find_overlapping_purposes()
        
        if not overlaps:
            print("\nNo functional overlaps detected.")
            print("All purposes are served by at most one asset.")
            return
        
        print("\n" + "=" * 80)
        print("FUNCTIONAL OVERLAPS DETECTED")
        print("=" * 80)
        print("\nThe following purposes are served by multiple assets:\n")
        
        for purpose_name, assets in sorted(overlaps.items()):
            print(f"\n📋 Purpose: {purpose_name}")
            purpose = self.graph.purposes[purpose_name]
            if purpose.description:
                print(f"   Description: {purpose.description}")
            print(f"   Covered by {len(assets)} assets:")
            
            for asset in sorted(assets, key=lambda a: a.name):
                print(f"     • {asset.name} ({asset.asset_type.value})")
                if asset.description:
                    print(f"       {asset.description}")
    
    def show_cross_domain_overlaps(self) -> None:
        """Show overlaps that span different asset types"""
        cross_domain = self.graph.find_cross_domain_overlaps()
        
        if not cross_domain:
            print("\nNo cross-domain overlaps detected.")
            return
        
        print("\n" + "=" * 80)
        print("CROSS-DOMAIN OVERLAPS")
        print("=" * 80)
        print("\nPurposes served by different types of assets:\n")
        
        for purpose_name, assets_by_type in sorted(cross_domain.items()):
            print(f"\n📋 Purpose: {purpose_name}")
            purpose = self.graph.purposes[purpose_name]
            if purpose.description:
                print(f"   Description: {purpose.description}")
            print(f"   Served across {len(assets_by_type)} domains:")
            
            for asset_type, assets in sorted(assets_by_type.items()):
                print(f"\n   {asset_type.upper()}:")
                for asset in sorted(assets, key=lambda a: a.name):
                    print(f"     • {asset.name}")
    
    def show_summary(self) -> None:
        """Show a summary of the purpose graph"""
        summary = self.graph.get_coverage_summary()
        
        print("\n" + "=" * 80)
        print("PURPOSE GRAPH SUMMARY")
        print("=" * 80)
        
        print(f"\nTotal Assets: {summary['total_assets']}")
        print(f"Total Purposes: {summary['total_purposes']}")
        
        if summary['total_purposes'] > 0:
            print(f"\nPurpose Coverage:")
            print(f"  • No assets: {summary['purposes_with_no_assets']}")
            print(f"  • Single asset: {summary['purposes_with_single_asset']}")
            print(f"  • Multiple assets (overlap): {summary['purposes_with_multiple_assets']}")
            print(f"  • Average assets per purpose: {summary['average_assets_per_purpose']:.2f}")
        
        if summary['overlapping_purposes']:
            print(f"\nOverlapping Purposes:")
            for overlap in summary['overlapping_purposes']:
                print(f"  • {overlap['purpose']}: {overlap['asset_count']} assets")


def main():
    parser = argparse.ArgumentParser(
        description="Purpose Graph - Map assets to purposes and discover functional overlaps"
    )
    parser.add_argument(
        "--file", "-f",
        default="purpose_graph.json",
        help="Data file to use (default: purpose_graph.json)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Asset commands
    add_asset_parser = subparsers.add_parser("add-asset", help="Add a new asset")
    add_asset_parser.add_argument("name", help="Asset name")
    add_asset_parser.add_argument("type", help="Asset type (physical/digital/shared/subscription)")
    add_asset_parser.add_argument("--description", "-d", help="Asset description")
    
    remove_asset_parser = subparsers.add_parser("remove-asset", help="Remove an asset")
    remove_asset_parser.add_argument("name", help="Asset name")
    
    list_assets_parser = subparsers.add_parser("list-assets", help="List all assets")
    list_assets_parser.add_argument("--type", "-t", help="Filter by asset type")
    
    # Purpose commands
    add_purpose_parser = subparsers.add_parser("add-purpose", help="Add a new purpose")
    add_purpose_parser.add_argument("name", help="Purpose name")
    add_purpose_parser.add_argument("--description", "-d", help="Purpose description")
    
    remove_purpose_parser = subparsers.add_parser("remove-purpose", help="Remove a purpose")
    remove_purpose_parser.add_argument("name", help="Purpose name")
    
    subparsers.add_parser("list-purposes", help="List all purposes")
    
    # Link commands
    link_parser = subparsers.add_parser("link", help="Link an asset to a purpose")
    link_parser.add_argument("asset", help="Asset name")
    link_parser.add_argument("purpose", help="Purpose name")
    
    unlink_parser = subparsers.add_parser("unlink", help="Unlink an asset from a purpose")
    unlink_parser.add_argument("asset", help="Asset name")
    unlink_parser.add_argument("purpose", help="Purpose name")
    
    # Analysis commands
    subparsers.add_parser("show-overlaps", help="Show functional overlaps")
    subparsers.add_parser("show-cross-domain", help="Show cross-domain overlaps")
    subparsers.add_parser("summary", help="Show summary statistics")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = PurposeGraphCLI(args.file)
    
    # Execute commands
    if args.command == "add-asset":
        cli.add_asset(args.name, args.type, args.description)
    elif args.command == "remove-asset":
        cli.remove_asset(args.name)
    elif args.command == "list-assets":
        cli.list_assets(args.type)
    elif args.command == "add-purpose":
        cli.add_purpose(args.name, args.description)
    elif args.command == "remove-purpose":
        cli.remove_purpose(args.name)
    elif args.command == "list-purposes":
        cli.list_purposes()
    elif args.command == "link":
        cli.link(args.asset, args.purpose)
    elif args.command == "unlink":
        cli.unlink(args.asset, args.purpose)
    elif args.command == "show-overlaps":
        cli.show_overlaps()
    elif args.command == "show-cross-domain":
        cli.show_cross_domain_overlaps()
    elif args.command == "summary":
        cli.show_summary()


if __name__ == "__main__":
    main()
