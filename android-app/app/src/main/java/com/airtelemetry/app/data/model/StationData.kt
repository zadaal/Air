package com.airtelemetry.app.data.model

import com.google.gson.annotations.SerializedName

/**
 * Response wrapper for station latest data
 */
data class StationDataResponse(
    @SerializedName("data")
    val data: StationLatestData
)

/**
 * Latest data from a station
 */
data class StationLatestData(
    @SerializedName("stationId")
    val stationId: Int,

    @SerializedName("datetime")
    val datetime: String,

    @SerializedName("channels")
    val channels: List<ChannelData>
)

/**
 * Data from a single channel/sensor
 */
data class ChannelData(
    @SerializedName("id")
    val id: Int,

    @SerializedName("name")
    val name: String,

    @SerializedName("alias")
    val alias: String? = null,

    @SerializedName("value")
    val value: Double?,

    @SerializedName("status")
    val status: Int? = null,

    @SerializedName("valid")
    val valid: Boolean? = true,

    @SerializedName("units")
    val units: String? = null
)

/**
 * Processed reading for display
 */
data class Reading(
    val channelId: Int,
    val name: String,
    val displayName: String,
    val value: Double?,
    val units: String,
    val status: ReadingStatus,
    val category: ReadingCategory,
    val description: String
)

/**
 * Status of a reading based on thresholds
 */
enum class ReadingStatus {
    GOOD,
    MODERATE,
    UNHEALTHY_SENSITIVE,
    UNHEALTHY,
    VERY_UNHEALTHY,
    HAZARDOUS,
    UNKNOWN
}

/**
 * Category of measurement
 */
enum class ReadingCategory {
    AIR_QUALITY,
    METEOROLOGICAL
}
