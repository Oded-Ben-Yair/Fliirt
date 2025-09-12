#!/usr/bin/env python3
"""
Generate a proper Xcode project file for Flirrt.ai
This creates a valid .pbxproj file that Xcode can open
"""

import os
import uuid
import json

def generate_uuid():
    """Generate a 24-character hex string like Xcode uses"""
    return uuid.uuid4().hex.upper()[:24]

def create_pbxproj_content():
    """Create the content for project.pbxproj file"""
    
    # Generate UUIDs for all objects
    uuids = {
        'project': generate_uuid(),
        'main_app_target': generate_uuid(),
        'keyboard_target': generate_uuid(),
        'main_app_product': generate_uuid(),
        'keyboard_product': generate_uuid(),
        'main_group': generate_uuid(),
        'products_group': generate_uuid(),
        'flirrt_app_group': generate_uuid(),
        'flirrt_keyboard_group': generate_uuid(),
        'shared_group': generate_uuid(),
        'assets_group': generate_uuid(),
        'preview_group': generate_uuid(),
        
        # File references
        'flirrt_app_swift': generate_uuid(),
        'content_view_swift': generate_uuid(),
        'settings_view_swift': generate_uuid(),
        'keyboard_controller_swift': generate_uuid(),
        'app_group_communicator_swift': generate_uuid(),
        'photo_picker_manager_swift': generate_uuid(),
        'photo_picker_view_swift': generate_uuid(),
        'ai_service_swift': generate_uuid(),
        'debug_view_swift': generate_uuid(),
        'main_info_plist': generate_uuid(),
        'keyboard_info_plist': generate_uuid(),
        'main_entitlements': generate_uuid(),
        'keyboard_entitlements': generate_uuid(),
        'assets_xcassets': generate_uuid(),
        'preview_assets': generate_uuid(),
        
        # Build files
        'flirrt_app_swift_build': generate_uuid(),
        'content_view_swift_build': generate_uuid(),
        'settings_view_swift_build': generate_uuid(),
        'keyboard_controller_swift_build': generate_uuid(),
        'app_group_communicator_main_build': generate_uuid(),
        'app_group_communicator_keyboard_build': generate_uuid(),
        'photo_picker_manager_build': generate_uuid(),
        'photo_picker_view_build': generate_uuid(),
        'ai_service_build': generate_uuid(),
        'debug_view_build': generate_uuid(),
        'assets_build': generate_uuid(),
        'preview_assets_build': generate_uuid(),
        'main_info_plist_build': generate_uuid(),
        'keyboard_info_plist_build': generate_uuid(),
        
        # Build phases
        'main_sources_phase': generate_uuid(),
        'main_resources_phase': generate_uuid(),
        'keyboard_sources_phase': generate_uuid(),
        'keyboard_resources_phase': generate_uuid(),
        'embed_extensions_phase': generate_uuid(),
        
        # Build configurations
        'debug_config': generate_uuid(),
        'release_config': generate_uuid(),
        'main_debug_config': generate_uuid(),
        'main_release_config': generate_uuid(),
        'keyboard_debug_config': generate_uuid(),
        'keyboard_release_config': generate_uuid(),
        'config_list': generate_uuid(),
        'main_config_list': generate_uuid(),
        'keyboard_config_list': generate_uuid(),
        
        # Dependencies
        'keyboard_dependency': generate_uuid(),
        'keyboard_proxy': generate_uuid(),
        'embed_keyboard_build': generate_uuid(),
    }
    
    content = f"""// !$*UTF8*$!
{{
	archiveVersion = 1;
	classes = {{
	}};
	objectVersion = 56;
	objects = {{

/* Begin PBXBuildFile section */
		{uuids['flirrt_app_swift_build']} /* FlirrtApp.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {uuids['flirrt_app_swift']} /* FlirrtApp.swift */; }};
		{uuids['content_view_swift_build']} /* ContentView.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {uuids['content_view_swift']} /* ContentView.swift */; }};
		{uuids['settings_view_swift_build']} /* SettingsView.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {uuids['settings_view_swift']} /* SettingsView.swift */; }};
		{uuids['keyboard_controller_swift_build']} /* KeyboardViewController.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {uuids['keyboard_controller_swift']} /* KeyboardViewController.swift */; }};
		{uuids['app_group_communicator_main_build']} /* AppGroupCommunicator.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {uuids['app_group_communicator_swift']} /* AppGroupCommunicator.swift */; }};
		{uuids['app_group_communicator_keyboard_build']} /* AppGroupCommunicator.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {uuids['app_group_communicator_swift']} /* AppGroupCommunicator.swift */; }};
		{uuids['photo_picker_manager_build']} /* PhotoPickerManager.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {uuids['photo_picker_manager_swift']} /* PhotoPickerManager.swift */; }};
		{uuids['photo_picker_view_build']} /* PhotoPickerView.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {uuids['photo_picker_view_swift']} /* PhotoPickerView.swift */; }};
		{uuids['ai_service_build']} /* AIService.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {uuids['ai_service_swift']} /* AIService.swift */; }};
		{uuids['debug_view_build']} /* AppGroupsDebugView.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {uuids['debug_view_swift']} /* AppGroupsDebugView.swift */; }};
		{uuids['assets_build']} /* Assets.xcassets in Resources */ = {{isa = PBXBuildFile; fileRef = {uuids['assets_xcassets']} /* Assets.xcassets */; }};
		{uuids['preview_assets_build']} /* Preview Assets.xcassets in Resources */ = {{isa = PBXBuildFile; fileRef = {uuids['preview_assets']} /* Preview Assets.xcassets */; }};
		{uuids['embed_keyboard_build']} /* FlirrtKeyboard.appex in Embed App Extensions */ = {{isa = PBXBuildFile; fileRef = {uuids['keyboard_product']} /* FlirrtKeyboard.appex */; settings = {{ATTRIBUTES = (RemoveHeadersOnCopy, ); }}; }};
/* End PBXBuildFile section */

/* Begin PBXContainerItemProxy section */
		{uuids['keyboard_proxy']} /* PBXContainerItemProxy */ = {{
			isa = PBXContainerItemProxy;
			containerPortal = {uuids['project']} /* Project object */;
			proxyType = 1;
			remoteGlobalIDString = {uuids['keyboard_target']};
			remoteInfo = FlirrtKeyboard;
		}};
/* End PBXContainerItemProxy section */

/* Begin PBXCopyFilesBuildPhase section */
		{uuids['embed_extensions_phase']} /* Embed App Extensions */ = {{
			isa = PBXCopyFilesBuildPhase;
			buildActionMask = 2147483647;
			dstPath = "";
			dstSubfolderSpec = 13;
			files = (
				{uuids['embed_keyboard_build']} /* FlirrtKeyboard.appex in Embed App Extensions */,
			);
			name = "Embed App Extensions";
			runOnlyForDeploymentPostprocessing = 0;
		}};
/* End PBXCopyFilesBuildPhase section */

/* Begin PBXFileReference section */
		{uuids['main_app_product']} /* FlirrtApp.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = FlirrtApp.app; sourceTree = BUILT_PRODUCTS_DIR; }};
		{uuids['keyboard_product']} /* FlirrtKeyboard.appex */ = {{isa = PBXFileReference; explicitFileType = "wrapper.app-extension"; includeInIndex = 0; path = FlirrtKeyboard.appex; sourceTree = BUILT_PRODUCTS_DIR; }};
		{uuids['flirrt_app_swift']} /* FlirrtApp.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = FlirrtApp.swift; sourceTree = "<group>"; }};
		{uuids['content_view_swift']} /* ContentView.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = ContentView.swift; sourceTree = "<group>"; }};
		{uuids['settings_view_swift']} /* SettingsView.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = SettingsView.swift; sourceTree = "<group>"; }};
		{uuids['keyboard_controller_swift']} /* KeyboardViewController.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = KeyboardViewController.swift; sourceTree = "<group>"; }};
		{uuids['app_group_communicator_swift']} /* AppGroupCommunicator.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = AppGroupCommunicator.swift; sourceTree = "<group>"; }};
		{uuids['photo_picker_manager_swift']} /* PhotoPickerManager.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = PhotoPickerManager.swift; sourceTree = "<group>"; }};
		{uuids['photo_picker_view_swift']} /* PhotoPickerView.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = PhotoPickerView.swift; sourceTree = "<group>"; }};
		{uuids['ai_service_swift']} /* AIService.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = AIService.swift; sourceTree = "<group>"; }};
		{uuids['debug_view_swift']} /* AppGroupsDebugView.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = AppGroupsDebugView.swift; sourceTree = "<group>"; }};
		{uuids['main_info_plist']} /* Info.plist */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.xml; path = Info.plist; sourceTree = "<group>"; }};
		{uuids['keyboard_info_plist']} /* Info.plist */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.xml; path = Info.plist; sourceTree = "<group>"; }};
		{uuids['main_entitlements']} /* FlirrtApp.entitlements */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.entitlements; path = FlirrtApp.entitlements; sourceTree = "<group>"; }};
		{uuids['keyboard_entitlements']} /* FlirrtKeyboard.entitlements */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.entitlements; path = FlirrtKeyboard.entitlements; sourceTree = "<group>"; }};
		{uuids['assets_xcassets']} /* Assets.xcassets */ = {{isa = PBXFileReference; lastKnownFileType = folder.assetcatalog; path = Assets.xcassets; sourceTree = "<group>"; }};
		{uuids['preview_assets']} /* Preview Assets.xcassets */ = {{isa = PBXFileReference; lastKnownFileType = folder.assetcatalog; path = "Preview Assets.xcassets"; sourceTree = "<group>"; }};
/* End PBXFileReference section */

/* Begin PBXFrameworksBuildPhase section */
		{generate_uuid()} /* Frameworks */ = {{
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
		{generate_uuid()} /* Frameworks */ = {{
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
/* End PBXFrameworksBuildPhase section */

/* Begin PBXGroup section */
		{uuids['main_group']} = {{
			isa = PBXGroup;
			children = (
				{uuids['flirrt_app_group']} /* FlirrtApp */,
				{uuids['flirrt_keyboard_group']} /* FlirrtKeyboard */,
				{uuids['shared_group']} /* Shared */,
				{uuids['products_group']} /* Products */,
			);
			sourceTree = "<group>";
		}};
		{uuids['products_group']} /* Products */ = {{
			isa = PBXGroup;
			children = (
				{uuids['main_app_product']} /* FlirrtApp.app */,
				{uuids['keyboard_product']} /* FlirrtKeyboard.appex */,
			);
			name = Products;
			sourceTree = "<group>";
		}};
		{uuids['flirrt_app_group']} /* FlirrtApp */ = {{
			isa = PBXGroup;
			children = (
				{uuids['flirrt_app_swift']} /* FlirrtApp.swift */,
				{uuids['content_view_swift']} /* ContentView.swift */,
				{uuids['settings_view_swift']} /* SettingsView.swift */,
				{uuids['main_entitlements']} /* FlirrtApp.entitlements */,
				{uuids['main_info_plist']} /* Info.plist */,
				{uuids['assets_group']} /* Assets */,
			);
			path = FlirrtApp;
			sourceTree = "<group>";
		}};
		{uuids['flirrt_keyboard_group']} /* FlirrtKeyboard */ = {{
			isa = PBXGroup;
			children = (
				{uuids['keyboard_controller_swift']} /* KeyboardViewController.swift */,
				{uuids['keyboard_entitlements']} /* FlirrtKeyboard.entitlements */,
				{uuids['keyboard_info_plist']} /* Info.plist */,
			);
			path = FlirrtKeyboard;
			sourceTree = "<group>";
		}};
		{uuids['shared_group']} /* Shared */ = {{
			isa = PBXGroup;
			children = (
				{uuids['app_group_communicator_swift']} /* AppGroupCommunicator.swift */,
				{uuids['photo_picker_manager_swift']} /* PhotoPickerManager.swift */,
				{uuids['photo_picker_view_swift']} /* PhotoPickerView.swift */,
				{uuids['ai_service_swift']} /* AIService.swift */,
				{uuids['debug_view_swift']} /* AppGroupsDebugView.swift */,
			);
			path = Shared;
			sourceTree = "<group>";
		}};
		{uuids['assets_group']} /* Assets */ = {{
			isa = PBXGroup;
			children = (
				{uuids['assets_xcassets']} /* Assets.xcassets */,
				{uuids['preview_group']} /* Preview Content */,
			);
			name = Assets;
			sourceTree = "<group>";
		}};
		{uuids['preview_group']} /* Preview Content */ = {{
			isa = PBXGroup;
			children = (
				{uuids['preview_assets']} /* Preview Assets.xcassets */,
			);
			path = "Preview Content";
			sourceTree = "<group>";
		}};
/* End PBXGroup section */

/* Begin PBXNativeTarget section */
		{uuids['main_app_target']} /* FlirrtApp */ = {{
			isa = PBXNativeTarget;
			buildConfigurationList = {uuids['main_config_list']} /* Build configuration list for PBXNativeTarget "FlirrtApp" */;
			buildPhases = (
				{uuids['main_sources_phase']} /* Sources */,
				{generate_uuid()} /* Frameworks */,
				{uuids['main_resources_phase']} /* Resources */,
				{uuids['embed_extensions_phase']} /* Embed App Extensions */,
			);
			buildRules = (
			);
			dependencies = (
				{uuids['keyboard_dependency']} /* PBXTargetDependency */,
			);
			name = FlirrtApp;
			productName = FlirrtApp;
			productReference = {uuids['main_app_product']} /* FlirrtApp.app */;
			productType = "com.apple.product-type.application";
		}};
		{uuids['keyboard_target']} /* FlirrtKeyboard */ = {{
			isa = PBXNativeTarget;
			buildConfigurationList = {uuids['keyboard_config_list']} /* Build configuration list for PBXNativeTarget "FlirrtKeyboard" */;
			buildPhases = (
				{uuids['keyboard_sources_phase']} /* Sources */,
				{generate_uuid()} /* Frameworks */,
				{uuids['keyboard_resources_phase']} /* Resources */,
			);
			buildRules = (
			);
			dependencies = (
			);
			name = FlirrtKeyboard;
			productName = FlirrtKeyboard;
			productReference = {uuids['keyboard_product']} /* FlirrtKeyboard.appex */;
			productType = "com.apple.product-type.app-extension";
		}};
/* End PBXNativeTarget section */

/* Begin PBXProject section */
		{uuids['project']} /* Project object */ = {{
			isa = PBXProject;
			attributes = {{
				BuildIndependentTargetsInParallel = 1;
				LastSwiftUpdateCheck = 1600;
				LastUpgradeCheck = 1600;
				TargetAttributes = {{
					{uuids['main_app_target']} = {{
						CreatedOnToolsVersion = 16.0;
					}};
					{uuids['keyboard_target']} = {{
						CreatedOnToolsVersion = 16.0;
					}};
				}};
			}};
			buildConfigurationList = {uuids['config_list']} /* Build configuration list for PBXProject "FlirrtApp" */;
			compatibilityVersion = "Xcode 14.0";
			developmentRegion = en;
			hasScannedForEncodings = 0;
			knownRegions = (
				en,
				Base,
			);
			mainGroup = {uuids['main_group']};
			productRefGroup = {uuids['products_group']} /* Products */;
			projectDirPath = "";
			projectRoot = "";
			targets = (
				{uuids['main_app_target']} /* FlirrtApp */,
				{uuids['keyboard_target']} /* FlirrtKeyboard */,
			);
		}};
/* End PBXProject section */

/* Begin PBXResourcesBuildPhase section */
		{uuids['main_resources_phase']} /* Resources */ = {{
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{uuids['preview_assets_build']} /* Preview Assets.xcassets in Resources */,
				{uuids['assets_build']} /* Assets.xcassets in Resources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
		{uuids['keyboard_resources_phase']} /* Resources */ = {{
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
/* End PBXResourcesBuildPhase section */

/* Begin PBXSourcesBuildPhase section */
		{uuids['main_sources_phase']} /* Sources */ = {{
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{uuids['content_view_swift_build']} /* ContentView.swift in Sources */,
				{uuids['settings_view_swift_build']} /* SettingsView.swift in Sources */,
				{uuids['flirrt_app_swift_build']} /* FlirrtApp.swift in Sources */,
				{uuids['app_group_communicator_main_build']} /* AppGroupCommunicator.swift in Sources */,
				{uuids['photo_picker_manager_build']} /* PhotoPickerManager.swift in Sources */,
				{uuids['photo_picker_view_build']} /* PhotoPickerView.swift in Sources */,
				{uuids['ai_service_build']} /* AIService.swift in Sources */,
				{uuids['debug_view_build']} /* AppGroupsDebugView.swift in Sources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
		{uuids['keyboard_sources_phase']} /* Sources */ = {{
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{uuids['keyboard_controller_swift_build']} /* KeyboardViewController.swift in Sources */,
				{uuids['app_group_communicator_keyboard_build']} /* AppGroupCommunicator.swift in Sources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
/* End PBXSourcesBuildPhase section */

/* Begin PBXTargetDependency section */
		{uuids['keyboard_dependency']} /* PBXTargetDependency */ = {{
			isa = PBXTargetDependency;
			target = {uuids['keyboard_target']} /* FlirrtKeyboard */;
			targetProxy = {uuids['keyboard_proxy']} /* PBXContainerItemProxy */;
		}};
/* End PBXTargetDependency section */

/* Begin XCBuildConfiguration section */
		{uuids['debug_config']} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ALWAYS_SEARCH_USER_PATHS = NO;
				ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS = YES;
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
				ENABLE_USER_SCRIPT_SANDBOXING = YES;
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
				LOCALIZATION_PREFERS_STRING_CATALOGS = YES;
				MTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;
				MTL_FAST_MATH = YES;
				ONLY_ACTIVE_ARCH = YES;
				SDKROOT = iphoneos;
				SWIFT_ACTIVE_COMPILATION_CONDITIONS = "DEBUG $(inherited)";
				SWIFT_OPTIMIZATION_LEVEL = "-Onone";
			}};
			name = Debug;
		}};
		{uuids['release_config']} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ALWAYS_SEARCH_USER_PATHS = NO;
				ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS = YES;
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
				ENABLE_USER_SCRIPT_SANDBOXING = YES;
				GCC_C_LANGUAGE_STANDARD = gnu17;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				IPHONEOS_DEPLOYMENT_TARGET = 18.0;
				LOCALIZATION_PREFERS_STRING_CATALOGS = YES;
				MTL_ENABLE_DEBUG_INFO = NO;
				MTL_FAST_MATH = YES;
				SDKROOT = iphoneos;
				SWIFT_COMPILATION_MODE = wholemodule;
				VALIDATE_PRODUCT = YES;
			}};
			name = Release;
		}};
		{uuids['main_debug_config']} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_ENTITLEMENTS = FlirrtApp/FlirrtApp.entitlements;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_ASSET_PATHS = "\"FlirrtApp/Preview Content\"";
				DEVELOPMENT_TEAM = "";
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_FILE = FlirrtApp/Info.plist;
				INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES;
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchScreen_Generation = YES;
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				IPHONEOS_DEPLOYMENT_TARGET = 18.0;
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
		{uuids['main_release_config']} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_ENTITLEMENTS = FlirrtApp/FlirrtApp.entitlements;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_ASSET_PATHS = "\"FlirrtApp/Preview Content\"";
				DEVELOPMENT_TEAM = "";
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_FILE = FlirrtApp/Info.plist;
				INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES;
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchScreen_Generation = YES;
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				IPHONEOS_DEPLOYMENT_TARGET = 18.0;
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
		{uuids['keyboard_debug_config']} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				CODE_SIGN_ENTITLEMENTS = FlirrtKeyboard/FlirrtKeyboard.entitlements;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_TEAM = "";
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_FILE = FlirrtKeyboard/Info.plist;
				INFOPLIST_KEY_CFBundleDisplayName = Flirrt;
				INFOPLIST_KEY_NSHumanReadableCopyright = "";
				IPHONEOS_DEPLOYMENT_TARGET = 18.0;
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
					"@executable_path/../../Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = ai.flirrt.FlirrtApp.FlirrtKeyboard;
				PRODUCT_NAME = "$(TARGET_NAME)";
				SKIP_INSTALL = YES;
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 6.0;
				TARGETED_DEVICE_FAMILY = "1,2";
			}};
			name = Debug;
		}};
		{uuids['keyboard_release_config']} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				CODE_SIGN_ENTITLEMENTS = FlirrtKeyboard/FlirrtKeyboard.entitlements;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_TEAM = "";
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_FILE = FlirrtKeyboard/Info.plist;
				INFOPLIST_KEY_CFBundleDisplayName = Flirrt;
				INFOPLIST_KEY_NSHumanReadableCopyright = "";
				IPHONEOS_DEPLOYMENT_TARGET = 18.0;
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
					"@executable_path/../../Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = ai.flirrt.FlirrtApp.FlirrtKeyboard;
				PRODUCT_NAME = "$(TARGET_NAME)";
				SKIP_INSTALL = YES;
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 6.0;
				TARGETED_DEVICE_FAMILY = "1,2";
			}};
			name = Release;
		}};
/* End XCBuildConfiguration section */

/* Begin XCConfigurationList section */
		{uuids['config_list']} /* Build configuration list for PBXProject "FlirrtApp" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{uuids['debug_config']} /* Debug */,
				{uuids['release_config']} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
		{uuids['main_config_list']} /* Build configuration list for PBXNativeTarget "FlirrtApp" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{uuids['main_debug_config']} /* Debug */,
				{uuids['main_release_config']} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
		{uuids['keyboard_config_list']} /* Build configuration list for PBXNativeTarget "FlirrtKeyboard" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{uuids['keyboard_debug_config']} /* Debug */,
				{uuids['keyboard_release_config']} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
/* End XCConfigurationList section */
	}};
	rootObject = {uuids['project']} /* Project object */;
}}
"""
    
    return content

def create_xcode_project():
    """Create the complete Xcode project structure"""
    
    print("🔨 Creating proper Xcode project...")
    
    # Create project directory
    project_dir = "/home/ubuntu/Fliirt/iOS/FlirrtApp.xcodeproj"
    os.makedirs(project_dir, exist_ok=True)
    
    # Create project.pbxproj file
    pbxproj_path = os.path.join(project_dir, "project.pbxproj")
    
    try:
        with open(pbxproj_path, 'w') as f:
            f.write(create_pbxproj_content())
        
        print(f"✅ Created project.pbxproj: {pbxproj_path}")
        
        # Create project.xcworkspace if needed
        workspace_dir = os.path.join(project_dir, "project.xcworkspace")
        os.makedirs(workspace_dir, exist_ok=True)
        
        workspace_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Workspace
   version = "1.0">
   <FileRef
      location = "self:">
   </FileRef>
</Workspace>
'''
        
        workspace_path = os.path.join(workspace_dir, "contents.xcworkspacedata")
        with open(workspace_path, 'w') as f:
            f.write(workspace_content)
        
        print(f"✅ Created workspace: {workspace_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating Xcode project: {e}")
        return False

def main():
    """Create the Xcode project"""
    success = create_xcode_project()
    
    if success:
        print("\n🎉 Xcode project created successfully!")
        print("📁 Project location: /home/ubuntu/Fliirt/iOS/FlirrtApp.xcodeproj")
        print("🚀 Ready to open in Xcode")
        return 0
    else:
        print("\n❌ Failed to create Xcode project")
        return 1

if __name__ == "__main__":
    exit(main())

