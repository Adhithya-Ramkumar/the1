"""
Purpose Graph System

A lightweight system for linking assets (physical objects, subscriptions, and shared tools)
to the functions they serve in daily life. Surfaces functional overlap across different
domains to support intentional decision-making.
"""

from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class AssetType(Enum):
    """Types of assets that can be tracked in the purpose graph."""
    PHYSICAL = "physical"
    DIGITAL = "digital"
    SHARED = "shared"


@dataclass
class Asset:
    """
    Represents an asset that serves one or more purposes.
    
    Attributes:
        id: Unique identifier for the asset
        name: Human-readable name
        asset_type: Type of asset (physical, digital, or shared)
        description: Optional detailed description
        purposes: Set of purpose IDs this asset serves
        metadata: Additional flexible metadata
    """
    id: str
    name: str
    asset_type: AssetType
    description: str = ""
    purposes: Set[str] = field(default_factory=set)
    metadata: Dict[str, str] = field(default_factory=dict)
    
    def add_purpose(self, purpose_id: str) -> None:
        """Add a purpose to this asset."""
        self.purposes.add(purpose_id)
    
    def remove_purpose(self, purpose_id: str) -> None:
        """Remove a purpose from this asset."""
        self.purposes.discard(purpose_id)


@dataclass
class Purpose:
    """
    Represents a functional purpose or need.
    
    Attributes:
        id: Unique identifier for the purpose
        name: Human-readable name (e.g., "remote work", "cooking basic meals")
        description: Optional detailed description
        category: Optional category for grouping purposes
    """
    id: str
    name: str
    description: str = ""
    category: str = ""


class PurposeGraph:
    """
    The main purpose graph system that manages assets, purposes, and their relationships.
    
    This system allows users to:
    - Add and manage assets (physical, digital, shared)
    - Define purposes that assets serve
    - Link assets to purposes
    - Detect functional overlap where multiple assets serve the same purpose
    - Query the graph for insights
    """
    
    def __init__(self):
        self.assets: Dict[str, Asset] = {}
        self.purposes: Dict[str, Purpose] = {}
        self._purpose_to_assets: Dict[str, Set[str]] = defaultdict(set)
    
    # Asset Management
    
    def add_asset(self, asset_id: str, name: str, asset_type: AssetType,
                  description: str = "", metadata: Optional[Dict[str, str]] = None) -> Asset:
        """
        Add a new asset to the graph.
        
        Args:
            asset_id: Unique identifier for the asset
            name: Human-readable name
            asset_type: Type of asset (physical, digital, or shared)
            description: Optional description
            metadata: Optional additional metadata
            
        Returns:
            The created Asset object
        """
        if asset_id in self.assets:
            raise ValueError(f"Asset with id '{asset_id}' already exists")
        
        asset = Asset(
            id=asset_id,
            name=name,
            asset_type=asset_type,
            description=description,
            metadata=metadata or {}
        )
        self.assets[asset_id] = asset
        return asset
    
    def remove_asset(self, asset_id: str) -> None:
        """Remove an asset from the graph."""
        if asset_id not in self.assets:
            raise ValueError(f"Asset with id '{asset_id}' not found")
        
        asset = self.assets[asset_id]
        # Remove from all purpose mappings
        for purpose_id in asset.purposes:
            self._purpose_to_assets[purpose_id].discard(asset_id)
        
        del self.assets[asset_id]
    
    def get_asset(self, asset_id: str) -> Optional[Asset]:
        """Get an asset by ID."""
        return self.assets.get(asset_id)
    
    def get_all_assets(self) -> List[Asset]:
        """Get all assets in the graph."""
        return list(self.assets.values())
    
    def get_assets_by_type(self, asset_type: AssetType) -> List[Asset]:
        """Get all assets of a specific type."""
        return [a for a in self.assets.values() if a.asset_type == asset_type]
    
    # Purpose Management
    
    def add_purpose(self, purpose_id: str, name: str,
                    description: str = "", category: str = "") -> Purpose:
        """
        Add a new purpose to the graph.
        
        Args:
            purpose_id: Unique identifier for the purpose
            name: Human-readable name (e.g., "remote work", "entertainment")
            description: Optional description
            category: Optional category for grouping
            
        Returns:
            The created Purpose object
        """
        if purpose_id in self.purposes:
            raise ValueError(f"Purpose with id '{purpose_id}' already exists")
        
        purpose = Purpose(
            id=purpose_id,
            name=name,
            description=description,
            category=category
        )
        self.purposes[purpose_id] = purpose
        return purpose
    
    def remove_purpose(self, purpose_id: str) -> None:
        """Remove a purpose from the graph."""
        if purpose_id not in self.purposes:
            raise ValueError(f"Purpose with id '{purpose_id}' not found")
        
        # Remove from all assets
        for asset_id in self._purpose_to_assets[purpose_id]:
            if asset_id in self.assets:
                self.assets[asset_id].remove_purpose(purpose_id)
        
        del self._purpose_to_assets[purpose_id]
        del self.purposes[purpose_id]
    
    def get_purpose(self, purpose_id: str) -> Optional[Purpose]:
        """Get a purpose by ID."""
        return self.purposes.get(purpose_id)
    
    def get_all_purposes(self) -> List[Purpose]:
        """Get all purposes in the graph."""
        return list(self.purposes.values())
    
    # Asset-Purpose Mapping
    
    def link_asset_to_purpose(self, asset_id: str, purpose_id: str) -> None:
        """
        Link an asset to a purpose it serves.
        
        Args:
            asset_id: ID of the asset
            purpose_id: ID of the purpose
        """
        if asset_id not in self.assets:
            raise ValueError(f"Asset with id '{asset_id}' not found")
        if purpose_id not in self.purposes:
            raise ValueError(f"Purpose with id '{purpose_id}' not found")
        
        self.assets[asset_id].add_purpose(purpose_id)
        self._purpose_to_assets[purpose_id].add(asset_id)
    
    def unlink_asset_from_purpose(self, asset_id: str, purpose_id: str) -> None:
        """
        Unlink an asset from a purpose.
        
        Args:
            asset_id: ID of the asset
            purpose_id: ID of the purpose
        """
        if asset_id in self.assets:
            self.assets[asset_id].remove_purpose(purpose_id)
        
        if purpose_id in self._purpose_to_assets:
            self._purpose_to_assets[purpose_id].discard(asset_id)
    
    def get_assets_for_purpose(self, purpose_id: str) -> List[Asset]:
        """
        Get all assets that serve a specific purpose.
        
        Args:
            purpose_id: ID of the purpose
            
        Returns:
            List of assets serving this purpose
        """
        asset_ids = self._purpose_to_assets.get(purpose_id, set())
        return [self.assets[aid] for aid in asset_ids if aid in self.assets]
    
    def get_purposes_for_asset(self, asset_id: str) -> List[Purpose]:
        """
        Get all purposes served by a specific asset.
        
        Args:
            asset_id: ID of the asset
            
        Returns:
            List of purposes this asset serves
        """
        if asset_id not in self.assets:
            return []
        
        purpose_ids = self.assets[asset_id].purposes
        return [self.purposes[pid] for pid in purpose_ids if pid in self.purposes]
    
    # Overlap Detection
    
    def detect_overlap(self) -> Dict[str, Dict]:
        """
        Detect functional overlap across all purposes.
        
        Returns:
            Dictionary mapping purpose IDs to overlap information, including:
            - purpose: Purpose object
            - asset_count: Number of assets serving this purpose
            - assets: List of assets
            - has_overlap: Boolean indicating if multiple assets serve this purpose
            - type_diversity: Asset types involved (shows cross-domain overlap)
        """
        overlap = {}
        
        for purpose_id, purpose in self.purposes.items():
            assets = self.get_assets_for_purpose(purpose_id)
            asset_types = set(a.asset_type for a in assets)
            
            overlap[purpose_id] = {
                'purpose': purpose,
                'asset_count': len(assets),
                'assets': assets,
                'has_overlap': len(assets) > 1,
                'type_diversity': list(asset_types),
                'cross_domain': len(asset_types) > 1
            }
        
        return overlap
    
    def get_overlapping_purposes(self) -> List[Dict]:
        """
        Get only purposes that have functional overlap (multiple assets).
        
        Returns:
            List of purposes with overlap information, sorted by asset count (descending)
        """
        overlap = self.detect_overlap()
        overlapping = [
            info for info in overlap.values()
            if info['has_overlap']
        ]
        return sorted(overlapping, key=lambda x: x['asset_count'], reverse=True)
    
    def get_cross_domain_overlap(self) -> List[Dict]:
        """
        Get purposes served by assets across different domains (physical, digital, shared).
        This is particularly valuable as it shows redundancy that might not be obvious.
        
        Returns:
            List of purposes with cross-domain overlap
        """
        overlap = self.detect_overlap()
        cross_domain = [
            info for info in overlap.values()
            if info['cross_domain']
        ]
        return sorted(cross_domain, key=lambda x: x['asset_count'], reverse=True)
    
    def get_coverage_summary(self) -> Dict:
        """
        Get a summary of purpose coverage.
        
        Returns:
            Dictionary with summary statistics
        """
        overlap = self.detect_overlap()
        
        total_purposes = len(self.purposes)
        covered_purposes = sum(1 for info in overlap.values() if info['asset_count'] > 0)
        overlapping_purposes = sum(1 for info in overlap.values() if info['has_overlap'])
        cross_domain_purposes = sum(1 for info in overlap.values() if info['cross_domain'])
        
        total_assets = len(self.assets)
        physical_assets = len(self.get_assets_by_type(AssetType.PHYSICAL))
        digital_assets = len(self.get_assets_by_type(AssetType.DIGITAL))
        shared_assets = len(self.get_assets_by_type(AssetType.SHARED))
        
        return {
            'total_purposes': total_purposes,
            'covered_purposes': covered_purposes,
            'uncovered_purposes': total_purposes - covered_purposes,
            'overlapping_purposes': overlapping_purposes,
            'cross_domain_purposes': cross_domain_purposes,
            'total_assets': total_assets,
            'physical_assets': physical_assets,
            'digital_assets': digital_assets,
            'shared_assets': shared_assets,
        }
    
    # Utility Methods
    
    def get_uncovered_purposes(self) -> List[Purpose]:
        """Get purposes that have no assets assigned to them."""
        return [
            purpose for purpose_id, purpose in self.purposes.items()
            if len(self._purpose_to_assets.get(purpose_id, set())) == 0
        ]
    
    def suggest_consolidation_opportunities(self) -> List[Dict]:
        """
        Suggest consolidation opportunities based on overlap patterns.
        
        Returns:
            List of suggestions with reasoning
        """
        suggestions = []
        overlapping = self.get_overlapping_purposes()
        
        for info in overlapping:
            purpose = info['purpose']
            assets = info['assets']
            
            # Check for same-type redundancy
            type_groups = defaultdict(list)
            for asset in assets:
                type_groups[asset.asset_type].append(asset)
            
            for asset_type, type_assets in type_groups.items():
                if len(type_assets) > 1:
                    suggestions.append({
                        'type': 'same_type_redundancy',
                        'purpose': purpose.name,
                        'asset_type': asset_type.value,
                        'count': len(type_assets),
                        'assets': [a.name for a in type_assets],
                        'suggestion': f"Consider consolidating {len(type_assets)} {asset_type.value} assets serving '{purpose.name}'"
                    })
            
            # Check for digital alternatives to physical
            physical = [a for a in assets if a.asset_type == AssetType.PHYSICAL]
            digital = [a for a in assets if a.asset_type == AssetType.DIGITAL]
            
            if physical and digital:
                suggestions.append({
                    'type': 'digital_alternative',
                    'purpose': purpose.name,
                    'physical_assets': [a.name for a in physical],
                    'digital_assets': [a.name for a in digital],
                    'suggestion': f"Digital alternatives exist for physical assets serving '{purpose.name}'"
                })
            
            # Check for shared alternatives
            shared = [a for a in assets if a.asset_type == AssetType.SHARED]
            personal = [a for a in assets if a.asset_type != AssetType.SHARED]
            
            if shared and personal:
                suggestions.append({
                    'type': 'shared_alternative',
                    'purpose': purpose.name,
                    'shared_assets': [a.name for a in shared],
                    'personal_assets': [a.name for a in personal],
                    'suggestion': f"Shared resources available for '{purpose.name}' - consider if personal assets are needed"
                })
        
        return suggestions
