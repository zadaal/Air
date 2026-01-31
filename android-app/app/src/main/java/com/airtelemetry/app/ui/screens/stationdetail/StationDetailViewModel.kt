package com.airtelemetry.app.ui.screens.stationdetail

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.airtelemetry.app.data.model.Reading
import com.airtelemetry.app.data.model.ReadingCategory
import com.airtelemetry.app.data.model.Station
import com.airtelemetry.app.data.repository.AirTelemetryRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class StationDetailUiState(
    val station: Station? = null,
    val readings: List<Reading> = emptyList(),
    val lastUpdated: String? = null,
    val isLoading: Boolean = false,
    val error: String? = null,
    val selectedCategory: ReadingCategory? = null
)

@HiltViewModel
class StationDetailViewModel @Inject constructor(
    private val repository: AirTelemetryRepository,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val stationId: Int = checkNotNull(savedStateHandle["stationId"])

    private val _uiState = MutableStateFlow(StationDetailUiState())
    val uiState: StateFlow<StationDetailUiState> = _uiState.asStateFlow()

    private var allReadings: List<Reading> = emptyList()

    init {
        loadStationData()
    }

    fun loadStationData() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }

            // Load station info
            val stationResult = repository.getStation(stationId)
            stationResult.fold(
                onSuccess = { station ->
                    _uiState.update { it.copy(station = station) }
                },
                onFailure = { /* Handle silently, we'll still try to get readings */ }
            )

            // Load latest readings
            val dataResult = repository.getStationLatestData(stationId)
            dataResult.fold(
                onSuccess = { data ->
                    _uiState.update { it.copy(lastUpdated = data.datetime) }
                },
                onFailure = { /* Continue */ }
            )

            // Load processed readings
            val readingsResult = repository.getStationReadings(stationId)
            readingsResult.fold(
                onSuccess = { readings ->
                    allReadings = readings
                    _uiState.update {
                        it.copy(
                            readings = filterReadings(readings, it.selectedCategory),
                            isLoading = false,
                            error = null
                        )
                    }
                },
                onFailure = { e ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            error = e.message ?: "Failed to load station data"
                        )
                    }
                }
            )
        }
    }

    fun onCategorySelected(category: ReadingCategory?) {
        _uiState.update {
            it.copy(
                selectedCategory = category,
                readings = filterReadings(allReadings, category)
            )
        }
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }

    private fun filterReadings(readings: List<Reading>, category: ReadingCategory?): List<Reading> {
        return if (category == null) {
            readings
        } else {
            readings.filter { it.category == category }
        }
    }
}
