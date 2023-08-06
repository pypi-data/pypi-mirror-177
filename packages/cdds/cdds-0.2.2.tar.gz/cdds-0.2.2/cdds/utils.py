def list2df(list, index_col=None, caption=None, return_df=True,df_kwds={}): #, sort_values='index'):  
    """ Quick turn an appened list with a header (row[0]) into a pretty dataframe.
        
        Args
            list (list of lists):
            index_col (string): name of column to set as index; None (Default) has integer index.
            set_caption (string):
            show_and_return (bool):
    
    EXAMPLE USE:
    >> list_results = [["Test","N","p-val"]] 
    
    # ... run test and append list of result values ...
    
    >> list_results.append([test_Name,length(data),p])
    
    ## Displays styled dataframe if caption:
    >> df = list2df(list_results, index_col="Test",
                     set_caption="Stat Test for Significance")
    """
    from IPython.display import display
    import pandas as pd
    df_list = pd.DataFrame(list[1:],columns=list[0],**df_kwds)
    
        
    if index_col is not None:
        df_list.reset_index(inplace=True)
        df_list.set_index(index_col, inplace=True)
        
    if caption is not None:
        dfs = df_list.style.set_caption(caption)
        display(dfs)
    return df_list


def arr2series(array,series_index=None, series_name='array'):
    """
    Converts an array into a named series. 
    
    Args:
        array (numpy array): Array to transform.
        series_index (list, optional): List of values to be used as index.
                                    Defaults to None, a numerical index.
        series_name (str, optional): Name for series. Defaults to 'array'.
    
    Returns:
        converted_array: Pandas Series with the name and index specified. 
    """
    import pandas as pd
    if len(series_index)==0:
        series_index=list(range(len(array)))

    if len(series_index)>len(array):
        new_index= series_index[-len(array):]
        series_index=new_index

    converted_array = pd.Series(array.ravel(), index=series_index, name=series_name)
    return converted_array
	
	
	


def show_del_me_code(called_by_inspect_vars=False):
    """Prints code to copy and paste into a cell to delete vars using a list of their names.
    Companion function inspect_variables(locals(),print_names=True) will provide var names tocopy/paste """
    from pprint import pprint
    if called_by_inspect_vars==False:
        print("#[i]Call: `inspect_variables(locals(), print_names=True)` for list of var names")

    del_me = """
    del_me= []#list of variable names
    for me in del_me:
        try:
            exec(f'del {me}')
            print(f'del {me} succeeded')
        except:
            print(f'del {me} failed')
            continue
        """
    print(del_me)



def save_ihelp_to_file(function,save_help=False,save_code=True, 
                        as_md=False,as_txt=True,
                        folder='readme_resources/ihelp_outputs/',
                        filename=None,file_mode='w'):
    """Saves the string representation of the ihelp source code as markdown. 
    Filename should NOT have an extension. .txt or .md will be added based on
    as_md/as_txt.
    If filename is None, function name is used."""

    if as_md & as_txt:
        raise Exception('Only one of as_md / as_txt may be true.')

    import sys
    from io import StringIO
    ## save original output to restore
    orig_output = sys.stdout
    ## instantiate io stream to capture output
    io_out = StringIO()
    ## Redirect output to output stream
    sys.stdout = io_out
    
    if save_code:
        print('### SOURCE:')
        help_md = get_source_code_markdown(function)
        ## print output to io_stream
        print(help_md)
        
    if save_help:
        print('### HELP:')
        help(function)
        
    ## Get printed text from io stream
    text_to_save = io_out.getvalue()
    

    ## MAKE FULL FILENAME
    if filename is None:

        ## Find the name of the function
        import re
        func_names_exp = re.compile(r'def (\w*)\(')
        func_name = func_names_exp.findall(text_to_save)[0]    
        print(f'Found code for {func_name}')

        save_filename = folder+func_name#+'.txt'
    else:
        save_filename = folder+filename

    if as_md:
        ext = '.md'
    elif as_txt:
        ext='.txt'

    full_filename = save_filename + ext
    
    with open(full_filename,file_mode) as f:
        f.write(text_to_save)
        
    print(f'Output saved as {full_filename}')
    
    sys.stdout = orig_output



def get_source_code_markdown(function):
    """Retrieves the source code as a string and appends the markdown
    python syntax notation"""
    import inspect
    from IPython.display import display, Markdown
    source_DF = inspect.getsource(function)            
    output = "```python" +'\n'+source_DF+'\n'+"```"
    return output

def get_methods(obj,private=False):
    """
    Retrieves a list of all non-private methods (default) from inside of obj.
    - If private==False: only returns methods whose names do NOT start with a '_'
    
    Args:
        obj (object): Object to retrieve methods from.
        private (bool): Whether to retrieve private methods or public.

    Returns:
        list: the names of all of the retrieved methods.
    """
    method_list = [func for func in dir(obj) if callable(getattr(obj, func))]
    if private:
        filt_methods = list(filter(lambda x: '_' in x[0] ,method_list))
    else:
        filt_methods = list(filter(lambda x: '_' not in x[0] ,method_list))
    return  filt_methods


def get_attributes(obj,private=False):
    """
    Retrieves a list of all non-private attributes (default) from inside of obj.
    - If private==False: only returns methods whose names do NOT start with a '_'
    
    Args:
        obj (object): Object to retrieve attributes from.
        private (bool): Whether to retrieve private attributes or public.
    
    Returns:
        list: the names of all of the retrieved attributes.
    """
    method_list = [func for func in dir(obj) if not callable(getattr(obj, func))]
    if private:
        filt_methods = list(filter(lambda x: '_' in x[0] ,method_list))
    else:
        filt_methods = list(filter(lambda x: '_' not in x[0] ,method_list))
    return  filt_methods