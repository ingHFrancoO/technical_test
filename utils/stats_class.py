class StatisticsManager:
    """
    Class to manage statistics in memory.

    This class keeps track of minimum, maximum, total sum, and count of values
    to calculate aggregate statistics like average in real-time.
    """
    def __init__(self):
        """
        Initialize the StatisticsManager with default values:
            - min_value: Set to positive infinity for comparison.
            - max_value: Set to negative infinity for comparison.
            - total_sum: Accumulates the sum of all values.
            - record_count: Counts the number of records processed.
        """
        self.min_value = float('inf')  # Smallest value encountered.
        self.max_value = float('-inf')  # Largest value encountered.
        self.total_sum = 0.0  # Sum of all values processed.
        self.record_count = 0  # Number of values processed.

    def update_statistics(self, new_value: float):
        """
        Update the global statistics with a new value.

        Args:
            new_value (float): The new value to include in the statistics.
        
        Updates:
            - `min_value` to the smaller of the current or new value.
            - `max_value` to the larger of the current or new value.
            - `total_sum` by adding the new value.
            - `record_count` by incrementing it by 1.
        """
        self.min_value = min(self.min_value, new_value)  # Update minimum value.
        self.max_value = max(self.max_value, new_value)  # Update maximum value.
        self.total_sum += new_value  # Add to total sum.
        self.record_count += 1  # Increment the count of records.

    def get_statistics(self) -> dict:
        """
        Retrieve the current statistics.

        Returns:
            dict: A dictionary containing:
                - `min`: Minimum value encountered (None if no records).
                - `max`: Maximum value encountered (None if no records).
                - `average`: Average of all values (None if no records).
                - `record_count`: Total number of values processed.

        Notes:
            - If no values have been processed, returns default values with None
                for min, max, and average, and 0 for record_count.
        """
        if self.record_count == 0:
            # No records processed; return default values.
            return {
                'min': None,
                'max': None,
                'average': None,
                'record_count': 0
            }
        
        # Calculate and return statistics with rounded values.
        return {
            'min': round(self.min_value, 2),  # Round min to 2 decimal places.
            'max': round(self.max_value, 2),  # Round max to 2 decimal places.
            'average': round(self.total_sum / self.record_count, 2),  # Calculate and round average.
            'record_count': self.record_count  # Total records processed.
        }
