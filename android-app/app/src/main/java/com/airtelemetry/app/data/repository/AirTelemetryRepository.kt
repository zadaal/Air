package com.airtelemetry.app.data.repository

import com.airtelemetry.app.BuildConfig
import com.airtelemetry.app.data.api.AirTelemetryApi
import com.airtelemetry.app.data.model.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Repository for accessing air telemetry data
 */
@Singleton
class AirTelemetryRepository @Inject constructor(
    private val api: AirTelemetryApi
) {
    private val authHeader = "ApiToken ${BuildConfig.API_TOKEN}"

    /**
     * Get all monitoring stations
     */
    suspend fun getStations(): Result<List<Station>> = withContext(Dispatchers.IO) {
        try {
            val response = api.getStations(authHeader)
            Result.success(response.data.filter { it.active })
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Get all stations including inactive ones
     */
    suspend fun getAllStations(): Result<List<Station>> = withContext(Dispatchers.IO) {
        try {
            val response = api.getStations(authHeader)
            Result.success(response.data)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Get specific station details
     */
    suspend fun getStation(stationId: Int): Result<Station> = withContext(Dispatchers.IO) {
        try {
            val response = api.getStation(authHeader, stationId = stationId)
            response.data.firstOrNull()?.let {
                Result.success(it)
            } ?: Result.failure(Exception("Station not found"))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Get latest readings from a station
     */
    suspend fun getStationLatestData(stationId: Int): Result<StationLatestData> = withContext(Dispatchers.IO) {
        try {
            val response = api.getStationLatestData(authHeader, stationId = stationId)
            Result.success(response.data)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Get processed readings for a station
     */
    suspend fun getStationReadings(stationId: Int): Result<List<Reading>> = withContext(Dispatchers.IO) {
        try {
            val response = api.getStationLatestData(authHeader, stationId = stationId)
            val readings = response.data.channels.map { channel ->
                Reading(
                    channelId = channel.id,
                    name = channel.name,
                    displayName = channel.alias ?: channel.name,
                    value = channel.value,
                    units = AirQualityThresholds.getDisplayUnits(channel.name, channel.units),
                    status = AirQualityThresholds.getStatus(channel.name, channel.value),
                    category = AirQualityThresholds.getCategory(channel.name),
                    description = AirQualityThresholds.getParameterDescription(channel.name)
                )
            }
            Result.success(readings)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Get latest data for multiple stations
     */
    suspend fun getMultipleStationsData(stationIds: List<Int>): Result<Map<Int, StationLatestData>> = withContext(Dispatchers.IO) {
        try {
            val dataMap = mutableMapOf<Int, StationLatestData>()
            stationIds.forEach { stationId ->
                try {
                    val response = api.getStationLatestData(authHeader, stationId = stationId)
                    dataMap[stationId] = response.data
                } catch (e: Exception) {
                    // Skip failed stations
                }
            }
            Result.success(dataMap)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
