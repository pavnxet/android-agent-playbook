package com.example.starter.ui.navigation

import androidx.navigation3.runtime.NavKey

/**
 * Navigation 3 routes are plain [NavKey] objects - the back stack is data, not a graph.
 * A `@Serializable` key is only required when you use `rememberNavBackStack` (process-death
 * restoration); this starter keeps the back stack in `remember` to stay dependency-light.
 */
data object HomeKey : NavKey
