"""
Purpose Graph System

A lightweight system for mapping assets (physical objects, digital services, shared resources)
to the purposes they serve, making functional overlap visible without focusing on cost or ownership.
"""

from typing import Dict, Set, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json


class AssetType(Enum):
    """Types of assets that can be tracked"""
    PHYSICAL = "physical"
    DIGITAL = "digital"
    SHARED = "shared"
    SUBSCRIPTION = "subscription"


@dataclass
class Asset:
    """Represents an asset (object, service, or shared resource)"""
    name: str
    asset_type: AssetType
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert asset to dictionary for serialization"""
        return {
            "name": self.name,
            "asset_type": self.asset_type.value,
            "description": self.description,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Asset':
        """Create asset from dictionary"""
        return cls(
            name=data["name"],
            asset_type=AssetType(data["asset_type"]),
            description=data.get("description"),
            metadata=data.get("metadata", {})
        )


@dataclass
class Purpose:
    """Represents a purpose or function that assets can serve"""
    name: str
    description: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert purpose to dictionary for serialization"""
        return {
            "name": self.name,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Purpose':
        """Create purpose from dictionary"""
        return cls(
            name=data["name"],
            description=data.get("description")
        )


class PurposeGraph:
    """
    Core purpose graph that links assets to purposes and reveals functional overlap
    """
    
    def __init__(self):
        self.assets: Dict[str, Asset] = {}
        self.purposes: Dict[str, Purpose] = {}
        # Maps purpose name to set of asset names
        self.purpose_to_assets: Dict[str, Set[str]] = {}
        # Maps asset name to set of purpose names
        self.asset_to_purposes: Dict[str, Set[str]] = {}
    
    def add_asset(self, asset: Asset) -> None:
        """Add an asset to the graph"""
        self.assets[asset.name] = asset
        if asset.name not in self.asset_to_purposes:
            self.asset_to_purposes[asset.name] = set()
    
    def remove_asset(self, asset_name: str) -> None:
        """Remove an asset from the graph"""
        if asset_name in self.assets:
            # Remove from all purposes
            purposes = self.asset_to_purposes.get(asset_name, set()).copy()
            for purpose_name in purposes:
                self.unlink_asset_from_purpose(asset_name, purpose_name)
            
            del self.assets[asset_name]
            if asset_name in self.asset_to_purposes:
                del self.asset_to_purposes[asset_name]
    
    def add_purpose(self, purpose: Purpose) -> None:
        """Add a purpose to the graph"""
        self.purposes[purpose.name] = purpose
        if purpose.name not in self.purpose_to_assets:
            self.purpose_to_assets[purpose.name] = set()
    
    def remove_purpose(self, purpose_name: str) -> None:
        """Remove a purpose from the graph"""
        if purpose_name in self.purposes:
            # Remove from all assets
            assets = self.purpose_to_assets.get(purpose_name, set()).copy()
            for asset_name in assets:
                self.unlink_asset_from_purpose(asset_name, purpose_name)
            
            del self.purposes[purpose_name]
            if purpose_name in self.purpose_to_assets:
                del self.purpose_to_assets[purpose_name]
    
    def link_asset_to_purpose(self, asset_name: str, purpose_name: str) -> None:
        """Link an asset to a purpose"""
        if asset_name not in self.assets:
            raise ValueError(f"Asset '{asset_name}' does not exist")
        if purpose_name not in self.purposes:
            raise ValueError(f"Purpose '{purpose_name}' does not exist")
        
        self.purpose_to_assets[purpose_name].add(asset_name)
        self.asset_to_purposes[asset_name].add(purpose_name)
    
    def unlink_asset_from_purpose(self, asset_name: str, purpose_name: str) -> None:
        """Unlink an asset from a purpose"""
        if purpose_name in self.purpose_to_assets:
            self.purpose_to_assets[purpose_name].discard(asset_name)
        if asset_name in self.asset_to_purposes:
            self.asset_to_purposes[asset_name].discard(purpose_name)
    
    def get_assets_for_purpose(self, purpose_name: str) -> List[Asset]:
        """Get all assets linked to a purpose"""
        asset_names = self.purpose_to_assets.get(purpose_name, set())
        return [self.assets[name] for name in asset_names if name in self.assets]
    
    def get_purposes_for_asset(self, asset_name: str) -> List[Purpose]:
        """Get all purposes linked to an asset"""
        purpose_names = self.asset_to_purposes.get(asset_name, set())
        return [self.purposes[name] for name in purpose_names if name in self.purposes]
    
    def find_overlapping_purposes(self) -> Dict[str, List[Asset]]:
        """
        Find purposes that have multiple assets (functional overlap)
        Returns a dictionary mapping purpose names to lists of assets
        """
        overlaps = {}
        for purpose_name, asset_names in self.purpose_to_assets.items():
            if len(asset_names) > 1:
                overlaps[purpose_name] = self.get_assets_for_purpose(purpose_name)
        return overlaps
    
    def find_cross_domain_overlaps(self) -> Dict[str, Dict[str, List[Asset]]]:
        """
        Find overlaps that span different asset types (physical/digital/shared)
        Returns purposes with assets grouped by type
        """
        cross_domain = {}
        for purpose_name, asset_names in self.purpose_to_assets.items():
            if len(asset_names) > 1:
                assets_by_type = {}
                for asset_name in asset_names:
                    asset = self.assets[asset_name]
                    type_name = asset.asset_type.value
                    if type_name not in assets_by_type:
                        assets_by_type[type_name] = []
                    assets_by_type[type_name].append(asset)
                
                # Only include if we have assets from different types
                if len(assets_by_type) > 1:
                    cross_domain[purpose_name] = assets_by_type
        
        return cross_domain
    
    def get_coverage_summary(self) -> Dict[str, Any]:
        """
        Get a summary of purpose coverage showing which purposes
        have single vs multiple assets
        """
        summary = {
            "total_assets": len(self.assets),
            "total_purposes": len(self.purposes),
            "purposes_with_no_assets": 0,
            "purposes_with_single_asset": 0,
            "purposes_with_multiple_assets": 0,
            "average_assets_per_purpose": 0.0,
            "overlapping_purposes": []
        }
        
        asset_counts = []
        for purpose_name, asset_names in self.purpose_to_assets.items():
            count = len(asset_names)
            asset_counts.append(count)
            
            if count == 0:
                summary["purposes_with_no_assets"] += 1
            elif count == 1:
                summary["purposes_with_single_asset"] += 1
            else:
                summary["purposes_with_multiple_assets"] += 1
                summary["overlapping_purposes"].append({
                    "purpose": purpose_name,
                    "asset_count": count,
                    "assets": [self.assets[name].name for name in asset_names]
                })
        
        if asset_counts:
            summary["average_assets_per_purpose"] = sum(asset_counts) / len(asset_counts)
        
        return summary
    
    def to_dict(self) -> Dict:
        """Serialize the entire graph to a dictionary"""
        return {
            "assets": {name: asset.to_dict() for name, asset in self.assets.items()},
            "purposes": {name: purpose.to_dict() for name, purpose in self.purposes.items()},
            "links": {
                purpose_name: list(asset_names)
                for purpose_name, asset_names in self.purpose_to_assets.items()
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PurposeGraph':
        """Deserialize a graph from a dictionary"""
        graph = cls()
        
        # Load assets
        for asset_data in data.get("assets", {}).values():
            graph.add_asset(Asset.from_dict(asset_data))
        
        # Load purposes
        for purpose_data in data.get("purposes", {}).values():
            graph.add_purpose(Purpose.from_dict(purpose_data))
        
        # Load links
        for purpose_name, asset_names in data.get("links", {}).items():
            for asset_name in asset_names:
                try:
                    graph.link_asset_to_purpose(asset_name, purpose_name)
                except ValueError:
                    # Skip invalid links
                    pass
        
        return graph
    
    def save_to_file(self, filename: str) -> None:
        """Save the graph to a JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'PurposeGraph':
        """Load a graph from a JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
