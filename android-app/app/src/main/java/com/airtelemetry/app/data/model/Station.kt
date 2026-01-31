package com.airtelemetry.app.data.model

import com.google.gson.annotations.SerializedName

/**
 * Response wrapper for list of stations
 */
data class StationsResponse(
    @SerializedName("data")
    val data: List<Station>
)

/**
 * Represents an air monitoring station
 */
data class Station(
    @SerializedName("stationId")
    val stationId: Int,

    @SerializedName("name")
    val name: String,

    @SerializedName("shortName")
    val shortName: String? = null,

    @SerializedName("location")
    val location: Location? = null,

    @SerializedName("timebase")
    val timebase: Int? = null,

    @SerializedName("active")
    val active: Boolean = true,

    @SerializedName("owner")
    val owner: String? = null,

    @SerializedName("regionId")
    val regionId: Int? = null,

    @SerializedName("regionName")
    val regionName: String? = null,

    @SerializedName("monitors")
    val monitors: List<Monitor>? = null
)

/**
 * Station geographic location
 */
data class Location(
    @SerializedName("latitude")
    val latitude: Double?,

    @SerializedName("longitude")
    val longitude: Double?
)

/**
 * Monitor/channel at a station
 */
data class Monitor(
    @SerializedName("channelId")
    val channelId: Int,

    @SerializedName("name")
    val name: String,

    @SerializedName("alias")
    val alias: String? = null,

    @SerializedName("active")
    val active: Boolean = true,

    @SerializedName("units")
    val units: String? = null,

    @SerializedName("description")
    val description: String? = null
)
