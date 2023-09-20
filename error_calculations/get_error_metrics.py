from .error_metrics_builder import ErrorMetricsBuilder

def get_error_metrics(dataframe_of_3d_data):
    error_metrics_builder = ErrorMetricsBuilder(dataframe_of_3d_data=dataframe_of_3d_data)

    return (error_metrics_builder.calculate_squared_error_dataframe(dataframe_of_3d_data=dataframe_of_3d_data)
                                                .calculate_absolute_error_from_squared_error_dataframe()
                                                .calculate_rmse_from_dataframe()
                                                .build())
