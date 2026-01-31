package com.airtelemetry.app.data.api

import com.airtelemetry.app.data.model.StationDataResponse
import com.airtelemetry.app.data.model.StationsResponse
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Path

/**
 * Retrofit API interface for MANA Air Quality API
 */
interface AirTelemetryApi {

    /**
     * Get all monitoring stations
     */
    @GET("stations")
    suspend fun getStations(
        @Header("Authorization") authorization: String,
        @Header("envi-data-source") dataSource: String = "MANA"
    ): StationsResponse

    /**
     * Get specific station details
     */
    @GET("stations/{stationId}")
    suspend fun getStation(
        @Header("Authorization") authorization: String,
        @Header("envi-data-source") dataSource: String = "MANA",
        @Path("stationId") stationId: Int
    ): StationsResponse

    /**
     * Get latest data for a station
     */
    @GET("stations/{stationId}/data/latest")
    suspend fun getStationLatestData(
        @Header("Authorization") authorization: String,
        @Header("envi-data-source") dataSource: String = "MANA",
        @Path("stationId") stationId: Int
    ): StationDataResponse
}
