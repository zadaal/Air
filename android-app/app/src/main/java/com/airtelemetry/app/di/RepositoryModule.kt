package com.airtelemetry.app.di

import com.airtelemetry.app.data.api.AirTelemetryApi
import com.airtelemetry.app.data.repository.AirTelemetryRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {

    @Provides
    @Singleton
    fun provideAirTelemetryRepository(api: AirTelemetryApi): AirTelemetryRepository {
        return AirTelemetryRepository(api)
    }
}
