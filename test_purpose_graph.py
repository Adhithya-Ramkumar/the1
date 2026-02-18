#!/usr/bin/env python3
"""
Tests for the purpose graph system
"""

import unittest
import os
import tempfile
from purpose_graph import PurposeGraph, Asset, Purpose, AssetType


class TestAsset(unittest.TestCase):
    """Test Asset class"""
    
    def test_create_asset(self):
        asset = Asset("laptop", AssetType.PHYSICAL, "Work computer")
        self.assertEqual(asset.name, "laptop")
        self.assertEqual(asset.asset_type, AssetType.PHYSICAL)
        self.assertEqual(asset.description, "Work computer")
    
    def test_asset_to_dict(self):
        asset = Asset("phone", AssetType.DIGITAL, "Smartphone")
        data = asset.to_dict()
        self.assertEqual(data["name"], "phone")
        self.assertEqual(data["asset_type"], "digital")
        self.assertEqual(data["description"], "Smartphone")
    
    def test_asset_from_dict(self):
        data = {
            "name": "scanner",
            "asset_type": "physical",
            "description": "Document scanner"
        }
        asset = Asset.from_dict(data)
        self.assertEqual(asset.name, "scanner")
        self.assertEqual(asset.asset_type, AssetType.PHYSICAL)


class TestPurpose(unittest.TestCase):
    """Test Purpose class"""
    
    def test_create_purpose(self):
        purpose = Purpose("remote work", "Video calls and documents")
        self.assertEqual(purpose.name, "remote work")
        self.assertEqual(purpose.description, "Video calls and documents")
    
    def test_purpose_to_dict(self):
        purpose = Purpose("cooking", "Meal preparation")
        data = purpose.to_dict()
        self.assertEqual(data["name"], "cooking")
        self.assertEqual(data["description"], "Meal preparation")
    
    def test_purpose_from_dict(self):
        data = {"name": "fitness", "description": "Exercise"}
        purpose = Purpose.from_dict(data)
        self.assertEqual(purpose.name, "fitness")


class TestPurposeGraph(unittest.TestCase):
    """Test PurposeGraph class"""
    
    def setUp(self):
        self.graph = PurposeGraph()
    
    def test_add_asset(self):
        asset = Asset("laptop", AssetType.PHYSICAL)
        self.graph.add_asset(asset)
        self.assertIn("laptop", self.graph.assets)
        self.assertEqual(self.graph.assets["laptop"], asset)
    
    def test_remove_asset(self):
        asset = Asset("laptop", AssetType.PHYSICAL)
        self.graph.add_asset(asset)
        self.graph.remove_asset("laptop")
        self.assertNotIn("laptop", self.graph.assets)
    
    def test_add_purpose(self):
        purpose = Purpose("work")
        self.graph.add_purpose(purpose)
        self.assertIn("work", self.graph.purposes)
    
    def test_remove_purpose(self):
        purpose = Purpose("work")
        self.graph.add_purpose(purpose)
        self.graph.remove_purpose("work")
        self.assertNotIn("work", self.graph.purposes)
    
    def test_link_asset_to_purpose(self):
        asset = Asset("laptop", AssetType.PHYSICAL)
        purpose = Purpose("work")
        self.graph.add_asset(asset)
        self.graph.add_purpose(purpose)
        
        self.graph.link_asset_to_purpose("laptop", "work")
        
        self.assertIn("laptop", self.graph.purpose_to_assets["work"])
        self.assertIn("work", self.graph.asset_to_purposes["laptop"])
    
    def test_link_nonexistent_asset(self):
        purpose = Purpose("work")
        self.graph.add_purpose(purpose)
        
        with self.assertRaises(ValueError):
            self.graph.link_asset_to_purpose("nonexistent", "work")
    
    def test_link_nonexistent_purpose(self):
        asset = Asset("laptop", AssetType.PHYSICAL)
        self.graph.add_asset(asset)
        
        with self.assertRaises(ValueError):
            self.graph.link_asset_to_purpose("laptop", "nonexistent")
    
    def test_unlink_asset_from_purpose(self):
        asset = Asset("laptop", AssetType.PHYSICAL)
        purpose = Purpose("work")
        self.graph.add_asset(asset)
        self.graph.add_purpose(purpose)
        self.graph.link_asset_to_purpose("laptop", "work")
        
        self.graph.unlink_asset_from_purpose("laptop", "work")
        
        self.assertNotIn("laptop", self.graph.purpose_to_assets["work"])
        self.assertNotIn("work", self.graph.asset_to_purposes["laptop"])
    
    def test_get_assets_for_purpose(self):
        asset1 = Asset("laptop", AssetType.PHYSICAL)
        asset2 = Asset("phone", AssetType.DIGITAL)
        purpose = Purpose("work")
        
        self.graph.add_asset(asset1)
        self.graph.add_asset(asset2)
        self.graph.add_purpose(purpose)
        self.graph.link_asset_to_purpose("laptop", "work")
        self.graph.link_asset_to_purpose("phone", "work")
        
        assets = self.graph.get_assets_for_purpose("work")
        self.assertEqual(len(assets), 2)
        asset_names = [a.name for a in assets]
        self.assertIn("laptop", asset_names)
        self.assertIn("phone", asset_names)
    
    def test_get_purposes_for_asset(self):
        asset = Asset("laptop", AssetType.PHYSICAL)
        purpose1 = Purpose("work")
        purpose2 = Purpose("entertainment")
        
        self.graph.add_asset(asset)
        self.graph.add_purpose(purpose1)
        self.graph.add_purpose(purpose2)
        self.graph.link_asset_to_purpose("laptop", "work")
        self.graph.link_asset_to_purpose("laptop", "entertainment")
        
        purposes = self.graph.get_purposes_for_asset("laptop")
        self.assertEqual(len(purposes), 2)
        purpose_names = [p.name for p in purposes]
        self.assertIn("work", purpose_names)
        self.assertIn("entertainment", purpose_names)
    
    def test_find_overlapping_purposes(self):
        # Create assets
        laptop = Asset("laptop", AssetType.PHYSICAL)
        phone = Asset("phone", AssetType.DIGITAL)
        tablet = Asset("tablet", AssetType.PHYSICAL)
        
        # Create purposes
        work = Purpose("work")
        entertainment = Purpose("entertainment")
        
        # Add to graph
        self.graph.add_asset(laptop)
        self.graph.add_asset(phone)
        self.graph.add_asset(tablet)
        self.graph.add_purpose(work)
        self.graph.add_purpose(entertainment)
        
        # Link multiple assets to work (overlap)
        self.graph.link_asset_to_purpose("laptop", "work")
        self.graph.link_asset_to_purpose("phone", "work")
        self.graph.link_asset_to_purpose("tablet", "work")
        
        # Link single asset to entertainment (no overlap)
        self.graph.link_asset_to_purpose("tablet", "entertainment")
        
        overlaps = self.graph.find_overlapping_purposes()
        
        # Work should be in overlaps (3 assets)
        self.assertIn("work", overlaps)
        self.assertEqual(len(overlaps["work"]), 3)
        
        # Entertainment should not be in overlaps (only 1 asset)
        self.assertNotIn("entertainment", overlaps)
    
    def test_find_cross_domain_overlaps(self):
        # Create assets of different types
        laptop = Asset("laptop", AssetType.PHYSICAL)
        app = Asset("app", AssetType.DIGITAL)
        shared = Asset("shared-resource", AssetType.SHARED)
        
        # Create purpose
        work = Purpose("work")
        
        # Add to graph
        self.graph.add_asset(laptop)
        self.graph.add_asset(app)
        self.graph.add_asset(shared)
        self.graph.add_purpose(work)
        
        # Link all to work
        self.graph.link_asset_to_purpose("laptop", "work")
        self.graph.link_asset_to_purpose("app", "work")
        self.graph.link_asset_to_purpose("shared-resource", "work")
        
        cross_domain = self.graph.find_cross_domain_overlaps()
        
        # Should find cross-domain overlap for work
        self.assertIn("work", cross_domain)
        self.assertEqual(len(cross_domain["work"]), 3)  # 3 different types
        self.assertIn("physical", cross_domain["work"])
        self.assertIn("digital", cross_domain["work"])
        self.assertIn("shared", cross_domain["work"])
    
    def test_get_coverage_summary(self):
        # Create graph with known state
        asset1 = Asset("asset1", AssetType.PHYSICAL)
        asset2 = Asset("asset2", AssetType.DIGITAL)
        asset3 = Asset("asset3", AssetType.SHARED)
        
        purpose1 = Purpose("purpose1")  # Will have 2 assets
        purpose2 = Purpose("purpose2")  # Will have 1 asset
        purpose3 = Purpose("purpose3")  # Will have 0 assets
        
        self.graph.add_asset(asset1)
        self.graph.add_asset(asset2)
        self.graph.add_asset(asset3)
        self.graph.add_purpose(purpose1)
        self.graph.add_purpose(purpose2)
        self.graph.add_purpose(purpose3)
        
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        self.graph.link_asset_to_purpose("asset2", "purpose1")
        self.graph.link_asset_to_purpose("asset3", "purpose2")
        
        summary = self.graph.get_coverage_summary()
        
        self.assertEqual(summary["total_assets"], 3)
        self.assertEqual(summary["total_purposes"], 3)
        self.assertEqual(summary["purposes_with_no_assets"], 1)
        self.assertEqual(summary["purposes_with_single_asset"], 1)
        self.assertEqual(summary["purposes_with_multiple_assets"], 1)
        self.assertEqual(len(summary["overlapping_purposes"]), 1)
    
    def test_serialization(self):
        # Create a graph with data
        asset = Asset("laptop", AssetType.PHYSICAL, "Work computer")
        purpose = Purpose("work", "Remote work")
        
        self.graph.add_asset(asset)
        self.graph.add_purpose(purpose)
        self.graph.link_asset_to_purpose("laptop", "work")
        
        # Serialize
        data = self.graph.to_dict()
        
        # Deserialize
        new_graph = PurposeGraph.from_dict(data)
        
        # Verify
        self.assertIn("laptop", new_graph.assets)
        self.assertIn("work", new_graph.purposes)
        self.assertIn("laptop", new_graph.purpose_to_assets["work"])
    
    def test_save_and_load(self):
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # Create graph with data
            asset = Asset("laptop", AssetType.PHYSICAL, "Work computer")
            purpose = Purpose("work", "Remote work")
            
            self.graph.add_asset(asset)
            self.graph.add_purpose(purpose)
            self.graph.link_asset_to_purpose("laptop", "work")
            
            # Save
            self.graph.save_to_file(temp_file)
            
            # Load
            loaded_graph = PurposeGraph.load_from_file(temp_file)
            
            # Verify
            self.assertIn("laptop", loaded_graph.assets)
            self.assertIn("work", loaded_graph.purposes)
            self.assertIn("laptop", loaded_graph.purpose_to_assets["work"])
        
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_remove_asset_cleans_up_links(self):
        asset = Asset("laptop", AssetType.PHYSICAL)
        purpose = Purpose("work")
        
        self.graph.add_asset(asset)
        self.graph.add_purpose(purpose)
        self.graph.link_asset_to_purpose("laptop", "work")
        
        # Remove asset
        self.graph.remove_asset("laptop")
        
        # Verify links are cleaned up
        self.assertNotIn("laptop", self.graph.purpose_to_assets.get("work", set()))
        self.assertNotIn("laptop", self.graph.asset_to_purposes)
    
    def test_remove_purpose_cleans_up_links(self):
        asset = Asset("laptop", AssetType.PHYSICAL)
        purpose = Purpose("work")
        
        self.graph.add_asset(asset)
        self.graph.add_purpose(purpose)
        self.graph.link_asset_to_purpose("laptop", "work")
        
        # Remove purpose
        self.graph.remove_purpose("work")
        
        # Verify links are cleaned up
        self.assertNotIn("work", self.graph.asset_to_purposes.get("laptop", set()))
        self.assertNotIn("work", self.graph.purpose_to_assets)


if __name__ == "__main__":
    unittest.main()
