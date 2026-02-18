#!/usr/bin/env python3
"""
Example usage scenarios for the purpose graph system
"""

from purpose_graph import PurposeGraph, Asset, Purpose, AssetType


def example_relocation_scenario():
    """
    Example: Person moving to a new shared housing situation
    Demonstrates discovering overlap before relocating
    """
    print("\n" + "=" * 80)
    print("EXAMPLE: Relocation to Shared Housing")
    print("=" * 80)
    print("\nScenario: Moving to a co-living space with shared amenities")
    print("Question: What can I leave behind?\n")
    
    graph = PurposeGraph()
    
    # Define purposes
    purposes = [
        Purpose("remote work", "Video calls, document editing, presentations"),
        Purpose("cooking basic meals", "Preparing breakfast, lunch, and dinner"),
        Purpose("entertainment", "Movies, music, reading"),
        Purpose("document scanning", "Digitizing papers and receipts"),
        Purpose("physical fitness", "Exercise and staying active")
    ]
    
    for purpose in purposes:
        graph.add_purpose(purpose)
    
    # Personal assets (what the person currently owns)
    personal_assets = [
        Asset("laptop", AssetType.PHYSICAL, "Personal work computer"),
        Asset("office-365", AssetType.SUBSCRIPTION, "Cloud productivity suite"),
        Asset("scanner", AssetType.PHYSICAL, "Flatbed document scanner"),
        Asset("adobe-scan-app", AssetType.DIGITAL, "Phone scanning app"),
        Asset("microwave", AssetType.PHYSICAL, "Personal microwave"),
        Asset("netflix", AssetType.SUBSCRIPTION, "Streaming service"),
        Asset("yoga-mat", AssetType.PHYSICAL, "Personal exercise mat"),
        Asset("dumbbells", AssetType.PHYSICAL, "10lb weights"),
    ]
    
    # Shared resources available at new location
    shared_assets = [
        Asset("shared-printer-scanner", AssetType.SHARED, "Multi-function printer in common area"),
        Asset("shared-kitchen", AssetType.SHARED, "Full kitchen with appliances"),
        Asset("shared-gym", AssetType.SHARED, "Building gym with equipment"),
        Asset("house-netflix", AssetType.SHARED, "Shared Netflix account"),
    ]
    
    for asset in personal_assets + shared_assets:
        graph.add_asset(asset)
    
    # Link assets to purposes
    # Remote work
    graph.link_asset_to_purpose("laptop", "remote work")
    graph.link_asset_to_purpose("office-365", "remote work")
    
    # Document scanning
    graph.link_asset_to_purpose("scanner", "document scanning")
    graph.link_asset_to_purpose("adobe-scan-app", "document scanning")
    graph.link_asset_to_purpose("shared-printer-scanner", "document scanning")
    
    # Cooking
    graph.link_asset_to_purpose("microwave", "cooking basic meals")
    graph.link_asset_to_purpose("shared-kitchen", "cooking basic meals")
    
    # Entertainment
    graph.link_asset_to_purpose("netflix", "entertainment")
    graph.link_asset_to_purpose("house-netflix", "entertainment")
    
    # Fitness
    graph.link_asset_to_purpose("yoga-mat", "physical fitness")
    graph.link_asset_to_purpose("dumbbells", "physical fitness")
    graph.link_asset_to_purpose("shared-gym", "physical fitness")
    
    # Show analysis
    print("\n📊 OVERLAP ANALYSIS\n")
    
    overlaps = graph.find_overlapping_purposes()
    for purpose_name, assets in overlaps.items():
        print(f"Purpose: {purpose_name}")
        print(f"  Covered by {len(assets)} assets:")
        for asset in assets:
            coverage_type = "SHARED" if asset.asset_type == AssetType.SHARED else "PERSONAL"
            print(f"    [{coverage_type}] {asset.name} ({asset.asset_type.value})")
        print()
    
    print("\n💡 INSIGHTS FOR RELOCATION:\n")
    print("• Document scanning: Already covered by shared printer and phone app")
    print("  → Consider leaving personal scanner behind")
    print()
    print("• Cooking: Shared kitchen provides full coverage")
    print("  → Can leave personal microwave behind")
    print()
    print("• Entertainment: Netflix available through house account")
    print("  → Can cancel personal subscription during stay")
    print()
    print("• Fitness: Shared gym available, but yoga mat is portable/personal")
    print("  → Keep yoga mat, consider leaving dumbbells if gym has weights")
    
    return graph


def example_work_mode_transition():
    """
    Example: Transitioning from office to remote work
    """
    print("\n" + "=" * 80)
    print("EXAMPLE: Office to Remote Work Transition")
    print("=" * 80)
    print("\nScenario: Company switching to permanent remote work")
    print("Question: What office equipment is now redundant?\n")
    
    graph = PurposeGraph()
    
    # Define purposes
    purposes = [
        Purpose("video conferencing", "Team meetings and client calls"),
        Purpose("file storage", "Storing and sharing work documents"),
        Purpose("task management", "Tracking projects and deadlines"),
    ]
    
    for purpose in purposes:
        graph.add_purpose(purpose)
    
    # Assets
    assets = [
        Asset("office-desk-phone", AssetType.PHYSICAL, "VoIP desk phone at office"),
        Asset("zoom-subscription", AssetType.SUBSCRIPTION, "Video meeting platform"),
        Asset("office-network-drive", AssetType.SHARED, "Company file server at office"),
        Asset("google-drive", AssetType.DIGITAL, "Cloud storage"),
        Asset("dropbox", AssetType.SUBSCRIPTION, "Personal cloud storage"),
        Asset("trello-board", AssetType.DIGITAL, "Personal task board"),
        Asset("company-jira", AssetType.SHARED, "Company project management"),
    ]
    
    for asset in assets:
        graph.add_asset(asset)
    
    # Links
    graph.link_asset_to_purpose("office-desk-phone", "video conferencing")
    graph.link_asset_to_purpose("zoom-subscription", "video conferencing")
    
    graph.link_asset_to_purpose("office-network-drive", "file storage")
    graph.link_asset_to_purpose("google-drive", "file storage")
    graph.link_asset_to_purpose("dropbox", "file storage")
    
    graph.link_asset_to_purpose("trello-board", "task management")
    graph.link_asset_to_purpose("company-jira", "task management")
    
    # Analysis
    cross_domain = graph.find_cross_domain_overlaps()
    
    print("\n🔄 CROSS-DOMAIN OVERLAP ANALYSIS\n")
    
    for purpose_name, assets_by_type in cross_domain.items():
        print(f"Purpose: {purpose_name}")
        for asset_type, assets in assets_by_type.items():
            print(f"  {asset_type}:")
            for asset in assets:
                print(f"    • {asset.name}")
        print()
    
    print("\n💡 INSIGHTS FOR WORK MODE TRANSITION:\n")
    print("• Video conferencing: Zoom covers remote needs, office phone now redundant")
    print()
    print("• File storage: Multiple solutions (office drive, 2 cloud services)")
    print("  → Consider consolidating to company-preferred cloud solution")
    print()
    print("• Task management: Personal Trello + company Jira may cause fragmentation")
    print("  → Evaluate if one system can serve both needs")
    
    return graph


def example_minimal_living():
    """
    Example: Evaluating possessions for minimal living
    """
    print("\n" + "=" * 80)
    print("EXAMPLE: Minimal Living Assessment")
    print("=" * 80)
    print("\nScenario: Reducing possessions for a more intentional lifestyle")
    print("Question: Where do I have redundancy?\n")
    
    graph = PurposeGraph()
    
    # Purposes
    purposes = [
        Purpose("music listening", "Enjoying music at home and on the go"),
        Purpose("reading", "Books, articles, and news"),
        Purpose("timekeeping", "Knowing what time it is"),
    ]
    
    for purpose in purposes:
        graph.add_purpose(purpose)
    
    # Assets showing common redundancies
    assets = [
        Asset("bluetooth-speaker", AssetType.PHYSICAL, "Portable speaker"),
        Asset("home-stereo", AssetType.PHYSICAL, "Home audio system"),
        Asset("phone-speakers", AssetType.PHYSICAL, "Built-in phone speakers"),
        Asset("spotify", AssetType.SUBSCRIPTION, "Music streaming"),
        Asset("physical-books", AssetType.PHYSICAL, "Book collection"),
        Asset("kindle", AssetType.PHYSICAL, "E-reader device"),
        Asset("kindle-app", AssetType.DIGITAL, "Reading app on phone"),
        Asset("wristwatch", AssetType.PHYSICAL, "Analog watch"),
        Asset("phone-clock", AssetType.DIGITAL, "Phone clock app"),
        Asset("wall-clock", AssetType.PHYSICAL, "Kitchen wall clock"),
    ]
    
    for asset in assets:
        graph.add_asset(asset)
    
    # Links
    graph.link_asset_to_purpose("bluetooth-speaker", "music listening")
    graph.link_asset_to_purpose("home-stereo", "music listening")
    graph.link_asset_to_purpose("phone-speakers", "music listening")
    graph.link_asset_to_purpose("spotify", "music listening")
    
    graph.link_asset_to_purpose("physical-books", "reading")
    graph.link_asset_to_purpose("kindle", "reading")
    graph.link_asset_to_purpose("kindle-app", "reading")
    
    graph.link_asset_to_purpose("wristwatch", "timekeeping")
    graph.link_asset_to_purpose("phone-clock", "timekeeping")
    graph.link_asset_to_purpose("wall-clock", "timekeeping")
    
    # Analysis
    summary = graph.get_coverage_summary()
    
    print(f"\n📊 COVERAGE SUMMARY\n")
    print(f"Total assets tracked: {summary['total_assets']}")
    print(f"Average assets per purpose: {summary['average_assets_per_purpose']:.1f}")
    print(f"\nAll {summary['total_purposes']} purposes have multiple assets (overlap)")
    
    print("\n🔍 DETAILED OVERLAP:\n")
    overlaps = graph.find_overlapping_purposes()
    for purpose_name, assets in overlaps.items():
        print(f"{purpose_name}: {len(assets)} ways to accomplish this")
        for asset in assets:
            print(f"  • {asset.name}")
        print()
    
    print("💡 REFLECTION POINTS:\n")
    print("• Music listening: 4 playback options - which contexts truly need separate devices?")
    print("• Reading: 3 formats - does digital access reduce need for physical books?")
    print("• Timekeeping: 3 clocks - phone already always present, others optional?")
    print("\nThis is information, not prescription. The graph reveals patterns for")
    print("intentional decision-making about what serves you best.")
    
    return graph


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("PURPOSE GRAPH EXAMPLES")
    print("=" * 80)
    print("\nThese examples demonstrate how the purpose graph reveals functional")
    print("overlap during moments of transition and reflection.\n")
    
    # Run examples
    example_relocation_scenario()
    print("\n" + "=" * 80 + "\n")
    
    example_work_mode_transition()
    print("\n" + "=" * 80 + "\n")
    
    example_minimal_living()
    print("\n" + "=" * 80 + "\n")
    
    print("\nThese examples show how the purpose graph:")
    print("  • Makes overlap visible across physical, digital, and shared assets")
    print("  • Supports decisions during transitions (moving, work changes, lifestyle shifts)")
    print("  • Focuses on function and access rather than cost or ownership")
    print("  • Provides information for intentional choices without prescribing actions")
    print()


if __name__ == "__main__":
    main()
