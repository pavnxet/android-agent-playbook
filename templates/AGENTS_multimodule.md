# [App name]

> Canonical code, Gradle version catalogs and GitHub Actions workflows live in
> `docs/CODE_SNIPPETS.md`. Copy snippets from there, never from the PDF.
> Capability → library lookup (PDF, camera, upload, QR, AI) lives in `docs/FEATURE_RECIPES.md`.

Native Android app in Kotlin. Multi-module, Single Activity, Compose, Material 3.

## Stack
- AGP 9.3.2, Gradle 9.7.1, Kotlin 2.3, KSP >= 2.3.6, Hilt >= 2.59.2
- compileSdk 37 (fall back to 36 if a library lacks API 37 metadata), minSdk 24
- Room, DataStore, Retrofit + OkHttp, kotlinx.serialization
- Navigation 3 (NavDisplay + @Serializable NavKey), Coroutines/Flow

## Modules
- :app - Application, MainActivity, top-level NavDisplay, DI entry points
- :core:model (pure JVM), :core:data, :core:database, :core:network
- :core:designsystem, :core:ui, :core:navigation, :core:common, :core:testing
- :feature:<name>:api (NavKey + contract), :feature:<name>:impl (screen, VM)

## Dependency rules
- feature -> core -> model; a core module never imports a feature
- a feature never depends on another feature's impl
- only :app and a feature's own impl see that impl module
- no Context, Bitmap or Cursor in :core:model

## Rules
- One StateFlow<UiState> per screen, stateIn(WhileSubscribed(5_000))
- One-shot effects in a Channel; never inside the state object
- SavedStateHandle for user input (rotation survives, process death does not)
- Room is the source of truth; the network writes into Room
- Inject dispatchers; never reference Dispatchers.IO inline
- No business logic in composables; hoist state
- enableEdgeToEdge() before setContent; consume Scaffold innerPadding

## Commands
- Build: ./gradlew assembleDebug
- Test: ./gradlew testDebugUnitTest
- R8 report: ./gradlew :app:analyzeReleaseR8Config
- Screenshots: ./gradlew verifyRoborazziDebug
- Single test: ./gradlew testDebugUnitTest --tests "*FeedViewModelTest"

## Do not
- Run ./gradlew clean unless the cache is corrupt
- Call bare gradle; always the wrapper
- Commit keystores, local.properties or secrets
- Add -keep rules before running :app:analyzeReleaseR8Config
