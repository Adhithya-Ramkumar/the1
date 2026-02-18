"""
Example usage scenarios for the Purpose Graph System

This file demonstrates practical use cases for the purpose graph,
particularly in transition scenarios like moving, co-living, and
changing work modes.
"""

from purpose_graph import PurposeGraph, AssetType


def example_moving_scenario():
    """
    Example: Someone moving to a new apartment and deciding what to bring.
    """
    print("=" * 60)
    print("SCENARIO: Moving to a New Apartment")
    print("=" * 60)
    print()
    
    graph = PurposeGraph()
    
    # Define purposes
    graph.add_purpose("remote_work", "Remote Work", 
                     "Ability to work from home effectively")
    graph.add_purpose("document_scanning", "Document Scanning",
                     "Digitize paper documents")
    graph.add_purpose("entertainment", "Entertainment",
                     "Watch movies, shows, listen to music")
    graph.add_purpose("cooking_basic", "Basic Cooking",
                     "Prepare simple meals")
    graph.add_purpose("exercise", "Exercise",
                     "Stay physically active")
    
    # Add existing assets (things they already own)
    graph.add_asset("laptop", "Personal Laptop", AssetType.PHYSICAL,
                   "MacBook Pro for work and personal use")
    graph.add_asset("desktop_pc", "Desktop PC", AssetType.PHYSICAL,
                   "Gaming/work desktop computer")
    graph.add_asset("scanner", "Physical Scanner", AssetType.PHYSICAL,
                   "HP Document Scanner")
    graph.add_asset("scanner_app", "Scanner App", AssetType.DIGITAL,
                   "Adobe Scan mobile app")
    graph.add_asset("tv", "Smart TV", AssetType.PHYSICAL,
                   "55-inch Samsung Smart TV")
    graph.add_asset("netflix", "Netflix Subscription", AssetType.DIGITAL,
                   "Streaming service")
    graph.add_asset("spotify", "Spotify Subscription", AssetType.DIGITAL,
                   "Music streaming service")
    graph.add_asset("cookware_set", "Complete Cookware Set", AssetType.PHYSICAL,
                   "Pots, pans, utensils")
    graph.add_asset("yoga_mat", "Yoga Mat", AssetType.PHYSICAL,
                   "Personal yoga mat")
    graph.add_asset("gym_membership", "Gym Membership", AssetType.DIGITAL,
                   "Local gym subscription")
    
    # Add assets available at new location (shared resources)
    graph.add_asset("shared_printer", "Shared Office Printer", AssetType.SHARED,
                   "Multi-function printer in apartment building office")
    graph.add_asset("community_gym", "Building Gym", AssetType.SHARED,
                   "Fitness center in apartment building")
    graph.add_asset("shared_kitchen", "Common Kitchen", AssetType.SHARED,
                   "Shared kitchen with basic cookware")
    
    # Link assets to purposes
    graph.link_asset_to_purpose("laptop", "remote_work")
    graph.link_asset_to_purpose("desktop_pc", "remote_work")
    graph.link_asset_to_purpose("desktop_pc", "entertainment")
    
    graph.link_asset_to_purpose("scanner", "document_scanning")
    graph.link_asset_to_purpose("scanner_app", "document_scanning")
    graph.link_asset_to_purpose("shared_printer", "document_scanning")
    
    graph.link_asset_to_purpose("tv", "entertainment")
    graph.link_asset_to_purpose("netflix", "entertainment")
    graph.link_asset_to_purpose("spotify", "entertainment")
    
    graph.link_asset_to_purpose("cookware_set", "cooking_basic")
    graph.link_asset_to_purpose("shared_kitchen", "cooking_basic")
    
    graph.link_asset_to_purpose("yoga_mat", "exercise")
    graph.link_asset_to_purpose("gym_membership", "exercise")
    graph.link_asset_to_purpose("community_gym", "exercise")
    
    # Analyze overlap
    print("Coverage Summary:")
    print("-" * 60)
    summary = graph.get_coverage_summary()
    for key, value in summary.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    print()
    
    print("Functional Overlap Detected:")
    print("-" * 60)
    overlapping = graph.get_overlapping_purposes()
    for info in overlapping:
        purpose = info['purpose']
        assets = info['assets']
        print(f"\n  {purpose.name}:")
        print(f"    {len(assets)} assets serving this purpose:")
        for asset in assets:
            print(f"      - {asset.name} ({asset.asset_type.value})")
    print()
    
    print("Cross-Domain Overlap (Physical + Digital + Shared):")
    print("-" * 60)
    cross_domain = graph.get_cross_domain_overlap()
    for info in cross_domain:
        purpose = info['purpose']
        types = info['type_diversity']
        print(f"  {purpose.name}: {len(types)} different asset types")
    print()
    
    print("Consolidation Suggestions:")
    print("-" * 60)
    suggestions = graph.suggest_consolidation_opportunities()
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n  {i}. {suggestion['suggestion']}")
        if suggestion['type'] == 'shared_alternative':
            print(f"     Shared: {', '.join(suggestion['shared_assets'])}")
            print(f"     Personal: {', '.join(suggestion['personal_assets'])}")
        elif suggestion['type'] == 'digital_alternative':
            print(f"     Physical: {', '.join(suggestion['physical_assets'])}")
            print(f"     Digital: {', '.join(suggestion['digital_assets'])}")
    
    print("\n" + "=" * 60)
    print("Decision Support:")
    print("=" * 60)
    print("""
Based on the overlap analysis:

1. Document Scanning: The shared printer and scanner app can replace
   the physical scanner, saving space during the move.

2. Exercise: The building gym provides an alternative to both the gym
   membership and could supplement the yoga mat for varied workouts.

3. Remote Work: Both laptop and desktop serve this purpose. Consider
   if both are needed in a smaller space.

4. Cooking: Shared kitchen provides basic cookware. Could bring only
   specialized items not available there.

These are reflection points, not prescriptions. The graph surfaces
connections to support intentional decisions.
    """)
    
    return graph


def example_co_living_scenario():
    """
    Example: Group of people moving into a co-living space together.
    """
    print("\n" + "=" * 60)
    print("SCENARIO: Co-Living Space with 3 Roommates")
    print("=" * 60)
    print()
    
    graph = PurposeGraph()
    
    # Define shared purposes
    purposes = [
        ("coffee_making", "Coffee Making", "Make coffee in the morning"),
        ("cleaning", "Cleaning", "Keep living space clean"),
        ("cooking_advanced", "Advanced Cooking", "Cook complex meals"),
        ("entertainment_group", "Group Entertainment", "Watch content together"),
        ("internet_access", "Internet Access", "Access to internet"),
    ]
    
    for purpose_id, name, desc in purposes:
        graph.add_purpose(purpose_id, name, desc)
    
    # Person A's assets
    graph.add_asset("coffee_maker_a", "Coffee Maker (Person A)", AssetType.PHYSICAL,
                   metadata={"owner": "Person A"})
    graph.add_asset("vacuum_a", "Vacuum Cleaner (Person A)", AssetType.PHYSICAL,
                   metadata={"owner": "Person A"})
    
    # Person B's assets
    graph.add_asset("espresso_machine_b", "Espresso Machine (Person B)", AssetType.PHYSICAL,
                   metadata={"owner": "Person B"})
    graph.add_asset("cleaning_service_b", "Cleaning Service (Person B)", AssetType.DIGITAL,
                   metadata={"owner": "Person B"})
    graph.add_asset("stand_mixer_b", "Stand Mixer (Person B)", AssetType.PHYSICAL,
                   metadata={"owner": "Person B"})
    
    # Person C's assets
    graph.add_asset("french_press_c", "French Press (Person C)", AssetType.PHYSICAL,
                   metadata={"owner": "Person C"})
    graph.add_asset("food_processor_c", "Food Processor (Person C)", AssetType.PHYSICAL,
                   metadata={"owner": "Person C"})
    graph.add_asset("netflix_c", "Netflix (Person C)", AssetType.DIGITAL,
                   metadata={"owner": "Person C"})
    graph.add_asset("wifi_router_c", "WiFi Router (Person C)", AssetType.PHYSICAL,
                   metadata={"owner": "Person C"})
    
    # Shared/building resources
    graph.add_asset("building_wifi", "Building WiFi", AssetType.SHARED,
                   "Free WiFi provided by building")
    
    # Map to purposes
    graph.link_asset_to_purpose("coffee_maker_a", "coffee_making")
    graph.link_asset_to_purpose("espresso_machine_b", "coffee_making")
    graph.link_asset_to_purpose("french_press_c", "coffee_making")
    
    graph.link_asset_to_purpose("vacuum_a", "cleaning")
    graph.link_asset_to_purpose("cleaning_service_b", "cleaning")
    
    graph.link_asset_to_purpose("stand_mixer_b", "cooking_advanced")
    graph.link_asset_to_purpose("food_processor_c", "cooking_advanced")
    
    graph.link_asset_to_purpose("netflix_c", "entertainment_group")
    
    graph.link_asset_to_purpose("wifi_router_c", "internet_access")
    graph.link_asset_to_purpose("building_wifi", "internet_access")
    
    print("Collective Overlap Analysis:")
    print("-" * 60)
    
    overlapping = graph.get_overlapping_purposes()
    for info in overlapping:
        purpose = info['purpose']
        assets = info['assets']
        print(f"\n  {purpose.name} - {len(assets)} assets:")
        
        owners = {}
        for asset in assets:
            owner = asset.metadata.get('owner', 'Shared')
            if owner not in owners:
                owners[owner] = []
            owners[owner].append(asset.name)
        
        for owner, asset_names in owners.items():
            for name in asset_names:
                print(f"    [{owner}] {name}")
    
    print("\n" + "=" * 60)
    print("Group Coordination Insights:")
    print("=" * 60)
    print("""
The purpose graph reveals collective redundancy:

1. Coffee Making: Three different coffee makers for 3 people.
   Each person could keep their preferred method, or the group
   could coordinate to have variety while reducing total items.

2. Cleaning: Both a vacuum and a cleaning service. The group
   could decide if both are needed or coordinate usage.

3. Internet: Both personal router and building WiFi available.
   Could test building WiFi quality before bringing router.

This doesn't enforce coordination, but makes collective overlap
visible for the group to discuss and decide together.
    """)
    
    return graph


def example_work_transition_scenario():
    """
    Example: Transitioning from office work to remote work.
    """
    print("\n" + "=" * 60)
    print("SCENARIO: Transitioning from Office to Remote Work")
    print("=" * 60)
    print()
    
    graph = PurposeGraph()
    
    # Purposes
    graph.add_purpose("video_calls", "Video Calls", "Professional video conferencing")
    graph.add_purpose("focus_work", "Focused Work", "Distraction-free work environment")
    graph.add_purpose("file_storage", "File Storage", "Store and access work files")
    graph.add_purpose("printing", "Printing", "Print documents as needed")
    graph.add_purpose("ergonomic_setup", "Ergonomic Setup", "Comfortable work posture")
    
    # Previously relied on office resources (shared)
    graph.add_asset("office_conference_rooms", "Office Conference Rooms", AssetType.SHARED,
                   "Previously available at office")
    graph.add_asset("office_printer", "Office Printer", AssetType.SHARED,
                   "Previously available at office")
    graph.add_asset("office_desk", "Office Desk & Chair", AssetType.SHARED,
                   "Previously available at office")
    graph.add_asset("office_network_drive", "Office Network Drive", AssetType.SHARED,
                   "Previously available at office")
    
    # New assets being considered
    graph.add_asset("webcam", "External Webcam", AssetType.PHYSICAL,
                   "HD webcam for better video quality")
    graph.add_asset("zoom_account", "Zoom Pro Account", AssetType.DIGITAL,
                   "Video conferencing subscription")
    graph.add_asset("noise_canceling_headphones", "Noise-Canceling Headphones", 
                   AssetType.PHYSICAL, "For focus and calls")
    graph.add_asset("cloud_storage", "Cloud Storage", AssetType.DIGITAL,
                   "Google Drive / Dropbox subscription")
    graph.add_asset("home_printer", "Home Printer", AssetType.PHYSICAL,
                   "All-in-one printer for home")
    graph.add_asset("print_service", "Online Print Service", AssetType.DIGITAL,
                   "Print and deliver service")
    graph.add_asset("standing_desk", "Standing Desk", AssetType.PHYSICAL,
                   "Adjustable height desk")
    graph.add_asset("ergonomic_chair", "Ergonomic Chair", AssetType.PHYSICAL,
                   "Office chair for home")
    
    # Existing assets at home
    graph.add_asset("laptop_builtin_cam", "Laptop Built-in Camera", AssetType.PHYSICAL,
                   "Already have this")
    graph.add_asset("dining_table", "Dining Table", AssetType.PHYSICAL,
                   "Could use as workspace")
    
    # Map purposes
    graph.link_asset_to_purpose("office_conference_rooms", "video_calls")
    graph.link_asset_to_purpose("webcam", "video_calls")
    graph.link_asset_to_purpose("zoom_account", "video_calls")
    graph.link_asset_to_purpose("laptop_builtin_cam", "video_calls")
    
    graph.link_asset_to_purpose("noise_canceling_headphones", "focus_work")
    
    graph.link_asset_to_purpose("office_network_drive", "file_storage")
    graph.link_asset_to_purpose("cloud_storage", "file_storage")
    
    graph.link_asset_to_purpose("office_printer", "printing")
    graph.link_asset_to_purpose("home_printer", "printing")
    graph.link_asset_to_purpose("print_service", "printing")
    
    graph.link_asset_to_purpose("office_desk", "ergonomic_setup")
    graph.link_asset_to_purpose("standing_desk", "ergonomic_setup")
    graph.link_asset_to_purpose("ergonomic_chair", "ergonomic_setup")
    graph.link_asset_to_purpose("dining_table", "ergonomic_setup")
    
    print("Transition Analysis:")
    print("-" * 60)
    
    print("\nPurposes with existing alternatives:")
    overlapping = graph.get_overlapping_purposes()
    for info in overlapping:
        purpose = info['purpose']
        assets = info['assets']
        
        shared = [a for a in assets if a.asset_type == AssetType.SHARED]
        owned = [a for a in assets if a.asset_type != AssetType.SHARED]
        
        if shared and owned:
            print(f"\n  {purpose.name}:")
            print(f"    Previously at office: {', '.join(a.name for a in shared)}")
            print(f"    New/existing alternatives: {', '.join(a.name for a in owned)}")
    
    print("\n" + "=" * 60)
    print("Reflection Points for Transition:")
    print("=" * 60)
    print("""
Questions the graph helps surface:

1. Video Calls: Laptop camera already exists. Is external webcam
   needed, or test laptop camera quality first?

2. File Storage: Company may provide cloud storage. Check before
   subscribing to personal service.

3. Printing: Three options identified. Actual printing frequency
   could determine if home printer is needed or if occasional
   print service is sufficient.

4. Ergonomic Setup: Dining table exists. Could try it temporarily
   before investing in standing desk and chair.

The graph doesn't answer "what to buy" but reveals what access
already exists and where gaps truly are.
    """)
    
    return graph


if __name__ == "__main__":
    # Run all example scenarios
    example_moving_scenario()
    example_co_living_scenario()
    example_work_transition_scenario()
    
    print("\n" + "=" * 60)
    print("Purpose Graph System - Example Scenarios Complete")
    print("=" * 60)
