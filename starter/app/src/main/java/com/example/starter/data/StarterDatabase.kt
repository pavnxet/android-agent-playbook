package com.example.starter.data

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(entities = [NoteEntity::class], version = 1, exportSchema = false)
abstract class StarterDatabase : RoomDatabase() {
    abstract fun noteDao(): NoteDao
}
