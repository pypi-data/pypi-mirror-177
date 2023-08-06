import re
import pyreadstat
import pandas as pd
from typing import Union


class MetaTable:
    def __init__(self, df: pd.DataFrame, meta: pyreadstat._readstat_parser.metadata_container) -> None:
        """creates MetaTable object that makes data wrangling of files read with pyreadstat easy

        Args:
            df (pd.DataFrame): DataFrame read with pyreadstat
            meta (pyreadstat._readstat_parser.metadata_container): pyreadstat metadata
        """
        self.df = df
        self.meta = meta

    def select_columns(self, columns: list):
        """selects the given columns and removes all others.

        Args:
            columns (list): Columns to select
        """
        column_indexes = [i for i, v in enumerate(self.meta.column_names) if v in columns]
        column_labels = [v for i, v in enumerate(self.meta.column_labels) if i in column_indexes]

        self.meta.column_labels = column_labels
        self.meta.column_names = columns
        self.meta.column_names_to_labels = {key: value for key, value in zip(columns, column_labels)}
        self.meta.original_variable_types = {
            key: value for key, value in self.meta.original_variable_types.items() if key in columns}
        self.meta.readstat_variable_types = {
            key: value for key, value in self.meta.readstat_variable_types.items() if key in columns}
        self.meta.variable_alignment = {
            key: value for key, value in self.meta.variable_alignment.items() if key in columns}
        self.meta.variable_display_width = {
            key: value for key, value in self.meta.variable_display_width.items() if key in columns}
        self.meta.variable_measure = {
            key: value for key, value in self.meta.variable_measure.items() if key in columns}
        self.meta.variable_storage_width = {
            key: value for key, value in self.meta.variable_storage_width.items() if key in columns}
        self.meta.variable_to_label = {
            key: value for key, value in self.meta.variable_to_label.items() if key in columns}
        self.meta.variable_value_labels = {
            key: value for key, value in self.meta.variable_value_labels.items() if key in columns}

        labels = set(self.meta.variable_to_label.values())
        self.meta.value_labels = {
            key: value for key, value in self.meta.value_labels.items() if key in labels}

        self.meta.number_columns = len(columns)
        self.df = self.df[columns]

    def val_lab(self, columns: list[str], labels: Union[dict[int, str], str]):
        """Changes the value labels of the given columns

        Args:
            columns (list[str]): A list of columns that need new value labels
            labels (Union[dict[int, str], str]): A dictionary with new labels \
{1 : "label for code 1", 2: "label for code 2"} or the variable name with the labels to be used "variable_name"
        """
        # my_indexes = [i for i, v in enumerate(self.meta.column_names) if v in columns]

        # if string use labels of other variables, else use the given labels
        if isinstance(labels, str):
            labels = self.meta.variable_value_labels[labels]

        # find correct label name
        used = set([int(re.findall(r'\d+', v)[-1]) for v in list(self.meta.variable_to_label.values())])
        all = range(len(used) + 1)
        label_name = f'labels{min(set(all) - used)}'

        for column in columns:
            self.meta.original_variable_types[column] = 'F10.0'
            self.meta.readstat_variable_types[column] = 'double'
            self.meta.variable_measure[column] = 'nominal'
            self.meta.variable_to_label[column] = label_name
            self.meta.variable_value_labels[column] = labels

        self.meta.value_labels[label_name] = labels

    def var_lab(self, columns: list[str], text: str):
        """Changes the variable labels of the given columns

        Args:
            columns (list[str]): A list of columns that need a new variable label
            text (str): Text of the variable label
        """
        my_indexes = [i for i, v in enumerate(self.meta.column_names) if v in columns]

        for column in columns:
            self.meta.column_names_to_labels[column] = text

        for i in my_indexes:
            self.meta.column_labels[i] = text

    def show(self, variable: str):
        """Shows info about the value labels and variable label of the given variable

        Args:
            variable (str): Variable to be shown
        """
        print(self.meta.column_names_to_labels[variable])

        print('')
        value_labels = self.meta.variable_value_labels[variable]
        for key, value in value_labels.items():
            print(f'{key: >12}   {value}')

        print('')
        print(list(value_labels.keys()))
        print(list(value_labels.values()))

    def write_sav(self, path: str):
        """Writes a sav file of the MetaTable object which includes a Dataframe and the metadata.

        Args:
            path (str): Path of the new file, includes the file name. To save the file in the package directory use \
"./filename.sav"
        """
        pyreadstat.write_sav(
            df=self.df,
            dst_path=path,
            column_labels=self.meta.column_labels,
            variable_value_labels=dict(self.meta.variable_value_labels),
            variable_measure=self.meta.variable_measure,
        )

    def return_components(self) -> tuple[pd.DataFrame, pyreadstat._readstat_parser.metadata_container]:
        """Returns the updated DataFrame and metadata that are contained within the object

        Returns:
            tuple[pd.DataFrame, pyreadstat._readstat_parser.metadata_container]: returns tuple with objects
        """
        return self.df, self.meta


if __name__ == '__main__':
    df1, meta1 = pyreadstat.read_sav('./data/fertig_R.sav')

    print(meta1.column_names_to_labels['F5_01'])
    print(meta1.variable_value_labels['F5_01'])

    x = MetaTable(df1, meta1)

    x.val_lab(['F5_03', 'F5_04'], 'F1_01')
    x.show('F5_03')

    x.val_lab(['F5_01', 'F5_02'], {1: 'Fish', 2: 'Chips'})
    x.var_lab(['F5_01', 'F5_02'], 'New Label')

    x.select_columns(['F5_01', 'F5_02', 'F5_03', 'F5_04'])
    x.show('F5_01')

    df, meta = x.return_components()

    x.write_sav('./data/fertig_test.sav')
