package com.airtelemetry.app.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.airtelemetry.app.ui.screens.stationdetail.StationDetailScreen
import com.airtelemetry.app.ui.screens.stations.StationsScreen

sealed class Screen(val route: String) {
    object Stations : Screen("stations")
    object StationDetail : Screen("station/{stationId}") {
        fun createRoute(stationId: Int) = "station/$stationId"
    }
}

@Composable
fun AirTelemetryNavigation(
    navController: NavHostController = rememberNavController()
) {
    NavHost(
        navController = navController,
        startDestination = Screen.Stations.route
    ) {
        composable(Screen.Stations.route) {
            StationsScreen(
                onStationClick = { stationId ->
                    navController.navigate(Screen.StationDetail.createRoute(stationId))
                }
            )
        }

        composable(
            route = Screen.StationDetail.route,
            arguments = listOf(
                navArgument("stationId") { type = NavType.IntType }
            )
        ) {
            StationDetailScreen(
                onBackClick = { navController.popBackStack() }
            )
        }
    }
}
