"""
Unit tests for the Purpose Graph System
"""

import unittest
from purpose_graph import PurposeGraph, Asset, Purpose, AssetType


class TestAsset(unittest.TestCase):
    """Test the Asset class."""
    
    def test_asset_creation(self):
        """Test creating an asset."""
        asset = Asset(
            id="test_asset",
            name="Test Asset",
            asset_type=AssetType.PHYSICAL,
            description="A test asset"
        )
        
        self.assertEqual(asset.id, "test_asset")
        self.assertEqual(asset.name, "Test Asset")
        self.assertEqual(asset.asset_type, AssetType.PHYSICAL)
        self.assertEqual(asset.description, "A test asset")
        self.assertEqual(len(asset.purposes), 0)
    
    def test_asset_add_purpose(self):
        """Test adding a purpose to an asset."""
        asset = Asset(id="test", name="Test", asset_type=AssetType.DIGITAL)
        asset.add_purpose("purpose1")
        asset.add_purpose("purpose2")
        
        self.assertEqual(len(asset.purposes), 2)
        self.assertIn("purpose1", asset.purposes)
        self.assertIn("purpose2", asset.purposes)
    
    def test_asset_remove_purpose(self):
        """Test removing a purpose from an asset."""
        asset = Asset(id="test", name="Test", asset_type=AssetType.SHARED)
        asset.add_purpose("purpose1")
        asset.add_purpose("purpose2")
        asset.remove_purpose("purpose1")
        
        self.assertEqual(len(asset.purposes), 1)
        self.assertNotIn("purpose1", asset.purposes)
        self.assertIn("purpose2", asset.purposes)


class TestPurpose(unittest.TestCase):
    """Test the Purpose class."""
    
    def test_purpose_creation(self):
        """Test creating a purpose."""
        purpose = Purpose(
            id="test_purpose",
            name="Test Purpose",
            description="A test purpose",
            category="test"
        )
        
        self.assertEqual(purpose.id, "test_purpose")
        self.assertEqual(purpose.name, "Test Purpose")
        self.assertEqual(purpose.description, "A test purpose")
        self.assertEqual(purpose.category, "test")


class TestPurposeGraph(unittest.TestCase):
    """Test the PurposeGraph class."""
    
    def setUp(self):
        """Set up a fresh graph for each test."""
        self.graph = PurposeGraph()
    
    # Asset Management Tests
    
    def test_add_asset(self):
        """Test adding an asset to the graph."""
        asset = self.graph.add_asset(
            "asset1", "Asset 1", AssetType.PHYSICAL, "Description"
        )
        
        self.assertEqual(asset.id, "asset1")
        self.assertEqual(asset.name, "Asset 1")
        self.assertEqual(len(self.graph.assets), 1)
    
    def test_add_duplicate_asset_raises_error(self):
        """Test that adding duplicate asset raises error."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        
        with self.assertRaises(ValueError):
            self.graph.add_asset("asset1", "Asset 1 Duplicate", AssetType.DIGITAL)
    
    def test_remove_asset(self):
        """Test removing an asset."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.remove_asset("asset1")
        
        self.assertEqual(len(self.graph.assets), 0)
    
    def test_remove_nonexistent_asset_raises_error(self):
        """Test that removing non-existent asset raises error."""
        with self.assertRaises(ValueError):
            self.graph.remove_asset("nonexistent")
    
    def test_get_asset(self):
        """Test getting an asset by ID."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        asset = self.graph.get_asset("asset1")
        
        self.assertIsNotNone(asset)
        self.assertEqual(asset.id, "asset1")
    
    def test_get_nonexistent_asset_returns_none(self):
        """Test that getting non-existent asset returns None."""
        asset = self.graph.get_asset("nonexistent")
        self.assertIsNone(asset)
    
    def test_get_all_assets(self):
        """Test getting all assets."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_asset("asset2", "Asset 2", AssetType.DIGITAL)
        
        assets = self.graph.get_all_assets()
        self.assertEqual(len(assets), 2)
    
    def test_get_assets_by_type(self):
        """Test filtering assets by type."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_asset("asset2", "Asset 2", AssetType.DIGITAL)
        self.graph.add_asset("asset3", "Asset 3", AssetType.PHYSICAL)
        
        physical = self.graph.get_assets_by_type(AssetType.PHYSICAL)
        digital = self.graph.get_assets_by_type(AssetType.DIGITAL)
        
        self.assertEqual(len(physical), 2)
        self.assertEqual(len(digital), 1)
    
    # Purpose Management Tests
    
    def test_add_purpose(self):
        """Test adding a purpose to the graph."""
        purpose = self.graph.add_purpose("purpose1", "Purpose 1", "Description")
        
        self.assertEqual(purpose.id, "purpose1")
        self.assertEqual(purpose.name, "Purpose 1")
        self.assertEqual(len(self.graph.purposes), 1)
    
    def test_add_duplicate_purpose_raises_error(self):
        """Test that adding duplicate purpose raises error."""
        self.graph.add_purpose("purpose1", "Purpose 1")
        
        with self.assertRaises(ValueError):
            self.graph.add_purpose("purpose1", "Purpose 1 Duplicate")
    
    def test_remove_purpose(self):
        """Test removing a purpose."""
        self.graph.add_purpose("purpose1", "Purpose 1")
        self.graph.remove_purpose("purpose1")
        
        self.assertEqual(len(self.graph.purposes), 0)
    
    def test_remove_nonexistent_purpose_raises_error(self):
        """Test that removing non-existent purpose raises error."""
        with self.assertRaises(ValueError):
            self.graph.remove_purpose("nonexistent")
    
    def test_get_purpose(self):
        """Test getting a purpose by ID."""
        self.graph.add_purpose("purpose1", "Purpose 1")
        purpose = self.graph.get_purpose("purpose1")
        
        self.assertIsNotNone(purpose)
        self.assertEqual(purpose.id, "purpose1")
    
    def test_get_all_purposes(self):
        """Test getting all purposes."""
        self.graph.add_purpose("purpose1", "Purpose 1")
        self.graph.add_purpose("purpose2", "Purpose 2")
        
        purposes = self.graph.get_all_purposes()
        self.assertEqual(len(purposes), 2)
    
    # Asset-Purpose Mapping Tests
    
    def test_link_asset_to_purpose(self):
        """Test linking an asset to a purpose."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_purpose("purpose1", "Purpose 1")
        
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        
        asset = self.graph.get_asset("asset1")
        self.assertIn("purpose1", asset.purposes)
    
    def test_link_nonexistent_asset_raises_error(self):
        """Test that linking non-existent asset raises error."""
        self.graph.add_purpose("purpose1", "Purpose 1")
        
        with self.assertRaises(ValueError):
            self.graph.link_asset_to_purpose("nonexistent", "purpose1")
    
    def test_link_to_nonexistent_purpose_raises_error(self):
        """Test that linking to non-existent purpose raises error."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        
        with self.assertRaises(ValueError):
            self.graph.link_asset_to_purpose("asset1", "nonexistent")
    
    def test_unlink_asset_from_purpose(self):
        """Test unlinking an asset from a purpose."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_purpose("purpose1", "Purpose 1")
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        
        self.graph.unlink_asset_from_purpose("asset1", "purpose1")
        
        asset = self.graph.get_asset("asset1")
        self.assertNotIn("purpose1", asset.purposes)
    
    def test_get_assets_for_purpose(self):
        """Test getting all assets serving a purpose."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_asset("asset2", "Asset 2", AssetType.DIGITAL)
        self.graph.add_purpose("purpose1", "Purpose 1")
        
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        self.graph.link_asset_to_purpose("asset2", "purpose1")
        
        assets = self.graph.get_assets_for_purpose("purpose1")
        self.assertEqual(len(assets), 2)
    
    def test_get_purposes_for_asset(self):
        """Test getting all purposes served by an asset."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_purpose("purpose1", "Purpose 1")
        self.graph.add_purpose("purpose2", "Purpose 2")
        
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        self.graph.link_asset_to_purpose("asset1", "purpose2")
        
        purposes = self.graph.get_purposes_for_asset("asset1")
        self.assertEqual(len(purposes), 2)
    
    # Overlap Detection Tests
    
    def test_detect_overlap(self):
        """Test detecting functional overlap."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_asset("asset2", "Asset 2", AssetType.DIGITAL)
        self.graph.add_purpose("purpose1", "Purpose 1")
        
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        self.graph.link_asset_to_purpose("asset2", "purpose1")
        
        overlap = self.graph.detect_overlap()
        
        self.assertIn("purpose1", overlap)
        self.assertTrue(overlap["purpose1"]["has_overlap"])
        self.assertEqual(overlap["purpose1"]["asset_count"], 2)
    
    def test_detect_no_overlap(self):
        """Test detecting when there's no overlap."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_purpose("purpose1", "Purpose 1")
        
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        
        overlap = self.graph.detect_overlap()
        
        self.assertIn("purpose1", overlap)
        self.assertFalse(overlap["purpose1"]["has_overlap"])
        self.assertEqual(overlap["purpose1"]["asset_count"], 1)
    
    def test_detect_cross_domain_overlap(self):
        """Test detecting cross-domain overlap."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_asset("asset2", "Asset 2", AssetType.DIGITAL)
        self.graph.add_purpose("purpose1", "Purpose 1")
        
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        self.graph.link_asset_to_purpose("asset2", "purpose1")
        
        overlap = self.graph.detect_overlap()
        
        self.assertTrue(overlap["purpose1"]["cross_domain"])
        self.assertEqual(len(overlap["purpose1"]["type_diversity"]), 2)
    
    def test_get_overlapping_purposes(self):
        """Test getting only purposes with overlap."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_asset("asset2", "Asset 2", AssetType.DIGITAL)
        self.graph.add_asset("asset3", "Asset 3", AssetType.SHARED)
        
        self.graph.add_purpose("purpose1", "Purpose 1")
        self.graph.add_purpose("purpose2", "Purpose 2")
        
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        self.graph.link_asset_to_purpose("asset2", "purpose1")
        self.graph.link_asset_to_purpose("asset3", "purpose2")
        
        overlapping = self.graph.get_overlapping_purposes()
        
        self.assertEqual(len(overlapping), 1)
        self.assertEqual(overlapping[0]["purpose"].id, "purpose1")
    
    def test_get_cross_domain_overlap(self):
        """Test getting purposes with cross-domain overlap."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_asset("asset2", "Asset 2", AssetType.DIGITAL)
        self.graph.add_asset("asset3", "Asset 3", AssetType.PHYSICAL)
        self.graph.add_asset("asset4", "Asset 4", AssetType.PHYSICAL)
        
        self.graph.add_purpose("purpose1", "Purpose 1")
        self.graph.add_purpose("purpose2", "Purpose 2")
        
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        self.graph.link_asset_to_purpose("asset2", "purpose1")
        self.graph.link_asset_to_purpose("asset3", "purpose2")
        self.graph.link_asset_to_purpose("asset4", "purpose2")
        
        cross_domain = self.graph.get_cross_domain_overlap()
        
        self.assertEqual(len(cross_domain), 1)
        self.assertEqual(cross_domain[0]["purpose"].id, "purpose1")
    
    def test_get_coverage_summary(self):
        """Test getting coverage summary."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_asset("asset2", "Asset 2", AssetType.DIGITAL)
        self.graph.add_asset("asset3", "Asset 3", AssetType.SHARED)
        
        self.graph.add_purpose("purpose1", "Purpose 1")
        self.graph.add_purpose("purpose2", "Purpose 2")
        
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        self.graph.link_asset_to_purpose("asset2", "purpose1")
        
        summary = self.graph.get_coverage_summary()
        
        self.assertEqual(summary["total_purposes"], 2)
        self.assertEqual(summary["covered_purposes"], 1)
        self.assertEqual(summary["uncovered_purposes"], 1)
        self.assertEqual(summary["overlapping_purposes"], 1)
        self.assertEqual(summary["total_assets"], 3)
        self.assertEqual(summary["physical_assets"], 1)
        self.assertEqual(summary["digital_assets"], 1)
        self.assertEqual(summary["shared_assets"], 1)
    
    def test_get_uncovered_purposes(self):
        """Test getting purposes with no assets."""
        self.graph.add_purpose("purpose1", "Purpose 1")
        self.graph.add_purpose("purpose2", "Purpose 2")
        
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        
        uncovered = self.graph.get_uncovered_purposes()
        
        self.assertEqual(len(uncovered), 1)
        self.assertEqual(uncovered[0].id, "purpose2")
    
    def test_suggest_consolidation_opportunities(self):
        """Test suggesting consolidation opportunities."""
        # Create same-type redundancy
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_asset("asset2", "Asset 2", AssetType.PHYSICAL)
        self.graph.add_purpose("purpose1", "Purpose 1")
        
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        self.graph.link_asset_to_purpose("asset2", "purpose1")
        
        suggestions = self.graph.suggest_consolidation_opportunities()
        
        self.assertGreater(len(suggestions), 0)
        self.assertEqual(suggestions[0]["type"], "same_type_redundancy")
    
    def test_suggest_digital_alternative(self):
        """Test suggesting digital alternative."""
        self.graph.add_asset("physical", "Physical Item", AssetType.PHYSICAL)
        self.graph.add_asset("digital", "Digital Item", AssetType.DIGITAL)
        self.graph.add_purpose("purpose1", "Purpose 1")
        
        self.graph.link_asset_to_purpose("physical", "purpose1")
        self.graph.link_asset_to_purpose("digital", "purpose1")
        
        suggestions = self.graph.suggest_consolidation_opportunities()
        
        digital_suggestions = [s for s in suggestions if s["type"] == "digital_alternative"]
        self.assertEqual(len(digital_suggestions), 1)
    
    def test_suggest_shared_alternative(self):
        """Test suggesting shared alternative."""
        self.graph.add_asset("personal", "Personal Item", AssetType.PHYSICAL)
        self.graph.add_asset("shared", "Shared Item", AssetType.SHARED)
        self.graph.add_purpose("purpose1", "Purpose 1")
        
        self.graph.link_asset_to_purpose("personal", "purpose1")
        self.graph.link_asset_to_purpose("shared", "purpose1")
        
        suggestions = self.graph.suggest_consolidation_opportunities()
        
        shared_suggestions = [s for s in suggestions if s["type"] == "shared_alternative"]
        self.assertEqual(len(shared_suggestions), 1)
    
    # Integration Tests
    
    def test_remove_asset_removes_from_purpose_mappings(self):
        """Test that removing an asset also removes it from purpose mappings."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_purpose("purpose1", "Purpose 1")
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        
        self.graph.remove_asset("asset1")
        
        assets = self.graph.get_assets_for_purpose("purpose1")
        self.assertEqual(len(assets), 0)
    
    def test_remove_purpose_removes_from_asset_mappings(self):
        """Test that removing a purpose also removes it from asset mappings."""
        self.graph.add_asset("asset1", "Asset 1", AssetType.PHYSICAL)
        self.graph.add_purpose("purpose1", "Purpose 1")
        self.graph.link_asset_to_purpose("asset1", "purpose1")
        
        self.graph.remove_purpose("purpose1")
        
        asset = self.graph.get_asset("asset1")
        self.assertNotIn("purpose1", asset.purposes)


if __name__ == "__main__":
    unittest.main()
