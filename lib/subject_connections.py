import pandas as pd

class SubjectConnections(object):
    def __init__(self, base_df, base_column_id):
        self.base_df = base_df
        self.base_column_id = base_column_id

    def __extract_data_from_subject(self, base_df, subject_df, column_input, column_output):
        for i in base_df.index:
            base_value = base_df.loc[i, self.base_column_id]
            find_student = subject_df[self.base_column_id] == base_value
            student = subject_df[find_student]

            if(len(student.index) > 0):
                value = student.get_value(student.index[0], column_input)
                base_df.loc[i, column_output] = value

        return base_df

    def parse_column(self, input_col, output_col, func):
        additional_column = pd.Series(
            None,
            index = self.base_df.index,
            name  = output_col
        )
        self.base_df = self.base_df.join(additional_column)
        self.base_df[output_col] = self.base_df[input_col].apply(func)

    def obtain_values_from(self, subject_df, additional_column_name, columns_to_keep = []):
        connection_df = self.base_df[
            [self.base_column_id] + columns_to_keep
        ].copy()

        additional_column = pd.Series(
            None,
            index = connection_df.index,
            name  = additional_column_name
        )
        connection_df = connection_df.join(additional_column)

        connection_df = self.__extract_data_from_subject(
            connection_df, subject_df, 'Média Final', additional_column_name
        )

        connection_df.dropna(inplace = True)

        return connection_df
