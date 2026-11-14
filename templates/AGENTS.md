# [App name]

> Canonical code, Gradle version catalogs and GitHub Actions workflows live in
> `docs/CODE_SNIPPETS.md`. Copy snippets from there, never from the PDF.
> Capability → library lookup (PDF, camera, upload, QR, AI) lives in `docs/FEATURE_RECIPES.md`.

Native Android app in Kotlin. One module, Single Activity, Compose, Material 3.

## Stack
- AGP 9.3.2, Gradle 9.7.1, Kotlin 2.3, KSP >= 2.3.6, Hilt >= 2.59.2
- compileSdk 37 (fall back to 36 if a library lacks API 37 metadata), minSdk 24
- Room, DataStore, Retrofit + OkHttp, kotlinx.serialization
- Navigation 3 (NavDisplay + @Serializable NavKey), Coroutines/Flow

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
