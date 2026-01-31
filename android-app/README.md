# Air Telemetry Android App

An Android application for viewing real-time air quality telemetry data from monitoring stations.

## Features

- View list of all active air monitoring stations
- Search stations by name, region, or ID
- View detailed current readings for each station
- Color-coded air quality status indicators
- Filter readings by category (Air Quality / Meteorological)
- Pull-to-refresh for latest data
- Material Design 3 UI with dark mode support

## Air Quality Parameters

The app displays the following air quality measurements:
- **PM2.5** - Fine particulate matter
- **PM10** - Coarse particulate matter
- **O3** - Ozone
- **NO2** - Nitrogen dioxide
- **SO2** - Sulfur dioxide
- **CO** - Carbon monoxide
- **NOX** - Nitrogen oxides
- **NO** - Nitrogen monoxide

## Meteorological Parameters

- Wind speed and direction
- Temperature
- Relative humidity
- Precipitation
- Solar radiation

## Technical Stack

- **Kotlin** - Primary language
- **Jetpack Compose** - Modern UI toolkit
- **Material Design 3** - UI design system
- **Hilt** - Dependency injection
- **Retrofit** - Network calls
- **Coroutines & Flow** - Asynchronous programming
- **MVVM Architecture** - Clean architecture pattern

## API

The app connects to the Israeli Ministry of Environmental Protection (MANA) Air Quality API:
- Base URL: `https://air-api.sviva.gov.il/v1/envista/`

## Building

1. Open the project in Android Studio
2. Sync Gradle dependencies
3. Build and run on device/emulator (minimum API 26)

## Project Structure

```
app/src/main/java/com/airtelemetry/app/
├── data/
│   ├── api/           # Retrofit API interfaces
│   ├── model/         # Data classes
│   └── repository/    # Data repository
├── di/                # Hilt modules
└── ui/
    ├── components/    # Reusable composables
    ├── navigation/    # Navigation setup
    ├── screens/       # Screen composables
    └── theme/         # Material theme
```

## Air Quality Index Scale

| Level | Color | Description |
|-------|-------|-------------|
| Good | Green | Air quality is satisfactory |
| Moderate | Yellow | Acceptable air quality |
| Unhealthy for Sensitive | Orange | Sensitive groups may experience effects |
| Unhealthy | Red | Health effects possible for everyone |
| Very Unhealthy | Purple | Health alert |
| Hazardous | Maroon | Emergency conditions |
