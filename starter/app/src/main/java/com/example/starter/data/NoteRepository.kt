package com.example.starter.data

import com.example.starter.di.IoDispatcher
import javax.inject.Inject
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.withContext

/** The only path to data. Screens and ViewModels never touch a DAO. */
interface NoteRepository {
    fun observeNotes(): Flow<List<Note>>
    suspend fun add(text: String)
}

class OfflineFirstNoteRepository @Inject constructor(
    private val dao: NoteDao,
    @IoDispatcher private val io: CoroutineDispatcher,
) : NoteRepository {

    override fun observeNotes(): Flow<List<Note>> =
        dao.observeAll().map { rows -> rows.map { Note(id = it.id, text = it.text) } }

    override suspend fun add(text: String) = withContext(io) {
        dao.insert(NoteEntity(text = text))
    }
}
