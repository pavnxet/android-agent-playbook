package com.example.starter.ui.home

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import kotlinx.coroutines.flow.collectLatest

/**
 * Stateful route composable: it owns the ViewModel subscription and passes plain data down.
 * Effects are consumed here, never inside the stateless content composable.
 */
@Composable
fun HomeRoute(
    viewModel: HomeViewModel,
    onEffect: (HomeEffect) -> Unit = {},
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(viewModel) {
        viewModel.effects.collectLatest(onEffect)
    }

    HomeScreen(uiState = uiState, onAddNote = viewModel::onAddNote)
}
