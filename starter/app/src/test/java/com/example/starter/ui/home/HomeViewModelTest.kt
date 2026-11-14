package com.example.starter.ui.home

import app.cash.turbine.test
import com.example.starter.data.Note
import com.example.starter.data.NoteRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.advanceUntilIdle
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Before
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class HomeViewModelTest {

    private val dispatcher = StandardTestDispatcher()

    @Before
    fun setUp() {
        Dispatchers.setMain(dispatcher)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `emits loading first, then the notes from the repository`() = runTest(dispatcher) {
        val repository = FakeNoteRepository(initial = listOf(Note(id = 1, text = "first")))
        val viewModel = HomeViewModel(repository)

        viewModel.uiState.test {
            assertEquals(HomeUiState(), awaitItem())

            val loaded = awaitItem()
            assertFalse(loaded.isLoading)
            assertEquals(1, loaded.notes.size)
            assertEquals("first", loaded.notes.first().text)

            cancelAndIgnoreRemainingEvents()
        }
    }

    @Test
    fun `adding a note writes through the repository and emits a one-shot effect`() = runTest(dispatcher) {
        val repository = FakeNoteRepository()
        val viewModel = HomeViewModel(repository)

        viewModel.effects.test {
            viewModel.onAddNote("  revise deck  ")
            advanceUntilIdle()

            assertEquals(HomeEffect.ShowMessage("Saved \"revise deck\""), awaitItem())
            assertEquals(listOf("revise deck"), repository.added)
            cancelAndIgnoreRemainingEvents()
        }
    }

    @Test
    fun `blank input is ignored`() = runTest(dispatcher) {
        val repository = FakeNoteRepository()
        val viewModel = HomeViewModel(repository)

        viewModel.onAddNote("   ")
        advanceUntilIdle()

        assertEquals(emptyList<String>(), repository.added)
    }
}

private class FakeNoteRepository(
    initial: List<Note> = emptyList(),
) : NoteRepository {

    private val notes = MutableStateFlow(initial)
    val added = mutableListOf<String>()

    override fun observeNotes(): Flow<List<Note>> = notes

    override suspend fun add(text: String) {
        added += text
        notes.value = notes.value + Note(id = (notes.value.size + 1).toLong(), text = text)
    }
}
