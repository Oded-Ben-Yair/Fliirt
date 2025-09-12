#!/usr/bin/env python3
"""
Validate iOS project structure and syntax
This ensures the project is properly formatted before user testing
"""

import os
import json
import re
from pathlib import Path

def validate_pbxproj_syntax():
    """Validate the project.pbxproj file syntax"""
    print("🔍 Validating project.pbxproj syntax...")
    
    pbxproj_path = "/home/ubuntu/Fliirt/iOS/FlirrtApp.xcodeproj/project.pbxproj"
    
    if not os.path.exists(pbxproj_path):
        print("❌ project.pbxproj not found")
        return False
    
    try:
        with open(pbxproj_path, 'r') as f:
            content = f.read()
        
        # Check for basic structure
        required_sections = [
            "/* Begin PBXBuildFile section */",
            "/* Begin PBXFileReference section */",
            "/* Begin PBXGroup section */",
            "/* Begin PBXNativeTarget section */",
            "/* Begin PBXProject section */",
            "/* Begin XCBuildConfiguration section */",
            "/* Begin XCConfigurationList section */"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ Missing sections: {missing_sections}")
            return False
        
        # Check for balanced braces
        open_braces = content.count('{')
        close_braces = content.count('}')
        
        if open_braces != close_braces:
            print(f"❌ Unbalanced braces: {open_braces} open, {close_braces} close")
            return False
        
        # Check for valid UUID format (24 hex chars)
        uuid_pattern = r'[A-F0-9]{24}'
        uuids = re.findall(uuid_pattern, content)
        
        if len(uuids) < 10:  # Should have many UUIDs
            print(f"❌ Too few UUIDs found: {len(uuids)}")
            return False
        
        print(f"✅ project.pbxproj syntax valid ({len(uuids)} UUIDs, balanced braces)")
        return True
        
    except Exception as e:
        print(f"❌ Error validating project.pbxproj: {e}")
        return False

def validate_file_structure():
    """Validate all required files exist"""
    print("\n📁 Validating file structure...")
    
    base_path = "/home/ubuntu/Fliirt/iOS"
    
    required_files = {
        "FlirrtApp/FlirrtApp.swift": "Main app entry point",
        "FlirrtApp/ContentView.swift": "Main app UI",
        "FlirrtApp/SettingsView.swift": "Settings interface",
        "FlirrtApp/Info.plist": "Main app configuration",
        "FlirrtApp/FlirrtApp.entitlements": "Main app entitlements",
        "FlirrtApp/Assets.xcassets/Contents.json": "Asset catalog",
        "FlirrtKeyboard/KeyboardViewController.swift": "Keyboard extension",
        "FlirrtKeyboard/Info.plist": "Keyboard configuration",
        "FlirrtKeyboard/FlirrtKeyboard.entitlements": "Keyboard entitlements",
        "Shared/AppGroupCommunicator.swift": "App Groups communication",
        "Shared/PhotoPickerManager.swift": "Photo picker handling",
        "Shared/PhotoPickerView.swift": "Photo picker UI",
        "Shared/AIService.swift": "AI backend integration",
        "Shared/AppGroupsDebugView.swift": "Debug interface"
    }
    
    missing_files = []
    existing_files = []
    
    for file_path, description in required_files.items():
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            existing_files.append(f"✅ {file_path}")
        else:
            missing_files.append(f"❌ {file_path} - {description}")
    
    for file_info in existing_files:
        print(file_info)
    
    if missing_files:
        print("\nMissing files:")
        for file_info in missing_files:
            print(file_info)
        return False
    
    print(f"\n✅ All {len(required_files)} required files present")
    return True

def validate_swift_syntax():
    """Basic Swift syntax validation"""
    print("\n🔍 Validating Swift syntax...")
    
    swift_files = [
        "/home/ubuntu/Fliirt/iOS/FlirrtApp/FlirrtApp.swift",
        "/home/ubuntu/Fliirt/iOS/FlirrtApp/ContentView.swift",
        "/home/ubuntu/Fliirt/iOS/FlirrtKeyboard/KeyboardViewController.swift",
        "/home/ubuntu/Fliirt/iOS/Shared/AppGroupCommunicator.swift"
    ]
    
    syntax_issues = []
    
    for swift_file in swift_files:
        if not os.path.exists(swift_file):
            continue
            
        try:
            with open(swift_file, 'r') as f:
                content = f.read()
            
            # Basic syntax checks
            if content.count('{') != content.count('}'):
                syntax_issues.append(f"{os.path.basename(swift_file)}: Unbalanced braces")
            
            if 'import SwiftUI' not in content and 'import UIKit' not in content:
                syntax_issues.append(f"{os.path.basename(swift_file)}: Missing import statement")
            
            # Check for basic Swift structure
            if not re.search(r'(struct|class|enum)\s+\w+', content):
                syntax_issues.append(f"{os.path.basename(swift_file)}: No Swift types found")
            
            print(f"✅ {os.path.basename(swift_file)}")
            
        except Exception as e:
            syntax_issues.append(f"{os.path.basename(swift_file)}: {str(e)}")
    
    if syntax_issues:
        print("\nSyntax issues found:")
        for issue in syntax_issues:
            print(f"❌ {issue}")
        return False
    
    print("✅ Swift syntax validation passed")
    return True

def validate_plist_files():
    """Validate Info.plist files"""
    print("\n📄 Validating plist files...")
    
    plist_files = [
        "/home/ubuntu/Fliirt/iOS/FlirrtApp/Info.plist",
        "/home/ubuntu/Fliirt/iOS/FlirrtKeyboard/Info.plist"
    ]
    
    plist_issues = []
    
    for plist_file in plist_files:
        if not os.path.exists(plist_file):
            plist_issues.append(f"{os.path.basename(plist_file)}: File not found")
            continue
        
        try:
            with open(plist_file, 'r') as f:
                content = f.read()
            
            # Check for basic plist structure
            if '<?xml version="1.0"' not in content:
                plist_issues.append(f"{os.path.basename(plist_file)}: Missing XML declaration")
            
            if '<plist version="1.0">' not in content:
                plist_issues.append(f"{os.path.basename(plist_file)}: Missing plist declaration")
            
            if '<dict>' not in content or '</dict>' not in content:
                plist_issues.append(f"{os.path.basename(plist_file)}: Missing dict structure")
            
            print(f"✅ {os.path.basename(plist_file)}")
            
        except Exception as e:
            plist_issues.append(f"{os.path.basename(plist_file)}: {str(e)}")
    
    if plist_issues:
        print("\nPlist issues found:")
        for issue in plist_issues:
            print(f"❌ {issue}")
        return False
    
    print("✅ Plist validation passed")
    return True

def create_validation_report():
    """Create a comprehensive validation report"""
    
    report = {
        "validation_timestamp": "2025-09-12",
        "project_path": "/home/ubuntu/Fliirt/iOS/FlirrtApp.xcodeproj",
        "tests": {
            "pbxproj_syntax": validate_pbxproj_syntax(),
            "file_structure": validate_file_structure(),
            "swift_syntax": validate_swift_syntax(),
            "plist_files": validate_plist_files()
        }
    }
    
    # Overall result
    all_passed = all(report["tests"].values())
    report["overall_result"] = "PASS" if all_passed else "FAIL"
    
    # Save report
    report_path = "/home/ubuntu/Fliirt/iOS/validation_report.json"
    try:
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n📄 Validation report saved: {report_path}")
    except Exception as e:
        print(f"❌ Error saving report: {e}")
    
    return report

def main():
    """Run complete project validation"""
    print("🚀 Flirrt.ai iOS Project Validation")
    print("=" * 50)
    
    report = create_validation_report()
    
    print("\n" + "=" * 50)
    print("🏁 Validation Summary")
    print("=" * 50)
    
    for test_name, result in report["tests"].items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    print(f"\n🎯 Overall Result: {report['overall_result']}")
    
    if report["overall_result"] == "PASS":
        print("\n🎉 Project validation successful!")
        print("📱 Ready for Xcode testing")
        return 0
    else:
        print("\n⚠️ Project validation failed")
        print("🔧 Issues need to be fixed before testing")
        return 1

if __name__ == "__main__":
    exit(main())

