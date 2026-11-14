# Golden starter

A one-screen Android app that proves the playbook's baseline stack **compiles and passes its tests**. It is a build proof, not a template to clone blindly — the templates in [`../templates/`](../templates/) are what you install into a real project.

Verified in CI by [`.github/workflows/verify-starter.yml`](../.github/workflows/verify-starter.yml) on every change to this folder.

## What it demonstrates

| Rule from the playbook | Where |
|---|---|
| Single Activity, `enableEdgeToEdge()` before `setContent` | `MainActivity.kt` |
| Navigation 3: back stack as data, `NavKey` routes, `NavDisplay` | `MainActivity.kt`, `ui/navigation/NavigationKeys.kt` |
| One immutable `UiState` per screen, `stateIn(WhileSubscribed(5_000))` | `ui/home/HomeUiState.kt`, `HomeViewModel.kt` |
| One-shot effects in a `Channel`, never in state | `HomeViewModel.kt` |
| Injected `@IoDispatcher`, no inline `Dispatchers.IO` | `di/AppModule.kt`, `data/NoteRepository.kt` |
| Room as the source of truth; repository is the only path to data | `data/` |
| Stateless content composable + stateful route composable | `HomeScreen.kt`, `HomeRoute.kt` |
| Unit tests with `StandardTestDispatcher` + Turbine, fakes over mocks | `app/src/test/.../HomeViewModelTest.kt` |
| 16 GB laptop `gradle.properties` | `gradle.properties` |

## Pinned versions

AGP 9.3.2 · Gradle 9.7.1 · Kotlin 2.3.0 · KSP 2.3.6 · Hilt 2.59.2 · compileSdk 37 · minSdk 24 · Compose BOM 2025.09.01 · Navigation 3 1.2.0 · Room 2.8.3 · Turbine 1.2.0.

These are the same numbers as playbook Part 2. Change one, change the other in the same commit.

## Build it

```bash
cd starter
./gradlew testDebugUnitTest assembleDebug
```

Requires JDK 17+ and the Android SDK (`compileSdk 37`). CI installs both; locally, Android Studio's SDK is enough.

## Two deliberate simplifications

1. **The ViewModel is Activity-scoped**, obtained with `by viewModels()` and passed into the `NavDisplay` entry, rather than `hiltViewModel()` inside the entry. Navigation 3's entry-level ViewModel ownership is newer than Hilt's Compose integration; a one-screen starter does not need to prove that path, and a compile-green proof should not depend on it. Swap it when you have a second screen.
2. **`robolectric` is in the version catalog but not in `testImplementation`.** These tests are pure JVM. Robolectric 4.16 does not yet target `compileSdk 37`, and a fragile dependency in a build proof defeats the point. It is catalogued so the version stays pinned when you need it.
