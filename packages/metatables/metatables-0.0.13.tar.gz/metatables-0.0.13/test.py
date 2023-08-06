import pyreadstat
from metatables import MetaTable

if __name__ == '__main__':
    df1, meta1 = pyreadstat.read_sav('./data/fertig_R.sav')

    print(meta1.column_names_to_labels['F5_01'])
    print(meta1.variable_value_labels['F5_01'])

    x = MetaTable(df1, meta1)
    x.val_lab(['F5_01', 'F5_02'], {1: 'Fish', 2: 'Chips'})
    x.var_lab(['F5_01', 'F5_02'], 'New Label')
    x.select_columns(['F5_01', 'F5_02'])
    x.show('F5_01')
    x.write_sav('./data/fertig_test.sav')
