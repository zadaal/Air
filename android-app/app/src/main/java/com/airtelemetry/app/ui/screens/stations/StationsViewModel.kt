package com.airtelemetry.app.ui.screens.stations

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.airtelemetry.app.data.model.Station
import com.airtelemetry.app.data.repository.AirTelemetryRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class StationsUiState(
    val stations: List<Station> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val searchQuery: String = "",
    val showOnlyActive: Boolean = true
)

@HiltViewModel
class StationsViewModel @Inject constructor(
    private val repository: AirTelemetryRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(StationsUiState())
    val uiState: StateFlow<StationsUiState> = _uiState.asStateFlow()

    private var allStations: List<Station> = emptyList()

    init {
        loadStations()
    }

    fun loadStations() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }

            val result = if (_uiState.value.showOnlyActive) {
                repository.getStations()
            } else {
                repository.getAllStations()
            }

            result.fold(
                onSuccess = { stations ->
                    allStations = stations
                    _uiState.update {
                        it.copy(
                            stations = filterStations(stations, it.searchQuery),
                            isLoading = false,
                            error = null
                        )
                    }
                },
                onFailure = { e ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            error = e.message ?: "Failed to load stations"
                        )
                    }
                }
            )
        }
    }

    fun onSearchQueryChange(query: String) {
        _uiState.update {
            it.copy(
                searchQuery = query,
                stations = filterStations(allStations, query)
            )
        }
    }

    fun toggleShowOnlyActive() {
        _uiState.update { it.copy(showOnlyActive = !it.showOnlyActive) }
        loadStations()
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }

    private fun filterStations(stations: List<Station>, query: String): List<Station> {
        return if (query.isBlank()) {
            stations
        } else {
            stations.filter { station ->
                station.name.contains(query, ignoreCase = true) ||
                        station.shortName?.contains(query, ignoreCase = true) == true ||
                        station.regionName?.contains(query, ignoreCase = true) == true ||
                        station.stationId.toString().contains(query)
            }
        }
    }
}
