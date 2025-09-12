#!/usr/bin/env python3
"""
Create a minimal, working Xcode project for Flirrt.ai
This creates the simplest possible project structure that Xcode can open
"""

import os
import uuid
import json

def create_minimal_project():
    """Create a minimal Xcode project that actually works"""
    
    print("🔨 Creating minimal working Xcode project...")
    
    # Remove any existing project
    if os.path.exists("FlirrtApp.xcodeproj"):
        os.system("rm -rf FlirrtApp.xcodeproj")
    
    # Create project directory
    os.makedirs("FlirrtApp.xcodeproj", exist_ok=True)
    
    # Generate minimal UUIDs
    project_uuid = "1A2B3C4D5E6F7890ABCD1230"
    main_target_uuid = "1A2B3C4D5E6F7890ABCD1231"
    main_product_uuid = "1A2B3C4D5E6F7890ABCD1232"
    main_group_uuid = "1A2B3C4D5E6F7890ABCD1233"
    products_group_uuid = "1A2B3C4D5E6F7890ABCD1234"
    
    # File references
    app_swift_uuid = "1A2B3C4D5E6F7890ABCD1235"
    content_view_uuid = "1A2B3C4D5E6F7890ABCD1236"
    assets_uuid = "1A2B3C4D5E6F7890ABCD1237"
    
    # Build files
    app_swift_build_uuid = "1A2B3C4D5E6F7890ABCD1238"
    content_view_build_uuid = "1A2B3C4D5E6F7890ABCD1239"
    assets_build_uuid = "1A2B3C4D5E6F7890ABCD123A"
    
    # Build phases
    sources_phase_uuid = "1A2B3C4D5E6F7890ABCD123B"
    resources_phase_uuid = "1A2B3C4D5E6F7890ABCD123C"
    frameworks_phase_uuid = "1A2B3C4D5E6F7890ABCD123D"
    
    # Build configurations
    debug_config_uuid = "1A2B3C4D5E6F7890ABCD123E"
    release_config_uuid = "1A2B3C4D5E6F7890ABCD123F"
    target_debug_uuid = "1A2B3C4D5E6F7890ABCD1240"
    target_release_uuid = "1A2B3C4D5E6F7890ABCD1241"
    config_list_uuid = "1A2B3C4D5E6F7890ABCD1242"
    target_config_list_uuid = "1A2B3C4D5E6F7890ABCD1243"
    
    # Create minimal project.pbxproj
    pbxproj_content = f"""// !$*UTF8*$!
{{
	archiveVersion = 1;
	classes = {{
	}};
	objectVersion = 56;
	objects = {{

/* Begin PBXBuildFile section */
		{app_swift_build_uuid} /* FlirrtApp.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {app_swift_uuid} /* FlirrtApp.swift */; }};
		{content_view_build_uuid} /* ContentView.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {content_view_uuid} /* ContentView.swift */; }};
		{assets_build_uuid} /* Assets.xcassets in Resources */ = {{isa = PBXBuildFile; fileRef = {assets_uuid} /* Assets.xcassets */; }};
/* End PBXBuildFile section */

/* Begin PBXFileReference section */
		{main_product_uuid} /* FlirrtApp.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = FlirrtApp.app; sourceTree = BUILT_PRODUCTS_DIR; }};
		{app_swift_uuid} /* FlirrtApp.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = FlirrtApp.swift; sourceTree = "<group>"; }};
		{content_view_uuid} /* ContentView.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = ContentView.swift; sourceTree = "<group>"; }};
		{assets_uuid} /* Assets.xcassets */ = {{isa = PBXFileReference; lastKnownFileType = folder.assetcatalog; path = Assets.xcassets; sourceTree = "<group>"; }};
/* End PBXFileReference section */

/* Begin PBXFrameworksBuildPhase section */
		{frameworks_phase_uuid} /* Frameworks */ = {{
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
/* End PBXFrameworksBuildPhase section */

/* Begin PBXGroup section */
		{main_group_uuid} = {{
			isa = PBXGroup;
			children = (
				{app_swift_uuid} /* FlirrtApp.swift */,
				{content_view_uuid} /* ContentView.swift */,
				{assets_uuid} /* Assets.xcassets */,
				{products_group_uuid} /* Products */,
			);
			sourceTree = "<group>";
		}};
		{products_group_uuid} /* Products */ = {{
			isa = PBXGroup;
			children = (
				{main_product_uuid} /* FlirrtApp.app */,
			);
			name = Products;
			sourceTree = "<group>";
		}};
/* End PBXGroup section */

/* Begin PBXNativeTarget section */
		{main_target_uuid} /* FlirrtApp */ = {{
			isa = PBXNativeTarget;
			buildConfigurationList = {target_config_list_uuid} /* Build configuration list for PBXNativeTarget "FlirrtApp" */;
			buildPhases = (
				{sources_phase_uuid} /* Sources */,
				{frameworks_phase_uuid} /* Frameworks */,
				{resources_phase_uuid} /* Resources */,
			);
			buildRules = (
			);
			dependencies = (
			);
			name = FlirrtApp;
			productName = FlirrtApp;
			productReference = {main_product_uuid} /* FlirrtApp.app */;
			productType = "com.apple.product-type.application";
		}};
/* End PBXNativeTarget section */

/* Begin PBXProject section */
		{project_uuid} /* Project object */ = {{
			isa = PBXProject;
			attributes = {{
				BuildIndependentTargetsInParallel = 1;
				LastSwiftUpdateCheck = 1600;
				LastUpgradeCheck = 1600;
				TargetAttributes = {{
					{main_target_uuid} = {{
						CreatedOnToolsVersion = 16.0;
					}};
				}};
			}};
			buildConfigurationList = {config_list_uuid} /* Build configuration list for PBXProject "FlirrtApp" */;
			compatibilityVersion = "Xcode 14.0";
			developmentRegion = en;
			hasScannedForEncodings = 0;
			knownRegions = (
				en,
				Base,
			);
			mainGroup = {main_group_uuid};
			productRefGroup = {products_group_uuid} /* Products */;
			projectDirPath = "";
			projectRoot = "";
			targets = (
				{main_target_uuid} /* FlirrtApp */,
			);
		}};
/* End PBXProject section */

/* Begin PBXResourcesBuildPhase section */
		{resources_phase_uuid} /* Resources */ = {{
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{assets_build_uuid} /* Assets.xcassets in Resources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
/* End PBXResourcesBuildPhase section */

/* Begin PBXSourcesBuildPhase section */
		{sources_phase_uuid} /* Sources */ = {{
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{content_view_build_uuid} /* ContentView.swift in Sources */,
				{app_swift_build_uuid} /* FlirrtApp.swift in Sources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
/* End PBXSourcesBuildPhase section */

/* Begin XCBuildConfiguration section */
		{debug_config_uuid} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ALWAYS_SEARCH_USER_PATHS = NO;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_ENABLE_OBJC_WEAK = YES;
				CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_COMMA = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
				CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
				CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INFINITE_RECURSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
				CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
				CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
				CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
				CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
				CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
				CLANG_WARN_STRICT_PROTOTYPES = YES;
				CLANG_WARN_SUSPICIOUS_MOVE = YES;
				CLANG_WARN_UNGUARDED_AVAILABILITY = YES_AGGRESSIVE;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = dwarf;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				ENABLE_TESTABILITY = YES;
				GCC_C_LANGUAGE_STANDARD = gnu17;
				GCC_DYNAMIC_NO_PIC = NO;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_OPTIMIZATION_LEVEL = 0;
				GCC_PREPROCESSOR_DEFINITIONS = (
					"DEBUG=1",
					"$(inherited)",
				);
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				IPHONEOS_DEPLOYMENT_TARGET = 18.0;
				MTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;
				MTL_FAST_MATH = YES;
				ONLY_ACTIVE_ARCH = YES;
				SDKROOT = iphoneos;
				SWIFT_ACTIVE_COMPILATION_CONDITIONS = "DEBUG $(inherited)";
				SWIFT_OPTIMIZATION_LEVEL = "-Onone";
			}};
			name = Debug;
		}};
		{release_config_uuid} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ALWAYS_SEARCH_USER_PATHS = NO;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_ENABLE_OBJC_WEAK = YES;
				CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_COMMA = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
				CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
				CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INFINITE_RECURSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
				CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
				CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
				CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
				CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
				CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
				CLANG_WARN_STRICT_PROTOTYPES = YES;
				CLANG_WARN_SUSPICIOUS_MOVE = YES;
				CLANG_WARN_UNGUARDED_AVAILABILITY = YES_AGGRESSIVE;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
				ENABLE_NS_ASSERTIONS = NO;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				GCC_C_LANGUAGE_STANDARD = gnu17;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				IPHONEOS_DEPLOYMENT_TARGET = 18.0;
				MTL_ENABLE_DEBUG_INFO = NO;
				MTL_FAST_MATH = YES;
				SDKROOT = iphoneos;
				SWIFT_COMPILATION_MODE = wholemodule;
				VALIDATE_PRODUCT = YES;
			}};
			name = Release;
		}};
		{target_debug_uuid} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_TEAM = "";
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES;
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchScreen_Generation = YES;
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = ai.flirrt.FlirrtApp;
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 6.0;
				TARGETED_DEVICE_FAMILY = "1,2";
			}};
			name = Debug;
		}};
		{target_release_uuid} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_TEAM = "";
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES;
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchScreen_Generation = YES;
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = ai.flirrt.FlirrtApp;
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 6.0;
				TARGETED_DEVICE_FAMILY = "1,2";
			}};
			name = Release;
		}};
/* End XCBuildConfiguration section */

/* Begin XCConfigurationList section */
		{config_list_uuid} /* Build configuration list for PBXProject "FlirrtApp" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{debug_config_uuid} /* Debug */,
				{release_config_uuid} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
		{target_config_list_uuid} /* Build configuration list for PBXNativeTarget "FlirrtApp" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{target_debug_uuid} /* Debug */,
				{target_release_uuid} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
/* End XCConfigurationList section */
	}};
	rootObject = {project_uuid} /* Project object */;
}}
"""
    
    # Write project file
    with open("FlirrtApp.xcodeproj/project.pbxproj", "w") as f:
        f.write(pbxproj_content)
    
    # Create workspace
    os.makedirs("FlirrtApp.xcodeproj/project.xcworkspace", exist_ok=True)
    workspace_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Workspace
   version = "1.0">
   <FileRef
      location = "self:">
   </FileRef>
</Workspace>
'''
    with open("FlirrtApp.xcodeproj/project.xcworkspace/contents.xcworkspacedata", "w") as f:
        f.write(workspace_content)
    
    print("✅ Minimal project created successfully")
    return True

def validate_minimal_project():
    """Validate the minimal project"""
    print("\n🔍 Validating minimal project...")
    
    # Check project file exists
    if not os.path.exists("FlirrtApp.xcodeproj/project.pbxproj"):
        print("❌ project.pbxproj not found")
        return False
    
    # Check basic syntax
    try:
        with open("FlirrtApp.xcodeproj/project.pbxproj", "r") as f:
            content = f.read()
        
        # Check for balanced braces
        if content.count('{') != content.count('}'):
            print("❌ Unbalanced braces")
            return False
        
        # Check for required sections
        required_sections = [
            "/* Begin PBXBuildFile section */",
            "/* Begin PBXFileReference section */",
            "/* Begin PBXNativeTarget section */",
            "/* Begin PBXProject section */"
        ]
        
        for section in required_sections:
            if section not in content:
                print(f"❌ Missing section: {section}")
                return False
        
        print("✅ Project file syntax valid")
        return True
        
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def main():
    """Create and validate minimal project"""
    print("🚀 Creating Minimal Flirrt.ai Project")
    print("=" * 50)
    
    success = create_minimal_project()
    if not success:
        print("❌ Failed to create project")
        return 1
    
    valid = validate_minimal_project()
    if not valid:
        print("❌ Project validation failed")
        return 1
    
    print("\n🎉 Minimal project created and validated!")
    print("📱 This is a basic single-target project that should open in Xcode")
    print("🔧 You can then manually add the keyboard extension target")
    
    return 0

if __name__ == "__main__":
    exit(main())

