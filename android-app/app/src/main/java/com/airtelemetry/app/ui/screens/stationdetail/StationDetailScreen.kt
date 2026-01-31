package com.airtelemetry.app.ui.screens.stationdetail

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.ExperimentalMaterialApi
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.pullrefresh.PullRefreshIndicator
import androidx.compose.material.pullrefresh.pullRefresh
import androidx.compose.material.pullrefresh.rememberPullRefreshState
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.airtelemetry.app.data.model.ReadingCategory
import com.airtelemetry.app.ui.components.*

@OptIn(ExperimentalMaterial3Api::class, ExperimentalMaterialApi::class)
@Composable
fun StationDetailScreen(
    onBackClick: () -> Unit,
    viewModel: StationDetailViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val pullRefreshState = rememberPullRefreshState(
        refreshing = uiState.isLoading,
        onRefresh = { viewModel.loadStationData() }
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        text = uiState.station?.name ?: "Station Details",
                        fontWeight = FontWeight.Bold
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(
                            imageVector = Icons.Default.ArrowBack,
                            contentDescription = "Back"
                        )
                    }
                },
                actions = {
                    IconButton(onClick = { viewModel.loadStationData() }) {
                        Icon(
                            imageVector = Icons.Default.Refresh,
                            contentDescription = "Refresh"
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary,
                    navigationIconContentColor = MaterialTheme.colorScheme.onPrimary,
                    actionIconContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .pullRefresh(pullRefreshState)
        ) {
            when {
                uiState.isLoading && uiState.readings.isEmpty() -> {
                    LoadingScreen()
                }
                uiState.error != null && uiState.readings.isEmpty() -> {
                    ErrorScreen(
                        message = uiState.error!!,
                        onRetry = { viewModel.loadStationData() }
                    )
                }
                else -> {
                    LazyColumn(
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        // Station header
                        uiState.station?.let { station ->
                            item {
                                StationHeader(station = station)
                            }
                        }

                        // Last updated
                        uiState.lastUpdated?.let { lastUpdated ->
                            item {
                                Text(
                                    text = "Last updated: $lastUpdated",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }

                        // Category filters
                        item {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .horizontalScroll(rememberScrollState()),
                                horizontalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                CategoryFilterChip(
                                    category = null,
                                    selected = uiState.selectedCategory == null,
                                    onClick = { viewModel.onCategorySelected(null) }
                                )
                                CategoryFilterChip(
                                    category = ReadingCategory.AIR_QUALITY,
                                    selected = uiState.selectedCategory == ReadingCategory.AIR_QUALITY,
                                    onClick = { viewModel.onCategorySelected(ReadingCategory.AIR_QUALITY) }
                                )
                                CategoryFilterChip(
                                    category = ReadingCategory.METEOROLOGICAL,
                                    selected = uiState.selectedCategory == ReadingCategory.METEOROLOGICAL,
                                    onClick = { viewModel.onCategorySelected(ReadingCategory.METEOROLOGICAL) }
                                )
                            }
                        }

                        // Readings section header
                        item {
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = "Current Readings",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.SemiBold
                            )
                        }

                        // Readings list
                        if (uiState.readings.isEmpty()) {
                            item {
                                Text(
                                    text = "No readings available",
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        } else {
                            items(
                                items = uiState.readings,
                                key = { it.channelId }
                            ) { reading ->
                                ReadingCard(reading = reading)
                            }
                        }

                        // Air Quality Legend
                        item {
                            Spacer(modifier = Modifier.height(16.dp))
                            AirQualityLegend()
                        }
                    }
                }
            }

            PullRefreshIndicator(
                refreshing = uiState.isLoading,
                state = pullRefreshState,
                modifier = Modifier.align(Alignment.TopCenter),
                contentColor = MaterialTheme.colorScheme.primary
            )
        }
    }
}

@Composable
fun AirQualityLegend() {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
        )
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = "Air Quality Index Legend",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold
            )
            Spacer(modifier = Modifier.height(12.dp))

            LegendItem(
                status = com.airtelemetry.app.data.model.ReadingStatus.GOOD,
                label = "Good - Air quality is satisfactory"
            )
            LegendItem(
                status = com.airtelemetry.app.data.model.ReadingStatus.MODERATE,
                label = "Moderate - Acceptable air quality"
            )
            LegendItem(
                status = com.airtelemetry.app.data.model.ReadingStatus.UNHEALTHY_SENSITIVE,
                label = "Unhealthy for Sensitive Groups"
            )
            LegendItem(
                status = com.airtelemetry.app.data.model.ReadingStatus.UNHEALTHY,
                label = "Unhealthy - Health effects possible"
            )
            LegendItem(
                status = com.airtelemetry.app.data.model.ReadingStatus.VERY_UNHEALTHY,
                label = "Very Unhealthy - Health alert"
            )
            LegendItem(
                status = com.airtelemetry.app.data.model.ReadingStatus.HAZARDOUS,
                label = "Hazardous - Emergency conditions"
            )
        }
    }
}

@Composable
private fun LegendItem(
    status: com.airtelemetry.app.data.model.ReadingStatus,
    label: String
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Surface(
            modifier = Modifier.size(16.dp),
            color = status.toColor(),
            shape = MaterialTheme.shapes.small
        ) {}
        Spacer(modifier = Modifier.width(12.dp))
        Text(
            text = label,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
