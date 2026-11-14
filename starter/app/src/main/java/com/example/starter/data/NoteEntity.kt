package com.example.starter.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "notes")
data class NoteEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val text: String,
)

/** Domain model. Room entities never leave the data layer. */
data class Note(val id: Long, val text: String)
