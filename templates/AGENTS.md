# [App name]

> Canonical code, Gradle version catalogs and GitHub Actions workflows live in
> `docs/CODE_SNIPPETS.md`. Copy snippets from there, never from the PDF.
> Capability → library lookup (PDF, camera, upload, QR, AI) lives in `docs/FEATURE_RECIPES.md`.
> Feature-genre library recipes live in docs/FEATURE_RECIPES.md; copy-paste task prompts live in PROMPTS.md.

Native Android app in Kotlin. One module, Single Activity, Compose, Material 3.

## Stack
- AGP 9.5.1, Gradle 9.9.1, Kotlin 2.4.21, KSP 2.3.14, Hilt 2.60.1
- compileSdk 37, minSdk 24 (material3 1.5.x requires 37)
- Compose BOM 2026.09.00 + material3 1.5.0-rc01 (pinned - the BOM does not move it)
- Room 2.8.5, DataStore, Retrofit + OkHttp, kotlinx.serialization - only if the app needs them
- Navigation 3 (NavDisplay + @Serializable NavKey), Coroutines/Flow

# The dependency chain that decides the toolchain (playbook Part 6.6):
#   M3 Expressive -> material3 1.5.x -> compileSdk 37 -> AGP >= 9.1 -> Gradle 9.x -> built-in Kotlin
# material3 is NOT moved by the Compose BOM - pin it (1.5.0-rc01 as of 15 Nov 2026).

## Packages - com.<you>.<app>
- ui/theme/{Color.kt, Type.kt, Theme.kt}
- ui/navigation/{NavigationKeys.kt, Navigation.kt}
- ui/screens/<feature>/{<Feature>Screen.kt, ViewModel.kt, UiState.kt}
- data/local/ (Room), data/remote/ (Retrofit), data/repository/
- domain/model/ (pure Kotlin); add domain/usecase/ only when reused
- di/ per layer (DataModule.kt, DatabaseModule.kt)

## Rules
- One StateFlow<UiState> per screen, stateIn(WhileSubscribed(5_000))
- One-shot effects in a Channel; never inside the state object
- SavedStateHandle for user input (rotation survives, process death does not)
- Room is the source of truth; the network writes into Room
- Inject dispatchers; never reference Dispatchers.IO inline
- No business logic in composables; hoist state
- enableEdgeToEdge() before setContent; consume Scaffold innerPadding
- No feature package imports another feature package
- Do not add Gradle modules until there are 4+ features

## Commands
- Build: ./gradlew assembleDebug
- Test: ./gradlew testDebugUnitTest
- Lint: ./gradlew lintDebug
- Single test: ./gradlew testDebugUnitTest --tests "*FeedViewModelTest"

## Do not
- Run ./gradlew clean unless the cache is corrupt
- Call bare gradle; always the wrapper
- Commit keystores, local.properties or secrets
- Add -keep rules before running :app:analyzeReleaseR8Config
- Apply `org.jetbrains.kotlin.android` on AGP 9+ - Kotlin is built in and the plugin fails the build
- Use `kotlinOptions { jvmTarget = "17" }` on Kotlin 2.3+ - use `kotlin { compilerOptions { jvmTarget.set(JvmTarget.JVM_17) } }`
- Assume `sdkmanager "platforms;android-37"` exists - 37 ships as `platforms;android-37.0` / `37.1` / `37.2`
- Pin `material3` by assuming the Compose BOM moves it - it does not; pin it, and know that 1.5.x forces compileSdk 37 + AGP >= 9.1
