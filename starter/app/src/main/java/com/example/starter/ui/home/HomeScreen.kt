package com.example.starter.ui.home

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.starter.data.Note

/**
 * Stateless content composable: it takes data and callbacks, holds nothing that survives
 * recomposition except throwaway UI state, and is therefore previewable and testable.
 */
@Composable
fun HomeScreen(
    uiState: HomeUiState,
    onAddNote: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    var draft by rememberSaveable { mutableStateOf("") }

    Scaffold(modifier = modifier.fillMaxSize()) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Text(text = "Starter", style = MaterialTheme.typography.headlineMedium)

            OutlinedTextField(
                value = draft,
                onValueChange = { draft = it },
                label = { Text("New note") },
                modifier = Modifier.fillMaxWidth(),
            )

            Button(
                onClick = {
                    onAddNote(draft)
                    draft = ""
                },
                modifier = Modifier.fillMaxWidth(),
            ) {
                Text("Save")
            }

            when {
                uiState.isLoading -> CircularProgressIndicator()
                uiState.errorMessage != null -> Text(
                    text = uiState.errorMessage,
                    color = MaterialTheme.colorScheme.error,
                )
                uiState.notes.isEmpty() -> Text("No notes yet. Add one above.")
                else -> LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    items(items = uiState.notes, key = { it.id }) { note ->
                        NoteRow(note = note)
                    }
                }
            }
        }
    }
}

@Composable
private fun NoteRow(note: Note, modifier: Modifier = Modifier) {
    Text(text = note.text, style = MaterialTheme.typography.bodyLarge, modifier = modifier)
}

@Preview(showBackground = true)
@Composable
private fun HomeScreenPreview() {
    MaterialTheme {
        HomeScreen(
            uiState = HomeUiState(
                isLoading = false,
                notes = listOf(Note(id = 1, text = "Revise FSRS deck"), Note(id = 2, text = "Ship the playbook")),
            ),
            onAddNote = {},
        )
    }
}
