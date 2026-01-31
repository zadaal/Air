package com.airtelemetry.app.data.model

/**
 * Air quality thresholds based on Israeli/WHO standards
 * Values are in standard units (ug/m3 for most pollutants, mg/m3 for CO)
 */
object AirQualityThresholds {

    data class Threshold(
        val good: Double,
        val moderate: Double,
        val unhealthySensitive: Double,
        val unhealthy: Double,
        val veryUnhealthy: Double,
        val hazardous: Double
    )

    private val thresholds = mapOf(
        // PM2.5 (ug/m3) - 24hr average thresholds
        "PM2.5" to Threshold(12.0, 35.4, 55.4, 150.4, 250.4, 350.4),

        // PM10 (ug/m3) - 24hr average thresholds
        "PM10" to Threshold(54.0, 154.0, 254.0, 354.0, 424.0, 504.0),

        // O3 - Ozone (ppb) - 8hr average
        "O3" to Threshold(54.0, 70.0, 85.0, 105.0, 200.0, 300.0),

        // NO2 (ppb) - 1hr average
        "NO2" to Threshold(53.0, 100.0, 360.0, 649.0, 1249.0, 1649.0),

        // SO2 (ppb) - 1hr average
        "SO2" to Threshold(35.0, 75.0, 185.0, 304.0, 604.0, 804.0),

        // CO (ppm) - 8hr average
        "CO" to Threshold(4.4, 9.4, 12.4, 15.4, 30.4, 40.4),

        // NOX (ppb)
        "NOX" to Threshold(100.0, 200.0, 400.0, 600.0, 1000.0, 1500.0),

        // NO (ppb)
        "NO" to Threshold(50.0, 100.0, 200.0, 400.0, 800.0, 1200.0)
    )

    fun getStatus(parameterName: String, value: Double?): ReadingStatus {
        if (value == null || value < 0 || value == -9999.0) return ReadingStatus.UNKNOWN

        val normalizedName = normalizeParameterName(parameterName)
        val threshold = thresholds[normalizedName] ?: return ReadingStatus.UNKNOWN

        return when {
            value <= threshold.good -> ReadingStatus.GOOD
            value <= threshold.moderate -> ReadingStatus.MODERATE
            value <= threshold.unhealthySensitive -> ReadingStatus.UNHEALTHY_SENSITIVE
            value <= threshold.unhealthy -> ReadingStatus.UNHEALTHY
            value <= threshold.veryUnhealthy -> ReadingStatus.VERY_UNHEALTHY
            else -> ReadingStatus.HAZARDOUS
        }
    }

    private fun normalizeParameterName(name: String): String {
        return when {
            name.contains("PM2.5", ignoreCase = true) || name.contains("PM25", ignoreCase = true) -> "PM2.5"
            name.contains("PM10", ignoreCase = true) -> "PM10"
            name.contains("O3", ignoreCase = true) || name.contains("Ozone", ignoreCase = true) -> "O3"
            name.contains("NO2", ignoreCase = true) -> "NO2"
            name.contains("SO2", ignoreCase = true) -> "SO2"
            name.equals("CO", ignoreCase = true) -> "CO"
            name.contains("NOX", ignoreCase = true) || name.contains("NOx", ignoreCase = true) -> "NOX"
            name.equals("NO", ignoreCase = true) -> "NO"
            else -> name.uppercase()
        }
    }

    fun getCategory(parameterName: String): ReadingCategory {
        val meteorological = listOf("WS", "WD", "Temp", "Temperature", "RH", "Humidity", "Rain", "GSR", "StWd", "BP", "Pressure")
        return if (meteorological.any { parameterName.contains(it, ignoreCase = true) }) {
            ReadingCategory.METEOROLOGICAL
        } else {
            ReadingCategory.AIR_QUALITY
        }
    }

    fun getParameterDescription(parameterName: String): String {
        return when {
            parameterName.contains("PM2.5", ignoreCase = true) -> "Fine particulate matter (2.5 micrometers or smaller)"
            parameterName.contains("PM10", ignoreCase = true) -> "Coarse particulate matter (10 micrometers or smaller)"
            parameterName.contains("O3", ignoreCase = true) -> "Ozone - Ground level ozone"
            parameterName.contains("NO2", ignoreCase = true) -> "Nitrogen dioxide"
            parameterName.contains("SO2", ignoreCase = true) -> "Sulfur dioxide"
            parameterName.equals("CO", ignoreCase = true) -> "Carbon monoxide"
            parameterName.contains("NOX", ignoreCase = true) -> "Nitrogen oxides (total)"
            parameterName.equals("NO", ignoreCase = true) -> "Nitrogen monoxide"
            parameterName.contains("WS", ignoreCase = true) -> "Wind speed"
            parameterName.contains("WD", ignoreCase = true) -> "Wind direction"
            parameterName.contains("Temp", ignoreCase = true) -> "Temperature"
            parameterName.contains("RH", ignoreCase = true) -> "Relative humidity"
            parameterName.contains("Rain", ignoreCase = true) -> "Precipitation"
            parameterName.contains("GSR", ignoreCase = true) -> "Global solar radiation"
            parameterName.contains("BP", ignoreCase = true) -> "Barometric pressure"
            else -> parameterName
        }
    }

    fun getDisplayUnits(parameterName: String, originalUnits: String?): String {
        return originalUnits ?: when {
            parameterName.contains("PM", ignoreCase = true) -> "ug/m3"
            parameterName.contains("O3", ignoreCase = true) -> "ppb"
            parameterName.contains("NO", ignoreCase = true) -> "ppb"
            parameterName.contains("SO2", ignoreCase = true) -> "ppb"
            parameterName.equals("CO", ignoreCase = true) -> "ppm"
            parameterName.contains("WS", ignoreCase = true) -> "m/s"
            parameterName.contains("WD", ignoreCase = true) -> "deg"
            parameterName.contains("Temp", ignoreCase = true) -> "C"
            parameterName.contains("RH", ignoreCase = true) -> "%"
            parameterName.contains("Rain", ignoreCase = true) -> "mm"
            parameterName.contains("GSR", ignoreCase = true) -> "W/m2"
            else -> ""
        }
    }
}
