package com.example.starter.ui.home

import com.example.starter.data.Note

/** One immutable state object per screen. Partial state is impossible by construction. */
data class HomeUiState(
    val isLoading: Boolean = true,
    val notes: List<Note> = emptyList(),
    val errorMessage: String? = null,
)

/** One-shot effects live outside the state, so rotation cannot replay a navigation or a snackbar. */
sealed interface HomeEffect {
    data class ShowMessage(val text: String) : HomeEffect
}
