package com.example.starter.di

import android.content.Context
import androidx.room.Room
import com.example.starter.data.NoteDao
import com.example.starter.data.NoteRepository
import com.example.starter.data.OfflineFirstNoteRepository
import com.example.starter.data.StarterDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Qualifier
import javax.inject.Singleton
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers

/** Injected, never referenced inline - a hardcoded Dispatchers.IO is the top cause of flaky tests. */
@Qualifier
@Retention(AnnotationRetention.RUNTIME)
annotation class IoDispatcher

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @IoDispatcher
    fun provideIoDispatcher(): CoroutineDispatcher = Dispatchers.IO

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): StarterDatabase =
        Room.databaseBuilder(context, StarterDatabase::class.java, "starter.db").build()

    @Provides
    fun provideNoteDao(database: StarterDatabase): NoteDao = database.noteDao()

    @Provides
    @Singleton
    fun provideNoteRepository(
        dao: NoteDao,
        @IoDispatcher io: CoroutineDispatcher,
    ): NoteRepository = OfflineFirstNoteRepository(dao = dao, io = io)
}
