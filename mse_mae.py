simplified_rf_pipeline = Pipeline([
    ('preprocessor', column_transformer),
    ('imputer', imputer),
    ('regressor', RandomForestRegressor(n_estimators=10, random_state=42))  # Reduced from 100 to 10
])

simplified_rf_pipeline.fit(X_train_5, y_train_5)
predictions_rf_5_simplified = simplified_rf_pipeline.predict(X_test_5)
mse_rf_5_simplified = mean_squared_error(y_test_5, predictions_rf_5_simplified)
mae_rf_5_simplified = mean_absolute_error(y_test_5, predictions_rf_5_simplified)

simplified_rf_pipeline.fit(X_train_7, y_train_7)
predictions_rf_7_simplified = simplified_rf_pipeline.predict(X_test_7)
mse_rf_7_simplified = mean_squared_error(y_test_7, predictions_rf_7_simplified)
mae_rf_7_simplified = mean_absolute_error(y_test_7, predictions_rf_7_simplified)

simplified_rf_metrics = {
    'Model': 'Simplified Random Forest',
    'MSE 5-Day': [mse_rf_5_simplified],
    'MAE 5-Day': [mae_rf_5_simplified],
    'MSE 7-Day': [mse_rf_7_simplified],
    'MAE 7-Day': [mae_rf_7_simplified]
}

pd.DataFrame(simplified_rf_metrics)
