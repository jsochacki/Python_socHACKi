"""
Author: John Sochacki
This module is a collection of static and class methods that are used for
making working with pandas data frames more simple.
"""
import pandas as pd


class SKungFu(object):

    def __init__(self):
        pass

    def PackageIdentification(self):
        return 'SKungFu'

    def ArgKwargViewer(self, *args, **kwargs):
        # print(len(args))
        return(args, kwargs)
        # return(args[0])
        # return(kwargs)

    @staticmethod
    def PandasSeriesCellIndiciesBasedOnString(ps, STRING_VAL):
        """
        This function does a simple list comprehension comparison and returns
        the indicies for whom which the comparison results in true

        Parameters
        ----------
            ps : pandas.core.series
                 Pandas Series Object
            STRING_VAL : string
                         The string in the Series that the user wants the index
                         locations for

        kwargs
        ------
        NONE

        Example
        -------
        >>> import pandas as pd
        >>> pseries=pd.Series(['there','there','now','child'])
        >>> PandasSeriesCellIndiciesBasedOnString(pseries,'there')
        [0, 1]

        """
        try:
            assert isinstance(ps, pd.Series)
        except AttributeError as e:
            print(e)
            print('You are seeing this error because the item you provided is'
                  ' of type {} but must be of type {}'.format(
                      type(ps), type(pd.Series())))
        except KeyError as e:
            print(e)
            print('You are seeing this error because the item you provided is'
                  ' of type {} but must be of type {}'.format(
                      type(ps), type(pd.Series())))
        else:
            return [index for index, value in enumerate(ps)
                    if ps.astype(str) [index].lower() == STRING_VAL.lower()]

    @classmethod
    def PandasCellIndicies(cls, *args, **kwargs):
        """
        This function take in a pandas data frame.  By default it will return
        the indicies of the cells that contain nan values in the first column.
        Through the kwargs you can change this.

        Parameters
        ----------
        pd : pandas.core.frame
             Pandas DataFrame Object passed in throught args[0]
             i.e. the leftmost argurment

        kwargs:
        ------
            string_value :  string
                            sets the string that the function
                            will drop rows when contained
            column_number : int NOT float
                            sets the column number to search
                            for string_value or 'nan'
            column_name :   string
                            sets the column name to search
                            for string_value or 'nan'

        Example
        -------
        >>> import pandas as pd
        >>> dframe=pd.DataFrame({'a':['hi','nan',float('nan'),float('nan')]
                                 ,'b':['hi','there','good','looking']})
        >>> SKungFu.PandasCellIndicies(dframe)
        [1, 2, 3]
        >>> SKungFu.PandasCellIndicies(dframe,string_value='nan')
        [1, 2, 3]
        >>> SKungFu.PandasCellIndicies(dframe,column_name='b',
        ...                            string_value='there')
        [1]

        Warning
        --------
        If you dont pass in any key words the default behavior is to drop
        all rows that contain nan in the first column

        Also, if specifying keyword argurments
        please either specify column_name or column_number but not both.
        """
        if len(args) != 1:
            raise TypeError('PandasCellIndicies expected 1 arguement and'
                            ' 0 - 3 Keywords, got {} and {}'.format(
                                len(args), len(kwargs)))
        else:
            pdf = args[0]

        try:
            assert isinstance(pdf, pd.DataFrame)
        except AssertionError as e:
            print(e)
            print('You are seeing this error because the item you provided is'
                  ' of type {} but must be of type {}'.format(
                      type(pdf), type(pd.DataFrame())))
        else:
            if 'string_value' in kwargs:
                if 'column_number' in kwargs:
                    ps = pdf[pdf.columns[kwargs['column_number']]]
                elif 'column_name' in kwargs:
                    ps = pdf[kwargs['column_name']]
                else:
                    ps = pdf[pdf.columns[0]]
                return cls.PandasSeriesCellIndiciesBasedOnString(
                                             ps, kwargs['string_value'])
            else:
                if 'column_number' in kwargs:
                    ps = pdf[pdf.columns[kwargs['column_number']]]
                elif 'column_name' in kwargs:
                    ps = pdf[kwargs['column_name']]
                else:
                    ps = pdf[pdf.columns[0]]
                return cls.PandasSeriesCellIndiciesBasedOnString(ps, 'nan')

    @staticmethod
    def PandasDropAndFormat(*args, **kwargs):
        """
        This function takes in a pandas data frame.
        By default it drops all rows whos indicies correspond to the values in
        the provided list in args[1], the second function arguement provided.
        The values can be indicies or names of cells.
        Through the kwargs you can change this.

        kwargs:
        ------
            columns : bool
                     if True specifies that columns whos indicies correspond
                     to the values in the provided list in args[1], the second
                     function arguement provided are to be dropped rather
                     than rows, by default this is False.

        Example
        -------
        >>> import pandas as pd
        >>> dframe=pd.DataFrame({'a':['hi','nan',float('nan'),float('nan')]
                                 ,'b':['hi','there','good','looking']})
        >>> SKungFu.PandasDropAndFormat(dframe,[0, 1])
           a       b
        0  NaN     good
        1  NaN     looking
        >>> SKungFu.PandasDropAndFormat(dframe,['a'],columns=True)
           b
        0  good
        1  looking

        Warning
        --------

        If no keyword arguements are provided the method assumes that you
        are passing in column indicies as ints and NOT as strings
        """
        if len(args) != 2:
            raise TypeError('PandasDropAndFormat expected 2 arguement and '
                            '0 - 1 Keywords, got {} and {}'.format(
                                len(args), len(kwargs)))
        else:
            pdf = args[0]
            values = args[1]

        try:
            assert isinstance(pdf, pd.DataFrame)
        except AssertionError as e:
            print(e)
            print('You are seeing this error because the item you provided is'
                  ' of type {} but must be of type {}'.format(
                      type(pdf), type(pd.DataFrame())))
        else:
            if kwargs.get('columns'):
                if isinstance(values[0], str):
                    # THIS PREVENTS THE FUNCTION FROM TRYING TO DROP COLUMNS
                    # THAT DONT EXHIST ALREADY
                    values = [column_name
                              for column_name in values
                              if column_name in
                              [value for index, value in
                               enumerate(pdf.columns)]]
                    pdf.drop(values, axis=1, inplace=True)
                else:
                    pdf.drop(pdf.iloc[:, values], axis=1, inplace=True)
            else:
                pdf.drop(values, axis=0, inplace=True)
                pdf.reset_index(inplace=True)
                pdf.drop('index', axis=1, inplace=True)

    @classmethod
    def PandasDropRowsContainingValueInColumn(cls, *args, **kwargs):
        """
        This function take in a pandas data frame.
        By default it will drop all rows that contain
        nan values in the first column.
        Through the kwargs you can change this.

        Parameters
        ----------
        pd : pandas.core.frame
             Pandas DataFrame Object passed in throught args[0]
             i.e. the leftmost argurment

        kwargs:
        ------
            string_value :  string
                            sets the string that the function
                            will drop rows when contained
            column_number : int NOT float
                            sets the column number to search
                            for string_value or 'nan'
            column_name :   string
                            sets the column name to search
                            for string_value or 'nan'

        Example
        -------
        >>> import pandas as pd
        >>> dframe=pd.DataFrame({'a':['hi','nan',float('nan'),float('nan')]
        ...                     ,'b':['hi','there','good','looking']})
        >>> SKungFu.PandasDropRowsContainingValueInColumn(dframe,
        ...                                               column_name='b',
        ...                                               string_value='there')
        >>> dframe
             a        b
        0   hi       hi
        1  NaN     good
        2  NaN  looking
        >>> SKungFu.PandasDropRowsContainingValueInColumn(dframe)
        >>> dframe
            a   b
        0  hi  hi

        See Also
        --------
        This method uses the class method PandasCellIndicies

        Warning
        --------
        If you dont pass in any key words the default behavior is to drop
        all rows that contain nan in the first column

        Also, if specifying keyword argurments
        please either specify column_name or column_number but not both.
        """
        if len(args) != 1:
            raise TypeError('PandasDropRowsContainingValueInColumn expected'
                            ' 1 arguement and 0 - 3 Keywords,'
                            ' got {} and {}'.format(
                                len(args), len(kwargs)))
        else:
            pdf = args[0]

        try:
            assert isinstance(pdf, pd.DataFrame)
        except AssertionError as e:
            print(e)
            print('You are seeing this error because the item you provided is'
                  ' of type {} but must be of type {}'.format(
                      type(pdf), type(pd.DataFrame())))
        else:
            pdf.drop(
                     cls.PandasCellIndicies(pdf, **kwargs),
                     axis=0, inplace=True)
            pdf.reset_index(inplace=True)
            pdf.drop('index', axis=1, inplace=True)

    @classmethod
    def RemoveNonUniqueRowsKeepNewestBasedOnColumns(cls, *args, **kwargs):
        """
        THIS IS DEPRICATED
        """
        if len(args) != 1 or len(kwargs) != 2:
            raise TypeError('RemoveNonUniqueRowsKeepNewestBasedOnColumns '
                            'expected 1 arguement and 2 Keywords,'
                            ' got {} and {}'.format(
                                len(args), len(kwargs)))
        else:
            pdf = args[0]
            sort_column = kwargs['unique_values_column_name']
            newest_based_on = kwargs['rev_or_date_column_name']

        NonUniqueValues = {key: val
                           for key, val in
                           pdf.groupby(sort_column).groups.items()
                           if len(val) > 1}
        NonUniqueIndiciesToKeep = {}
        for key, val in NonUniqueValues.items():
            index_to_grab = val[0]
            for index in val[1:]:
                # IF THE REV AT THE CURRENT INDEX IS THE SAME AS THAT AT THE
                # REV THAT IS IDENTIFIED TO BE THE NEWEST SKIP ALL OF THE
                # FOLLOWING
                if pdf[newest_based_on].loc[index] != \
                   pdf[newest_based_on].loc[index_to_grab]:
                    # CAN BE A NAN IF SOMEHOW AGILE HAS NO REV
                    # (IT HAS HAPPENED ALREADY)
                    if not isinstance(pdf[newest_based_on].loc[index_to_grab],
                                      (float, pd.types.dtypes.np.float,
                                       pd.types.dtypes.np.float16,
                                       pd.types.dtypes.np.float32,
                                       pd.types.dtypes.np.float64)):
                        # COMPARE THE FLOAT CAST OF THE REVS OR DATES TO
                        # DETERMINE THE MORE RECENT ONE AND USE THE INDEX OF
                        # THAT ONE
                        if float(pdf[newest_based_on].loc[index].split(' ')[0]) \
                           > float(pdf[newest_based_on].loc[index_to_grab].split(' ')[0]):
                            index_to_grab = index
            # ADD TO THE LIST
            NonUniqueIndiciesToKeep[key] = index_to_grab

        NonUniqueIndiciesToDrop = {}
        for key, val in NonUniqueIndiciesToKeep.items():
            NonUniqueIndiciesToDrop[key] = [item
                                            for item in NonUniqueValues[key]
                                            if item != val]

        ListIndiciesToDrop = []
        [ListIndiciesToDrop.extend(vals)
         for keys, vals in NonUniqueIndiciesToDrop.items()]
        ListIndiciesToDrop.sort()
        cls.PandasDropAndFormat(pdf, ListIndiciesToDrop)

    @classmethod
    def RemoveNonUniqueRowsKeepNewestBasedOnColumns2(cls, *args, **kwargs):
        """
        The following function has zero
        error handling, protection, or generality.
        All it currently works to do is take in
        a agile_export that already has its columns sorted to be
        in the data base order and of the database set and then
        removes non unique rows based on part number keeping
        the one with the newest revision date
        """
        if len(args) != 1 or len(kwargs) != 2:
            raise TypeError('RemoveNonUniqueRowsKeepNewestBasedOnColumns '
                            'expected 1 arguement and 2 Keywords,'
                            ' got {} and {}'.format(
                                len(args), len(kwargs)))
        else:
            pdf = args[0]
            sort_column = kwargs['unique_values_column_name']
            newest_based_on = kwargs['rev_or_date_column_name']

        NonUniqueValues = {key: val
                           for key, val in
                           pdf.groupby(sort_column).groups.items()
                           if len(val) > 1}
        NonUniqueIndiciesToKeep = {}
        for key, val in NonUniqueValues.items():
            index_to_grab = val[-1]
            for index in val[:-1]:
                # IF THE REV AT THE CURRENT INDEX IS THE SAME AS THAT AT THE
                # REV THAT IS IDENTIFIED TO BE THE NEWEST
                # SKIP ALL OF THE FOLLOWING
                if pdf[newest_based_on].loc[index] != \
                   pdf[newest_based_on].loc[index_to_grab]:
                    try:
                        float(pdf[newest_based_on].loc[index].split(' ')[0]) \
                        > float(pdf[newest_based_on].loc[index_to_grab].split(' ')[0])
                    except ValueError as e:
                        try:
                            float(pdf[newest_based_on].loc[index].split(' ')[0])
                        except ValueError as e:
                            pass
                        else:
                            index_to_grab = index
                    else:
                        if float(pdf[newest_based_on].loc[index].split(' ')[0]) \
                           > float(pdf[newest_based_on].loc[index_to_grab].split(' ')[0]):
                            index_to_grab = index
            # ADD TO THE LIST
            NonUniqueIndiciesToKeep[key] = index_to_grab

        NonUniqueIndiciesToDrop = {}
        for key, val in NonUniqueIndiciesToKeep.items():
            NonUniqueIndiciesToDrop[key] = [item
                                            for item in NonUniqueValues[key]
                                            if item != val]

        ListIndiciesToDrop = []
        [ListIndiciesToDrop.extend(vals)
         for keys, vals in NonUniqueIndiciesToDrop.items()]
        ListIndiciesToDrop.sort()
        cls.PandasDropAndFormat(pdf, ListIndiciesToDrop)

    @staticmethod
    def IfNumCastToString(*args, **kwargs):
        """
        THIS IS DEPRICATED

        The following function checks the column that is specified
        to see if it is a float or string type.
        If it is a string it does nothing.
        If it is a float it generates the string representation and
        replaces the column with the string values

        Parameters
        ----------

            column_name : string
                          is the name of the column to check/replace/modify

        Warning
        -------
        THIS IS DEPRICATED

        todo
        ----
        Drop In Future Versions
        """
        if len(args) != 1 or len(kwargs) != 1:
            raise TypeError('IfNumCastToString expected 1 arguement and 1 '
                            'Keywords, got {} and {}'.format(
                                len(args), len(kwargs)))
        else:
            pdf = args[0]
            column_name = kwargs['column_name']

        if not pdf.empty:
            if isinstance(pdf[column_name][0],
                          (pd.types.dtypes.np.float,
                           pd.types.dtypes.np.float16,
                           pd.types.dtypes.np.float32,
                           pd.types.dtypes.np.float64)):
                NumberValue = \
                    [[index, pdf[column_name][index].astype(str).split('.')[0]]
                     for index, string in enumerate(pdf[column_name])]
                pdf.update(pd.DataFrame(data=[value[1] for value in NumberValue],
                                        columns=[column_name]))

            if isinstance(pdf[column_name][0],
                          (int,
                           pd.types.dtypes.np.int,
                           pd.types.dtypes.np.int0,
                           pd.types.dtypes.np.int16,
                           pd.types.dtypes.np.int32,
                           pd.types.dtypes.np.int64,
                           pd.types.dtypes.np.int8)):
                NumberValue = \
                    [pdf[column_name][index].astype(str)
                     for index, string in enumerate(pdf[column_name])]
                pdf.update(pd.DataFrame(data=NumberValue,
                                        columns=[column_name]))

    @staticmethod
    def IfNumCastToString2(*args, **kwargs):
        """
        The following function checks the column that is specified
        to see if it is a float or string type.
        If it is a string it does nothing.
        If it is a float it generates the string representation and
        replaces the column with the string values

        kwargs:
        ------
            column_name : string
                          is the name of the column to check/replace/modify

        Example:
        -------
        >>> import pandas as pd
        >>> dframe=pd.DataFrame({'a':[1,2,3,2,1],'b':[1,2,3,4,5]})
        >>> SKungFu.IfNumCastToString2(dframe,column_name='b')
        >>> list(dframe.a)
        [1, 2, 3, 2, 1]
        >>> list(dframe.b)
        ['1', '2', '3', '4', '5']
        >>> type(dframe.b.values[0])
        numpy.str_

        todo
        ----
        Implement fix for casts without astype() method

        Finish Documentation
        """
        if len(args) != 1 or len(kwargs) != 1:
            raise TypeError('IfNumCastToString expected 1 arguement and 1 '
                            'Keywords, got {} and {}'.format(
                                len(args), len(kwargs)))
        else:
            pdf = args[0]
            column_name = kwargs['column_name']

        if not pdf.empty:
            if isinstance(pdf[column_name][0],
                          (pd.types.dtypes.np.float,
                           pd.types.dtypes.np.float16,
                           pd.types.dtypes.np.float32,
                           pd.types.dtypes.np.float64)):
                # FIXIT : Needs to handle the case where pandas imports the
                # data as a standard float and not just a numpy float
                # <jjs a:swim>
                # IF PANDAS IMPORTS AS A STANDARD FLOAT YOU MAY HAVE AN ISSUES
                # AS FLOAT HAS NO METHOD ASTYPE WHILE NP FLOAT DO,
                # DEAL WITH IT THEN IF IT EVER HAPPENS
                NumberValue = \
                    [[index, pdf[column_name][index].astype(str).split('.')[0]]
                     for index, string in enumerate(pdf[column_name])]
                pdf.update(pd.DataFrame(data=[value[1] for value in NumberValue],
                                        columns=[column_name]))

            if isinstance(pdf[column_name][0],
                          (int,
                           pd.types.dtypes.np.int,
                           pd.types.dtypes.np.int0,
                           pd.types.dtypes.np.int16,
                           pd.types.dtypes.np.int32,
                           pd.types.dtypes.np.int64,
                           pd.types.dtypes.np.int8)):
                # THE REASON THAT THIS IS DIFFERENT FROM THE IfNumCastToString
                # METHOD IS THAT INT HAS NO ASTYPE METHOD
                # SO THIS WAY IF PANDAS CASTS AS INT AND NOT NP INT
                # IT WONT CRASH
                NumberValue = list(pdf[column_name].values.astype(str))
                pdf.update(pd.DataFrame(data=NumberValue,
                                        columns=[column_name]))

    @staticmethod
    def IfNumCastValToString(*args, **kwargs):
        """
        The following function checks the value for type
        if it is a string it does nothing.  if it is a float or int
        it generates the string representation and then returns
        the string representation of the value
        """
        if len(args) != 1 or len(kwargs) != 0:
            raise TypeError('IfNumCastValToString expected 1 arguement and'
                            ' 0 Keywords, got {} and {}'.format(
                                len(args), len(kwargs)))
        else:
            value = args[0]

        if value:
            if isinstance(value,
                          (pd.types.dtypes.np.float,
                           pd.types.dtypes.np.float16,
                           pd.types.dtypes.np.float32,
                           pd.types.dtypes.np.float64)):
                return value.astype(str).split('.')[0]

            if isinstance(value,
                          (int,
                           pd.types.dtypes.np.int,
                           pd.types.dtypes.np.int0,
                           pd.types.dtypes.np.int16,
                           pd.types.dtypes.np.int32,
                           pd.types.dtypes.np.int64,
                           pd.types.dtypes.np.int8)):
                return value.astype(str)

            if isinstance(value, str):
                return value

    @staticmethod
    def DataFrameColumnRename(*args, **kwargs):
        """
        The following function renames the columns of a dataframe.
        It expects the dataframe and two lists
        where the first list is the "from" list
        and the second list is the "to" list

        The order in this case must be one to one per list
        (irrelevant to column order but list element x in the "from" must
        correspond to list element x in the "to" list that
        you want column z renamed to)

        kwargs
        ------
            per_location : bool
                           Is false by default but when true
                           only requires that the arguement
                           be the list of the new column names and will map
                           the column names that currently exist to
                           the names provided per location passed in

            remap : bool
                    is false by default but when true will apply the
                    remap the values in the
                    "from" list to the value in the "to" list at the
                    location in the "to" list specified by
                    the list passed in through remap

        Warning
        -------
        Documentation is incomplete

        todo
        ----
        Finish Documentation
        """
        if (len(args) < 2 | len(args) > 3) | (len(kwargs) > 2):
            raise TypeError('DataFrameColumnRename expected 2 to 3 '
                            'arguements and 0 to 2 Keywords,'
                            ' got {} and {}'.format(
                                len(args), len(kwargs)))
        else:
            pdf = args[0]

            try:
                assert isinstance(pdf, pd.DataFrame)
            except AssertionError as e:
                print(e)
                print('You are seeing this error because the item you '
                      'provided is of type {} but must be of type {}'.format(
                          type(pdf), type(pd.DataFrame())))

            if kwargs.get('per_location'):
                ToList = args[1]
                FromList = list(pdf.columns.values)
                if kwargs.get('remap'):
                    RemapFromTo = kwargs['remap']
                else:
                    RemapFromTo = list(range(len(ToList)))
            elif kwargs.get('remap'):
                FromList = args[1]
                ToList = args[2]
                RemapFromTo = kwargs['remap']
            else:
                FromList = args[1]
                ToList = args[2]
                RemapFromTo = list(range(len(ToList)))

            TempToList = ToList
            ToList = [TempToList[RemapFromTo[index]]
                      for index, value in enumerate(TempToList)]

            column_name_mapping_dict = dict(zip(FromList, ToList))
            pdf.rename(columns=column_name_mapping_dict, inplace=True)

    @staticmethod
    def PLGenerate(*args, **kwargs):
        """
        The following function takes in the excelbomhumanmade dataframe
        and returns the cpnlist or mfgpnlist.

        kwargs
        ------
            human_bom_filename : string path
                                 is a keyword that specifies the path
                                 excelbomhumanmadefilename
                                 (the path to the human bom file)
                                 if not specified the function defaults to
                                 generating the mfgpnlist,
                                 if specified it will generate the cpnlist

        Warning
        -------
        There is absolutly no thought put forth on error handling at this point

        todo
        ----
        Finish Documentation
        """
        if len(args) != 1 | len(kwargs) > 1:
            raise TypeError('PLGenerate expected 1 arguements and'
                            ' 0 to 1 Keywords, got {} and {}'.format(
                                len(args), len(kwargs)))
        else:
            pdf = args[0]

        try:
            assert isinstance(pdf, pd.DataFrame)
        except AssertionError as e:
            print(e)
            print('You are seeing this error because the item you provided '
                  'is of type {} but must be of type {}'.format(
                      type(pdf), type(pd.DataFrame())))
        else:
            if kwargs.get('human_bom_filename'):
                List = \
                    [pd.ExcelFile(kwargs['human_bom_filename']).sheet_names[0]]
                List.extend(pdf.Number)
            else:
                List = [float('nan')]
                List.extend(pdf['AML.Mfr. Part Number'])
        return List

    @classmethod
    def CreateMachineGeneratedBOM(cls, *args, **kwargs):
        """
        The following function takes in the
        excelbomhumanmade and the agilepartdatabase.
        If it fails it returns either:
            a set of lists with mfgpns and cpns
            that are missing from the local agile database
            or
            if it succeeds it returns a machine generated agile bom dataframe
            and updates the excelbomhumanmade
            with the cpn to the corresponding mfgpns

        kwargs:
        ------
            human_bom_filename : string path
                                 A required keyword that specifies the path
                                 excelbomhumanmadefilename
                                 (the path to the human bom file)
        Returns
        -------
        Pass
            MachineGeneratedAgileBOM : pandas.core.frame
                                   Pandas DataFrame Object
        Fail
           Dictionary : dict
                     Dictionary containing missing CPN and MFG PNs

        Warning
        -------
        There is absolutly no thought put forth on error handling at this point

        Todo
        ----
        Implement error handling
        """
        if len(args) != 2 or len(kwargs) != 1:
            raise TypeError('CreateMachineGeneratedBOM expected 2 arguement'
                            ' and 1 Keyword, got {} and {}'.format(
                                len(args), len(kwargs)))
        else:
            BOMpdf = args[0]
            DBpdf = args[1]

        # GENERATE THE LIST OF CPN TO PULL FROM THE DATABASE
        CPNList = cls.PLGenerate(BOMpdf, **kwargs)

        # GENERATE THE LIST OF MFG PN TO PULL FROM THE DATABASE
        MFGPNList = cls.PLGenerate(BOMpdf)

        # CREATE THE MACHINE GENERATED RAW BOM
        MFGPNListMissing = []
        CPNListMissing = []

        # The database will always case as str if there are sufficient items
        # in it as there are bound to be strings but just in case
        if not isinstance(DBpdf.Number.values[0], str):
            DBpdf.Number = DBpdf.Number.values.astype(str)

        for index in range(len(CPNList)):
            if index:
                if CPNList[index] == 'nan':
                    try:
                        assert DBpdf[DBpdf['AML.Mfr. Part Number'].values ==
                                     MFGPNList[index]].Number.values, \
                                     '{}'.format(MFGPNList[index])
                    except AssertionError as e:
                        MFGPNListMissing.extend(['{}'.format(
                                                 MFGPNList[index])])
                        # MFGPNListMissing.extend([e]) # DONT DO THIS AS YOU
                        # WILL GET AssertionError('e') ADDED TO THE LIST
                        # AND NOT JUST e
                    else:
                        MachineGeneratedAgileBOM = \
                            MachineGeneratedAgileBOM.append(
                                DBpdf[DBpdf['AML.Mfr. Part Number'].values ==
                                      MFGPNList[index]],
                                ignore_index=True)
                        BOMpdf.Number.values[index-1] = \
                            DBpdf[DBpdf['AML.Mfr. Part Number'].values ==
                                  MFGPNList[index]].Number.values[0]
                else:
                    try:
                        assert DBpdf[DBpdf.Number.values ==
                                     CPNList[index]].Number.values, \
                                     '{}'.format(CPNList[index])
                    except AssertionError as e:
                        CPNListMissing.extend(['{}'.format(CPNList[index])])
                        # CPNListMissing.extend([e]) #DONT DO THIS AS
                        # YOU WILL GET AssertionError('e') ADDED TO THE
                        # LIST AND NOT JUST e
                    else:
                        MachineGeneratedAgileBOM = \
                            MachineGeneratedAgileBOM.append(
                                DBpdf[DBpdf.Number.values == CPNList[index]],
                                ignore_index=True)
            else:
                try:
                    assert CPNList[index] != 'nan', \
                           '{}'.format(MFGPNList[index])
                except AssertionError as e:
                    MFGPNListMissing.extend(['{} Must Be replaced With The'
                                             ' Corresponding CPN'.format(
                                                 MFGPNList[index])])
                else:
                    try:
                        assert DBpdf[DBpdf.Number.values ==
                                     CPNList[index]].Number.values, \
                                     '{}'.format(CPNList[index])
                    except AssertionError as e:
                        CPNListMissing.extend(['{}'.format(CPNList[index])])
                        # CPNListMissing.extend([e]) #DONT DO THIS AS
                        # YOU WILL GET AssertionError('e') ADDED TO
                        # THE LIST AND NOT JUST e
                        MachineGeneratedAgileBOM = \
                            pd.DataFrame([])
                    else:
                        MachineGeneratedAgileBOM = \
                            pd.DataFrame(data=DBpdf[DBpdf.Number.values ==
                                                    CPNList[index]])

        if MFGPNListMissing or CPNListMissing:
            return {'List of Manufacturer Part Numbers'
                    ' Missing From Database': MFGPNListMissing,
                    'List of Your Companies Part Numbers'
                    ' Missing From Database': CPNListMissing}
        else:
            return MachineGeneratedAgileBOM

# Required imports if put in sepatate package
# import pandas as pd


class AgileHumanMapping(object):
    """
    This is all completely generic to Agile and
    does not contain sensitive information.
    """
    AHM_dict = {
    'Transfer_From_HRBOM_to_BOM':
        {
         0: 'NO', 1: 'NO', 2: 'NO', 3: 'NO', 4: 'NO', 5: 'YES', 6: 'YES',
         7: 'YES', 8: 'NO', 9:'YES', 10: 'NO', 11: 'NO', 12: 'NO', 13: 'NO',
         14: 'NO', 15: 'NO', 16: 'NO', 17: 'NO', 18: 'NO', 19: 'NO', 20: 'NO',
         21: 'NO', 22: 'NO', 23: 'NO', 24: 'NO', 25: 'NO', 26: 'NO', 27: 'NO',
         28: 'NO', 29: 'NO', 30: 'NO', 31: 'NO', 32: 'NO', 33: 'NO', 34: 'NO',
         35: 'NO', 36: 'NO', 37: 'NO', 38: 'NO', 39: 'NO', 40: 'NO', 41: 'NO',
         42: 'NO', 43: 'NO', 44: 'NO', 45: 'NO', 46: 'NO', 47: 'NO', 48: 'NO',
         49: 'NO', 50: 'NO', 51: 'NO', 52: 'NO', 53: 'NO', 54: 'NO', 55: 'NO',
         56: 'NO', 57: 'NO'
        },
    'Database':
        {
         0: 'Level', 1: 'Number', 2: 'AML.Mfr. Name',
         3: 'AML.Mfr. Part Number', 4: 'BOM.Seq Num', 5: 'BOM.Qty',
         6: 'BOM.U/M', 7: 'BOM.Ref Des', 8: 'Description*', 9: 'BOM.BOM Notes',
         10: 'Lifecycle Phase', 11: 'Part Category*', 12: 'Part Type',
         13: 'Organization*', 14: 'Rev', 15: 'Rev Incorp Date',
         16: 'Rev Release Date', 17: 'Effectivity Date', 18: 'Size',
         19: 'Part Family', 20: 'Mass', 21: 'Mass-measure',
         22: 'Compliance Calculated Date', 23: 'Overall Compliance',
         24: 'Shippable Item', 25: 'Exclude from Compliance Roll-up',
         26: 'Thumbnail', 27: 'Base Model', 28: 'Sites',
         29: 'BOM.Item Description', 30: 'BOM.Rev', 31: 'BOM.Lifecycle Phase',
         32: 'BOM.Design Guidelines', 33: "BOM.Rec'd Replacement",
         34: 'BOM.Access Restriction', 35: 'BOM.COMSEC Material?',
         36: 'BOM.ST Applies', 37: 'BOM.Contract Pricing (Contact Buyer)',
         38: 'BOM.Lead Time (wk or day)', 39: 'BOM.Summary Compliance',
         40: 'BOM.Optional', 41: 'BOM.Mut Excl', 42: 'BOM.Min Qty',
         43: 'BOM.Max Qty', 44: 'BOM.Thumbnail', 45: 'AML.Part Mark',
         46: 'AML.Status', 47: 'AML.Mfr. Part Description',
         48: 'AML.Summary Compliance', 49: 'AML.Reference Notes',
         50: '', 51: '', 52: '', 53: '', 54: '', 55: '',
         56: '', 57: ''
        },
    'Transfer_To_DB':
         {
          0: 'NO', 1: 'YES', 2: 'YES', 3: 'YES', 4: 'NO', 5: 'NO', 6: 'NO',
          7: 'NO', 8: 'YES', 9: 'NO', 10: 'YES', 11: 'YES', 12: 'YES',
          13: 'YES', 14: 'YES', 15: 'YES', 16: 'YES', 17: 'YES', 18: 'YES',
          19: 'YES', 20: 'YES', 21: 'YES', 22: 'YES', 23: 'YES', 24: 'YES',
          25: 'YES', 26: 'YES', 27: 'YES', 28: 'YES', 29: 'YES', 30: 'YES',
          31: 'YES', 32: 'YES', 33: 'YES', 34: 'YES', 35: 'YES', 36: 'YES',
          37: 'YES', 38: 'YES', 39: 'YES', 40: 'YES', 41: 'YES', 42: 'YES',
          43: 'YES', 44: 'YES', 45: 'YES', 46: 'YES', 47: 'YES', 48: 'YES',
          49: 'YES', 50: 'NO', 51: 'NO', 52: 'NO', 53: 'NO', 54: 'NO',
          55: 'NO', 56: 'NO', 57: 'NO'
         },
    'Transfer_To_HRBOM':
        {
         0: 'NO', 1: 'YES', 2: 'YES', 3: 'YES', 4: 'NO', 5: 'YES', 6: 'YES',
         7: 'YES', 8: 'NO', 9: 'NO', 10: 'NO', 11: 'NO', 12: 'NO', 13: 'NO',
         14: 'NO', 15: 'NO', 16: 'NO', 17: 'NO', 18: 'NO', 19: 'NO',
         20: 'NO', 21: 'NO', 22: 'NO', 23: 'NO', 24: 'NO', 25: 'NO',
         26: 'NO', 27: 'NO', 28: 'NO', 29: 'NO', 30: 'NO', 31: 'NO',
         32: 'NO', 33: 'NO', 34: 'NO', 35: 'NO', 36: 'NO', 37: 'NO',
         38: 'NO', 39: 'NO', 40: 'NO', 41: 'NO', 42: 'NO', 43: 'NO',
         44: 'NO', 45: 'NO', 46: 'NO', 47: 'NO', 48: 'NO', 49: 'NO',
         50: 'NO', 51: 'NO', 52: 'NO', 53: 'NO', 54: 'NO', 55: 'NO',
         56: 'NO', 57: 'NO'
        },
    'Agile_Out':
        {
         0: 'Level', 1: 'Number', 2: 'AML.Mfr. Name',
         3: 'AML.Mfr. Part Number', 4: 'BOM.Seq Num', 5: 'BOM.Qty',
         6: 'BOM.U/M', 7: 'BOM.Ref Des', 8: 'Description*',
         9: 'BOM.BOM Notes', 10: 'Lifecycle Phase', 11: 'Part Category*',
         12: 'Part Type', 13: 'Organization*', 14: 'Rev',
         15: 'Rev Incorp Date', 16: 'Rev Release Date',
         17: 'Effectivity Date', 18: 'Size', 19: 'Part Family',
         20: 'Mass', 21: 'Mass-measure', 22: 'Compliance Calculated Date',
         23: 'Overall Compliance', 24: 'Shippable Item',
         25: 'Exclude from Compliance Roll-up', 26: 'Thumbnail',
         27: 'Base Model', 28: 'Sites', 29: 'BOM.Item Description',
         30: 'BOM.Rev', 31: 'BOM.Lifecycle Phase',
         32: 'BOM.Design Guidelines', 33: "BOM.Rec'd Replacement",
         34: 'BOM.Access Restriction', 35: 'BOM.COMSEC Material?',
         36: 'BOM.ST Applies', 37: 'BOM.Contract Pricing (Contact Buyer)',
         38: 'BOM.Lead Time (wk or day)', 39: 'BOM.Summary Compliance',
         40: 'BOM.Optional', 41: 'BOM.Mut Excl', 42: 'BOM.Min Qty',
         43: 'BOM.Max Qty', 44: 'BOM.Thumbnail', 45: 'AML.Part Mark',
         46: 'AML.Status', 47: 'AML.Mfr. Part Description',
         48: 'AML.Summary Compliance', 49: 'AML.Reference Notes',
         50: 'AML.Last Time to Buy (LTB) Date',
         51: 'AML.Summary Compliance', 52: 'AML.Reference Notes',
         53: 'AML.Mfr. Tab Text01', 54: 'AML.Mfr. Tab Text02',
         55: 'AML.Mfr. Tab Text03', 56: 'AML.Mfr. Tab Text04',
         57: 'AML.Mfr. Tab Text05'
        },
    'Agile_In':
        {
         0: 'Level', 1: 'Number', 2: 'AML.Mfr. Name',
         3: 'AML.Mfr. Part Number', 4: 'BOM.Seq Num', 5: 'BOM.Qty',
         6: 'BOM.U/M', 7: 'BOM.Ref Des', 8: 'Description*',
         9: 'BOM.BOM Notes', 10: 'Lifecycle Phase', 11: 'Part Category*',
         12: 'Part Type', 13: 'Organization*', 14: 'Rev',
         15: 'Rev Incorp Date', 16: 'Rev Release Date',
         17: 'Effectivity Date', 18: 'Size', 19: 'Part Family',
         20: 'Mass', 21: 'Mass-measure', 22: 'Compliance Calculated Date',
         23: 'Overall Compliance', 24: 'Shippable Item',
         25: 'Exclude from Compliance Roll-up', 26: 'Thumbnail',
         27: 'Base Model', 28: 'Sites', 29: 'BOM.Item Description',
         30: 'BOM.Rev', 31: 'BOM.Lifecycle Phase',
         32: 'BOM.Design Guidelines', 33: "BOM.Rec'd Replacement",
         34: 'BOM.Access Restriction', 35: 'BOM.COMSEC Material?',
         36: 'BOM.ST Applies', 37: 'BOM.Contract Pricing (Contact Buyer)',
         38: 'BOM.Lead Time (wk or day)', 39: 'BOM.Summary Compliance',
         40: 'BOM.Optional', 41: 'BOM.Mut Excl', 42: 'BOM.Min Qty',
         43: 'BOM.Max Qty', 44: 'BOM.Thumbnail', 45: 'AML.Part Mark',
         46: 'AML.Status', 47: 'AML.Mfr. Part Description',
         48: 'AML.Summary Compliance', 49: 'AML.Reference Notes',
         50: '', 51: '', 52: '', 53: '', 54: '', 55: '',
         56: '', 57: ''
        },
    'Transfer_From_DB_To_BOM':
        {
         0: 'NO', 1: 'YES', 2: 'YES', 3: 'YES', 4: 'NO', 5: 'NO',
         6: 'NO', 7: 'NO', 8: 'YES', 9: 'NO', 10: 'YES', 11: 'YES',
         12: 'YES', 13: 'YES', 14: 'YES', 15: 'NO', 16: 'NO', 17: 'NO',
         18: 'NO', 19: 'NO', 20: 'NO', 21: 'NO', 22: 'NO', 23: 'NO',
         24: 'YES', 25: 'YES', 26: 'NO', 27: 'NO', 28: 'NO', 29: 'NO',
         30: 'NO', 31: 'NO', 32: 'NO', 33: 'NO', 34: 'NO', 35: 'NO',
         36: 'NO', 37: 'NO', 38: 'NO', 39: 'NO', 40: 'NO', 41: 'NO',
         42: 'NO', 43: 'NO', 44: 'NO', 45: 'NO', 46: 'NO', 47: 'NO',
         48: 'NO', 49: 'NO', 50: 'NO', 51: 'NO', 52: 'NO', 53: 'NO',
         54: 'NO', 55: 'NO', 56: 'NO', 57: 'NO'
        },
    'From_Row_In_Agile_Out_To_Row_In_Agile_In':
        {
         0: 0.0, 1: 1.0, 2: 45.0, 3: 46.0, 4: 25.0, 5: 26.0, 6: 27.0,
         7: 28.0, 8: 3.0, 9: 30.0, 10: 4.0, 11: 5.0, 12: 2.0, 13: 6.0,
         14: 7.0, 15: 8.0, 16: 9.0, 17: 10.0, 18: 11.0, 19: 12.0,
         20: 13.0, 21: 14.0, 22: 15.0, 23: 16.0, 24: 17.0, 25: 18.0,
         26: 19.0, 27: 20.0, 28: 22.0, 29: 23.0, 30: 24.0, 31: 29.0,
         32: 31.0, 33: 32.0, 34: 33.0, 35: 34.0, 36: 35.0, 37: 36.0,
         38: 37.0, 39: 38.0, 40: 39.0, 41: 40.0, 42: 41.0, 43: 42.0,
         44: 43.0, 45: 47.0, 46: 48.0, 47: 49.0, 48: 51.0, 49: 52.0,
         50: '', 51: '', 52: '', 53: '', 54: '', 55: '',
         56: '', 57: ''
        },
    'Human':
        {
         0: 'Level', 1: 'CPN', 2: 'Manufacturer_Name',
         3: 'Manufacturer_Part_Number', 4: 'BOM_List_Order',
         5: 'BOM_Quantity_Per_CPN', 6: 'BOM_Quantity_Units',
         7: 'BOM_Reference_Designator', 8: 'CPN_Desctiption',
         9: 'BOM_Special_Notes_About_CPN', 10: 'Lifecycle_Phase',
         11: 'Part Category', 12: 'Part Type', 13: 'Organization Names',
         14: 'Part Revision', 15: 'Revision Incorporation Date',
         16: 'Revision Release Date', 17: 'Revision Effectivity Date',
         18: 'Part Size', 19: 'Part Family ', 20: 'Part Mass',
         21: 'Part Mass Units', 22: 'Compliance Calculated Date',
         23: 'Overall Compliance', 24: 'Shippable Item?',
         25: 'Exclude From Compliance Roll-up?', 26: 'Thumbnail',
         27: 'Base Model', 28: 'Sites', 29: 'BOM Item Description',
         30: 'BOM Revision', 31: 'BOM Lifecycle Phase',
         32: 'BOM Design Guidelines', 33: 'BOM Received Replacement',
         34: 'BOM Access Restriction', 35: 'BOM Comsec Material?',
         36: 'BOM ST Applies', 37: 'BOM Contract Buyer Pricing',
         38: 'BOM Lead Time Type', 39: 'BOM Summary Compliance',
         40: 'BOM Optional', 41: 'BOM Mut EXCL',
         42: 'BOM Minimum Quantity', 43: 'BOM Maximum Quantity',
         44: 'BOM Thumbnail', 45: 'AML Part Mark', 46: 'AML Status',
         47: 'AML Manufacturer Part Desctiption',
         48: 'AML Summary Compliance', 49: 'AML Reference Notes',
         50: '', 51: '', 52: '', 53: '', 54: '', 55: '',
         56: '', 57: ''
        }
}

    @classmethod
    def return_ahm_dataframe(cls):
        return pd.DataFrame.from_dict(cls.AHM_dict).reindex_axis(
                ['Agile_Out',
                 'Agile_In',
                 'Database',
                 'Human',
                 'From_Row_In_Agile_Out_To_Row_In_Agile_In',
                 'Transfer_To_HRBOM',
                 'Transfer_To_DB',
                 'Transfer_From_HRBOM_to_BOM',
                 'Transfer_From_DB_To_BOM'],
                     axis='columns',
                     fill_value='').replace('', pd.np.nan)

class STypeConversion(object):
    def __init__(self):
        pass

    def PassFunction(self):
        """Currently Unused"""
        pass

    def PackageIdentification(self):
        return 'STypeConversion'
