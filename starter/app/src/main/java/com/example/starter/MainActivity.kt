package com.example.starter

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.remember
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation3.runtime.NavKey
import androidx.navigation3.runtime.entryProvider
import androidx.navigation3.ui.NavDisplay
import com.example.starter.ui.home.HomeRoute
import com.example.starter.ui.home.HomeViewModel
import com.example.starter.ui.navigation.HomeKey
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    private val homeViewModel: HomeViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                StarterApp(homeViewModel = homeViewModel)
            }
        }
    }
}

@Composable
private fun StarterApp(homeViewModel: HomeViewModel) {
    // The back stack is data. Swap this for rememberNavBackStack(...) once the keys are
    // @Serializable and you want process-death restoration.
    val backStack = remember { mutableStateListOf<NavKey>(HomeKey) }

    NavDisplay(
        backStack = backStack,
        onBack = { backStack.removeLastOrNull() },
        entryProvider = entryProvider {
            entry<HomeKey> {
                HomeRoute(viewModel = homeViewModel)
            }
        },
    )
}
