package com.airtelemetry.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.airtelemetry.app.data.model.Reading
import com.airtelemetry.app.data.model.ReadingCategory
import com.airtelemetry.app.data.model.ReadingStatus
import com.airtelemetry.app.ui.theme.*

@Composable
fun ReadingCard(
    reading: Reading,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Status indicator
            Box(
                modifier = Modifier
                    .size(12.dp)
                    .clip(RoundedCornerShape(6.dp))
                    .background(reading.status.toColor())
            )

            Spacer(modifier = Modifier.width(12.dp))

            // Parameter info
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = reading.displayName,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Text(
                    text = reading.description,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }

            Spacer(modifier = Modifier.width(12.dp))

            // Value
            Column(horizontalAlignment = Alignment.End) {
                Text(
                    text = reading.value?.let { formatValue(it) } ?: "--",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    color = if (reading.value != null) reading.status.toColor() else MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = reading.units,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}

@Composable
fun ReadingStatusChip(
    status: ReadingStatus,
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier,
        color = status.toColor().copy(alpha = 0.15f),
        shape = RoundedCornerShape(16.dp)
    ) {
        Text(
            text = status.toDisplayString(),
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
            style = MaterialTheme.typography.labelMedium,
            color = status.toColor()
        )
    }
}

@Composable
fun CategoryFilterChip(
    category: ReadingCategory?,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    FilterChip(
        modifier = modifier,
        selected = selected,
        onClick = onClick,
        label = {
            Text(
                text = when (category) {
                    null -> "All"
                    ReadingCategory.AIR_QUALITY -> "Air Quality"
                    ReadingCategory.METEOROLOGICAL -> "Weather"
                }
            )
        }
    )
}

fun ReadingStatus.toColor(): Color {
    return when (this) {
        ReadingStatus.GOOD -> AqiGood
        ReadingStatus.MODERATE -> AqiModerate
        ReadingStatus.UNHEALTHY_SENSITIVE -> AqiUnhealthySensitive
        ReadingStatus.UNHEALTHY -> AqiUnhealthy
        ReadingStatus.VERY_UNHEALTHY -> AqiVeryUnhealthy
        ReadingStatus.HAZARDOUS -> AqiHazardous
        ReadingStatus.UNKNOWN -> AqiUnknown
    }
}

fun ReadingStatus.toDisplayString(): String {
    return when (this) {
        ReadingStatus.GOOD -> "Good"
        ReadingStatus.MODERATE -> "Moderate"
        ReadingStatus.UNHEALTHY_SENSITIVE -> "Unhealthy for Sensitive"
        ReadingStatus.UNHEALTHY -> "Unhealthy"
        ReadingStatus.VERY_UNHEALTHY -> "Very Unhealthy"
        ReadingStatus.HAZARDOUS -> "Hazardous"
        ReadingStatus.UNKNOWN -> "Unknown"
    }
}

private fun formatValue(value: Double): String {
    return if (value == value.toLong().toDouble()) {
        value.toLong().toString()
    } else {
        String.format("%.1f", value)
    }
}
